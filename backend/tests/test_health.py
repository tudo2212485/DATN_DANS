import pytest

def test_root_endpoint(client):
    """Kiểm tra endpoint root trả về thông tin hệ thống"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "version" in data
    assert "docs" in data

def test_health_check_with_db(client):
    """Kiểm tra endpoint /health kiểm tra kết nối DB"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"

def test_cors_headers(client):
    """Kiểm tra CORS headers được cấu hình đúng"""
    response = client.options(
        "/api/v1/commodities",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET"
        }
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
