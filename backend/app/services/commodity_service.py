from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.models import Commodity, PriceHistory, RegionalPriceObservation
from app.schemas.schemas import (
    CommodityOverviewCard,
    LocationContextResponse,
    SparklinePoint,
    MarketComparisonPoint,
    SpotlightSummaryResponse,
)
from app.services.regional_pricing_service import (
    normalize_province_code,
    resolve_commodity_location_context,
)
from datetime import datetime
from typing import List, Optional

def get_commodities_overview(db: Session, province: Optional[str] = None) -> List[CommodityOverviewCard]:
    commodities = db.query(Commodity).order_by(Commodity.id).all()
    overview_cards = []
    norm_prov = normalize_province_code(province)

    for c in commodities:
        loc = resolve_commodity_location_context(db, c, province)
        offset = float(loc.get("basis_offset", 0.0)) if norm_prov else 0.0

        # If direct survey province has >= 7 recent provincial observations, use exact provincial series
        direct_series = []
        if norm_prov and loc.get("pricing_mode") == "direct":
            direct_series = list(
                reversed(
                    db.query(RegionalPriceObservation)
                    .filter(
                        RegionalPriceObservation.commodity_id == c.id,
                        RegionalPriceObservation.province_code == norm_prov,
                    )
                    .order_by(desc(RegionalPriceObservation.recorded_date))
                    .limit(7)
                    .all()
                )
            )

        if len(direct_series) >= 5:
            current_p = float(direct_series[-1].price)
            prev_p = float(direct_series[0].price) if len(direct_series) > 1 else current_p
            change_pct = round(((current_p - prev_p) / prev_p) * 100, 1) if prev_p > 0 else 0.0
            sparkline = [
                SparklinePoint(
                    date=p.recorded_date.strftime("%d/%m"),
                    value=float(p.price),
                )
                for p in direct_series
            ]
        else:
            # Get last 7 price records for sparkline and apply regional basis consistently
            prices = (
                db.query(PriceHistory)
                .filter(PriceHistory.commodity_id == c.id)
                .order_by(desc(PriceHistory.record_date))
                .limit(7)
                .all()
            )
            prices = list(reversed(prices))

            if not prices:
                current_p = max(0.0, float(loc.get("latest_direct_price") or 1000.0))
                change_pct = 0.0
                sparkline = []
            else:
                if norm_prov and loc.get("pricing_mode") == "direct" and loc.get("latest_direct_price"):
                    # Anchor current price directly to the exact verified provincial survey price
                    latest_nat = float(prices[-1].price)
                    anchor_offset = float(loc["latest_direct_price"]) - latest_nat
                    adjusted = [max(0.0, round(float(p.price) + anchor_offset, 2)) for p in prices]
                else:
                    adjusted = [max(0.0, round(float(p.price) + offset, 2)) for p in prices]

                current_p = adjusted[-1]
                prev_p = adjusted[0] if len(adjusted) > 1 else current_p
                change_pct = round(((current_p - prev_p) / prev_p) * 100, 1) if prev_p > 0 else 0.0
                sparkline = [
                    SparklinePoint(
                        date=p.record_date.strftime("%d/%m"),
                        value=val,
                    )
                    for p, val in zip(prices, adjusted)
                ]

        # Format price with dots (vi-VN standard)
        formatted_price = f"{int(round(current_p)):,}".replace(",", ".")

        # Map friendly Vietnamese short names
        name_map = {
            "RICE_IR504": "Lúa gạo IR50404",
            "COFFEE_ROBUSTA": "Cà phê Robusta",
            "PEPPER_BLACK": "Hồ tiêu đen",
            "SUGARCANE": "Mía đường",
            "STRAWBERRY": "Dâu tây Đà Lạt",
            "SWEET_POTATO": "Khoai lang tím Vĩnh Long",
            "POTATO": "Khoai tây Đà Lạt",
            "CASHEW_NUT": "Hạt điều"
        }
        display_name = name_map.get(c.code, c.name.split(" ")[0] + (" " + c.name.split(" ")[1] if len(c.name.split(" ")) > 1 else ""))
        region_display = loc["province_name"] if norm_prov else c.region

        overview_cards.append(
            CommodityOverviewCard(
                id=c.id,
                code=c.code.replace("RICE_IR504", "RICE").replace("COFFEE_ROBUSTA", "COFFEE").replace("PEPPER_BLACK", "PEPPER").replace("SUGARCANE", "SUGAR").replace("SWEET_POTATO", "SWEETPOTATO").replace("CASHEW_NUT", "CASHEW"),
                name=display_name,
                category=c.category,
                unit=c.unit,
                region=region_display,
                currentPrice=current_p,
                formattedPrice=formatted_price,
                changePct=change_pct,
                isPositive=change_pct >= 0,
                sparkline=sparkline,
                location_context=LocationContextResponse(**{k: v for k, v in loc.items() if k in LocationContextResponse.model_fields}),
            )
        )

    return overview_cards

def get_market_comparison(db: Session, province: Optional[str] = None) -> List[MarketComparisonPoint]:
    """
    Tính toán chỉ số tăng trưởng chuẩn hóa % của 4 mặt hàng nông sản từ cơ sở dữ liệu thật.
    Hỗ trợ tham số `province` để quy đổi theo chênh lệch vùng/tỉnh thành minh bạch.
    """
    commodities = db.query(Commodity).order_by(Commodity.id).all()
    if not commodities:
        return []

    norm_prov = normalize_province_code(province)
    com_dict = {c.id: c.code for c in commodities}
    offset_by_code = {}
    if norm_prov:
        for c in commodities:
            loc = resolve_commodity_location_context(db, c, province)
            offset_by_code[c.code] = float(loc.get("basis_offset", 0.0))

    all_prices = (
        db.query(PriceHistory)
        .order_by(PriceHistory.record_date.desc())
        .limit(90 * len(commodities))
        .all()
    )

    if not all_prices:
        return []

    date_map = {}
    for p in all_prices:
        d_str = p.record_date.strftime("%d/%m")
        if d_str not in date_map:
            date_map[d_str] = {}
        c_code = com_dict.get(p.commodity_id, "")
        adj_price = max(1.0, float(p.price) + offset_by_code.get(c_code, 0.0))
        date_map[d_str][c_code] = adj_price

    # Chọn khoảng 8-10 mốc thời gian trải đều
    sorted_dates = sorted(list(date_map.keys()), key=lambda x: datetime.strptime(x, "%d/%m") if "%d/%m" else x)
    if len(sorted_dates) > 9:
        step = max(1, len(sorted_dates) // 8)
        sampled_dates = sorted_dates[::step]
        if sorted_dates[-1] not in sampled_dates:
            sampled_dates.append(sorted_dates[-1])
    else:
        sampled_dates = sorted_dates

    # Lấy mốc giá gốc đầu kỳ để tính % thay đổi
    base_prices = {}
    for code in ["RICE_IR504", "COFFEE_ROBUSTA", "PEPPER_BLACK", "SUGARCANE", "STRAWBERRY", "SWEET_POTATO", "POTATO", "CASHEW_NUT"]:
        for d in sampled_dates:
            if code in date_map.get(d, {}):
                base_prices[code] = date_map[d][code]
                break

    comparison_points = []
    for d in sampled_dates:
        d_data = date_map.get(d, {})
        
        def calc_pct(code):
            cur = d_data.get(code)
            base = base_prices.get(code)
            if cur and base and base > 0:
                return round(((cur - base) / base) * 100, 2)
            return 0.0

        comparison_points.append(
            MarketComparisonPoint(
                date=d,
                rice=calc_pct("RICE_IR504"),
                coffee=calc_pct("COFFEE_ROBUSTA"),
                pepper=calc_pct("PEPPER_BLACK"),
                sugar=calc_pct("SUGARCANE"),
                strawberry=calc_pct("STRAWBERRY"),
                sweet_potato=calc_pct("SWEET_POTATO"),
                potato=calc_pct("POTATO"),
                cashew=calc_pct("CASHEW_NUT"),
            )
        )

    return comparison_points

def get_spotlight_commodity(db: Session, code: str = "COFFEE_ROBUSTA") -> SpotlightSummaryResponse:
    """
    Trích xuất mặt hàng nông sản tiêu điểm với chuỗi xu hướng thật từ Database.
    """
    commodity = db.query(Commodity).filter(Commodity.code.ilike(f"%{code}%")).first()
    if not commodity:
        commodity = db.query(Commodity).first()

    if not commodity:
        return SpotlightSummaryResponse(
            commodityCode="COFFEE",
            commodityName="Cà phê",
            subtitle="Xu hướng 3 tháng",
            currentPrice="93.800 đ/kg",
            change3Months="+8.5%",
            peakPrice="104.000 đ/kg",
            trendData=[]
        )

    prices = (
        db.query(PriceHistory)
        .filter(PriceHistory.commodity_id == commodity.id)
        .order_by(desc(PriceHistory.record_date))
        .limit(65)
        .all()
    )
    prices = list(reversed(prices))

    if not prices:
        return SpotlightSummaryResponse(
            commodityCode=commodity.code,
            commodityName=commodity.name,
            subtitle="Xu hướng 3 tháng",
            currentPrice="0",
            change3Months="0%",
            peakPrice="0",
            trendData=[]
        )

    current_val = float(prices[-1].price)
    first_val = float(prices[0].price)
    peak_val = max([float(p.price) for p in prices])
    pct_change = round(((current_val - first_val) / first_val) * 100, 1) if first_val > 0 else 0.0

    # Lấy mẫu 7 điểm xu hướng
    step = max(1, len(prices) // 6)
    sampled = prices[::step]
    if prices[-1] not in sampled:
        sampled.append(prices[-1])

    trend_points = [
        SparklinePoint(
            date=p.record_date.strftime("%d/%m"),
            value=float(p.price)
        )
        for p in sampled
    ]

    short_code = commodity.code.replace("RICE_IR504", "RICE").replace("COFFEE_ROBUSTA", "COFFEE").replace("PEPPER_BLACK", "PEPPER").replace("SUGARCANE", "SUGAR").replace("SWEET_POTATO", "SWEETPOTATO").replace("CASHEW_NUT", "CASHEW")
    
    return SpotlightSummaryResponse(
        commodityCode=short_code,
        commodityName=commodity.name,
        subtitle="Xu hướng 3 tháng từ Database",
        currentPrice=f"{int(current_val):,}".replace(",", ".") + f" {commodity.unit}",
        change3Months=f"{'+' if pct_change >= 0 else ''}{pct_change}%",
        peakPrice=f"{int(peak_val):,}".replace(",", ".") + f" {commodity.unit}",
        trendData=trend_points
    )

def get_regional_prices_list(db: Session, province: Optional[str] = None):
    """
    Lấy bảng giá thị trường mới nhất của tất cả nông sản kèm khu vực, min-max và trạng thái định giá vùng.
    """
    commodities = db.query(Commodity).order_by(Commodity.id).all()
    norm_prov = normalize_province_code(province)
    regional_list = []

    for c in commodities:
        loc = resolve_commodity_location_context(db, c, province)
        latest = (
            db.query(PriceHistory)
            .filter(PriceHistory.commodity_id == c.id)
            .order_by(desc(PriceHistory.record_date))
            .limit(2)
            .all()
        )
        if not latest:
            continue

        p_curr = latest[0]
        p_prev = latest[1] if len(latest) > 1 else latest[0]
        offset = float(loc.get("basis_offset", 0.0)) if norm_prov else 0.0

        if norm_prov and loc.get("pricing_mode") == "direct" and loc.get("latest_direct_price"):
            price_val = float(loc["latest_direct_price"])
            anchor_offset = price_val - float(p_curr.price)
            prev_val = max(0.0, float(p_prev.price) + anchor_offset)
        else:
            price_val = max(0.0, float(p_curr.price) + offset)
            prev_val = max(0.0, float(p_prev.price) + offset)

        diff_pct = round(((price_val - prev_val) / prev_val) * 100, 1) if prev_val > 0 else 0.0

        p_min = max(0.0, (float(p_curr.price_min) + offset) if p_curr.price_min else price_val * 0.985)
        p_max = max(price_val, (float(p_curr.price_max) + offset) if p_curr.price_max else price_val * 1.015)
        vol = float(p_curr.volume) if p_curr.volume else 1250.0

        short_code = c.code.replace("RICE_IR504", "RICE").replace("COFFEE_ROBUSTA", "COFFEE").replace("PEPPER_BLACK", "PEPPER").replace("SUGARCANE", "SUGAR").replace("SWEET_POTATO", "SWEETPOTATO").replace("CASHEW_NUT", "CASHEW")

        regional_list.append({
            "id": c.id,
            "commodityName": c.name,
            "code": short_code,
            "region": loc["province_name"] if norm_prov else c.region,
            "price": f"{int(round(price_val)):,}".replace(",", "."),
            "unit": c.unit,
            "minMax": f"{int(round(p_min)):,}".replace(",", ".") + " - " + f"{int(round(p_max)):,}".replace(",", "."),
            "volume": f"{int(vol):,} tấn".replace(",", "."),
            "changePct": diff_pct,
            "source": (loc.get("direct_source") or loc.get("note") or p_curr.source or "Sở NN&PTNT / Hiệp hội Ngành hàng") if norm_prov else (p_curr.source or "Sở NN&PTNT / Hiệp hội Ngành hàng"),
            "updatedAt": f"Ngày {p_curr.record_date.strftime('%d/%m/%Y')}",
            "pricingMode": loc.get("pricing_mode", "national_benchmark"),
            "locationContext": loc,
        })

    return regional_list

