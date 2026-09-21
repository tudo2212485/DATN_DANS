import pytest
import pandas as pd
import numpy as np
from datetime import date, timedelta
from ml_pipeline.data_loader import handle_outliers_iqr, load_clean_data
from app.models.models import Commodity, PriceHistory, AlertRule, AlertLog
from app.services.alert_service import evaluate_all_alert_rules, create_alert_rule
from app.schemas.schemas import AlertRuleCreate

def test_handle_outliers_iqr():
    """Kiểm tra thuật toán xử lý và chặn ngoại lai (Outliers Capping) với IQR"""
    df = pd.DataFrame({
        "price": [10.0, 10.5, 11.0, 10.8, 10.2, 10.7, 500.0, -100.0]  # Có 2 giá trị ngoại lai
    })
    cleaned_df = handle_outliers_iqr(df, column="price")
    # Giá trị 500.0 và -100.0 phải bị chặn lại theo ngưỡng IQR
    assert cleaned_df["price"].max() < 500.0
    assert cleaned_df["price"].min() > -100.0

def test_load_clean_data_empty(db_session):
    """Kiểm tra load_clean_data khi chưa có dữ liệu lịch sử giá"""
    df = load_clean_data(commodity_id=999, db_session=db_session)
    assert df.empty

def test_load_clean_data_with_history(db_session):
    """Kiểm tra load_clean_data điền khuyết chuỗi thời gian khi có dữ liệu"""
    # Lấy commodity có sẵn từ fixture
    com = db_session.query(Commodity).first()
    
    # Tạo 5 ngày lịch sử giá
    base_date = date(2026, 8, 1)
    for i in range(5):
        ph = PriceHistory(
            commodity_id=com.id,
            record_date=base_date + timedelta(days=i),
            price=60000.0 + i * 500.0,
            volume=1000.0,
            source="Test Source"
        )
        db_session.add(ph)
    db_session.commit()
    
    df = load_clean_data(commodity_id=com.id, db_session=db_session)
    assert not df.empty
    assert "record_date" in df.columns
    assert "price" in df.columns
    assert len(df) == 5

def test_alert_rule_evaluation(db_session):
    """Kiểm tra bộ đánh giá cảnh báo tự động khi giá vượt ngưỡng"""
    com = db_session.query(Commodity).first()
    
    # 1. Thêm bản ghi giá hôm nay là 95,000 VND
    ph = PriceHistory(
        commodity_id=com.id,
        record_date=date(2026, 8, 28),
        price=95000.0,
        source="Test"
    )
    db_session.add(ph)
    db_session.commit()
    
    # 2. Tạo quy tắc cảnh báo khi giá vượt 90,000 VND
    rule_in = AlertRuleCreate(
        commodity_id=com.id,
        rule_name="Cảnh báo giá vượt 90k",
        condition_type="PRICE_ABOVE",
        threshold_value=90000.0,
        email="farmer@test.com"
    )
    create_alert_rule(db_session, rule_in)
    
    # 3. Đánh giá tất cả cảnh báo
    triggered = evaluate_all_alert_rules(db_session)
    assert triggered >= 1
    
    # 4. Kiểm tra xem log cảnh báo đã được ghi chưa
    logs = db_session.query(AlertLog).all()
    assert len(logs) >= 1
    assert "vượt ngưỡng" in logs[0].message

def test_admin_trigger_scrape_api(client, monkeypatch):
    """Kiểm tra API kích hoạt cào dữ liệu chạy nền dành cho Admin"""
    # 1. Đăng nhập Admin
    login_res = client.post("/api/v1/auth/login", json={
        "email": "admin@test.com",
        "password": "Admin123!"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # The endpoint is tested independently from the external publisher.
    monkeypatch.setattr("app.api.v1.endpoints.admin.run_job", lambda *args: None)
    # 2. Gọi trigger scrape
    response = client.post("/api/v1/admin/tasks/scrape?days=7", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "RUNNING"
    assert "Cào dữ liệu" in data["task_name"]
