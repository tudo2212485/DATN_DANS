# -*- coding: utf-8 -*-
"""
Targeted Backend Coverage Tests (TDD + Coverage-Analysis)
Closes uncovered critical business branches across:
  1. Auth / JWT Dependencies / Rate Limiting / Security Hardening
  2. Admin CRUD / Manual Price Validation / CSV Import-Export / Audit Revisions
  3. Alerts Evaluation (PCT_INC_7D / PCT_DEC_7D / Empty History / Ownership / SMTP)
  4. Regional Pricing / Direct Series / History Readiness / Spotlight / Prices
  5. Job & Scraper Lifecycle / ML Training Error Recovery / Forecast Errors / Scheduler / Schema Upgrade
"""
from datetime import date, datetime, timedelta
import json
import smtplib
from types import SimpleNamespace

import jwt
import numpy as np
import pytest
from pydantic import ValidationError
from sqlalchemy import create_engine, inspect, text

from app.core.config import settings
from app.core.security import (
    auth_rate_limiter,
    create_access_token,
    get_password_hash,
    sanitize_csv_cell,
    task_rate_limiter,
    verify_password,
)
from app.models.models import (
    AlertLog,
    AlertRule,
    BackgroundJob,
    Commodity,
    Forecast,
    PriceHistory,
    RegionalPriceObservation,
    SystemSetting,
    TrainingRun,
    User,
)
from app.schemas.schemas import PriceCreateManual


def _login_headers(client, email: str, password: str) -> dict:
    resp = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200, resp.text
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _seed_daily_prices(db_session, commodity_id: int, days: int = 65, base_price: float = 100000.0, provenance: str = "collected"):
    start = date.today() - timedelta(days=days)
    for i in range(days):
        db_session.add(
            PriceHistory(
                commodity_id=commodity_id,
                record_date=start + timedelta(days=i),
                price=base_price + i * 100.0,
                price_min=base_price + i * 100.0 - 500.0,
                price_max=base_price + i * 100.0 + 500.0,
                volume=1000.0,
                source="https://giacaphe.com/gia-ca-phe-noi-dia/",
                provenance=provenance,
            )
        )
    db_session.commit()


# =====================================================================
# 1. AUTH, JWT DEPENDENCIES & SECURITY HARDENING
# =====================================================================

def test_auth_rate_limiting_login_and_register(client):
    """Rate limiter blocks excessive login/register bursts with 429."""
    # Exhaust login limit (25 requests per 60s window)
    for _ in range(25):
        r = client.post("/api/v1/auth/login", json={"email": "nobody@test.com", "password": "wrong"})
        assert r.status_code == 401
    blocked = client.post("/api/v1/auth/login", json={"email": "nobody@test.com", "password": "wrong"})
    assert blocked.status_code == 429

    # Exhaust register limit (25 requests per 60s window)
    for _ in range(25):
        r = client.post(
            "/api/v1/auth/register",
            json={"email": "admin@test.com", "full_name": "Dup", "password": "Password123!"},
        )
        assert r.status_code == 400
    reg_blocked = client.post(
        "/api/v1/auth/register",
        json={"email": "fresh@test.com", "full_name": "Fresh", "password": "Password123!"},
    )
    assert reg_blocked.status_code == 429


def test_jwt_missing_sub_and_deleted_user(client):
    """Valid-signature JWT without `sub` -> 401; JWT for deleted user -> 404."""
    no_sub_token = jwt.encode(
        {"role": "admin", "exp": datetime.utcnow() + timedelta(minutes=10)},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    r_no_sub = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {no_sub_token}"})
    assert r_no_sub.status_code == 401

    ghost_token = create_access_token(subject="999999", role="admin")
    r_ghost = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {ghost_token}"})
    assert r_ghost.status_code == 404


def test_optional_current_user_edge_tokens_and_security_helpers(client, db_session):
    """Optional auth handles malformed/no-sub/non-int sub tokens safely; security helpers handle invalid inputs."""
    # Malformed token -> gracefully treated as anonymous (200)
    assert client.get("/api/v1/alerts", headers={"Authorization": "Bearer not.a.jwt"}).status_code == 200

    # Valid JWT without `sub` -> anonymous (200)
    no_sub = jwt.encode(
        {"role": "analyst", "exp": datetime.utcnow() + timedelta(minutes=10)},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    assert client.get("/api/v1/alerts", headers={"Authorization": f"Bearer {no_sub}"}).status_code == 200

    # Non-integer `sub` triggers int(user_id) exception path inside get_optional_current_user -> None (200)
    bad_sub = create_access_token(subject="not-an-integer", role="analyst")
    assert client.get("/api/v1/alerts", headers={"Authorization": f"Bearer {bad_sub}"}).status_code == 200

    # Security helper edge cases
    assert verify_password("secret", "corrupted-hash-value") is False
    assert sanitize_csv_cell("") == ""
    assert sanitize_csv_cell(None) == ""
    assert sanitize_csv_cell("=HYPERLINK(\"http://evil\")").startswith("'")

    # Targeted key reset in RateLimiter
    assert auth_rate_limiter.is_rate_limited("key_a") is False
    assert auth_rate_limiter.is_rate_limited("key_b") is False
    auth_rate_limiter.reset("key_a")
    assert "key_a" not in auth_rate_limiter._records
    assert "key_b" in auth_rate_limiter._records


# =====================================================================
# 2. ADMIN CRUD, MANUAL PRICE VALIDATION, AUDIT & CSV IMPORT/EXPORT
# =====================================================================

def test_admin_and_public_commodities_crud_lifecycle(client):
    """Full CRUD + duplicate/404 guards on both `/admin/commodities` and `/commodities`."""
    headers = _login_headers(client, "admin@test.com", "Admin123!")

    # Admin GET list
    res_list = client.get("/api/v1/admin/commodities", headers=headers)
    assert res_list.status_code == 200
    assert len(res_list.json()) >= 1

    # Admin POST create + duplicate 400
    payload = {
        "code": "PEPPER_BLACK",
        "name": "Hồ tiêu đen",
        "category": "Gia vị",
        "unit": "VNĐ/kg",
        "region": "Tây Nguyên",
        "description": "Tiêu đen xuất khẩu",
    }
    created = client.post("/api/v1/admin/commodities", json=payload, headers=headers)
    assert created.status_code == 200
    cid = created.json()["id"]

    dup = client.post("/api/v1/admin/commodities", json=payload, headers=headers)
    assert dup.status_code == 400

    # Admin PUT update + 404
    updated_payload = {**payload, "name": "Hồ tiêu đen Gia Lai"}
    upd = client.put(f"/api/v1/admin/commodities/{cid}", json=updated_payload, headers=headers)
    assert upd.status_code == 200
    assert upd.json()["name"] == "Hồ tiêu đen Gia Lai"
    assert client.put("/api/v1/admin/commodities/99999", json=updated_payload, headers=headers).status_code == 404

    # Public /commodities PUT & DELETE (Admin-only) + 404
    upd2 = client.put(f"/api/v1/commodities/{cid}", json={**payload, "name": "Hồ tiêu Đắk Lắk"}, headers=headers)
    assert upd2.status_code == 200
    assert upd2.json()["name"] == "Hồ tiêu Đắk Lắk"
    assert client.put("/api/v1/commodities/99999", json=payload, headers=headers).status_code == 404
    assert client.delete("/api/v1/commodities/99999", headers=headers).status_code == 404
    assert client.delete(f"/api/v1/commodities/{cid}", headers=headers).status_code == 200

    # Admin DELETE created & 404
    created2 = client.post(
        "/api/v1/admin/commodities",
        json={**payload, "code": "CASHEW_TEST"},
        headers=headers,
    )
    cid2 = created2.json()["id"]
    assert client.delete(f"/api/v1/admin/commodities/{cid2}", headers=headers).status_code == 200
    assert client.delete("/api/v1/admin/commodities/99999", headers=headers).status_code == 404


def test_admin_manual_price_audit_and_schema_validation(client, db_session):
    """Covers manual price insert/update/verify/delete audit trail and all PriceCreateManual validation rules."""
    headers = _login_headers(client, "admin@test.com", "Admin123!")
    c = db_session.query(Commodity).first()
    rec_date = str(date.today() - timedelta(days=2))

    # 404 unknown commodity
    r404 = client.post(
        "/api/v1/admin/prices",
        json={"commodity_id": 99999, "record_date": rec_date, "price": 100000, "reviewed": False},
        headers=headers,
    )
    assert r404.status_code == 404

    # Create unverified manual price
    r_create = client.post(
        "/api/v1/admin/prices",
        json={
            "commodity_id": c.id,
            "record_date": rec_date,
            "price": 105000,
            "price_min": 104000,
            "price_max": 106000,
            "volume": 500,
            "reviewed": False,
        },
        headers=headers,
    )
    assert r_create.status_code == 200
    price_id = r_create.json()["id"]
    assert r_create.json()["provenance"] == "unverified"

    # Update same date to reviewed=True with authentic source -> creates audit revision ("Xác minh bản ghi giá")
    r_verify = client.post(
        "/api/v1/admin/prices",
        json={
            "commodity_id": c.id,
            "record_date": rec_date,
            "price": 105000,
            "price_min": 104000,
            "price_max": 106000,
            "source": "Sở NN&PTNT Đắk Lắk",
            "reviewed": True,
        },
        headers=headers,
    )
    assert r_verify.status_code == 200
    assert r_verify.json()["provenance"] == "reviewed"

    # Recent prices date filter + invalid range 400
    bad_range = client.get(
        f"/api/v1/admin/prices/recent?start_date={date.today()}&end_date={date.today() - timedelta(days=5)}",
        headers=headers,
    )
    assert bad_range.status_code == 400
    ok_recent = client.get(
        f"/api/v1/admin/prices/recent?commodity_id={c.id}&start_date={rec_date}&end_date={date.today()}",
        headers=headers,
    )
    assert ok_recent.status_code == 200
    assert len(ok_recent.json()) == 1

    # Revisions before delete -> UPDATED
    revs_before = client.get("/api/v1/admin/prices/revisions", headers=headers)
    assert revs_before.status_code == 200
    assert revs_before.json()[0]["action"] == "UPDATED"
    assert revs_before.json()[0]["reason"] == "Xác minh bản ghi giá"

    # Delete price + 404 unknown
    assert client.delete("/api/v1/admin/prices/99999", headers=headers).status_code == 404
    assert client.delete(f"/api/v1/admin/prices/{price_id}", headers=headers).status_code == 200

    revs_after = client.get("/api/v1/admin/prices/revisions", headers=headers)
    assert revs_after.status_code == 200
    assert revs_after.json()[0]["action"] == "DELETED"

    # Exhaustive PriceCreateManual schema validation edge cases
    today = date.today()
    invalid_cases = [
        # reviewed=True without real source
        dict(commodity_id=1, record_date=today, price=10000, reviewed=True, source="Nhập thủ công bởi Quản trị viên"),
        # price <= 0
        dict(commodity_id=1, record_date=today, price=0, reviewed=False),
        # future date
        dict(commodity_id=1, record_date=today + timedelta(days=1), price=10000, reviewed=False),
        # price_min > price
        dict(commodity_id=1, record_date=today, price=10000, price_min=12000, reviewed=False),
        # price_max < price
        dict(commodity_id=1, record_date=today, price=10000, price_max=8000, reviewed=False),
        # source > 100 chars
        dict(commodity_id=1, record_date=today, price=10000, source="X" * 101, reviewed=False),
    ]
    for kwargs in invalid_cases:
        with pytest.raises(ValidationError):
            PriceCreateManual(**kwargs)


def test_admin_user_model_task_and_csv_branches(client, db_session):
    """Covers user role/status guards, model switcher, task validation/rate-limits, and CSV import/export errors."""
    headers = _login_headers(client, "admin@test.com", "Admin123!")
    admin_u = db_session.query(User).filter(User.email == "admin@test.com").first()
    analyst_u = db_session.query(User).filter(User.email == "user@test.com").first()
    c = db_session.query(Commodity).first()

    # Role update 404, invalid role 400, self-demote 400, valid update
    assert client.patch("/api/v1/admin/users/99999/role", json={"role": "analyst"}, headers=headers).status_code == 404
    assert client.patch(f"/api/v1/admin/users/{analyst_u.id}/role", json={"role": "superadmin"}, headers=headers).status_code == 400
    assert client.patch(f"/api/v1/admin/users/{admin_u.id}/role", json={"role": "analyst"}, headers=headers).status_code == 400
    assert client.patch(f"/api/v1/admin/users/{analyst_u.id}/role", json={"role": "user"}, headers=headers).status_code == 200

    # Toggle status 404, self-lock 400, legacy `_disabled` normalization
    assert client.patch("/api/v1/admin/users/99999/toggle-status", headers=headers).status_code == 404
    assert client.patch(f"/api/v1/admin/users/{admin_u.id}/toggle-status", headers=headers).status_code == 400
    analyst_u.role = "analyst_disabled"
    analyst_u.is_active = False
    db_session.commit()
    res_norm = client.patch(f"/api/v1/admin/users/{analyst_u.id}/toggle-status", headers=headers)
    assert res_norm.status_code == 200
    assert res_norm.json()["current_role"] == "analyst"
    assert res_norm.json()["is_active"] is True

    # Active model switcher: 400 invalid, insert & update
    assert client.post("/api/v1/admin/models/active", json={"active_model": "GPT9"}, headers=headers).status_code == 400
    r_m1 = client.post("/api/v1/admin/models/active", json={"active_model": "XGBoost"}, headers=headers)
    assert r_m1.status_code == 200 and r_m1.json()["active_model"] == "XGBOOST"
    r_m2 = client.post("/api/v1/admin/models/active", json={"active_model": "Prophet"}, headers=headers)
    assert r_m2.status_code == 200 and r_m2.json()["active_model"] == "PROPHET"

    # Tasks 404 & list with kind filter
    assert client.get("/api/v1/admin/tasks/99999", headers=headers).status_code == 404
    assert client.get("/api/v1/admin/tasks?kind=scrape", headers=headers).status_code == 200

    # Scrape & Retrain validation + rate limits
    assert client.post(f"/api/v1/admin/tasks/scrape?start_date={date.today() - timedelta(days=5)}", headers=headers).status_code == 400
    assert client.post("/api/v1/admin/tasks/scrape?commodity_id=99999", headers=headers).status_code == 400
    assert client.post("/api/v1/admin/tasks/retrain?commodity_id=99999", headers=headers).status_code == 404

    for _ in range(10):
        task_rate_limiter.is_rate_limited(f"scrape_{admin_u.id}")
        task_rate_limiter.is_rate_limited(f"retrain_{admin_u.id}")
    assert client.post("/api/v1/admin/tasks/scrape?days=7", headers=headers).status_code == 429
    assert client.post("/api/v1/admin/tasks/retrain", headers=headers).status_code == 429

    # CSV import error paths: wrong extension, empty file, mixed valid/invalid/update rows + latin-1 fallback
    bad_ext = client.post("/api/v1/admin/prices/import-csv", files={"file": ("hack.exe", b"abc", "application/octet-stream")}, headers=headers)
    assert bad_ext.status_code == 400
    empty_csv = client.post("/api/v1/admin/prices/import-csv", files={"file": ("empty.csv", b"", "text/csv")}, headers=headers)
    assert empty_csv.status_code == 400

    d1 = str(date.today() - timedelta(days=3))
    csv_body = (
        "commodity_id,record_date,price,source,reviewed\n"
        f", {d1}, ,missing,false\n"
        f"99999,{d1},100000,unknown,false\n"
        f"{c.id},{d1},112000,giacaphe.com,true\n"
        f"{c.id},{d1},113500,giacaphe.com,true\n"
        f"{c.id},bad-date,abc,giacaphe.com,false\n"
    ).encode("latin-1")
    imp = client.post("/api/v1/admin/prices/import-csv", files={"file": ("prices.csv", csv_body, "text/csv")}, headers=headers)
    assert imp.status_code == 200
    data = imp.json()
    assert data["records_created"] == 1
    assert data["records_updated"] == 1
    assert len(data["errors"]) == 3

    # Export CSV invalid range 400 & valid filtered export
    assert client.get(
        f"/api/v1/admin/prices/export-csv?start_date={date.today()}&end_date={date.today() - timedelta(days=2)}",
        headers=headers,
    ).status_code == 400
    exp_ok = client.get(
        f"/api/v1/admin/prices/export-csv?commodity_id={c.id}&start_date={d1}&end_date={date.today()}",
        headers=headers,
    )
    assert exp_ok.status_code == 200
    assert "113500.0" in exp_ok.text


# =====================================================================
# 3. ALERTS EVALUATION, OWNERSHIP, 404s & SMTP
# =====================================================================

def test_alert_evaluation_pct_triggers_ownership_and_404s(client, db_session):
    """Covers PCT_INC_7D, PCT_DEC_7D, empty price skip, full update, user filtering, and all 404 guards."""
    from app.services.alert_service import evaluate_all_alert_rules

    admin_headers = _login_headers(client, "admin@test.com", "Admin123!")
    analyst_headers = _login_headers(client, "user@test.com", "User123!")

    c_inc = db_session.query(Commodity).first()
    c_dec = Commodity(code="PEPPER_BLACK", name="Hồ tiêu đen", category="Gia vị", unit="VNĐ/kg", region="Tây Nguyên")
    c_empty = Commodity(code="EMPTY_COM", name="Nông sản trống", category="Khác", unit="VNĐ/kg", region="ĐBSCL")
    db_session.add_all([c_dec, c_empty])
    db_session.commit()

    # Seed 8 daily prices: c_inc jumps +20% (100k -> 120k), c_dec drops -20% (150k -> 120k)
    today = date.today()
    for i in range(8):
        dt = today - timedelta(days=7 - i)
        db_session.add(PriceHistory(commodity_id=c_inc.id, record_date=dt, price=100000.0 if i < 7 else 120000.0, provenance="collected"))
        db_session.add(PriceHistory(commodity_id=c_dec.id, record_date=dt, price=150000.0 if i < 7 else 120000.0, provenance="collected"))
    db_session.commit()

    # Create alerts via API
    r_inc = client.post(
        "/api/v1/alerts",
        json={"commodity_id": c_inc.id, "rule_name": "Tăng sốc 7N", "condition_type": "PCT_INC_7D", "threshold_value": 10.0, "email": "admin@test.com"},
        headers=admin_headers,
    )
    assert r_inc.status_code == 200
    r_dec = client.post(
        "/api/v1/alerts",
        json={"commodity_id": c_dec.id, "rule_name": "Giảm sâu 7N", "condition_type": "PCT_DEC_7D", "threshold_value": 10.0, "email": "user@test.com"},
        headers=analyst_headers,
    )
    assert r_dec.status_code == 200
    r_empty = client.post(
        "/api/v1/alerts",
        json={"commodity_id": c_empty.id, "rule_name": "Chưa có giá", "condition_type": "PRICE_ABOVE", "threshold_value": 100.0, "email": "user@test.com"},
        headers=analyst_headers,
    )
    assert r_empty.status_code == 200

    # Analyst sees only own rules; Admin sees all 3 rules
    assert len(client.get("/api/v1/alerts", headers=analyst_headers).json()) == 2
    assert len(client.get("/api/v1/alerts", headers=admin_headers).json()) == 3

    # Evaluate rules -> triggers exactly 2 (c_inc +20%, c_dec -20%), skips c_empty
    triggered = evaluate_all_alert_rules(db_session)
    assert triggered == 2
    logs = client.get("/api/v1/alerts/logs", headers=admin_headers).json()
    assert len(logs) == 2
    analyst_logs = client.get("/api/v1/alerts/logs", headers=analyst_headers).json()
    assert len(analyst_logs) == 1  # Analyst only sees own alert logs

    # Full field update on analyst's rule + 404 guards
    rule_id = r_dec.json()["id"]
    upd = client.put(
        f"/api/v1/alerts/{rule_id}",
        json={
            "commodity_id": c_inc.id,
            "rule_name": "Giảm sâu cập nhật",
            "condition_type": "PRICE_BELOW",
            "threshold_value": 90000.0,
            "email": "new@test.com",
            "is_active": False,
        },
        headers=analyst_headers,
    )
    assert upd.status_code == 200
    assert upd.json()["is_active"] is False
    assert upd.json()["email"] == "new@test.com"

    # 404 guards across all alert endpoints (authenticated)
    assert client.post("/api/v1/alerts", headers=analyst_headers, json={"commodity_id": 99999, "rule_name": "X", "condition_type": "PRICE_ABOVE", "threshold_value": 1, "email": "a@b.com"}).status_code == 404
    assert client.put("/api/v1/alerts/99999", headers=analyst_headers, json={"rule_name": "X"}).status_code == 404
    assert client.put(f"/api/v1/alerts/{rule_id}", json={"commodity_id": 99999}, headers=analyst_headers).status_code == 404
    assert client.patch("/api/v1/alerts/99999/toggle", headers=analyst_headers, json={"is_active": True}).status_code == 404
    assert client.delete("/api/v1/alerts/99999", headers=analyst_headers).status_code == 404
    assert client.post("/api/v1/alerts/99999/test", headers=analyst_headers).status_code == 404


def test_alert_email_smtp_success_and_error(monkeypatch):
    """Covers real SMTP branch (success and failure) alongside simulator branch."""
    from app.services.alert_service import send_email_notification

    # 1. Simulator branch (no SMTP creds)
    monkeypatch.setattr(settings, "SMTP_USER", "")
    monkeypatch.setattr(settings, "SMTP_PASSWORD", "")
    assert send_email_notification("a@b.com", "Test", "<p>Hi</p>") is True

    # 2. Configured SMTP success path
    called = []

    class FakeSMTP:
        def __init__(self, host, port, timeout=10):
            called.append(("init", host, port))
        def starttls(self):
            called.append(("starttls",))
        def login(self, user, pwd):
            called.append(("login", user))
        def sendmail(self, frm, to_list, body):
            called.append(("sendmail", to_list))
        def quit(self):
            called.append(("quit",))

    monkeypatch.setattr(settings, "SMTP_USER", "bot@agroforecast.vn")
    monkeypatch.setattr(settings, "SMTP_PASSWORD", "app-pass")
    monkeypatch.setattr(smtplib, "SMTP", FakeSMTP)
    assert send_email_notification("farmer@vn.org", "Alert", "<b>Spike</b>") is True
    assert [c[0] for c in called] == ["init", "starttls", "login", "sendmail", "quit"]

    # 3. Configured SMTP failure path -> catches safely and returns False
    def failing_smtp(*args, **kwargs):
        raise OSError("Connection refused")

    monkeypatch.setattr(smtplib, "SMTP", failing_smtp)
    assert send_email_notification("farmer@vn.org", "Alert", "<b>Spike</b>") is False


# =====================================================================
# 4. REGIONAL PRICING, HISTORY, PRICES & SPOTLIGHT
# =====================================================================

def test_regional_pricing_tonnes_unknown_province_and_direct_series(client, db_session, monkeypatch):
    """Covers VNĐ/tấn freight math, <=5km zero spread, unknown province fallback, direct >=5 series, and 404/400."""
    from app.services.regional_pricing_service import (
        compute_logistics_spread,
        resolve_commodity_location_context,
    )

    assert compute_logistics_spread(3.5, "VNĐ/kg", 100000.0) == 0.0
    assert compute_logistics_spread(100.0, "VNĐ/tấn", 1200000.0) == 70000.0
    assert compute_logistics_spread(500.0, "VNĐ/tấn", 1200000.0) == 120000.0  # capped

    sugar = Commodity(code="SUGARCANE", name="Mía đường", category="Cây công nghiệp", unit="VNĐ/tấn", region="Phú Yên - Khánh Hòa")
    db_session.add(sugar)
    db_session.commit()

    # Unknown province gracefully falls back to national_benchmark
    unknown_ctx = resolve_commodity_location_context(db_session, sugar, "atlantis-99")
    assert unknown_ctx["pricing_mode"] == "national_benchmark"

    # Seed 7 days of national PriceHistory + 6 direct RegionalPriceObservation rows for Khánh Hòa
    today = date.today()
    for i in range(7):
        dt = today - timedelta(days=6 - i)
        db_session.add(PriceHistory(commodity_id=sugar.id, record_date=dt, price=1250000.0 + i * 5000, source="VSSA", provenance="collected"))
        if i >= 1:
            db_session.add(
                RegionalPriceObservation(
                    commodity_id=sugar.id,
                    province_code="khanh-hoa",
                    recorded_date=dt,
                    price=1280000.0 + i * 5000,
                    source="Báo Khánh Hòa",
                    source_url="https://baokhanhhoa.vn/",
                )
            )
    db_session.commit()

    # Overview with >=5 direct observations uses exact provincial sparkline!
    ov = client.get("/api/v1/market/overview?province=khanh-hoa")
    assert ov.status_code == 200
    sugar_card = next(x for x in ov.json() if x["code"] == "SUGAR")
    assert sugar_card["currentPrice"] == 1310000.0
    assert len(sugar_card["sparkline"]) == 6
    assert sugar_card["location_context"]["pricing_mode"] == "direct"

    # History endpoint hits exact `direct_by_date` rows
    h = client.get(
        f"/api/v1/history?commodity_id={sugar.id}&start_date={today - timedelta(days=6)}&end_date={today}&province=khanh-hoa"
    )
    assert h.status_code == 200
    assert any("Báo Khánh Hòa (Khánh Hòa)" in rec["source"] for rec in h.json()["records"])

    # Regions list includes direct_commodities for Khánh Hòa
    regs = client.get("/api/v1/regions")
    assert regs.status_code == 200
    kh = next(r for r in regs.json() if r["code"] == "khanh-hoa")
    assert any(dc["commodity_code"] == "SUGARCANE" for dc in kh["direct_commodities"])

    # Unknown commodity in regional-prices -> 404
    assert client.get("/api/v1/market/regional-prices/UNKNOWN_ITEM").status_code == 404

    # Regions locate error path -> 400
    monkeypatch.setattr(
        "app.api.v1.endpoints.regions.locate_nearest_province",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("Geo failure")),
    )
    assert client.get("/api/v1/regions/locate?lat=12.2&lng=109.1").status_code == 400


def test_history_readiness_sources_prices_comparison_and_spotlight(client, db_session):
    """Covers /history/readiness, /history/training-runs/{id}, /history/sources, /prices/history, /spotlight, /comparison."""
    c = db_session.query(Commodity).first()

    # Empty prices -> comparison returns [], spotlight returns 0 placeholder
    assert client.get("/api/v1/commodities/comparison").json() == []
    sp_empty = client.get(f"/api/v1/commodities/spotlight?code={c.code}")
    assert sp_empty.status_code == 200 and sp_empty.json()["trendData"] == []

    # Seed 15 days -> comparison samples <= 9 points, spotlight computes trend & peak
    _seed_daily_prices(db_session, c.id, days=15, base_price=95000.0)
    comp = client.get("/api/v1/commodities/comparison?province=khanh-hoa")
    assert comp.status_code == 200 and len(comp.json()) >= 2

    sp_ok = client.get(f"/api/v1/commodities/spotlight?code={c.code}")
    assert sp_ok.status_code == 200 and len(sp_ok.json()["trendData"]) >= 2

    # /prices/history
    ph = client.get(f"/api/v1/prices/history?commodity_id={c.id}&days=10")
    assert ph.status_code == 200 and len(ph.json()) == 10

    # /history/readiness, /history/sources, /history/training-runs/{id} + 404s
    assert client.get(f"/api/v1/history/readiness?commodity_id={c.id}").status_code == 200
    assert client.get("/api/v1/history/readiness?commodity_id=99999").status_code == 404
    assert client.get("/api/v1/history/sources").status_code == 200
    assert client.get(f"/api/v1/history?commodity_id=99999&start_date={date.today() - timedelta(days=5)}&end_date={date.today()}").status_code == 404

    run = TrainingRun(commodity_id=c.id, dataset_hash="abc123", metadata_json=json.dumps({"cadence": "daily"}))
    db_session.add(run)
    db_session.commit()
    assert client.get(f"/api/v1/history/training-runs/{run.id}").status_code == 200
    assert client.get("/api/v1/history/training-runs/99999").status_code == 404

    # Empty Commodity table -> spotlight fallback & comparison []
    db_session.query(PriceHistory).delete()
    db_session.query(TrainingRun).delete()
    db_session.query(Commodity).delete()
    db_session.commit()
    assert client.get("/api/v1/commodities/comparison").json() == []
    assert client.get("/api/v1/commodities/spotlight?code=NONE").json()["commodityCode"] == "COFFEE"


# =====================================================================
# 5. HISTORY CADENCE, FORECAST ERRORS, TRAINING/JOB RECOVERY, SCHEDULER & UPGRADE
# =====================================================================

def test_history_service_cadence_and_readiness_branches(db_session, monkeypatch):
    """Covers unknown commodity ValueError, gap/invalid price readiness, periodic->daily fallback, and irregular cadence."""
    from app.services.history_service import readiness, training_context

    with pytest.raises(ValueError):
        training_context(db_session, 99999)

    # Gap > 14 days (20-day gap inside 65-row series -> readiness rejects with "khoảng trống")
    start = date.today() - timedelta(days=100)
    gapped_rows = [
        SimpleNamespace(record_date=start + timedelta(days=i if i < 30 else i + 20), price=100000.0)
        for i in range(65)
    ]
    q_gap = readiness(gapped_rows, cadence="daily")
    assert q_gap["ready"] is False and "khoảng trống" in q_gap["reason"]

    # Invalid price <= 0 -> readiness rejects with "giá không hợp lệ"
    bad_rows = [
        SimpleNamespace(record_date=start + timedelta(days=i), price=0.0 if i == 10 else 100000.0)
        for i in range(65)
    ]
    q_bad = readiness(bad_rows, cadence="daily")
    assert q_bad["ready"] is False and "giá không hợp lệ" in q_bad["reason"]

    # Periodic commodity (SUGARCANE) with daily PriceHistory fallback
    sugar = Commodity(code="SUGARCANE", name="Mía đường", category="Cây công nghiệp", unit="VNĐ/tấn", region="Phú Yên")
    db_session.add(sugar)
    db_session.commit()
    _seed_daily_prices(db_session, sugar.id, days=10, base_price=1200000.0)
    ctx_sugar = training_context(db_session, sugar)
    assert ctx_sugar["cadence"] == "daily"

    # Irregular cadence (monkeypatch SOURCES entry for COFFEE_ROBUSTA)
    coffee = db_session.query(Commodity).filter(Commodity.code == "COFFEE_ROBUSTA").first()
    _seed_daily_prices(db_session, coffee.id, days=5, base_price=100000.0)
    monkeypatch.setitem(
        __import__("ml_pipeline.source_catalog", fromlist=["SOURCES"]).SOURCES,
        "COFFEE_ROBUSTA",
        {"kind": "irregular"},
    )
    ctx_irreg = training_context(db_session, coffee)
    assert ctx_irreg["cadence"] == "irregular"
    assert "mốc công bố" in ctx_irreg["quality"]["reason"]


def test_forecast_service_errors_and_legacy_fallback(client, db_session):
    """Covers forecast 404, 409 not-ready, 400 unsupported model, 409 missing forecast, and legacy no-run forecast."""
    c = db_session.query(Commodity).first()

    # 404 unknown commodity
    assert client.get("/api/v1/forecast?commodity_id=99999").status_code == 404
    assert client.get("/api/v1/forecast/compare/99999").status_code == 404

    # Not ready (<60 rows) -> 409 on forecast, [] on compare
    assert client.get(f"/api/v1/forecast?commodity_id={c.id}").status_code == 409
    assert client.get(f"/api/v1/forecast/compare/{c.id}").json() == []

    # Seed 65 daily eligible prices
    _seed_daily_prices(db_session, c.id, days=65, base_price=100000.0)

    # Unsupported model -> 400
    assert client.get(f"/api/v1/forecast?commodity_id={c.id}&model_name=GPT4").status_code == 400

    # Ready data, zero forecasts -> 409
    assert client.get(f"/api/v1/forecast?commodity_id={c.id}&model_name=LSTM").status_code == 409

    # Insert legacy forecasts (training_run_id=None) -> forecast & compare succeed with fallback metadata
    for i in range(1, 8):
        db_session.add(
            Forecast(
                commodity_id=c.id,
                model_name="LSTM",
                training_run_id=None,
                forecast_date=date.today() + timedelta(days=i),
                predicted_price=108000.0 + i * 200,
                lower_ci=106000.0,
                upper_ci=110000.0,
                mae=850.0,
                rmse=1100.0,
                mape=0.85,
                r2=0.92,
                training_date=date.today(),
            )
        )
    db_session.commit()

    dash = client.get(f"/api/v1/forecast?commodity_id={c.id}&model_name=LSTM&days=7")
    assert dash.status_code == 200
    assert dash.json()["training"]["run_id"] == 0
    comp = client.get(f"/api/v1/forecast/compare/{c.id}")
    assert comp.status_code == 200 and comp.json()[0]["modelName"] == "LSTM"


def test_training_service_and_job_service_recovery(db_session, monkeypatch):
    """Covers training error isolation (PARTIAL/FAILED/overflow), walk-forward active_model update, and run_job retrain."""
    import app.services.training_service as ts
    from app.services.job_service import create_job, run_job, sync_forecast_after_scrape

    assert ts._select_best_model({}) == "LSTM"

    with pytest.raises(ValueError):
        ts.retrain(99999, lambda p, m: None)

    c = db_session.query(Commodity).first()
    _seed_daily_prices(db_session, c.id, days=125, base_price=100000.0)

    # 1. Partial failure: LSTM raises RuntimeError, ARIMA returns overflow >=1e12, others succeed
    def flaky_predict(name, series, horizon, future_index=None):
        if name == "LSTM":
            raise RuntimeError("CUDA OOM simulated")
        if name == "ARIMA":
            return np.full(horizon, 1e13)
        return np.full(horizon, float(series.iloc[-1]))

    monkeypatch.setattr(ts, "predict_series", flaky_predict)
    res_partial = ts.retrain(c.id, lambda p, m: None)
    assert res_partial["status"] == "PARTIAL"
    assert res_partial["count"] == 90  # 3 succeeding models * 30 days
    assert "CUDA OOM" in res_partial["message"]
    assert "vượt giới hạn" in res_partial["message"]

    # 2. Real walk-forward orchestration branch (commodity_id=None auto-selects best active_model)
    def fast_default_predict(name, series, horizon, future_index=None):
        return np.full(horizon, float(series.iloc[-1]))

    monkeypatch.setattr(ts, "_DEFAULT_PREDICT_SERIES", fast_default_predict)
    monkeypatch.setattr(ts, "predict_series", fast_default_predict)
    monkeypatch.setattr(ts, "walk_forward_baseline", lambda *a, **kw: {"mae": 500.0, "rmse": 600.0, "mape": 0.5, "r2": 0.9})
    monkeypatch.setattr(
        ts,
        "walk_forward_evaluate",
        lambda name, *a, **kw: {
            "metrics": {"mae": 100.0 if name == "XGBoost" else 300.0, "rmse": 150.0, "mape": 0.2 if name == "XGBoost" else 0.8, "r2": 0.96},
            "ci_scale_1d": 200.0,
            "accuracy": 99.8 if name == "XGBoost" else 99.2,
            "picp_95": 95.0,
            "q95": 200.0,
            "evaluated_points": 60,
        },
    )
    res_wf = ts.retrain(None, lambda p, m: None)
    assert res_wf["status"] == "SUCCESS"
    assert res_wf["count"] == 150  # 5 models * 30 days
    active_row = db_session.get(SystemSetting, "active_model")
    assert active_row is not None and active_row.value == "XGBOOST"

    # 3. sync_forecast_after_scrape recognizes already-synced commodity without retraining
    msg_synced, failed = sync_forecast_after_scrape(1, {"commodity_id": c.id})
    assert failed is False
    assert "đã đồng bộ" in msg_synced

    # 4. run_job("retrain") success + unhandled exception -> FAILED
    job_ok = create_job(db_session, "retrain")
    run_job(job_ok.id, "retrain", c.id)
    db_session.expire_all()
    assert db_session.get(BackgroundJob, job_ok.id).status == "SUCCESS"

    monkeypatch.setattr(ts, "retrain", lambda *a, **kw: (_ for _ in ()).throw(RuntimeError("Disk full")))
    job_fail = create_job(db_session, "retrain")
    run_job(job_fail.id, "retrain", c.id)
    db_session.expire_all()
    failed_job = db_session.get(BackgroundJob, job_fail.id)
    assert failed_job.status == "FAILED" and "Disk full" in failed_job.message


def test_predictions_endpoints_and_async_retrain(client, db_session, monkeypatch):
    """Covers /predictions/forecast (commodity_id, 500 error, empty 404), /predictions/metrics, and _async_retrain_task."""
    from app.api.v1.endpoints.predictions import _async_retrain_task
    import app.api.v1.endpoints.predictions as pred_mod

    c = db_session.query(Commodity).first()
    _seed_daily_prices(db_session, c.id, days=15, base_price=100000.0)

    # /predictions/forecast with commodity_id (valid response path)
    monkeypatch.setattr(
        pred_mod.PricePredictor,
        "forecast",
        lambda self, **kw: {
            "symbol": self.code,
            "commodity": {"id": c.id, "code": c.code, "name": c.name},
            "model_name": kw.get("model_name", "LSTM"),
            "forecast_days": kw.get("days", 7),
            "response_time_ms": 12.5,
            "cached": False,
            "metrics": {"mae": 100.0, "rmse": 120.0, "mape": 0.5, "r2": 0.95},
            "history": [],
            "forecast": [
                {
                    "date": str(date.today() + timedelta(days=1)),
                    "yhat": 102000.0,
                    "yhat_lower": 101000.0,
                    "yhat_upper": 103000.0,
                    "is_forecast": True,
                }
            ],
            "all_points": [],
        },
    )
    r_ok = client.get(f"/api/v1/predictions/forecast?commodity_id={c.id}&model=LSTM&days=7")
    assert r_ok.status_code == 200
    assert r_ok.json()["symbol"] == c.code

    # /predictions/forecast default fallback when neither symbol nor commodity_id is passed
    r_def = client.get("/api/v1/predictions/forecast")
    assert r_def.status_code == 200

    # /predictions/metrics with populated metrics summary
    monkeypatch.setattr(
        pred_mod.PricePredictor,
        "get_metrics_summary",
        lambda self: {"LSTM": {"metrics": {"mae": 100.0}, "trained_at": "2026-11-20", "passed_threshold": True}},
    )
    r_met = client.get(f"/api/v1/predictions/metrics?symbol={c.code}")
    assert r_met.status_code == 200 and len(r_met.json()["models"]) == 1

    # /predictions/forecast error branch -> 500
    monkeypatch.setattr(
        pred_mod.PricePredictor,
        "forecast",
        lambda self, **kw: (_ for _ in ()).throw(RuntimeError("Predictor broken")),
    )
    assert client.get(f"/api/v1/predictions/forecast?commodity_id={c.id}").status_code == 500

    # _async_retrain_task happy path & exception path
    trained = []
    monkeypatch.setattr(pred_mod.ModelTrainer, "train_all", lambda self, df: trained.append(self.commodity_code))
    _async_retrain_task(commodity_id=c.id)
    _async_retrain_task(commodity_id=None)
    assert trained == [c.code, c.code]

    monkeypatch.setattr(pred_mod, "load_clean_data", lambda *a, **kw: (_ for _ in ()).throw(RuntimeError("Boom")))
    _async_retrain_task(commodity_id=c.id)  # catches cleanly

    # Empty commodity table without symbol -> 404
    db_session.query(PriceHistory).delete()
    db_session.query(Commodity).delete()
    db_session.commit()
    assert client.get("/api/v1/predictions/forecast").status_code == 404


def test_scheduler_schema_upgrade_and_main_health(client, db_session, monkeypatch):
    """Covers APScheduler tasks/lifecycle, idempotent schema_upgrade on fresh SQLite, /health degraded, and global handler."""
    import app.core.scheduler as sched
    import app.core.schema_upgrade as su
    from app.main import global_exception_handler

    # 1. scheduled_scraper_task & scheduled_alert_evaluation_task (normal + error handling)
    scraped_ids = []
    monkeypatch.setattr("app.services.job_service.run_job", lambda jid, kind, opt: scraped_ids.append(opt["commodity_id"]))
    sched.scheduled_scraper_task()
    assert len(scraped_ids) == 1

    monkeypatch.setattr("app.services.job_service.create_job", lambda *a, **kw: (_ for _ in ()).throw(RuntimeError("Locked")))
    sched.scheduled_scraper_task()  # logs & survives

    monkeypatch.setattr(sched, "evaluate_all_alert_rules", lambda db: 3)
    sched.scheduled_alert_evaluation_task()
    monkeypatch.setattr(sched, "evaluate_all_alert_rules", lambda db: (_ for _ in ()).throw(RuntimeError("Alert err")))
    sched.scheduled_alert_evaluation_task()  # logs & survives

    # Start + idempotent second call + stop APScheduler
    inst1 = sched.start_scheduler()
    inst2 = sched.start_scheduler()
    assert inst1 is inst2
    sched.stop_scheduler()
    assert sched._scheduler_instance is None

    # 2. upgrade_existing_schema() adds missing legacy columns idempotently on a temp SQLite engine
    tmp_engine = create_engine("sqlite:///:memory:")
    with tmp_engine.begin() as conn:
        conn.execute(text("CREATE TABLE price_history (id INTEGER PRIMARY KEY, price REAL)"))
        conn.execute(text("CREATE TABLE forecasts (id INTEGER PRIMARY KEY, predicted_price REAL)"))
        conn.execute(text("CREATE TABLE users (id INTEGER PRIMARY KEY, email VARCHAR(100))"))
    monkeypatch.setattr(su, "engine", tmp_engine)
    su.upgrade_existing_schema()
    insp = inspect(tmp_engine)
    assert {"provenance", "source_details"}.issubset({c["name"] for c in insp.get_columns("price_history")})
    assert "training_run_id" in {c["name"] for c in insp.get_columns("forecasts")}
    assert "is_active" in {c["name"] for c in insp.get_columns("users")}

    # 3. Root, /health degraded branch, and global_exception_handler
    assert client.get("/").status_code == 200
    monkeypatch.setattr(db_session, "execute", lambda *a, **kw: (_ for _ in ()).throw(RuntimeError("DB offline")))
    r_deg = client.get("/health")
    assert r_deg.status_code == 200 and r_deg.json()["status"] == "degraded"

    import asyncio
    fake_req = SimpleNamespace(url="http://test/boom")
    resp = asyncio.run(global_exception_handler(fake_req, RuntimeError("Unexpected")))
    assert resp.status_code == 500
