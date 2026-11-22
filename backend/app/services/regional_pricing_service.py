"""
Location-Aware Regional Pricing Service for AgroForecast.

Transparent 2-Tier Pricing Resolution (ZERO fabricated prices):
1. `direct`: The selected province has genuine direct-survey prices in `regional_price_observations`
   extracted from authoritative portals (giacaphe.com, vietnambiz.vn, giatieu.com, VFA vietfood.org.vn,
   Báo Khánh Hòa / Báo Nhân Dân / Báo Nông nghiệp & Môi trường / Bộ Công Thương).
2. `regional_benchmark`: When a province does not publish a daily farm-gate quote for a commodity
   (e.g., Khánh Hòa checking Robusta Coffee or IR50404 Rice), finds the nearest direct-survey hub
   using exact Haversine distance (`distance_km`) and computes a transparent logistics spread
   (`estimated_local_price = benchmark_price + logistics_spread`) with full provenance metadata.
"""
from __future__ import annotations

import math
from datetime import date
from typing import Dict, List, Optional, Tuple

from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.models.models import Commodity, PriceHistory, RegionalMarket, RegionalPriceObservation

# Danh mục 32 tỉnh/thành phố trọng điểm nông nghiệp & trung tâm tiêu thụ lớn trên cả nước
DEFAULT_PROVINCES: List[Dict] = [
    # Nam Trung Bộ
    {"code": "khanh-hoa", "name": "Khánh Hòa", "region_name": "Nam Trung Bộ", "lat": 12.2388, "lng": 109.1967, "is_major_hub": True},
    {"code": "phu-yen", "name": "Phú Yên", "region_name": "Nam Trung Bộ", "lat": 13.0955, "lng": 109.3209, "is_major_hub": True},
    {"code": "da-nang", "name": "Đà Nẵng", "region_name": "Nam Trung Bộ", "lat": 16.0544, "lng": 108.2022, "is_major_hub": False},
    {"code": "quang-nam", "name": "Quảng Nam", "region_name": "Nam Trung Bộ", "lat": 15.5736, "lng": 108.4740, "is_major_hub": False},
    {"code": "quang-ngai", "name": "Quảng Ngãi", "region_name": "Nam Trung Bộ", "lat": 15.1214, "lng": 108.8044, "is_major_hub": True},
    {"code": "binh-dinh", "name": "Bình Định", "region_name": "Nam Trung Bộ", "lat": 13.7820, "lng": 109.2197, "is_major_hub": False},
    {"code": "ninh-thuan", "name": "Ninh Thuận", "region_name": "Nam Trung Bộ", "lat": 11.5752, "lng": 108.9890, "is_major_hub": False},
    {"code": "binh-thuan", "name": "Bình Thuận", "region_name": "Nam Trung Bộ", "lat": 10.9289, "lng": 108.1021, "is_major_hub": False},
    # Tây Nguyên
    {"code": "dak-lak", "name": "Đắk Lắk", "region_name": "Tây Nguyên", "lat": 12.6667, "lng": 108.0500, "is_major_hub": True},
    {"code": "lam-dong", "name": "Lâm Đồng", "region_name": "Tây Nguyên", "lat": 11.9404, "lng": 108.4583, "is_major_hub": True},
    {"code": "gia-lai", "name": "Gia Lai", "region_name": "Tây Nguyên", "lat": 13.9833, "lng": 108.0000, "is_major_hub": True},
    {"code": "dak-nong", "name": "Đắk Nông", "region_name": "Tây Nguyên", "lat": 12.0033, "lng": 107.6876, "is_major_hub": True},
    {"code": "kon-tum", "name": "Kon Tum", "region_name": "Tây Nguyên", "lat": 14.3497, "lng": 108.0005, "is_major_hub": False},
    # Đồng bằng sông Cửu Long (ĐBSCL)
    {"code": "an-giang", "name": "An Giang", "region_name": "ĐBSCL", "lat": 10.3864, "lng": 105.4352, "is_major_hub": True},
    {"code": "dong-thap", "name": "Đồng Tháp", "region_name": "ĐBSCL", "lat": 10.4569, "lng": 105.6350, "is_major_hub": True},
    {"code": "kien-giang", "name": "Kiên Giang", "region_name": "ĐBSCL", "lat": 10.0125, "lng": 105.0809, "is_major_hub": True},
    {"code": "tien-giang", "name": "Tiền Giang", "region_name": "ĐBSCL", "lat": 10.3600, "lng": 106.3600, "is_major_hub": True},
    {"code": "can-tho", "name": "Cần Thơ", "region_name": "ĐBSCL", "lat": 10.0452, "lng": 105.7469, "is_major_hub": True},
    {"code": "long-an", "name": "Long An", "region_name": "ĐBSCL", "lat": 10.5359, "lng": 106.4137, "is_major_hub": True},
    {"code": "bac-lieu", "name": "Bạc Liêu", "region_name": "ĐBSCL", "lat": 9.2940, "lng": 105.7216, "is_major_hub": True},
    {"code": "hau-giang", "name": "Hậu Giang", "region_name": "ĐBSCL", "lat": 9.7845, "lng": 105.4701, "is_major_hub": False},
    {"code": "vinh-long", "name": "Vĩnh Long", "region_name": "ĐBSCL", "lat": 10.2537, "lng": 105.9722, "is_major_hub": False},
    {"code": "soc-trang", "name": "Sóc Trăng", "region_name": "ĐBSCL", "lat": 9.6037, "lng": 105.9739, "is_major_hub": False},
    # Đông Nam Bộ
    {"code": "tp-hcm", "name": "TP. Hồ Chí Minh", "region_name": "Đông Nam Bộ", "lat": 10.7769, "lng": 106.7009, "is_major_hub": False},
    {"code": "binh-phuoc", "name": "Bình Phước", "region_name": "Đông Nam Bộ", "lat": 11.7512, "lng": 106.7235, "is_major_hub": True},
    {"code": "dong-nai", "name": "Đồng Nai", "region_name": "Đông Nam Bộ", "lat": 10.9465, "lng": 106.8235, "is_major_hub": True},
    {"code": "ba-ria-vung-tau", "name": "Bà Rịa - Vũng Tàu", "region_name": "Đông Nam Bộ", "lat": 10.5417, "lng": 107.2430, "is_major_hub": True},
    {"code": "tay-ninh", "name": "Tây Ninh", "region_name": "Đông Nam Bộ", "lat": 11.3352, "lng": 106.1099, "is_major_hub": True},
    # Miền Bắc & Bắc Trung Bộ
    {"code": "ha-noi", "name": "Hà Nội", "region_name": "Miền Bắc", "lat": 21.0285, "lng": 105.8542, "is_major_hub": False},
    {"code": "hai-phong", "name": "Hải Phòng", "region_name": "Miền Bắc", "lat": 20.8449, "lng": 106.6881, "is_major_hub": False},
    {"code": "son-la", "name": "Sơn La", "region_name": "Miền Bắc", "lat": 21.3256, "lng": 103.9188, "is_major_hub": False},
    {"code": "nghe-an", "name": "Nghệ An", "region_name": "Miền Bắc", "lat": 18.6796, "lng": 105.6813, "is_major_hub": False},
    {"code": "thanh-hoa", "name": "Thanh Hóa", "region_name": "Miền Bắc", "lat": 19.8067, "lng": 105.7852, "is_major_hub": False},
]

# Vùng chuẩn dự phòng khi bảng regional_price_observations chưa có bản ghi nào (VD: unit test SQLite sạch)
CANONICAL_HUB_BY_CODE: Dict[str, str] = {
    "RICE_IR504": "an-giang",
    "COFFEE_ROBUSTA": "dak-lak",
    "PEPPER_BLACK": "gia-lai",
    "SUGARCANE": "phu-yen",
    "STRAWBERRY": "lam-dong",
    "SWEET_POTATO": "vinh-long",
    "POTATO": "lam-dong",
    "CASHEW_NUT": "binh-phuoc",
}

PROVINCE_ALIASES: Dict[str, str] = {
    "daklak": "dak-lak",
    "đắk lắk": "dak-lak",
    "đăk lăk": "dak-lak",
    "lamdong": "lam-dong",
    "lâm đồng": "lam-dong",
    "gialai": "gia-lai",
    "gia lai": "gia-lai",
    "daknong": "dak-nong",
    "đắk nông": "dak-nong",
    "đăk nông": "dak-nong",
    "khanhhoa": "khanh-hoa",
    "khánh hòa": "khanh-hoa",
    "nha trang": "khanh-hoa",
    "ninh hòa": "khanh-hoa",
    "phuyen": "phu-yen",
    "phú yên": "phu-yen",
    "angiang": "an-giang",
    "an giang": "an-giang",
    "dongthap": "dong-thap",
    "đồng tháp": "dong-thap",
    "kiengiang": "kien-giang",
    "kiên giang": "kien-giang",
    "tiengiang": "tien-giang",
    "tiền giang": "tien-giang",
    "cantho": "can-tho",
    "cần thơ": "can-tho",
    "longan": "long-an",
    "long an": "long-an",
    "baclieu": "bac-lieu",
    "bạc liêu": "bac-lieu",
    "binhphuoc": "binh-phuoc",
    "bình phước": "binh-phuoc",
    "dongnai": "dong-nai",
    "đồng nai": "dong-nai",
    "baria": "ba-ria-vung-tau",
    "bà rịa - vũng tàu": "ba-ria-vung-tau",
    "bà rịa – vũng tàu": "ba-ria-vung-tau",
    "bà rịa": "ba-ria-vung-tau",
    "tayninh": "tay-ninh",
    "tây ninh": "tay-ninh",
    "hcm": "tp-hcm",
    "tphcm": "tp-hcm",
    "ho-chi-minh": "tp-hcm",
    "hanoi": "ha-noi",
    "hà nội": "ha-noi",
}


def normalize_province_code(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    cleaned = raw.strip().lower()
    if cleaned in ("", "all", "toan-quoc", "national"):
        return None
    return PROVINCE_ALIASES.get(cleaned, cleaned)


def ensure_regional_markets_seeded(db: Session) -> None:
    """Idempotently seed all 33 Vietnamese provinces/cities into `regional_markets`."""
    existing = {code for (code,) in db.query(RegionalMarket.code).all()}
    missing = [item for item in DEFAULT_PROVINCES if item["code"] not in existing]
    if not missing:
        return
    for item in missing:
        db.add(RegionalMarket(**item))
    db.commit()


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Compute exact great-circle distance (km) between two WGS-84 coordinates."""
    r_earth = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lam = math.radians(lng2 - lng1)
    a = math.sin(d_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lam / 2.0) ** 2
    return r_earth * 2.0 * math.atan2(math.sqrt(a), math.sqrt(max(0.0, 1.0 - a)))


def locate_nearest_province(db: Session, lat: float, lng: float) -> Dict:
    """Find the closest Vietnamese province from GPS coordinates (never raises 500)."""
    ensure_regional_markets_seeded(db)
    provinces = db.query(RegionalMarket).all()
    best_market: Optional[RegionalMarket] = None
    best_dist = float("inf")
    for p in provinces:
        d = haversine_km(lat, lng, float(p.lat), float(p.lng))
        if d < best_dist:
            best_dist = d
            best_market = p

    if not best_market:
        return {
            "province_code": "khanh-hoa",
            "province_name": "Khánh Hòa",
            "region_name": "Nam Trung Bộ",
            "distance_km": 0.0,
            "lat": lat,
            "lng": lng,
            "method": "fallback",
        }

    return {
        "province_code": best_market.code,
        "province_name": best_market.name,
        "region_name": best_market.region_name,
        "distance_km": round(best_dist, 1),
        "lat": float(best_market.lat),
        "lng": float(best_market.lng),
        "method": "haversine_db",
    }


def compute_logistics_spread(distance_km: float, unit: str, benchmark_price: float) -> float:
    """
    Transparent agricultural road-freight allowance by distance:
    - VNĐ/kg commodities (Lúa, Cà phê, Tiêu): ~1,8 VNĐ/kg/km (tương đương ~1.800 đ/tấn/km xe tải nông sản),
      làm tròn bội số 100 VNĐ, chặn trần hợp lý tối đa 6% giá trị gốc (hoặc 1.500 VNĐ/kg).
    - VNĐ/tấn commodities (Mía đường): ~700 VNĐ/tấn/km, làm tròn bội số 1.000 VNĐ, chặn trần 120.000 VNĐ/tấn.
    """
    if distance_km <= 5.0:
        return 0.0
    unit_low = (unit or "").lower().replace("đ", "d")
    if "tấn" in unit_low or "tan" in unit_low:
        raw = distance_km * 700.0
        capped = min(raw, 120000.0, max(benchmark_price * 0.10, 20000.0))
        return float(round(capped / 1000.0) * 1000.0)

    # VNĐ/kg
    raw = distance_km * 1.8
    cap_abs = 500.0 if benchmark_price < 15000.0 else 1500.0
    capped = min(raw, cap_abs, max(benchmark_price * 0.075, 100.0))
    return float(max(100.0, round(capped / 100.0) * 100.0))


def _format_vnd_int(val: float) -> str:
    return f"{int(round(val)):,}".replace(",", ".")


def resolve_commodity_location_context(
    db: Session,
    commodity: Commodity,
    province_code: Optional[str] = None,
) -> Dict:
    """
    Resolve transparent regional pricing context for `(commodity, province_code)`:
    - `None` / `'all'` -> `national_benchmark` (default behavior, 100% backward compatible).
    - Province with direct rows in `regional_price_observations` -> `pricing_mode = 'direct'`.
    - Province without direct rows -> Haversine nearest hub + transparent `logistics_spread` (`pricing_mode = 'regional_benchmark'`).
    """
    ensure_regional_markets_seeded(db)
    norm_code = normalize_province_code(province_code)

    latest_nat_row = (
        db.query(PriceHistory)
        .filter(PriceHistory.commodity_id == commodity.id)
        .order_by(desc(PriceHistory.record_date))
        .first()
    )
    nat_price = float(latest_nat_row.price) if latest_nat_row else 0.0

    if not norm_code:
        return {
            "province_code": "all",
            "province_name": "Toàn quốc (Vùng trọng điểm)",
            "region_name": commodity.region,
            "pricing_mode": "national_benchmark",
            "reference_province": commodity.region,
            "reference_province_code": CANONICAL_HUB_BY_CODE.get(commodity.code, "all"),
            "distance_km": 0.0,
            "logistics_spread": 0.0,
            "basis_offset": 0.0,
            "direct_source": None,
            "direct_source_url": None,
            "latest_direct_date": None,
            "observed_date": str(latest_nat_row.record_date) if latest_nat_row else None,
            "observed_price": nat_price if latest_nat_row else None,
            "explanation": f"Giá tham chiếu chuẩn tại vùng sản xuất trọng điểm ({commodity.region}).",
            "note": f"Vùng trọng điểm ({commodity.region})",
        }

    province = db.get(RegionalMarket, norm_code)
    if not province:
        # Unknown code: fall back gracefully to national benchmark without erroring
        return {
            "province_code": norm_code,
            "province_name": norm_code,
            "region_name": commodity.region,
            "pricing_mode": "national_benchmark",
            "reference_province": commodity.region,
            "reference_province_code": CANONICAL_HUB_BY_CODE.get(commodity.code, "all"),
            "distance_km": 0.0,
            "logistics_spread": 0.0,
            "basis_offset": 0.0,
            "direct_source": None,
            "direct_source_url": None,
            "latest_direct_date": None,
            "explanation": f"Chưa có cấu hình cho mã địa phương '{norm_code}'; hiển thị giá vùng trọng điểm.",
            "note": f"Vùng trọng điểm ({commodity.region})",
        }

    # --- CASE 1: Direct Survey Observations exist for this province ---
    latest_direct = (
        db.query(RegionalPriceObservation)
        .filter(
            RegionalPriceObservation.commodity_id == commodity.id,
            RegionalPriceObservation.province_code == province.code,
        )
        .order_by(desc(RegionalPriceObservation.recorded_date), desc(RegionalPriceObservation.id))
        .first()
    )
    if latest_direct is not None:
        direct_price = float(latest_direct.price)
        # Align basis_offset against same-day (or closest prior) national benchmark
        ref_nat_row = (
            db.query(PriceHistory)
            .filter(
                PriceHistory.commodity_id == commodity.id,
                PriceHistory.record_date <= latest_direct.recorded_date,
            )
            .order_by(desc(PriceHistory.record_date))
            .first()
        ) or latest_nat_row
        ref_nat_price = float(ref_nat_row.price) if ref_nat_row else direct_price
        basis_offset = round(direct_price - ref_nat_price, 2)
        date_vn = latest_direct.recorded_date.strftime("%d/%m/%Y")
        return {
            "province_code": province.code,
            "province_name": province.name,
            "region_name": province.region_name,
            "pricing_mode": "direct",
            "reference_province": province.name,
            "reference_province_code": province.code,
            "distance_km": 0.0,
            "logistics_spread": 0.0,
            "basis_offset": basis_offset,
            "latest_direct_price": direct_price,
            "latest_direct_date": str(latest_direct.recorded_date),
            "observed_date": str(latest_direct.recorded_date),
            "observed_price": direct_price,
            "direct_source": latest_direct.source,
            "direct_source_url": latest_direct.source_url,
            "explanation": (
                f"Khảo sát trực tiếp tại {province.name} ({latest_direct.source}, "
                f"cập nhật {date_vn}: {_format_vnd_int(direct_price)} {commodity.unit})."
            ),
            "note": f"Khảo sát tại {province.name}",
        }

    # --- CASE 2: Regional Benchmark via Haversine nearest hub + transparent logistics spread ---
    hub_subq = (
        db.query(
            RegionalPriceObservation.province_code,
            func.max(RegionalPriceObservation.recorded_date).label("max_date"),
        )
        .filter(RegionalPriceObservation.commodity_id == commodity.id)
        .group_by(RegionalPriceObservation.province_code)
        .all()
    )

    candidate_hubs: List[Tuple[RegionalMarket, Optional[RegionalPriceObservation]]] = []
    for hub_code, max_dt in hub_subq:
        hub_market = db.get(RegionalMarket, hub_code)
        if not hub_market:
            continue
        obs = (
            db.query(RegionalPriceObservation)
            .filter(
                RegionalPriceObservation.commodity_id == commodity.id,
                RegionalPriceObservation.province_code == hub_code,
                RegionalPriceObservation.recorded_date == max_dt,
            )
            .order_by(desc(RegionalPriceObservation.id))
            .first()
        )
        candidate_hubs.append((hub_market, obs))

    if not candidate_hubs:
        canonical_code = CANONICAL_HUB_BY_CODE.get(commodity.code, "dak-lak")
        canonical_market = db.get(RegionalMarket, canonical_code)
        if canonical_market:
            candidate_hubs.append((canonical_market, None))

    nearest_hub: Optional[RegionalMarket] = None
    nearest_obs: Optional[RegionalPriceObservation] = None
    min_dist = float("inf")
    for hub_m, hub_obs in candidate_hubs:
        dist = haversine_km(float(province.lat), float(province.lng), float(hub_m.lat), float(hub_m.lng))
        if dist < min_dist:
            min_dist = dist
            nearest_hub = hub_m
            nearest_obs = hub_obs

    dist_km = round(min_dist, 1) if math.isfinite(min_dist) else 0.0
    ref_name = nearest_hub.name if nearest_hub else commodity.region
    ref_code = nearest_hub.code if nearest_hub else "all"

    # Compute hub's real spread vs national index (if hub has direct observation)
    hub_basis = 0.0
    benchmark_price = nat_price
    if nearest_obs is not None:
        benchmark_price = float(nearest_obs.price)
        ref_nat_row = (
            db.query(PriceHistory)
            .filter(
                PriceHistory.commodity_id == commodity.id,
                PriceHistory.record_date <= nearest_obs.recorded_date,
            )
            .order_by(desc(PriceHistory.record_date))
            .first()
        ) or latest_nat_row
        if ref_nat_row:
            hub_basis = round(benchmark_price - float(ref_nat_row.price), 2)

    logistics_spread = compute_logistics_spread(dist_km, commodity.unit, benchmark_price or nat_price)
    total_basis = round(hub_basis + logistics_spread, 2)
    spread_label = f"+{_format_vnd_int(logistics_spread)} {commodity.unit}" if logistics_spread > 0 else "0"

    return {
        "province_code": province.code,
        "province_name": province.name,
        "region_name": province.region_name,
        "pricing_mode": "regional_benchmark",
        "reference_province": ref_name,
        "reference_province_code": ref_code,
        "distance_km": dist_km,
        "logistics_spread": logistics_spread,
        "basis_offset": total_basis,
        "latest_direct_price": None,
        "latest_direct_date": str(nearest_obs.recorded_date) if nearest_obs else None,
        "observed_date": str(nearest_obs.recorded_date) if nearest_obs else (str(latest_nat_row.record_date) if latest_nat_row else None),
        "observed_price": max(0.0, round((benchmark_price or nat_price) + logistics_spread, 2)),
        "direct_source": nearest_obs.source if nearest_obs else None,
        "direct_source_url": nearest_obs.source_url if nearest_obs else None,
        "explanation": (
            f"Tỉnh {province.name} chưa có bảng giá niêm yết hàng ngày cho {commodity.name}. "
            f"Tham chiếu vùng chuyên canh gần nhất là {ref_name} (cách ~{int(round(dist_km))} km) "
            f"cộng định mức cước vận chuyển ({spread_label})."
        ),
        "note": f"Tham chiếu {ref_name} (+cước ~{int(round(dist_km))} km)",
    }


def list_regions_with_coverage(db: Session) -> List[Dict]:
    """Return all supported Vietnamese provinces grouped cleanly with their direct-survey commodities."""
    ensure_regional_markets_seeded(db)
    provinces = db.query(RegionalMarket).order_by(RegionalMarket.region_name, RegionalMarket.name).all()
    commodities = {c.id: c for c in db.query(Commodity).all()}

    # Gather latest direct observation per (province_code, commodity_id)
    latest_subq = (
        db.query(
            RegionalPriceObservation.province_code,
            RegionalPriceObservation.commodity_id,
            func.max(RegionalPriceObservation.recorded_date).label("max_date"),
        )
        .group_by(RegionalPriceObservation.province_code, RegionalPriceObservation.commodity_id)
        .all()
    )
    coverage_map: Dict[str, List[Dict]] = {}
    for p_code, c_id, max_dt in latest_subq:
        comm = commodities.get(c_id)
        if not comm:
            continue
        obs = (
            db.query(RegionalPriceObservation)
            .filter(
                RegionalPriceObservation.province_code == p_code,
                RegionalPriceObservation.commodity_id == c_id,
                RegionalPriceObservation.recorded_date == max_dt,
            )
            .order_by(desc(RegionalPriceObservation.id))
            .first()
        )
        if not obs:
            continue
        coverage_map.setdefault(p_code, []).append({
            "commodity_id": comm.id,
            "commodity_code": comm.code,
            "commodity_name": comm.name,
            "unit": comm.unit,
            "latest_price": float(obs.price),
            "latest_date": str(obs.recorded_date),
            "source": obs.source,
        })

    return [
        {
            "code": p.code,
            "name": p.name,
            "region_name": p.region_name,
            "lat": float(p.lat),
            "lng": float(p.lng),
            "is_major_hub": bool(p.is_major_hub),
            "direct_commodities": sorted(coverage_map.get(p.code, []), key=lambda x: x["commodity_id"]),
        }
        for p in provinces
    ]


def get_commodity_province_comparison(
    db: Session,
    commodity_code: str,
    focus_province: Optional[str] = None,
) -> Dict:
    """
    Return the latest price comparison table across provinces for a single commodity:
    - Includes ALL provinces with genuine `direct_survey` data in `regional_price_observations`.
    - Also includes the user's `focus_province` (if selected and not already direct) + key hubs
      clearly tagged as `regional_benchmark` with Haversine distance & logistics spread.
    """
    ensure_regional_markets_seeded(db)
    code_upper = commodity_code.strip().upper()
    code_aliases = {
        "RICE": "RICE_IR504",
        "COFFEE": "COFFEE_ROBUSTA",
        "PEPPER": "PEPPER_BLACK",
        "SUGAR": "SUGARCANE",
        "STRAWBERRY": "STRAWBERRY",
        "POTATO": "POTATO",
        "SWEETPOTATO": "SWEET_POTATO",
        "CASHEW": "CASHEW_NUT",
    }
    target_code = code_aliases.get(code_upper, code_upper)
    commodity = (
        db.query(Commodity).filter(Commodity.code == target_code).first()
        or (db.get(Commodity, int(commodity_code)) if commodity_code.isdigit() else None)
    )
    if not commodity:
        return {"commodity": None, "national_price": 0.0, "provinces": []}

    latest_nat = (
        db.query(PriceHistory)
        .filter(PriceHistory.commodity_id == commodity.id)
        .order_by(desc(PriceHistory.record_date))
        .first()
    )
    nat_price = float(latest_nat.price) if latest_nat else 0.0
    nat_date = str(latest_nat.record_date) if latest_nat else None

    # All direct-survey provinces
    latest_subq = (
        db.query(
            RegionalPriceObservation.province_code,
            func.max(RegionalPriceObservation.recorded_date).label("max_date"),
        )
        .filter(RegionalPriceObservation.commodity_id == commodity.id)
        .group_by(RegionalPriceObservation.province_code)
        .all()
    )

    items: List[Dict] = []
    included_codes = set()
    for p_code, max_dt in latest_subq:
        market = db.get(RegionalMarket, p_code)
        obs = (
            db.query(RegionalPriceObservation)
            .filter(
                RegionalPriceObservation.commodity_id == commodity.id,
                RegionalPriceObservation.province_code == p_code,
                RegionalPriceObservation.recorded_date == max_dt,
            )
            .order_by(desc(RegionalPriceObservation.id))
            .first()
        )
        if not market or not obs:
            continue
        p_val = float(obs.price)
        diff_vs_nat = round(p_val - nat_price, 2) if nat_price > 0 else 0.0
        items.append({
            "province_code": market.code,
            "province_name": market.name,
            "region_name": market.region_name,
            "price": p_val,
            "formatted_price": _format_vnd_int(p_val),
            "unit": commodity.unit,
            "diff_vs_national": diff_vs_nat,
            "pricing_mode": "direct",
            "reference_province": market.name,
            "distance_km": 0.0,
            "logistics_spread": 0.0,
            "recorded_date": str(obs.recorded_date),
            "source": obs.source,
            "source_url": obs.source_url,
        })
        included_codes.add(market.code)

    # Add user's focused province (and Khánh Hòa / TP.HCM / Hà Nội if helpful) as transparent benchmark rows
    extra_codes = []
    norm_focus = normalize_province_code(focus_province)
    if norm_focus and norm_focus not in included_codes:
        extra_codes.append(norm_focus)
    for key_city in ("khanh-hoa", "tp-hcm", "ha-noi"):
        if key_city not in included_codes and key_city not in extra_codes:
            extra_codes.append(key_city)

    for extra_code in extra_codes:
        ctx = resolve_commodity_location_context(db, commodity, extra_code)
        if ctx["pricing_mode"] != "regional_benchmark":
            continue
        est_price = max(0.0, round(nat_price + float(ctx["basis_offset"]), 2))
        items.append({
            "province_code": ctx["province_code"],
            "province_name": ctx["province_name"],
            "region_name": ctx["region_name"],
            "price": est_price,
            "formatted_price": _format_vnd_int(est_price),
            "unit": commodity.unit,
            "diff_vs_national": round(est_price - nat_price, 2),
            "pricing_mode": "regional_benchmark",
            "reference_province": ctx["reference_province"],
            "distance_km": ctx["distance_km"],
            "logistics_spread": ctx["logistics_spread"],
            "recorded_date": ctx["latest_direct_date"] or nat_date,
            "source": f"Tham chiếu {ctx['reference_province']} (+cước ~{int(round(ctx['distance_km']))} km)",
            "source_url": ctx.get("direct_source_url"),
        })

    # Sort direct surveys first (by price desc), then regional benchmarks (focused province first)
    items.sort(
        key=lambda x: (
            0 if x["pricing_mode"] == "direct" else (1 if x["province_code"] == norm_focus else 2),
            -x["price"],
        )
    )

    return {
        "commodity": {
            "id": commodity.id,
            "code": commodity.code,
            "name": commodity.name,
            "unit": commodity.unit,
            "region": commodity.region,
        },
        "national_price": nat_price,
        "formatted_national_price": _format_vnd_int(nat_price),
        "latest_date": nat_date,
        "provinces": items,
    }

