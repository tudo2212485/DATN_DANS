"""Comparable chronological evaluation and auditable history-to-forecast runs."""
import json
from datetime import date
import numpy as np
import pandas as pd
from app.core.database import SessionLocal
from app.models.models import Commodity, Forecast, TrainingRun
from app.services.history_service import observations, modeling_rows, readiness, fingerprint
from ml_pipeline.history_models import predict_series, score

MODELS = ("Random Forest", "XGBoost", "Prophet", "ARIMA", "LSTM")


def retrain(commodity_id, progress):
    count, errors = 0, []
    with SessionLocal() as db:
        commodities = db.query(Commodity).filter(Commodity.id == commodity_id).all() if commodity_id else db.query(Commodity).all()
        if not commodities:
            raise ValueError("Không tìm thấy nông sản")
        for ci, commodity in enumerate(commodities):
            all_rows = observations(db, commodity.id)
            quality = readiness(all_rows)
            rows = modeling_rows(all_rows)
            if not quality["ready"]:
                errors.append(f"{commodity.name}: {quality['reason']}")
                continue
            series = pd.Series([float(r.price) for r in rows], index=pd.to_datetime([r.record_date for r in rows]))
            test_count = min(30, max(7, int(len(rows) * .15)))
            split_date = pd.Timestamp(rows[-test_count].record_date)
            daily = series.asfreq("D").ffill()
            train = daily.loc[daily.index < split_date]
            holdout = daily.loc[daily.index >= split_date]
            mask = holdout.index.isin(series.index)
            actual = holdout.to_numpy()[mask]
            baseline = score(actual, np.full(len(actual), float(train.iloc[-1])))
            metadata = dict(quality, commodity_unit=commodity.unit, test_start=str(holdout.index[0].date()),
                            test_end=str(holdout.index[-1].date()), test_count=test_count,
                            train_end=str(train.index[-1].date()), horizon=30,
                            filled_days=len(daily)-len(series), baseline=baseline,
                            evaluation="Dự báo nhiều bước từ một mốc cố định; kiểm thử 15% ngày quan sát cuối (tối đa 30).",
                            sources=sorted({r.source for r in rows if r.source}),
                            snapshot=[dict(date=str(r.record_date), price=float(r.price), source=r.source,
                                           provenance=r.provenance,
                                           source_details=json.loads(r.source_details) if r.source_details else None) for r in rows])
            run = TrainingRun(commodity_id=commodity.id, dataset_hash=fingerprint(rows),
                              metadata_json=json.dumps(metadata, ensure_ascii=False))
            db.add(run)
            db.commit()
            for mi, name in enumerate(MODELS):
                progress(int((ci*5+mi)*100/(len(commodities)*5)), f"{commodity.name}: đánh giá và huấn luyện {name}")
                try:
                    predictions = predict_series(name, train, len(holdout))
                    metrics = score(actual, predictions[mask])
                    future = predict_series(name, daily, 30)
                    if not np.isfinite(future).all() or np.max(future) >= 1e12:
                        raise ValueError("Dự báo vượt giới hạn giá hợp lệ")
                    db.query(Forecast).filter(Forecast.commodity_id == commodity.id, Forecast.model_name == name).delete()
                    for i, value in enumerate(future):
                        db.add(Forecast(commodity_id=commodity.id, model_name=name, training_run_id=run.id,
                                       forecast_date=(daily.index[-1]+pd.Timedelta(days=i+1)).date(),
                                       predicted_price=float(value), lower_ci=max(0, float(value)-1.96*metrics['rmse']),
                                       upper_ci=float(value)+1.96*metrics['rmse'], training_date=date.today(), **metrics))
                    db.commit()
                    count += len(future)
                except Exception as exc:
                    db.rollback()
                    errors.append(f"{commodity.name} / {name}: {exc}")
    return {"count": count, "status": ("PARTIAL" if count else "FAILED") if errors else "SUCCESS",
            "message": f"Đã lưu {count} điểm dự báo từ dữ liệu có nguồn." + (" Lỗi: " + "; ".join(errors) if errors else "")}
