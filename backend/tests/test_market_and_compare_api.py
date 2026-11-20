"""
Automated Testing Suite - Pillar 3.1.2: Market Overview, Normalized Comparison & CSV Import/Export
File: backend/tests/test_market_and_compare_api.py
"""
import math
from datetime import date, timedelta
import pytest
from app.models.models import Commodity, PriceHistory, PriceRevision


def get_admin_headers(client) -> dict:
    res = client.post("/api/v1/auth/login", json={"email": "admin@test.com", "password": "Admin123!"})
    return {"Authorization": f"Bearer {res.json()['access_token']}"}


def seed_four_commodities_with_prices(db_session):
    db_session.query(PriceHistory).delete()
    db_session.query(Commodity).delete()
    db_session.commit()

    items = [
        ("RICE_IR504", "Lúa gạo IR50404", "Lương thực", "VNĐ/kg", "An Giang", 8000.0),
        ("COFFEE_ROBUSTA", "Cà phê Robusta", "Nông sản xuất khẩu", "VNĐ/kg", "Đắk Lắk", 110000.0),
        ("PEPPER_BLACK", "Hồ tiêu đen", "Gia vị", "VNĐ/kg", "Gia Lai", 140000.0),
        ("SUGARCANE", "Mía đường", "Cây công nghiệp", "VNĐ/tấn", "Phú Yên", 1200000.0),
    ]
    created = []
    for code, name, cat, unit, reg, base_price in items:
        c = Commodity(code=code, name=name, category=cat, unit=unit, region=reg)
        db_session.add(c)
        db_session.flush()
        created.append(c)
        for i in range(15):
            d = date.today() - timedelta(days=15 - i)
            # Tăng đều 1% mỗi ngày so với mốc gốc
            p_val = round(base_price * (1.0 + 0.01 * i), 2)
            db_session.add(PriceHistory(
                commodity_id=c.id,
                record_date=d,
                price=p_val,
                price_min=round(p_val * 0.99, 2),
                price_max=round(p_val * 1.01, 2),
                volume=1200.0,
                provenance="reviewed",
                source="Sở NN&PTNT"
            ))
    db_session.commit()
    return created


def test_market_overview_and_consistent_sugarcane_unit(client, db_session):
    """TC-MKT-01: Kiểm tra API tổng quan thị trường và đơn vị chuẩn hóa (Mía đường là VNĐ/tấn)"""
    seed_four_commodities_with_prices(db_session)

    res = client.get("/api/v1/commodities/overview")
    assert res.status_code == 200
    cards = res.json()
    assert len(cards) == 4

    sugar_card = next(c for c in cards if c["code"] == "SUGAR")
    assert sugar_card["unit"] == "VNĐ/tấn"
    assert sugar_card["currentPrice"] > 1000000
    assert len(sugar_card["sparkline"]) == 7

    reg_res = client.get("/api/v1/commodities/regional-prices")
    assert reg_res.status_code == 200
    reg_items = reg_res.json()
    sugar_reg = next(r for r in reg_items if r["code"] == "SUGAR")
    assert sugar_reg["unit"] == "VNĐ/tấn"


def test_normalized_growth_comparison_formula_and_no_nan(client, db_session):
    """TC-MKT-02: Kiểm tra API /commodities/comparison trả đúng % tăng trưởng chuẩn hóa, không có NaN/Infinity"""
    seed_four_commodities_with_prices(db_session)

    res = client.get("/api/v1/commodities/comparison")
    assert res.status_code == 200
    points = res.json()
    assert len(points) >= 2

    # Điểm đầu kỳ phải có mức tăng trưởng 0.0%
    first = points[0]
    for key in ("rice", "coffee", "pepper", "sugar"):
        assert first[key] == pytest.approx(0.0, abs=1e-6)

    # Mọi điểm phải hữu hạn và điểm cuối kỳ phải phản ánh đúng công thức ((P_t - P_0) / P_0) * 100 = +14.0%
    for pt in points:
        for key in ("rice", "coffee", "pepper", "sugar"):
            assert math.isfinite(pt[key])

    last = points[-1]
    assert last["coffee"] == pytest.approx(14.0, abs=0.05)
    assert last["sugar"] == pytest.approx(14.0, abs=0.05)


def test_history_filtering_by_date_and_commodity(client, db_session):
    """TC-MKT-03: Kiểm tra API /history lọc theo nông sản và khoảng ngày"""
    comms = seed_four_commodities_with_prices(db_session)
    coffee = next(c for c in comms if c.code == "COFFEE_ROBUSTA")

    start_d = str(date.today() - timedelta(days=5))
    end_d = str(date.today() - timedelta(days=1))
    res = client.get(f"/api/v1/history?commodity_id={coffee.id}&start_date={start_d}&end_date={end_d}")
    assert res.status_code == 200
    data = res.json()
    assert len(data["records"]) == 5
    for rec in data["records"]:
        assert start_d <= rec["date"] <= end_d
        assert rec["provenance"] == "reviewed"


def test_csv_import_valid_invalid_and_formula_injection_defense(client, db_session):
    """TC-MKT-04: Kiểm tra Import CSV hợp lệ, bắt lỗi dòng sai/file sai/quá 5MB và chống CSV Formula Injection khi Export"""
    headers = get_admin_headers(client)
    com = db_session.query(Commodity).first()

    # 1. Từ chối định dạng file không phải CSV (.exe)
    bad_ext = client.post(
        "/api/v1/admin/prices/import-csv",
        headers=headers,
        files={"file": ("malware.exe", b"MZ...", "application/octet-stream")}
    )
    assert bad_ext.status_code == 400

    # 2. Từ chối file vượt quá 5MB
    oversized = b"commodity_code,record_date,price,source\n" + (b"COFFEE_ROBUSTA,2026-01-01,100000,Test\n" * 150000)
    assert len(oversized) > 5 * 1024 * 1024
    too_large_res = client.post(
        "/api/v1/admin/prices/import-csv",
        headers=headers,
        files={"file": ("huge.csv", oversized, "text/csv")}
    )
    assert too_large_res.status_code == 400

    # 3. Import CSV kết hợp dòng hợp lệ, dòng giá âm (lỗi), dòng thiếu giá (lỗi), và dòng chứa công thức độc hại
    csv_body = (
        "commodity_code,record_date,price,source,reviewed\n"
        f"{com.code},2026-02-01,115000,=cmd|' /C calc'!A0,true\n"
        f"{com.code},2026-02-02,-500,Nguồn lỗi giá âm,false\n"
        f"{com.code},2026-02-03,,Thiếu giá,false\n"
        f"UNKNOWN_CODE,2026-02-04,90000,Mã nông sản sai,false\n"
    )
    imp_res = client.post(
        "/api/v1/admin/prices/import-csv",
        headers=headers,
        files={"file": ("import_test.csv", csv_body.encode("utf-8"), "text/csv")}
    )
    assert imp_res.status_code == 200
    imp_data = imp_res.json()
    assert imp_data["records_created"] == 1
    assert len(imp_data["errors"]) == 3

    # 4. Kiểm tra Export CSV đã vô hiệu hóa CSV Formula Injection (thêm dấu nháy đơn ')
    exp_res = client.get("/api/v1/admin/prices/export-csv?start_date=2026-02-01&end_date=2026-02-01", headers=headers)
    assert exp_res.status_code == 200
    assert "'=cmd" in exp_res.text

    # 5. Kiểm tra xóa bản ghi giá ghi nhận vào Audit Log (PriceRevision)
    created_row = db_session.query(PriceHistory).filter(PriceHistory.record_date == date(2026, 2, 1)).one()
    del_res = client.delete(f"/api/v1/admin/prices/{created_row.id}", headers=headers)
    assert del_res.status_code == 200
    rev_res = client.get("/api/v1/admin/prices/revisions", headers=headers)
    assert rev_res.status_code == 200
    assert len(rev_res.json()) >= 1
    assert rev_res.json()[0]["action"] == "DELETED"

