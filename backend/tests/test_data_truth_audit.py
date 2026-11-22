# -*- coding: utf-8 -*-
"""Regression tests for data provenance truth audit:
- VietnamBiz URL date parsing (no 201 -> 2/01 or 301 -> 3/01 collision)
- Zero pre-2024 / ttcgroup.vn entries in sugarcane provincial scraper
- /api/v1/history never overrides daily benchmark source_url with a different-date regional article URL
"""
from datetime import date, timedelta
import json
from app.models.models import Commodity, PriceHistory, RegionalPriceObservation
from app.services.regional_pricing_service import ensure_regional_markets_seeded
from ml_pipeline.vietnam_real_scrapers import (
    ALLOWED_SCRAPER_DOMAINS,
    SUGARCANE_PROVINCIAL_SOURCES,
    _extract_date_from_vnbiz_url,
)


def test_vnbiz_url_date_parser_no_zero_pad_collision():
    cases = [
        (
            "https://vietnambiz.vn/gia-ca-phe-hom-nay-201-robusta-va-arabica-dong-loat-tang-tren-thi-truong-the-gioi-2024119173441643.htm",
            date(2024, 1, 20),
        ),
        (
            "https://vietnambiz.vn/gia-ca-phe-hom-nay-301-dong-loat-tang-tai-thi-truong-noi-dia-202412913535466.htm",
            date(2024, 1, 30),
        ),
        (
            "https://vietnambiz.vn/gia-tieu-hom-nay-206-noi-dia-giam-manh-mat-moc-140000-dongkg-2026619212142477.htm",
            date(2026, 6, 20),
        ),
        (
            "https://vietnambiz.vn/gia-lua-gao-hom-nay-301-di-ngang-tren-dien-rong-2024129141749841.htm",
            date(2024, 1, 30),
        ),
        (
            "https://vietnambiz.vn/gia-ca-phe-hom-nay-194-san-luong-ca-phe-cua-brazil-co-the-cao-hon-uoc-tinh-ban-dau-20254197146.htm",
            date(2025, 4, 19),
        ),
        (
            "https://vietnambiz.vn/gia-lua-gao-hom-nay-2011-gia-gao-an-do-va-thai-lan-tang-manh-gao-viet-nam-quay-dau-giam-20261120141235470.htm",
            date(2026, 11, 20),
        ),
        (
            "https://vietnambiz.vn/gia-ca-phe-hom-nay-21-tang-nhe-202412081500123.htm",
            date(2024, 1, 2),
        ),
    ]
    for url, expected in cases:
        assert _extract_date_from_vnbiz_url(url) == expected, f"Failed for {url}"


def test_sugarcane_provincial_sources_exclude_pre_2024_and_ttcgroup():
    assert "ttcgroup.vn" not in ALLOWED_SCRAPER_DOMAINS
    for item in SUGARCANE_PROVINCIAL_SOURCES:
        assert "ttcgroup.vn" not in item["url"].lower()
        assert item["fallback_date"] >= date(2024, 1, 1)


def test_history_never_inherits_other_date_direct_source_url(client, db_session):
    ensure_regional_markets_seeded(db_session)
    cane = Commodity(
        code="SUGARCANE",
        name="Mía đường",
        category="Cây công nghiệp",
        unit="VNĐ/tấn",
        region="Phú Yên",
    )
    db_session.add(cane)
    db_session.commit()
    db_session.refresh(cane)

    d_survey = date(2026, 4, 10)
    d_other = date(2026, 8, 24)
    yahoo_url = "https://finance.yahoo.com/quote/SB=F/history/"
    kh_url = "https://nongnghiepmoitruong.vn/lien-ket-trong-mia-khoi-thong-nguon-luc-de-phat-trien-ben-vung-d801982.html"

    for dt, price in [(d_survey, 1000000.0), (d_other, 1021000.0)]:
        db_session.add(
            PriceHistory(
                commodity_id=cane.id,
                record_date=dt,
                price=price,
                source="Quy đổi sàn ICE Sugar #11 (Yahoo Finance SB=F)",
                provenance="collected",
                source_details=json.dumps({"source_url": yahoo_url}),
            )
        )
    db_session.add(
        RegionalPriceObservation(
            commodity_id=cane.id,
            province_code="khanh-hoa",
            recorded_date=d_survey,
            price=1000000.0,
            source="Báo Nông nghiệp & Môi trường (Khánh Hòa)",
            source_url=kh_url,
            pricing_type="direct_survey",
        )
    )
    db_session.commit()

    resp = client.get(
        f"/api/v1/history?commodity_id={cane.id}&start_date=2026-04-01&end_date=2026-08-31&province=khanh-hoa"
    )
    assert resp.status_code == 200
    by_date = {r["date"]: r for r in resp.json()["records"]}

    # Exact same-day survey row gets the provincial article URL
    assert by_date["2026-04-10"]["source_url"] == kh_url
    # Different-day benchmark row MUST keep Yahoo Finance SB=F history URL (never inherit April article!)
    assert by_date["2026-08-24"]["source_url"] == yahoo_url
    assert "Yahoo Finance SB=F" in by_date["2026-08-24"]["source"]

