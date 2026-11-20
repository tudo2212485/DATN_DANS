"""
Automated Testing Suite - Location-Aware Regional Pricing (Haversine Benchmark & Direct Survey)
File: backend/tests/test_regional_pricing.py
"""
import math
from datetime import date, timedelta

import numpy as np
import pandas as pd

import app.services.training_service as training_service
from app.models.models import Commodity, PriceHistory, RegionalPriceObservation
from app.services.regional_pricing_service import ensure_regional_markets_seeded


def _seed_two_commodities_with_regional_obs(db_session, days: int = 70):
    ensure_regional_markets_seeded(db_session)
    coffee = db_session.query(Commodity).filter(Commodity.code == "COFFEE_ROBUSTA").first()
    sugar = db_session.query(Commodity).filter(Commodity.code == "SUGARCANE").first()
    if not sugar:
        sugar = Commodity(
            code="SUGARCANE",
            name="Mía đường",
            category="Cây công nghiệp",
            unit="VNĐ/tấn",
            region="Nam Trung Bộ & Tây Ninh",
        )
        db_session.add(sugar)
        db_session.commit()

    db_session.query(PriceHistory).delete()
    db_session.query(RegionalPriceObservation).delete()
    db_session.commit()

    today = date.today()
    for i in range(days):
        d = today - timedelta(days=days - i)
        db_session.add(
            PriceHistory(
                commodity_id=coffee.id,
                record_date=d,
                price=73000.0 + i * 15.0,
                provenance="collected",
                source="VietnamBiz (Khảo sát Tây Nguyên)",
            )
        )
        db_session.add(
            PriceHistory(
                commodity_id=sugar.id,
                record_date=d,
                price=1200000.0 + i * 250.0,
                provenance="collected",
                source="ICE Raw Sugar #11 (SB=F) × USD/VND",
            )
        )

    latest_day = today - timedelta(days=1)
    # Direct survey for Coffee ONLY in Đắk Lắk (NOT in Khánh Hòa)
    db_session.add(
        RegionalPriceObservation(
            commodity_id=coffee.id,
            province_code="dak-lak",
            recorded_date=latest_day,
            price=73800.0,
            source="VietnamBiz (Khảo sát Tây Nguyên)",
            source_url="https://vietnambiz.vn/gia-ca-phe-hom-nay.html",
            pricing_type="direct_survey",
        )
    )
    # Direct survey for Sugarcane directly in Khánh Hòa (Ninh Hòa)
    db_session.add(
        RegionalPriceObservation(
            commodity_id=sugar.id,
            province_code="khanh-hoa",
            recorded_date=latest_day,
            price=1070000.0,
            source="Báo Nông nghiệp & Môi trường (Khánh Hòa / AgriS Ninh Hòa)",
            source_url="https://nongnghiepmoitruong.vn/lien-ket-trong-mia-khoi-thong-nguon-luc-de-phat-trien-ben-vung-d801982.html",
            pricing_type="direct_survey",
        )
    )
    db_session.commit()
    return coffee, sugar


def test_regions_list_and_gps_locate_nha_trang_returns_khanh_hoa(client, db_session):
    """TC-REG-01: GET /api/v1/regions & /api/v1/regions/locate?lat=12.2388&lng=109.1967 trả đúng khanh-hoa."""
    res_list = client.get("/api/v1/regions")
    assert res_list.status_code == 200
    regions = res_list.json()
    assert len(regions) >= 25
    codes = {r["code"] for r in regions}
    assert {"khanh-hoa", "dak-lak", "lam-dong", "an-giang", "phu-yen", "tp-hcm", "ha-noi"}.issubset(codes)

    # Nha Trang GPS coordinates -> Khánh Hòa
    res_loc = client.get("/api/v1/regions/locate", params={"lat": 12.2388, "lng": 109.1967})
    assert res_loc.status_code == 200
    loc = res_loc.json()
    assert loc["province_code"] == "khanh-hoa"
    assert loc["province_name"] == "Khánh Hòa"
    assert loc["region_name"] == "Nam Trung Bộ"
    assert loc["distance_km"] < 1.0

    # Buôn Ma Thuột GPS coordinates -> Đắk Lắk
    res_dl = client.get("/api/v1/regions/locate", params={"lat": 12.6667, "lng": 108.0500})
    assert res_dl.status_code == 200
    assert res_dl.json()["province_code"] == "dak-lak"

    # Invalid coordinates rejected cleanly (never 500)
    assert client.get("/api/v1/regions/locate", params={"lat": 999, "lng": 109}).status_code == 422


def test_overview_with_province_khanh_hoa_distinguishes_direct_and_benchmark(client, db_session):
    """TC-REG-02: /overview?province=khanh-hoa phân biệt rõ direct (Mía đường) vs regional_benchmark (Cà phê)."""
    _seed_two_commodities_with_regional_obs(db_session)

    for endpoint in ("/api/v1/commodities/overview", "/api/v1/market/overview"):
        res = client.get(endpoint, params={"province": "khanh-hoa"})
        assert res.status_code == 200
        cards = res.json()
        by_code = {c["code"]: c for c in cards}
        assert "COFFEE" in by_code and "SUGAR" in by_code

        # Sugarcane has direct survey in Khánh Hòa
        sugar_card = by_code["SUGAR"]
        s_loc = sugar_card["location_context"]
        assert s_loc["province_code"] == "khanh-hoa"
        assert s_loc["pricing_mode"] == "direct"
        assert s_loc["distance_km"] == 0.0
        assert s_loc["logistics_spread"] == 0.0
        assert math.isfinite(sugar_card["currentPrice"]) and sugar_card["currentPrice"] == 1070000.0

        # Coffee has NO direct survey in Khánh Hòa -> Haversine nearest hub Đắk Lắk + logistics spread
        coffee_card = by_code["COFFEE"]
        c_loc = coffee_card["location_context"]
        assert c_loc["province_code"] == "khanh-hoa"
        assert c_loc["pricing_mode"] == "regional_benchmark"
        assert c_loc["reference_province"] == "Đắk Lắk"
        assert 100.0 < c_loc["distance_km"] < 200.0
        assert c_loc["logistics_spread"] > 0.0
        assert math.isfinite(coffee_card["currentPrice"])
        assert coffee_card["currentPrice"] > 73800.0


def test_history_forecast_compare_and_cross_province_table_with_khanh_hoa(client, db_session, monkeypatch):
    """TC-REG-03: /history, /forecast, /market/compare và /market/regional-prices/{code} hoạt động nhất quán với ?province=khanh-hoa."""
    coffee, sugar = _seed_two_commodities_with_regional_obs(db_session, days=70)

    def deterministic_predict(model_name, series: pd.Series, horizon: int, future_index=None):
        last = float(series.iloc[-1])
        return np.array([last + 50.0 * (i + 1) for i in range(horizon)], dtype=float)

    monkeypatch.setattr(training_service, "predict_series", deterministic_predict)
    retrain_res = training_service.retrain(coffee.id, lambda *args: None)
    assert retrain_res["status"] == "SUCCESS"

    # 1. History with ?province=khanh-hoa (both /history and /market/history)
    start_d = str(date.today() - timedelta(days=30))
    end_d = str(date.today())
    for hist_path in ("/api/v1/history", "/api/v1/market/history"):
        h_res = client.get(
            hist_path,
            params={"commodity_id": coffee.id, "start_date": start_d, "end_date": end_d, "province": "khanh-hoa"},
        )
        assert h_res.status_code == 200
        h_data = h_res.json()
        assert h_data["location_context"]["province_code"] == "khanh-hoa"
        assert h_data["location_context"]["pricing_mode"] == "regional_benchmark"
        assert len(h_data["records"]) > 0
        assert all(math.isfinite(r["price"]) and r["price"] > 0 for r in h_data["records"])

    # 2. Forecast with ?province=khanh-hoa -> consistent basis shift & valid 95% CI
    fc_nat = client.get("/api/v1/forecast", params={"commodity_id": coffee.id, "model_name": "ARIMA", "days": 14})
    fc_kh = client.get(
        "/api/v1/forecast",
        params={"commodity_id": coffee.id, "model_name": "ARIMA", "days": 14, "province": "khanh-hoa"},
    )
    assert fc_nat.status_code == 200 and fc_kh.status_code == 200
    d_nat, d_kh = fc_nat.json(), fc_kh.json()
    loc = d_kh["location_context"]
    assert loc["province_code"] == "khanh-hoa"
    assert loc["pricing_mode"] == "regional_benchmark"
    assert loc["basis_offset"] != 0.0

    fc_points = [p for p in d_kh["forecastData"] if p["isForecast"]]
    assert len(fc_points) == 14
    for pt in fc_points:
        assert math.isfinite(pt["predictedPrice"])
        assert math.isfinite(pt["lowerCI"]) and math.isfinite(pt["upperCI"])
        assert pt["lowerCI"] <= pt["predictedPrice"] <= pt["upperCI"]

    # Basis shift applied identically to both historical endpoint and forecast points (seamless transition)
    nat_last_hist = [p for p in d_nat["forecastData"] if not p["isForecast"]][-1]["actualPrice"]
    kh_last_hist = [p for p in d_kh["forecastData"] if not p["isForecast"]][-1]["actualPrice"]
    nat_first_fc = [p for p in d_nat["forecastData"] if p["isForecast"]][0]["predictedPrice"]
    kh_first_fc = fc_points[0]["predictedPrice"]
    assert round(kh_last_hist - nat_last_hist, 1) == round(kh_first_fc - nat_first_fc, 1)

    # 3. Cross-province comparison table for Coffee & Sugarcane
    cmp_coffee = client.get("/api/v1/market/regional-prices/COFFEE_ROBUSTA", params={"province": "khanh-hoa"})
    assert cmp_coffee.status_code == 200
    provs = {p["province_code"]: p for p in cmp_coffee.json()["provinces"]}
    assert provs["dak-lak"]["pricing_mode"] == "direct"
    assert provs["khanh-hoa"]["pricing_mode"] == "regional_benchmark"

    cmp_sugar = client.get("/api/v1/market/regional-prices/SUGARCANE", params={"province": "khanh-hoa"})
    assert cmp_sugar.status_code == 200
    s_provs = {p["province_code"]: p for p in cmp_sugar.json()["provinces"]}
    assert s_provs["khanh-hoa"]["pricing_mode"] == "direct"
    assert s_provs["khanh-hoa"]["price"] == 1070000.0

    # 4. Market comparison growth series with ?province=khanh-hoa
    mc_res = client.get("/api/v1/market/compare", params={"province": "khanh-hoa"})
    assert mc_res.status_code == 200
    mc_points = mc_res.json()
    assert len(mc_points) > 0
    assert all(math.isfinite(pt["coffee"]) and math.isfinite(pt["sugar"]) for pt in mc_points)

