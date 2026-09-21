import io
import pytest
from app.models.models import User, Commodity, PriceHistory

@pytest.fixture
def admin_headers(client):
    login_res = client.post("/api/v1/auth/login", json={
        "email": "admin@test.com",
        "password": "Admin123!"
    })
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def user_headers(client):
    login_res = client.post("/api/v1/auth/login", json={
        "email": "user@test.com",
        "password": "User123!"
    })
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_admin_stats(client, admin_headers):
    """Kiểm tra API thống kê tổng quan hệ thống dành cho Admin"""
    res = client.get("/api/v1/admin/stats", headers=admin_headers)
    assert res.status_code == 200
    data = res.json()
    assert "total_commodities" in data
    assert "total_price_records" in data
    assert data["system_status"] == "ONLINE"


def test_admin_crawler_logs(client, admin_headers):
    """Kiểm tra API lấy danh sách nhật ký cào dữ liệu"""
    res = client.get("/api/v1/admin/logs/crawler", headers=admin_headers)
    assert res.status_code == 200
    logs = res.json()
    assert isinstance(logs, list)
    # No fabricated entries are returned before the first collection job.
    assert logs == []


def test_admin_active_model_switcher(client, admin_headers):
    """Kiểm tra API cấu hình Model Switcher"""
    # 1. Get current active model
    get_res = client.get("/api/v1/admin/models/active", headers=admin_headers)
    assert get_res.status_code == 200
    assert "active_model" in get_res.json()

    # 2. Switch active model to XGBoost
    post_res = client.post("/api/v1/admin/models/active", headers=admin_headers, json={
        "active_model": "XGBoost",
        "description": "Chuyển sang dùng XGBoost Regressor"
    })
    assert post_res.status_code == 200
    assert post_res.json()["active_model"] == "XGBOOST"


def test_admin_import_and_export_csv(client, admin_headers, db_session):
    """Kiểm tra chức năng Upload CSV giá và Xuất CSV giá"""
    com = db_session.query(Commodity).first()
    
    # 1. Tạo file CSV giả lập
    csv_content = f"commodity_id,record_date,price,price_min,price_max,volume,source\n{com.id},2026-08-30,72500,71000,74000,5000,CSV Test Upload\n"
    file_bytes = io.BytesIO(csv_content.encode("utf-8"))
    
    # Upload CSV
    upload_res = client.post(
        "/api/v1/admin/prices/import-csv",
        headers=admin_headers,
        files={"file": ("prices_test.csv", file_bytes, "text/csv")}
    )
    assert upload_res.status_code == 200
    import_data = upload_res.json()
    assert import_data["records_created"] >= 1
    
    # Kiểm tra bản ghi trong DB
    ph = db_session.query(PriceHistory).filter(PriceHistory.commodity_id == com.id, PriceHistory.source == "CSV Test Upload").first()
    assert ph is not None
    assert float(ph.price) == 72500.0

    # 2. Xuất CSV
    export_res = client.get(f"/api/v1/admin/prices/export-csv?commodity_id={com.id}", headers=admin_headers)
    assert export_res.status_code == 200
    assert "text/csv" in export_res.headers["content-type"]
    assert "72500" in export_res.text


def test_admin_user_role_and_status(client, admin_headers, db_session):
    """Kiểm tra cập nhật Role và Khóa/Mở tài khoản người dùng"""
    user = db_session.query(User).filter(User.email == "user@test.com").first()
    
    # 1. Đổi role thành 'admin'
    role_res = client.patch(
        f"/api/v1/admin/users/{user.id}/role",
        headers=admin_headers,
        json={"role": "admin"}
    )
    assert role_res.status_code == 200
    assert role_res.json()["role"] == "admin"

    # 2. Toggle status (khóa tài khoản)
    toggle_res = client.patch(
        f"/api/v1/admin/users/{user.id}/toggle-status",
        headers=admin_headers
    )
    assert toggle_res.status_code == 200
    assert "Đã khóa" in toggle_res.json()["message"]
    db_session.refresh(user)
    assert user.is_active is False
    assert user.role == "admin"


def test_rbac_protection(client, user_headers):
    """Kiểm tra người dùng thường không có quyền Admin sẽ bị chặn 403 Forbidden"""
    # User analyst không được phép tạo nông sản mới hoặc đổi quyền
    res = client.post("/api/v1/admin/commodities", headers=user_headers, json={
        "code": "TEST_FAIL",
        "name": "Test Fail",
        "category": "Nông sản",
        "unit": "kg",
        "region": "Miền Bắc"
    })
    assert res.status_code == 403
