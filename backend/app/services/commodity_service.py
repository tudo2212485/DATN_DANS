from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.models import Commodity, PriceHistory
from app.schemas.schemas import (
    CommodityOverviewCard,
    SparklinePoint,
    MarketComparisonPoint,
    SpotlightSummaryResponse,
)
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

        overview_cards.append(
            CommodityOverviewCard(
                id=c.id,
                code=c.code.replace("RICE_IR504", "RICE").replace("COFFEE_ROBUSTA", "COFFEE").replace("PEPPER_BLACK", "PEPPER").replace("SUGARCANE", "SUGAR"),
                name=c.name.split(" ")[0] + (" " + c.name.split(" ")[1] if len(c.name.split(" ")) > 1 and "Cà" in c.name else ""),
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
    # Mock / calculated normalized comparison from database
    return [
        MarketComparisonPoint(date="01/06", rice=0.0, coffee=0.0, pepper=0.0, sugar=0.0),
        MarketComparisonPoint(date="08/06", rice=1.8, coffee=2.5, pepper=1.2, sugar=3.4),
        MarketComparisonPoint(date="15/06", rice=3.2, coffee=4.8, pepper=2.1, sugar=5.9),
        MarketComparisonPoint(date="22/06", rice=2.8, coffee=5.9, pepper=3.0, sugar=8.5),
        MarketComparisonPoint(date="29/06", rice=4.6, coffee=4.2, pepper=2.4, sugar=8.0),
        MarketComparisonPoint(date="06/07", rice=6.5, coffee=2.6, pepper=3.8, sugar=8.9),
        MarketComparisonPoint(date="13/07", rice=5.8, coffee=1.5, pepper=4.1, sugar=9.4),
        MarketComparisonPoint(date="20/07", rice=7.2, coffee=1.8, pepper=4.0, sugar=9.8),
        MarketComparisonPoint(date="28/08", rice=7.9, coffee=1.9, pepper=4.1, sugar=10.1),
    ]

def get_spotlight_commodity(db: Session, code: str = "SUGARCANE") -> SpotlightSummaryResponse:
    commodity = db.query(Commodity).filter(Commodity.code.ilike(f"%{code}%")).first()
    
    return SpotlightSummaryResponse(
        commodityCode="SUGAR",
        commodityName="Mía đường",
        subtitle="Xu hướng 3 tháng",
        currentPrice="1.200 đ/kg",
        change3Months="+10.1%",
        peakPrice="1.202 đ/kg",
        trendData=[
            SparklinePoint(date="01/06", value=1090),
            SparklinePoint(date="15/06", value=1120),
            SparklinePoint(date="01/07", value=1160),
            SparklinePoint(date="15/07", value=1150),
            SparklinePoint(date="01/08", value=1180),
            SparklinePoint(date="15/08", value=1198),
            SparklinePoint(date="28/08", value=1200),
        ]
    )
