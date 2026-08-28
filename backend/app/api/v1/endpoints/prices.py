from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from app.core.database import get_db
from app.models.models import PriceHistory
from app.schemas.schemas import PriceHistoryResponse

router = APIRouter()

@router.get("/history", response_model=List[PriceHistoryResponse])
def get_price_history(
    commodity_id: int = Query(..., description="ID nông sản"),
    days: Optional[int] = Query(60, description="Số ngày cần lấy"),
    db: Session = Depends(get_db)
):
    """Lấy dữ liệu chuỗi thời gian lịch sử giá"""
    prices = (
        db.query(PriceHistory)
        .filter(PriceHistory.commodity_id == commodity_id)
        .order_by(desc(PriceHistory.record_date))
        .limit(days)
        .all()
    )
    return list(reversed(prices))
