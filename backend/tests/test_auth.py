import pytest

def test_register_success(client):
    """Đăng ký tài khoản mới thành công"""
    payload = {
        "email": "newfarmer@example.com",
        "full_name": "Nông Dân Tri Thức",
        "password": "Password123!",
        "role": "user"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newfarmer@example.com"
    assert data["full_name"] == "Nông Dân Tri Thức"
    assert data["role"] == "user"
    assert "id" in data

def test_register_duplicate_email(client):
    """Đăng ký email đã tồn tại phải nhận lỗi 400 Bad Request"""
    payload = {
        "email": "admin@test.com",
        "full_name": "Admin Clone",
        "password": "Password123!"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400
    assert "đã được đăng ký" in response.json()["detail"]

def test_register_invalid_email(client):
    """Đăng ký với định dạng email sai phải nhận lỗi 422 Validation Error"""
    payload = {
        "email": "not-an-email",
        "full_name": "Test User",
        "password": "Password123!"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 422

def test_register_short_password(client):
    """Đăng ký với mật khẩu ngắn hơn 6 ký tự phải nhận lỗi 422"""
    payload = {
        "email": "valid@example.com",
        "full_name": "Test User",
        "password": "123"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 422

def test_login_success(client):
    """Kiểm tra đăng nhập đúng tài khoản và mật khẩu"""
    payload = {
        "email": "admin@test.com",
        "password": "Admin123!"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "admin@test.com"
    assert data["user"]["role"] == "admin"

def test_login_wrong_password(client):
    """Kiểm tra đăng nhập sai mật khẩu nhận 401"""
    payload = {
        "email": "admin@test.com",
        "password": "WrongPassword!"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401
    assert "Email hoặc mật khẩu không chính xác" in response.json()["detail"]

def test_login_nonexistent_email(client):
    """Kiểm tra đăng nhập email không tồn tại nhận 401"""
    payload = {
        "email": "ghost@test.com",
        "password": "Admin123!"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401

def test_read_current_user_success(client):
    """Gọi /auth/me với token hợp lệ trả về thông tin user"""
    # 1. Login
    login_res = client.post("/api/v1/auth/login", json={
        "email": "admin@test.com",
        "password": "Admin123!"
    })
    token = login_res.json()["access_token"]
    
    # 2. Get me
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "admin@test.com"
    assert data["role"] == "admin"

def test_read_current_user_unauthorized(client):
    """Gọi /auth/me mà không có token phải trả về 401 Unauthorized"""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401

def test_read_current_user_invalid_token(client):
    """Gọi /auth/me với token sai định dạng phải trả về 401 Unauthorized"""
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid.token.value"}
    )
    assert response.status_code == 401
