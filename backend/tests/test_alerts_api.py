"""
Automated Testing Suite - Pillar 3.1.4: Alert Rules CRUD, IDOR Defense & Threshold Trigger Engine
File: backend/tests/test_alerts_api.py
"""
from datetime import date, timedelta
import pytest
from app.models.models import Commodity, PriceHistory, AlertLog
from app.services.alert_service import evaluate_all_alert_rules


def get_token_headers(client, email: str, password: str) -> dict:
    res = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    return {"Authorization": f"Bearer {res.json()['access_token']}"}


def test_alerts_full_crud_and_test_email_trigger(client, db_session):
    """TC-ALT-01: Kiểm tra CRUD đầy đủ cho quy tắc cảnh báo (Create, Read, Update, Toggle, Test Email, Delete)"""
    com = db_session.query(Commodity).first()
    analyst_headers = get_token_headers(client, "user@test.com", "User123!")

    # 1. Create
    create_res = client.post("/api/v1/alerts", headers=analyst_headers, json={
        "commodity_id": com.id,
        "rule_name": "Cảnh báo Cà phê vượt trần 125.000",
        "condition_type": "PRICE_ABOVE",
        "threshold_value": 125000.0,
        "email": "analyst@agroforecast.vn"
    })
    assert create_res.status_code == 200
    created = create_res.json()
    rule_id = created["id"]
    assert created["is_active"] is True
    assert created["threshold_value"] == 125000.0

    # 2. Update (PUT /api/v1/alerts/{rule_id})
    update_res = client.put(f"/api/v1/alerts/{rule_id}", headers=analyst_headers, json={
        "rule_name": "Cảnh báo Cà phê vượt trần 128.000",
        "threshold_value": 128000.0,
        "email": "updated@agroforecast.vn"
    })
    assert update_res.status_code == 200
    assert update_res.json()["threshold_value"] == 128000.0
    assert update_res.json()["email"] == "updated@agroforecast.vn"

    # 3. Toggle status (PATCH /api/v1/alerts/{rule_id}/toggle)
    toggle_res = client.patch(f"/api/v1/alerts/{rule_id}/toggle", headers=analyst_headers, json={
        "is_active": False
    })
    assert toggle_res.status_code == 200
    assert toggle_res.json()["is_active"] is False

    # 4. Test Email Notification & Verify Audit Log entry
    test_res = client.post(f"/api/v1/alerts/{rule_id}/test", headers=analyst_headers)
    assert test_res.status_code == 200
    assert test_res.json()["status"] == "success"

    logs_res = client.get("/api/v1/alerts/logs", headers=analyst_headers)
    assert logs_res.status_code == 200
    assert any(l["rule_id"] == rule_id for l in logs_res.json())

    # 5. Delete
    del_res = client.delete(f"/api/v1/alerts/{rule_id}", headers=analyst_headers)
    assert del_res.status_code == 200


def test_alerts_idor_protection_between_analysts(client, db_session):
    """TC-ALT-02: Kiểm tra chống IDOR trên /alerts - Người dùng không được sửa/xóa quy tắc của người khác"""
    com = db_session.query(Commodity).first()
    analyst_a_headers = get_token_headers(client, "user@test.com", "User123!")

    # Analyst A tạo quy tắc cảnh báo riêng
    rule_res = client.post("/api/v1/alerts", headers=analyst_a_headers, json={
        "commodity_id": com.id,
        "rule_name": "Quy tắc riêng của Analyst A",
        "condition_type": "PRICE_ABOVE",
        "threshold_value": 120000.0,
        "email": "analyst_a@agroforecast.vn"
    })
    rule_id = rule_res.json()["id"]

    # Đăng ký & đăng nhập tài khoản User B khác
    client.post("/api/v1/auth/register", json={
        "email": "user_b@test.com",
        "full_name": "User B",
        "password": "UserB123!"
    })
    user_b_headers = get_token_headers(client, "user_b@test.com", "UserB123!")

    # User B cố tình sửa, bật/tắt hoặc xóa quy tắc của Analyst A -> Phải bị chặn 403 Forbidden
    assert client.put(f"/api/v1/alerts/{rule_id}", headers=user_b_headers, json={"threshold_value": 50000}).status_code == 403
    assert client.patch(f"/api/v1/alerts/{rule_id}/toggle", headers=user_b_headers, json={"is_active": False}).status_code == 403
    assert client.delete(f"/api/v1/alerts/{rule_id}", headers=user_b_headers).status_code == 403

    # Nhưng Admin có toàn quyền quản trị -> Xóa thành công (200)
    admin_headers = get_token_headers(client, "admin@test.com", "Admin123!")
    assert client.delete(f"/api/v1/alerts/{rule_id}", headers=admin_headers).status_code == 200


def test_alert_evaluation_engine_price_above_and_below(client, db_session):
    """TC-ALT-03: Kiểm tra logic đánh giá điều kiện kích hoạt cảnh báo (> vượt trần và < chạm sàn)"""
    com = db_session.query(Commodity).first()

    # Thêm giá thị trường mới nhất là 105,000 VNĐ/kg
    db_session.add(PriceHistory(
        commodity_id=com.id,
        record_date=date.today(),
        price=105000.0,
        provenance="reviewed",
        source="VICOFA"
    ))
    db_session.commit()

    analyst_headers = get_token_headers(client, "user@test.com", "User123!")

    # Quy tắc 1: Vượt trần 100,000 (sẽ kích hoạt vì 105,000 >= 100,000)
    client.post("/api/v1/alerts", headers=analyst_headers, json={
        "commodity_id": com.id,
        "rule_name": "Vượt trần 100k",
        "condition_type": "PRICE_ABOVE",
        "threshold_value": 100000.0,
        "email": "above@test.com"
    })

    # Quy tắc 2: Chạm sàn 110,000 (sẽ kích hoạt vì 105,000 <= 110,000)
    client.post("/api/v1/alerts", headers=analyst_headers, json={
        "commodity_id": com.id,
        "rule_name": "Chạm sàn 110k",
        "condition_type": "PRICE_BELOW",
        "threshold_value": 110000.0,
        "email": "below@test.com"
    })

    # Quy tắc 3: Vượt trần 130,000 (KHÔNG kích hoạt vì 105,000 < 130,000)
    client.post("/api/v1/alerts", headers=analyst_headers, json={
        "commodity_id": com.id,
        "rule_name": "Vượt trần 130k",
        "condition_type": "PRICE_ABOVE",
        "threshold_value": 130000.0,
        "email": "not_triggered@test.com"
    })

    triggered_count = evaluate_all_alert_rules(db_session)
    assert triggered_count == 2

    logs = db_session.query(AlertLog).all()
    assert len(logs) == 2
    messages = " | ".join(l.message for l in logs)
    assert "vượt ngưỡng" in messages
    assert "giảm dưới ngưỡng" in messages

