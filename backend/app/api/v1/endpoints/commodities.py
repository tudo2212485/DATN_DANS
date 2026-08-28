from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Commodity
from app.schemas.schemas import (
    CommodityResponse,
    CommodityCreate,
    CommodityOverviewCard,
    MarketComparisonPoint,
    SpotlightSummaryResponse,
)
from app.core.deps import require_role
from app.services.commodity_service import (
    get_commodities_overview,
    get_market_comparison,
    get_spotlight_commodity,
)

router = APIRouter()

@router.get("", response_model=List[CommodityResponse])
def read_commodities(db: Session = Depends(get_db)):
    """Lấy danh sách tất cả các loại nông sản"""
    return db.query(Commodity).order_by(Commodity.id).all()

@router.post("", response_model=CommodityResponse)
def create_commodity(
    item: CommodityCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["admin"]))
):
    """Thêm nông sản mới (Chỉ Admin)"""
    db_item = Commodity(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put("/{commodity_id}", response_model=CommodityResponse)
def update_commodity(
    commodity_id: int,
    item: CommodityCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["admin"]))
):
    """Cập nhật thông tin nông sản (Chỉ Admin)"""
    db_item = db.query(Commodity).filter(Commodity.id == commodity_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Không tìm thấy nông sản")
    
    for key, value in item.model_dump().items():
        setattr(db_item, key, value)
        
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{commodity_id}")
def delete_commodity(
    commodity_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["admin"]))
):
    """Xóa nông sản (Chỉ Admin)"""
    db_item = db.query(Commodity).filter(Commodity.id == commodity_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Không tìm thấy nông sản")
    
    db.delete(db_item)
    db.commit()
    return {"message": "Xóa thành công"}

@router.get("/overview", response_model=List[CommodityOverviewCard])
def read_overview(db: Session = Depends(get_db)):
    """Lấy 4 thẻ nông sản tổng quan kèm sparkline và % tăng giảm"""
    return get_commodities_overview(db)

@router.get("/comparison", response_model=List[MarketComparisonPoint])
def read_comparison(db: Session = Depends(get_db)):
    """Lấy dữ liệu chuỗi thời gian so sánh % tăng giảm từ đầu kỳ"""
    return get_market_comparison(db)

@router.get("/spotlight", response_model=SpotlightSummaryResponse)
def read_spotlight(code: str = "SUGARCANE", db: Session = Depends(get_db)):
    """Lấy dữ liệu tiêu điểm nông sản (xu hướng 3 tháng)"""
    return get_spotlight_commodity(db, code)
