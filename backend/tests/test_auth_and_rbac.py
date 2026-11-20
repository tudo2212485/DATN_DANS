"""
Automated Testing Suite - Pillar 3.1.1: Authentication, Session Security & RBAC Authorization
File: backend/tests/test_auth_and_rbac.py
"""
import pytest
from app.models.models import User, Commodity
from app.core.security import auth_rate_limiter, task_rate_limiter


def get_auth_headers(client, email: str, password: str) -> dict:
    res = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert res.status_code == 200, f"Login failed for {email}: {res.text}"
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_register_new_account_and_prevent_password_leak(client):
    """TC-AUTH-01: Đăng ký tài khoản mới thành công, mật khẩu băm Bcrypt và không lộ password_hash"""
    payload = {
        "email": "new.analyst@agroforecast.vn",
        "full_name": "Chuyên viên Phân tích Mới",
        "password": "StrongPassword123!"
    }
    res = client.post("/api/v1/auth/register", json=payload)
    assert res.status_code == 201
    body = res.json()
    assert body["email"] == "new.analyst@agroforecast.vn"
    assert body["is_active"] is True
    assert "password" not in body
    assert "password_hash" not in body
    assert "hashed_password" not in body

    # Đăng ký trùng email phải trả về 400 Bad Request
    dup_res = client.post("/api/v1/auth/register", json=payload)
    assert dup_res.status_code == 400


def test_login_success_and_wrong_password_rejected(client):
    """TC-AUTH-02: Đăng nhập thành công trả về JWT và đăng nhập sai mật khẩu trả về 401 Unauthorized"""
    ok_res = client.post("/api/v1/auth/login", json={
        "email": "admin@test.com",
        "password": "Admin123!"
    })
    assert ok_res.status_code == 200
    data = ok_res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["role"] == "admin"

    # Sai mật khẩu -> 401
    bad_res = client.post("/api/v1/auth/login", json={
        "email": "admin@test.com",
        "password": "WrongPassword999!"
    })
    assert bad_res.status_code == 401

    # Email không tồn tại -> 401
    no_user_res = client.post("/api/v1/auth/login", json={
        "email": "ghost@test.com",
        "password": "Admin123!"
    })
    assert no_user_res.status_code == 401


def test_locked_account_cannot_login_or_access_api(client, db_session):
    """TC-AUTH-03: Tài khoản bị khóa bởi Admin không thể đăng nhập hoặc sử dụng token cũ (403 Forbidden)"""
    admin_headers = get_auth_headers(client, "admin@test.com", "Admin123!")
    analyst_headers = get_auth_headers(client, "user@test.com", "User123!")

    analyst = db_session.query(User).filter(User.email == "user@test.com").one()

    # Admin khóa tài khoản analyst
    lock_res = client.patch(f"/api/v1/admin/users/{analyst.id}/toggle-status", headers=admin_headers)
    assert lock_res.status_code == 200
    assert lock_res.json()["is_active"] is False

    # Token cũ bị từ chối 403
    me_res = client.get("/api/v1/auth/me", headers=analyst_headers)
    assert me_res.status_code == 403

    # Đăng nhập lại bị từ chối 403
    login_locked = client.post("/api/v1/auth/login", json={
        "email": "user@test.com",
        "password": "User123!"
    })
    assert login_locked.status_code == 403


def test_unauthenticated_requests_return_401(client):
    """TC-AUTH-04: Truy cập các API bảo vệ không có JWT Token phải trả về 401 Unauthorized"""
    assert client.get("/api/v1/auth/me").status_code == 401
    assert client.get("/api/v1/admin/stats").status_code == 401
    assert client.get("/api/v1/admin/users").status_code == 401
    assert client.post("/api/v1/admin/tasks/scrape").status_code == 401
    assert client.post("/api/v1/admin/tasks/retrain").status_code == 401
    assert client.post("/api/v1/admin/prices", json={
        "commodity_id": 1,
        "record_date": "2026-08-01",
        "price": 90000
    }).status_code == 401


def test_analyst_blocked_from_admin_mutations_with_403(client, db_session):
    """TC-AUTH-05: Tài khoản Analyst gọi các API đặc quyền của Admin phải bị chặn 403 Forbidden"""
    analyst_headers = get_auth_headers(client, "user@test.com", "User123!")
    com = db_session.query(Commodity).first()

    # 1. Kích hoạt Scraper & Retrain -> 403
    assert client.post("/api/v1/admin/tasks/scrape", headers=analyst_headers).status_code == 403
    assert client.post("/api/v1/admin/tasks/retrain", headers=analyst_headers).status_code == 403

    # 2. Quản lý danh sách người dùng -> 403
    assert client.get("/api/v1/admin/users", headers=analyst_headers).status_code == 403
    assert client.post("/api/v1/admin/users", headers=analyst_headers, json={
        "email": "hack@test.com",
        "full_name": "Hacker",
        "password": "Password123!",
        "role": "admin"
    }).status_code == 403

    # 3. Thêm / sửa / xóa bản ghi giá hoặc đổi mô hình active -> 403
    assert client.post("/api/v1/admin/prices", headers=analyst_headers, json={
        "commodity_id": com.id,
        "record_date": "2026-08-01",
        "price": 95000.0,
        "source": "Analyst attempt"
    }).status_code == 403
    assert client.delete("/api/v1/admin/prices/1", headers=analyst_headers).status_code == 403
    assert client.post("/api/v1/admin/models/active", headers=analyst_headers, json={
        "active_model": "LSTM"
    }).status_code == 403

