from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.models import Commodity, PriceHistory
from app.schemas.schemas import (
    CommodityOverviewCard,
    SparklinePoint,
    MarketComparisonPoint,
    SpotlightSummaryResponse,
)
from datetime import datetime
from typing import List

def get_commodities_overview(db: Session) -> List[CommodityOverviewCard]:
    commodities = db.query(Commodity).order_by(Commodity.id).all()
    overview_cards = []

    for c in commodities:
        # Get last 7 price records for sparkline
        prices = (
            db.query(PriceHistory)
            .filter(PriceHistory.commodity_id == c.id)
            .order_by(desc(PriceHistory.record_date))
            .limit(7)
            .all()
        )
        prices = list(reversed(prices))

        if not prices:
            # Fallback if empty
            current_p = 1000.0
            change_pct = 0.0
            sparkline = []
        else:
            current_p = float(prices[-1].price)
            prev_p = float(prices[0].price) if len(prices) > 1 else current_p
            change_pct = round(((current_p - prev_p) / prev_p) * 100, 1) if prev_p > 0 else 0.0
            sparkline = [
                SparklinePoint(
                    date=p.record_date.strftime("%d/%m"),
                    value=float(p.price)
                )
                for p in prices
            ]

        # Format price with dots (vi-VN standard)
        formatted_price = f"{int(current_p):,}".replace(",", ".")

        # Map friendly Vietnamese short names
        name_map = {
            "RICE_IR504": "Lúa gạo",
            "COFFEE_ROBUSTA": "Cà phê",
            "PEPPER_BLACK": "Hồ tiêu",
            "SUGARCANE": "Mía đường"
        }
        display_name = name_map.get(c.code, c.name.split(" ")[0] + (" " + c.name.split(" ")[1] if len(c.name.split(" ")) > 1 else ""))

        overview_cards.append(
            CommodityOverviewCard(
                id=c.id,
                code=c.code.replace("RICE_IR504", "RICE").replace("COFFEE_ROBUSTA", "COFFEE").replace("PEPPER_BLACK", "PEPPER").replace("SUGARCANE", "SUGAR"),
                name=display_name,
                category=c.category,
                unit=c.unit,
                region=c.region,
                currentPrice=current_p,
                formattedPrice=formatted_price,
                changePct=change_pct,
                isPositive=change_pct >= 0,
                sparkline=sparkline
            )
        )

    return overview_cards

def get_market_comparison(db: Session) -> List[MarketComparisonPoint]:
    """
    Tính toán chỉ số tăng trưởng chuẩn hóa % của 4 mặt hàng nông sản từ cơ sở dữ liệu thật.
    Lấy mẫu 9 mốc thời gian trong 90 ngày gần nhất.
    """
    commodities = db.query(Commodity).order_by(Commodity.id).all()
    if not commodities:
        return []

    # Thu thập chuỗi giá của 4 nông sản
    com_dict = {c.id: c.code for c in commodities}
    
    # Lấy 90 ngày gần nhất
    all_prices = (
        db.query(PriceHistory)
        .order_by(PriceHistory.record_date.desc())
        .limit(90 * len(commodities))
        .all()
    )
    
    if not all_prices:
        return []

    # Nhóm theo ngày và commodity
    date_map = {}
    for p in all_prices:
        d_str = p.record_date.strftime("%d/%m")
        if d_str not in date_map:
            date_map[d_str] = {}
        c_code = com_dict.get(p.commodity_id, "")
        date_map[d_str][c_code] = float(p.price)

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
    for code in ["RICE_IR504", "COFFEE_ROBUSTA", "PEPPER_BLACK", "SUGARCANE"]:
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
                sugar=calc_pct("SUGARCANE")
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

    short_code = commodity.code.replace("RICE_IR504", "RICE").replace("COFFEE_ROBUSTA", "COFFEE").replace("PEPPER_BLACK", "PEPPER").replace("SUGARCANE", "SUGAR")
    
    return SpotlightSummaryResponse(
        commodityCode=short_code,
        commodityName=commodity.name,
        subtitle="Xu hướng 3 tháng từ Database",
        currentPrice=f"{int(current_val):,}".replace(",", ".") + f" {commodity.unit}",
        change3Months=f"{'+' if pct_change >= 0 else ''}{pct_change}%",
        peakPrice=f"{int(peak_val):,}".replace(",", ".") + f" {commodity.unit}",
        trendData=trend_points
    )

def get_regional_prices_list(db: Session):
    """
    Lấy bảng giá thị trường mới nhất của tất cả nông sản kèm khu vực, min-max và sản lượng từ PostgreSQL.
    """
    commodities = db.query(Commodity).order_by(Commodity.id).all()
    regional_list = []

    for c in commodities:
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

        price_val = float(p_curr.price)
        prev_val = float(p_prev.price)
        diff_pct = round(((price_val - prev_val) / prev_val) * 100, 1) if prev_val > 0 else 0.0

        p_min = float(p_curr.price_min) if p_curr.price_min else price_val * 0.985
        p_max = float(p_curr.price_max) if p_curr.price_max else price_val * 1.015
        vol = float(p_curr.volume) if p_curr.volume else 1250.0

        short_code = c.code.replace("RICE_IR504", "RICE").replace("COFFEE_ROBUSTA", "COFFEE").replace("PEPPER_BLACK", "PEPPER").replace("SUGARCANE", "SUGAR")

        regional_list.append({
            "id": c.id,
            "commodityName": c.name,
            "code": short_code,
            "region": c.region,
            "price": f"{int(price_val):,}".replace(",", "."),
            "unit": c.unit,
            "minMax": f"{int(p_min):,}".replace(",", ".") + " - " + f"{int(p_max):,}".replace(",", "."),
            "volume": f"{int(vol):,} tấn".replace(",", "."),
            "changePct": diff_pct,
            "source": p_curr.source or "Sở NN&PTNT / Hiệp hội Ngành hàng",
            "updatedAt": f"Ngày {p_curr.record_date.strftime('%d/%m/%Y')}"
        })

    return regional_list

