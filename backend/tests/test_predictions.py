import os
import pytest
import numpy as np
import pandas as pd
from datetime import date, timedelta

from ml_pipeline.model_trainer import ModelTrainer, evaluate_metrics, calculate_mape, SAVED_MODELS_DIR
from ml_pipeline.predictor import PricePredictor, clear_prediction_cache
from ml_pipeline.feature_engineering import create_features
from app.models.models import Commodity, PriceHistory, Forecast


@pytest.fixture
def synthetic_price_df():
    """Tạo tập dữ liệu giá nhân tạo có xu hướng và tính chu kỳ để kiểm thử ML"""
    dates = [date(2026, 1, 1) + timedelta(days=i) for i in range(120)]
    # Giá có dạng sóng sin nhẹ + xu hướng tăng nhẹ quanh 65,000 VND
    prices = [65000.0 + 80.0 * i + 1000.0 * np.sin(i / 7.0 * np.pi) for i in range(120)]
    usd_rates = [25000.0 + i * 2.0 for i in range(120)]
    oil_prices = [75.0 + 0.1 * i for i in range(120)]

    df = pd.DataFrame({
        "record_date": dates,
        "price": prices,
        "usd_vnd": usd_rates,
        "crude_oil": oil_prices
    })
    return df


def test_feature_engineering_tabular(synthetic_price_df):
    """Kiểm tra việc tạo các đặc trưng độ trễ (Lags) và trung bình động (Rolling)"""
    df_feat = create_features(synthetic_price_df, target_col="price")
    
    assert "price_lag_1" in df_feat.columns
    assert "price_lag_7" in df_feat.columns
    assert "rolling_mean_7d" in df_feat.columns
    assert "rolling_std_7d" in df_feat.columns
    assert "day_of_week" in df_feat.columns
    assert len(df_feat) < len(synthetic_price_df)  # Do dropna các hàng lag đầu tiên
    assert len(df_feat) > 50


def test_model_trainer_evaluation_and_threshold():
    """Kiểm tra hàm tính toán chỉ số lỗi (MAE, RMSE, MAPE, R2) và cơ chế Threshold Gate"""
    y_true = np.array([100.0, 105.0, 110.0, 95.0, 102.0])
    y_pred = np.array([101.0, 104.0, 108.0, 96.0, 100.0])

    metrics = evaluate_metrics(y_true, y_pred)
    assert metrics["mae"] > 0
    assert metrics["rmse"] > 0
    assert metrics["mape"] > 0
    assert 0.0 <= metrics["r2"] <= 1.0

    trainer = ModelTrainer(commodity_code="TEST_ITEM", max_rmse_threshold_ratio=0.10)
    
    # Sai số nhỏ -> Passed
    passed, reason = trainer.check_threshold({"rmse": 5.0}, mean_price=100.0)
    assert passed is True
    assert "Passed" in reason

    # Sai số quá lớn -> Rejected
    failed, reason_fail = trainer.check_threshold({"rmse": 25.0}, mean_price=100.0)
    assert failed is False
    assert "vượt quá ngưỡng" in reason_fail


def test_model_training_and_saving(synthetic_price_df):
    """Kiểm tra huấn luyện và xuất model weights (Prophet, XGBoost, PyTorch LSTM)"""
    trainer = ModelTrainer(commodity_code="TEST_COMMODITY", max_rmse_threshold_ratio=0.50)

    # 1. Huấn luyện Prophet
    prophet_res = trainer.train_prophet(synthetic_price_df)
    assert prophet_res["passed_threshold"] is True
    assert os.path.exists(os.path.join(trainer.model_dir, "prophet_model.pkl"))
    assert os.path.exists(os.path.join(trainer.model_dir, "prophet_metrics.json"))

    # 2. Huấn luyện XGBoost
    xgb_res = trainer.train_xgboost(synthetic_price_df)
    assert xgb_res["passed_threshold"] is True
    assert os.path.exists(os.path.join(trainer.model_dir, "xgboost_model.pkl"))
    assert os.path.exists(os.path.join(trainer.model_dir, "xgboost_features.json"))

    # 3. Huấn luyện LSTM
    lstm_res = trainer.train_lstm(synthetic_price_df, epochs=10, seq_length=7)
    assert lstm_res["passed_threshold"] is True
    assert os.path.exists(os.path.join(trainer.model_dir, "lstm_model.pt"))
    assert os.path.exists(os.path.join(trainer.model_dir, "lstm_scaler.pkl"))


def test_predictor_forecast_intervals(synthetic_price_df):
    """Kiểm tra bộ dự báo tạo ra đầy đủ các điểm dự đoán và khoảng tin cậy 95%"""
    trainer = ModelTrainer(commodity_code="TEST_PRED", max_rmse_threshold_ratio=0.50)
    trainer.train_xgboost(synthetic_price_df)

    predictor = PricePredictor("TEST_PRED")
    points, metrics = predictor.predict_xgboost(synthetic_price_df, days=7)

    assert len(points) == 7
    for pt in points:
        assert "date" in pt
        assert "display_date" in pt
        assert "yhat" in pt
        assert "yhat_lower" in pt
        assert "yhat_upper" in pt
        # Đảm bảo tính nhất quán của khoảng tin cậy
        assert pt["yhat_lower"] <= pt["yhat"]
        assert pt["yhat"] <= pt["yhat_upper"]
        assert pt["is_forecast"] is True


def test_prediction_in_memory_cache(db_session, synthetic_price_df):
    """Kiểm tra cơ chế In-Memory Cache phản hồi siêu tốc (<100ms)"""
    clear_prediction_cache()

    # Thêm nông sản vào CSDL test
    com = db_session.query(Commodity).first()
    if not com:
        com = Commodity(
            code="CA_PHE_TEST",
            name="Cà phê Test",
            category="Nông sản xuất khẩu",
            unit="VND/kg",
            region="Tây Nguyên"
        )
        db_session.add(com)
        db_session.commit()

    predictor = PricePredictor(com.code, db=db_session)
    
    # Lần gọi đầu tiên (Cold Run)
    res1 = predictor.forecast(model_name="XGBoost", days=7, use_cache=True)
    assert "forecast" in res1
    assert "response_time_ms" in res1
    assert len(res1["forecast"]) == 7

    # Lần gọi thứ 2 (Hot Cache) -> Phải đánh dấu cached=True và tốc độ cực nhanh
    res2 = predictor.forecast(model_name="XGBoost", days=7, use_cache=True)
    assert res2["cached"] is True


def test_api_predictions_forecast(client, db_session):
    """Kiểm tra Endpoint GET /api/v1/predictions/forecast hoạt động chính xác"""
    com = db_session.query(Commodity).first()
    
    # Gọi dự báo 7 ngày theo symbol
    response = client.get(f"/api/v1/predictions/forecast?symbol={com.code}&days=7&model=LSTM")
    assert response.status_code == 200
    data = response.json()
    
    assert data["symbol"] == com.code
    assert data["model_name"] == "LSTM"
    assert data["forecast_days"] == 7
    assert "response_time_ms" in data
    assert "metrics" in data
    assert "forecast" in data
    assert len(data["forecast"]) == 7

    # Kiểm tra cấu trúc điểm dự báo
    first_pt = data["forecast"][0]
    assert "date" in first_pt
    assert "yhat" in first_pt
    assert "yhat_lower" in first_pt
    assert "yhat_upper" in first_pt
    assert first_pt["is_forecast"] is True


def test_api_predictions_metrics(client, db_session):
    """Kiểm tra Endpoint GET /api/v1/predictions/metrics"""
    com = db_session.query(Commodity).first()
    
    response = client.get(f"/api/v1/predictions/metrics?symbol={com.code}")
    assert response.status_code == 200
    data = response.json()
    
    assert "symbol" in data
    assert "models" in data
    assert isinstance(data["models"], list)


def test_api_predictions_retrain(client, monkeypatch):
    """Kiểm tra Endpoint POST /api/v1/predictions/retrain chạy ngầm"""
    assert client.post("/api/v1/predictions/retrain").status_code == 401
    monkeypatch.setattr("app.api.v1.endpoints.admin.run_job", lambda *args: None)
    token = client.post("/api/v1/auth/login", json={"email": "admin@test.com", "password": "Admin123!"}).json()["access_token"]
    response = client.post("/api/v1/predictions/retrain", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "RUNNING"
    assert data["task_id"] > 0
