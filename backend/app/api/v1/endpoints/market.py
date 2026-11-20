"""Unified `/api/v1/market/*` endpoints supporting `?province=` and cross-province price comparison."""
from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.schemas import CommodityOverviewCard, MarketComparisonPoint
from app.services.commodity_service import (
    get_commodities_overview,
    get_market_comparison,
)
from app.services.regional_pricing_service import get_commodity_province_comparison

router = APIRouter()


@router.get("/overview", response_model=List[CommodityOverviewCard])
def market_overview(
    province: Optional[str] = Query(None, description="Mã tỉnh/thành phố (VD: khanh-hoa, dak-lak, all)"),
    db: Session = Depends(get_db),
):
    """Tổng quan giá nông sản theo vị trí địa lý hiện tại."""
    return get_commodities_overview(db, province=province)


@router.get("/compare", response_model=List[MarketComparisonPoint])
def market_compare(
    province: Optional[str] = Query(None, description="Mã tỉnh/thành phố (VD: khanh-hoa, dak-lak, all)"),
    db: Session = Depends(get_db),
):
    """Chuỗi so sánh tỷ suất biến động giá (%) theo tỉnh/thành phố."""
    return get_market_comparison(db, province=province)


@router.get("/history")
def market_history(
    commodity_id: int = Query(...),
    start_date: date = Query(...),
    end_date: date = Query(...),
    include_unverified: bool = False,
    province: Optional[str] = Query(None, description="Mã tỉnh/thành phố (VD: khanh-hoa)"),
    db: Session = Depends(get_db),
):
    """Lịch sử giá theo nông sản và tỉnh/thành phố."""
    from app.api.v1.endpoints.history import history as history_handler

    return history_handler(
        commodity_id=commodity_id,
        start_date=start_date,
        end_date=end_date,
        include_unverified=include_unverified,
        province=province,
        db=db,
    )


@router.get("/regional-prices/{commodity_code}")
def regional_prices_by_commodity(
    commodity_code: str,
    province: Optional[str] = Query(None, description="Tỉnh ưu tiên hiển thị so sánh (VD: khanh-hoa)"),
    db: Session = Depends(get_db),
):
    """Bảng so sánh chênh lệch giá mới nhất của 1 mặt hàng giữa các tỉnh/thành phố."""
    result = get_commodity_province_comparison(db, commodity_code, focus_province=province)
    if not result.get("commodity"):
        raise HTTPException(status_code=404, detail=f"Không tìm thấy nông sản '{commodity_code}'")
    return result

