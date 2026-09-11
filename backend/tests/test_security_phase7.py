import pytest
from fastapi.testclient import TestClient
from datetime import timedelta

from app.main import app
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token,
    sanitize_text,
    RateLimiter,
    auth_rate_limiter,
)
from app.models.models import User

client = TestClient(app)

def test_security_headers_present():
    """Test 1: Kiểm tra Security Response Headers theo chuẩn OWASP Top 10"""
    response = client.get("/")
    assert response.status_code == 200
    
    headers = response.headers
    assert headers.get("X-Content-Type-Options") == "nosniff"
    assert headers.get("X-Frame-Options") == "DENY"
    assert headers.get("X-XSS-Protection") == "1; mode=block"
    assert "Strict-Transport-Security" in headers
    assert headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"
    assert "Permissions-Policy" in headers

def test_password_hashing_and_verification():
    """Test 2: Kiểm tra băm mật khẩu bằng Bcrypt với Salt ngẫu nhiên"""
    raw_pass = "NongNghiepViet@2026"
    hash_1 = get_password_hash(raw_pass)
    hash_2 = get_password_hash(raw_pass)
    
    # 2 lần băm phải ra 2 chuỗi khác nhau do salt ngẫu nhiên
    assert hash_1 != hash_2
    
    # Cả 2 hash đều phải verify đúng với mật khẩu gốc
    assert verify_password(raw_pass, hash_1) is True
    assert verify_password(raw_pass, hash_2) is True
    assert verify_password("WrongPassword123", hash_1) is False

def test_sanitize_text_xss_protection():
    """Test 3: Kiểm tra làm sạch dữ liệu đầu vào, ngăn ngừa XSS/HTML Injection"""
    dirty_input = "<script>alert('XSS Attack');</script><b>Nông dân Cà phê Đắk Lắk</b>"
    cleaned = sanitize_text(dirty_input)
    
    assert "<script>" not in cleaned
    assert "</script>" not in cleaned
    assert "Nông dân Cà phê Đắk Lắk" in cleaned

def test_rate_limiter_mechanism():
    """Test 4: Kiểm tra cơ chế Rate Limiter chống brute force"""
    limiter = RateLimiter(max_requests=3, window_seconds=5)
    test_key = "ip_192_168_1_100"
    
    # 3 request đầu tiên phải được chấp nhận
    assert limiter.is_rate_limited(test_key) is False
    assert limiter.is_rate_limited(test_key) is False
    assert limiter.is_rate_limited(test_key) is False
    
    # Request thứ 4 phải bị Rate Limit chặn
    assert limiter.is_rate_limited(test_key) is True
    
    # Key khác không bị ảnh hưởng
    assert limiter.is_rate_limited("ip_192_168_1_200") is False

def test_jwt_tampering_and_expiration():
    """Test 5: Kiểm tra xác thực tính toàn vẹn và thời hạn của JWT Token"""
    token = create_access_token(subject=999, role="admin", expires_delta=timedelta(minutes=30))
    payload = decode_access_token(token)
    assert payload is not None
    assert payload["sub"] == "999"
    assert payload["role"] == "admin"
    
    # Token bị sửa đổi signature phải bị từ chối
    tampered_token = token[:-5] + "ABCDE"
    assert decode_access_token(tampered_token) is None
    
    # Token đã hết hạn phải bị từ chối
    expired_token = create_access_token(subject=999, role="admin", expires_delta=timedelta(seconds=-10))
    assert decode_access_token(expired_token) is None

def test_sql_injection_defense_in_commodity_query():
    """Test 6: Kiểm tra tính an toàn chống SQL Injection trên endpoint tra cứu"""
    # Payload injection nguy hiểm
    sqli_payload = "COFFEE' OR '1'='1"
    response = client.get(f"/api/v1/commodities/spotlight?code={sqli_payload}")
    
    # Hệ thống không được trả về lỗi 500 hoặc rò rỉ dữ liệu ngoài ý muốn
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        assert "commodityCode" in data or "commodityName" in data
