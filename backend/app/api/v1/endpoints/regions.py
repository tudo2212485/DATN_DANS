"""Endpoints for Vietnamese provinces/regions list and GPS auto-location."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.regional_pricing_service import (
    list_regions_with_coverage,
    locate_nearest_province,
)

router = APIRouter()


@router.get("")
def get_regions(db: Session = Depends(get_db)):
    """Trả danh sách tỉnh/thành phố hỗ trợ kèm tọa độ và các mặt hàng có khảo sát trực tiếp."""
    return list_regions_with_coverage(db)


@router.get("/locate")
def locate_region(
    lat: float = Query(..., ge=-90.0, le=90.0, description="Vĩ độ GPS (WGS-84)"),
    lng: float = Query(..., ge=-180.0, le=180.0, description="Kinh độ GPS (WGS-84)"),
    db: Session = Depends(get_db),
):
    """Tự động xác định tỉnh/thành phố Việt Nam gần nhất theo tọa độ GPS bằng công thức Haversine."""
    try:
        return locate_nearest_province(db, lat, lng)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Không xác định được vị trí: {exc}")

