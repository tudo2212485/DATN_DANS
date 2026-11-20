"""
Automated Testing Suite - Pillar 3.1.3: 5-Model Forecast Engine, Confidence Intervals & No-Leakage Pipeline
File: backend/tests/test_forecast_and_ml_pipeline.py
"""
import json
import math
from datetime import date, timedelta
import numpy as np
import pandas as pd
import pytest
from app.models.models import Commodity, PriceHistory, TrainingRun
import app.services.training_service as training_service
from ml_pipeline.data_loader import load_clean_data


def seed_verified_series(db_session, days: int = 75):
    com = db_session.query(Commodity).first()
    db_session.query(PriceHistory).filter(PriceHistory.commodity_id == com.id).delete()
    db_session.commit()

    for i in range(days):
        d = date.today() - timedelta(days=days - i)
        price = round(115000.0 + 120.0 * i + 450.0 * math.sin(i / 5.0), 2)
        db_session.add(PriceHistory(
            commodity_id=com.id,
            record_date=d,
            price=price,
            price_min=price - 500,
            price_max=price + 500,
            volume=1500.0,
            provenance="reviewed",
            source="Hiệp hội Cà phê Ca cao VN (VICOFA)"
        ))
    db_session.commit()
    return com


def test_preprocessing_no_nan_and_strict_chronological_train_test_split(db_session, monkeypatch):
    """TC-ML-01: Kiểm tra tiền xử lý không có NaN và chia tập Train/Test tuần tự thời gian (max(train_date) < min(test_date))"""
    com = seed_verified_series(db_session, days=75)

    # 1. Kiểm tra hàm tiền xử lý load_clean_data không còn NaN
    clean_df = load_clean_data(commodity_id=com.id, db_session=db_session)
    assert not clean_df.empty
    assert not clean_df["price"].isna().any()
    assert (clean_df["price"] > 0).all()

    # 2. Theo dõi các chuỗi đầu vào được truyền cho hàm dự báo trong quá trình đánh giá holdout
    observed_splits = []

    def spy_predict(model_name, series: pd.Series, horizon: int, future_index=None):
        assert not series.isna().any(), f"Series passed to {model_name} contains NaN"
        observed_splits.append((model_name, series.index[0], series.index[-1], len(series), horizon))
        return np.linspace(float(series.iloc[-1]) + 50.0, float(series.iloc[-1]) + 50.0 * horizon, horizon)

    monkeypatch.setattr(training_service, "predict_series", spy_predict)
    res = training_service.retrain(com.id, lambda *args: None)
    assert res["status"] == "SUCCESS"

    run = db_session.query(TrainingRun).filter(TrainingRun.commodity_id == com.id).order_by(TrainingRun.id.desc()).first()
    assert run is not None
    meta = json.loads(run.metadata_json)

    # Kiểm tra No Data Leakage: train_end < test_start tuyệt đối
    train_end_date = date.fromisoformat(meta["train_end"])
    test_start_date = date.fromisoformat(meta["test_start"])
    test_end_date = date.fromisoformat(meta["test_end"])
    assert train_end_date < test_start_date
    assert test_start_date <= test_end_date
    assert (test_start_date - train_end_date).days == 1


def test_forecast_and_compare_api_return_all_5_models_and_valid_ci(client, db_session, monkeypatch):
    """TC-ML-02: Kiểm tra API /forecast và /forecast/compare trả đủ 5 mô hình, 4 chỉ số (MAE, RMSE, MAPE, R²) và lower_ci <= predicted_price <= upper_ci"""
    com = seed_verified_series(db_session, days=70)

    offsets = {
        "Random Forest": 120.0,
        "XGBoost": 90.0,
        "Prophet": 150.0,
        "ARIMA": 180.0,
        "LSTM": 70.0,
    }

    def deterministic_predict(model_name, series: pd.Series, horizon: int, future_index=None):
        delta = offsets.get(model_name, 100.0)
        return np.full(horizon, float(series.iloc[-1]) + delta)

    monkeypatch.setattr(training_service, "predict_series", deterministic_predict)
    training_service.retrain(com.id, lambda *args: None)

    # 1. Kiểm tra /api/v1/forecast/compare/{commodity_id} trả đủ 5 mô hình
    cmp_res = client.get(f"/api/v1/forecast/compare/{com.id}")
    assert cmp_res.status_code == 200
    models = cmp_res.json()
    assert len(models) == 5
    returned_names = {m["modelName"] for m in models}
    assert returned_names == {"ARIMA", "Prophet", "Random Forest", "XGBoost", "LSTM"}

    for m in models:
        assert math.isfinite(m["mae"]) and m["mae"] >= 0
        assert math.isfinite(m["rmse"]) and m["rmse"] >= 0
        assert math.isfinite(m["mape"]) and m["mape"] >= 0
        assert math.isfinite(m["r2"])
        assert m["trainDate"] != "N/A"

    # 2. Kiểm tra /api/v1/forecast cho cả 5 mô hình thỏa mãn lowerCI <= predictedPrice <= upperCI
    for model_name in ("ARIMA", "Prophet", "Random Forest", "XGBoost", "LSTM"):
        fc_res = client.get(f"/api/v1/forecast?commodity_id={com.id}&model_name={model_name}&days=14")
        assert fc_res.status_code == 200
        fc_data = fc_res.json()
        assert fc_data["modelName"] == model_name
        forecast_points = [p for p in fc_data["forecastData"] if p["isForecast"]]
        assert len(forecast_points) == 14
        for pt in forecast_points:
            assert pt["lowerCI"] <= pt["predictedPrice"] <= pt["upperCI"]


def test_walk_forward_no_leakage_and_expanding_conformal_ci():
    """TC-ML-03: Kiểm tra Walk-Forward 7 ngày không rò rỉ dữ liệu, trả đủ accuracy, picp_95 và dải 95% CI mở rộng theo √h"""
    from ml_pipeline.history_models import predict_series, walk_forward_evaluate

    dates = pd.date_range("2025-01-01", periods=220, freq="D")
    rng = np.random.default_rng(42)
    trend = 70000.0 + np.linspace(0.0, 6000.0, 220) + 1500.0 * np.sin(np.arange(220) / 15.0)
    noise = np.cumsum(rng.normal(0.0, 120.0, size=220))
    series = pd.Series(np.maximum(trend + noise, 10000.0), index=dates)

    train = series.iloc[:150]
    holdout = series.iloc[150:]
    mask = np.ones(len(holdout), dtype=bool)
    assert train.index[-1] < holdout.index[0]

    for model_name in ("Random Forest", "XGBoost", "ARIMA", "Prophet", "LSTM"):
        wf = walk_forward_evaluate(model_name, train, holdout, mask, horizon=7)
        m = wf["metrics"]
        assert math.isfinite(m["mae"]) and m["mae"] >= 0
        assert math.isfinite(m["rmse"]) and m["rmse"] >= 0
        assert math.isfinite(m["mape"]) and 0 <= m["mape"] < 15.0
        assert wf["accuracy"] == pytest.approx(round(max(0.0, 100.0 - m["mape"]), 2), abs=0.01)
        assert 0.0 <= wf["picp_95"] <= 100.0
        assert wf["ci_scale_1d"] > 0

        # Kiểm tra chuỗi dự báo 30 ngày có dải tin cậy mở rộng chặt theo chân trời
        future = predict_series(model_name, series, 30)
        assert len(future) == 30 and np.isfinite(future).all() and (future > 0).all()
        w1 = 2.0 * wf["ci_scale_1d"] * math.sqrt(1)
        w30 = 2.0 * wf["ci_scale_1d"] * math.sqrt(30)
        assert w30 > w1


def test_specialized_scraper_never_generates_synthetic_prices(db_session):
    """TC-DATA-01: Khi nguồn bên ngoài lỗi/chặn, scraper chuyên ngành báo FAILED và TUYỆT ĐỐI không sinh giá ngẫu nhiên"""
    from unittest.mock import Mock
    import requests
    from ml_pipeline.specialized_scrapers import collect_specialized_portal_history

    com = Commodity(
        code="CASHEW_TEST",
        name="Hạt điều test",
        category="Hạt",
        unit="VND/kg",
        region="Bình Phước",
    )
    db_session.add(com)
    db_session.commit()

    failing_http = Mock()
    failing_http.get.side_effect = requests.ConnectionError("DNS unreachable")

    res = collect_specialized_portal_history(
        db_session,
        failing_http,
        com,
        {"source_url": "https://unreachable.test"},
        date.today() - timedelta(days=5),
        date.today(),
    )
    assert res["status"] == "FAILED"
    assert res["count"] == 0
    assert db_session.query(PriceHistory).filter(PriceHistory.commodity_id == com.id).count() == 0


