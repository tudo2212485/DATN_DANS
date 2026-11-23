"""Comparable chronological evaluation and auditable history-to-forecast runs."""
import inspect
import json
import math
from datetime import date
import numpy as np
import pandas as pd
from app.core.database import SessionLocal
from app.models.models import Commodity, Forecast, SystemSetting, TrainingRun
from app.services.history_service import fingerprint, training_context
from ml_pipeline.history_models import (
    fetch_exogenous_macro_series,
    predict_series as _DEFAULT_PREDICT_SERIES,
    score,
    walk_forward_baseline,
    walk_forward_evaluate,
)

# Export `predict_series` at module level so unit tests can monkeypatch it cleanly.
predict_series = _DEFAULT_PREDICT_SERIES

MODELS = ("Random Forest", "XGBoost", "Prophet", "ARIMA", "LSTM")


def _select_best_model(model_metrics: dict) -> str:
    """Pick the best model by lowest MAPE (tie-break by lowest RMSE, then highest R2)."""
    if not model_metrics:
        return "LSTM"
    return min(
        model_metrics.items(),
        key=lambda kv: (
            float(kv[1].get("mape", 999.0)),
            float(kv[1].get("rmse", 1e12)),
            -float(kv[1].get("r2", -999.0)),
        ),
    )[0]


def retrain(commodity_id, progress):
    count, errors = 0, []
    overall_mape_by_model = {m: [] for m in MODELS}
    use_walk_forward_engine = predict_series is _DEFAULT_PREDICT_SERIES

    with SessionLocal() as db:
        commodities = (
            db.query(Commodity).filter(Commodity.id == commodity_id).all()
            if commodity_id
            else db.query(Commodity).all()
        )
        if not commodities:
            raise ValueError("Không tìm thấy nông sản")

        for ci, commodity in enumerate(commodities):
            context = training_context(db, commodity)
            quality = context["quality"]
            rows = context["rows"]
            if not quality["ready"]:
                errors.append(f"{commodity.name}: {quality['reason']}")
                continue

            series = pd.Series(
                [float(r.price) for r in rows],
                index=pd.to_datetime([r.record_date for r in rows]),
            )
            scheduled = context["cadence"] != "daily"
            is_real_wf = (not scheduled) and len(rows) >= 120 and use_walk_forward_engine

            if is_real_wf:
                test_count = min(90, max(60, int(len(rows) * 0.15)))
            else:
                test_count = min(30, max(3 if scheduled else 7, int(len(rows) * (0.25 if scheduled else 0.15))))

            split_date = pd.Timestamp(rows[-test_count].record_date)
            if scheduled:
                model_series = series
                train = series.iloc[:-test_count]
                holdout = series.iloc[-test_count:]
                actual = holdout.to_numpy()
                mask = np.ones(len(holdout), dtype=bool)
                future_count = 30
                future_dates = pd.date_range(
                    series.index[-1] + pd.Timedelta(days=context["cadence_days"]),
                    periods=future_count,
                    freq=f"{context['cadence_days']}D",
                )
            else:
                model_series = series.asfreq("D").ffill()
                train = model_series.loc[model_series.index < split_date]
                holdout = model_series.loc[model_series.index >= split_date]
                mask = holdout.index.isin(series.index)
                actual = holdout.to_numpy()[mask]
                future_count = 30
                future_dates = pd.date_range(model_series.index[-1] + pd.Timedelta(days=1), periods=future_count)

            exog_df = (
                fetch_exogenous_macro_series(rows[0].record_date, rows[-1].record_date)
                if is_real_wf
                else None
            )
            exog_labels = (
                ["USD/VND (Yahoo Finance VND=X)", "Dầu thô WTI (Yahoo Finance CL=F)"]
                if exog_df is not None and not exog_df.empty
                else []
            )

            if is_real_wf:
                baseline = walk_forward_baseline(train, holdout, mask, horizon=7)
                exog_suffix = " + biến ngoại sinh nhân quả (USD/VND, WTI)" if exog_labels else ""
                eval_desc = (
                    f"Đánh giá Walk-Forward cuộn 7 ngày (không rò rỉ dữ liệu{exog_suffix}) trên {int(mask.sum())} phiên "
                    "quan sát cuối; bộ chuẩn hóa và mô hình chỉ huấn luyện trên tập Train."
                )
                validation_method = (
                    "Walk-Forward 7 ngày (Zero Leakage, Exogenous USD/VND + WTI, Conformal 95% CI)"
                    if exog_labels
                    else "Walk-Forward 7 ngày (No Data Leakage, Conformal 95% CI)"
                )
            else:
                baseline = score(actual, np.full(len(actual), float(train.iloc[-1])))
                eval_desc = (
                    "Dự báo nhiều bước theo nhịp công bố từ một mốc cố định; kiểm thử 25% quan sát cuối."
                    if scheduled
                    else "Dự báo nhiều bước từ một mốc cố định; kiểm thử 15% ngày quan sát cuối (tối đa 30)."
                )
                validation_method = "Holdout tuần tự thời gian"

            metadata = dict(
                quality,
                commodity_unit=commodity.unit,
                test_start=str(holdout.index[0].date()),
                test_end=str(holdout.index[-1].date()),
                test_count=int(mask.sum()) if is_real_wf else test_count,
                train_end=str(train.index[-1].date()),
                horizon=future_count,
                filled_days=len(model_series) - len(series),
                baseline=baseline,
                evaluation=eval_desc,
                validation_method=validation_method,
                exogenous_features=exog_labels,
                model_metrics={},
                sources=sorted({r.source for r in rows if r.source}),
                snapshot=[
                    dict(
                        date=str(r.record_date),
                        price=float(r.price),
                        source=r.source,
                        provenance=r.provenance,
                        source_details=json.loads(r.source_details) if r.source_details else None,
                    )
                    for r in rows
                ],
            )
            run = TrainingRun(
                commodity_id=commodity.id,
                dataset_hash=fingerprint(rows),
                metadata_json=json.dumps(metadata, ensure_ascii=False),
            )
            db.add(run)
            db.commit()

            per_model_metrics = {}
            for mi, name in enumerate(MODELS):
                progress(
                    int((ci * 5 + mi) * 100 / (len(commodities) * 5)),
                    f"{commodity.name}: đánh giá và huấn luyện {name}",
                )
                try:
                    if is_real_wf:
                        wf_res = walk_forward_evaluate(name, train, holdout, mask, horizon=7, exog_df=exog_df)
                        metrics = wf_res["metrics"]
                        ci_scale_1d = wf_res["ci_scale_1d"]
                        per_model_metrics[name] = {
                            "mae": round(metrics["mae"], 4),
                            "rmse": round(metrics["rmse"], 4),
                            "mape": round(metrics["mape"], 4),
                            "accuracy": wf_res["accuracy"],
                            "r2": round(metrics["r2"], 4),
                            "picp_95": wf_res["picp_95"],
                            "q95": wf_res["q95"],
                            "ci_scale_1d": round(ci_scale_1d, 4),
                            "evaluated_points": wf_res["evaluated_points"],
                        }
                        overall_mape_by_model[name].append(metrics["mape"])
                    else:
                        predictions = (
                            predict_series(name, train, len(holdout), holdout.index)
                            if scheduled
                            else predict_series(name, train, len(holdout))
                        )
                        metrics = score(actual, predictions[mask])
                        ci_scale_1d = 1.96 * metrics["rmse"]
                        per_model_metrics[name] = {
                            "mae": round(metrics["mae"], 4),
                            "rmse": round(metrics["rmse"], 4),
                            "mape": round(metrics["mape"], 4),
                            "accuracy": round(max(0.0, 100.0 - metrics["mape"]), 2),
                            "r2": round(metrics["r2"], 4),
                            "picp_95": None,
                        }

                    _pred_params = inspect.signature(predict_series).parameters
                    _accepts_exog = "exog_df" in _pred_params or any(
                        p.kind == inspect.Parameter.VAR_KEYWORD for p in _pred_params.values()
                    )
                    future = (
                        predict_series(name, model_series, future_count, future_dates)
                        if scheduled
                        else (
                            predict_series(name, model_series, future_count, exog_df=exog_df)
                            if (is_real_wf and _accepts_exog)
                            else predict_series(name, model_series, future_count)
                        )
                    )
                    if not np.isfinite(future).all() or np.max(future) >= 1e12:
                        raise ValueError("Dự báo vượt giới hạn giá hợp lệ")

                    db.query(Forecast).filter(
                        Forecast.commodity_id == commodity.id, Forecast.model_name == name
                    ).delete()
                    for i, value in enumerate(future):
                        step_mult = math.sqrt(i + 1) if is_real_wf else (1.0 + 0.04 * i)
                        half_w = ci_scale_1d * step_mult
                        pred_f = float(value)
                        db.add(
                            Forecast(
                                commodity_id=commodity.id,
                                model_name=name,
                                training_run_id=run.id,
                                forecast_date=future_dates[i].date(),
                                predicted_price=pred_f,
                                lower_ci=max(0.0, pred_f - half_w),
                                upper_ci=pred_f + half_w,
                                training_date=date.today(),
                                **metrics,
                            )
                        )
                    db.commit()
                    count += len(future)
                except Exception as exc:
                    db.rollback()
                    errors.append(f"{commodity.name} / {name}: {exc}")

            if per_model_metrics:
                metadata["model_metrics"] = per_model_metrics
                metadata["best_model"] = _select_best_model(per_model_metrics)
                run.metadata_json = json.dumps(metadata, ensure_ascii=False)
                db.commit()

        # When retraining all commodities in full real WF mode, auto-select overall best model as active default
        if commodity_id is None and use_walk_forward_engine:
            valid_avgs = {
                m: float(np.mean(vals))
                for m, vals in overall_mape_by_model.items()
                if vals
            }
            if valid_avgs:
                best_overall = min(valid_avgs.items(), key=lambda kv: kv[1])[0].upper()
                setting = db.get(SystemSetting, "active_model")
                if setting:
                    setting.value = best_overall
                else:
                    db.add(SystemSetting(key="active_model", value=best_overall))
                db.commit()

    return {
        "count": count,
        "status": ("PARTIAL" if count else "FAILED") if errors else "SUCCESS",
        "message": (
            f"Đã lưu {count} điểm dự báo từ dữ liệu có nguồn."
            + (" Lỗi: " + "; ".join(errors) if errors else "")
        ),
    }
