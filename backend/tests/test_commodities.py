import pytest

def test_read_commodities(client):
    """Kiểm tra lấy danh sách nông sản"""
    response = client.get("/api/v1/commodities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["code"] == "COFFEE_ROBUSTA"

def test_create_commodity_unauthorized(client):
    """Tạo mới nông sản mà không đăng nhập Admin phải bị chặn 401"""
    payload = {
        "code": "RICE_ST25",
        "name": "Gạo ST25",
        "category": "Nông sản",
        "unit": "VND/kg",
        "region": "Đồng Bằng Sông Cửu Long",
        "description": "Gạo thơm ST25 Sóc Trăng"
    }
    response = client.post("/api/v1/commodities", json=payload)
    assert response.status_code == 401

def test_create_commodity_as_admin(client):
    """Đăng nhập Admin và tạo mới nông sản thành công"""
    # 1. Đăng nhập lấy token
    login_res = client.post("/api/v1/auth/login", json={
        "email": "admin@test.com",
        "password": "Admin123!"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Tạo nông sản
    payload = {
        "code": "RICE_ST25",
        "name": "Gạo ST25",
        "category": "Nông sản",
        "unit": "VND/kg",
        "region": "Đồng Bằng Sông Cửu Long",
        "description": "Gạo thơm ST25 Sóc Trăng"
    }
    response = client.post("/api/v1/commodities", json=payload, headers=headers)
    assert response.status_code == 200
    created = response.json()
    assert created["code"] == "RICE_ST25"
    assert created["name"] == "Gạo ST25"
