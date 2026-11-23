from fastapi import APIRouter, Depends, Query
from pydantic import BeforeValidator
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.schemas import ForecastDashboardResponse, ModelMetricsResponse
from app.services.forecast_service import get_forecast_dashboard, get_forecast_comparison
from typing import Annotated, List, Literal, Optional
from app.services.job_service import active_model

router = APIRouter()


def _coerce_horizon_int(value: object) -> object:
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return value
    return value


ForecastHorizonDays = Annotated[
    Literal[7, 14, 30],
    BeforeValidator(_coerce_horizon_int),
    Query(description="Kỳ hạn dự báo chuẩn (chỉ hỗ trợ 7, 14 hoặc 30 ngày)"),
]


@router.get("", response_model=ForecastDashboardResponse)
def read_forecast(
    commodity_id: int = Query(2, description="ID nông sản (mặc định Cà phê Robusta = 2)"),
    model_name: Optional[str] = Query(None, description="Mô hình (LSTM, Prophet, ARIMA, XGBoost, Random Forest)"),
    days: ForecastHorizonDays = 14,
    region: Optional[str] = Query(None, description="Mã khu vực cũ (tương thích ngược)"),
    province: Optional[str] = Query(None, description="Mã tỉnh/thành phố (VD: khanh-hoa, dak-lak, all)"),
    db: Session = Depends(get_db)
):
    """Lấy dữ liệu dự báo giá theo tỉnh/thành phố, dải khoảng tin cậy 95% và các chỉ số sai số"""
    return get_forecast_dashboard(
        db,
        commodity_id=commodity_id,
        model_name=model_name or active_model(db),
        days=days,
        region=region,
        province=province,
    )

@router.get("/compare/{commodity_id}", response_model=List[ModelMetricsResponse])
def compare_models(
    commodity_id: int,
    db: Session = Depends(get_db)
):
    """Lấy số liệu so sánh hiệu năng giữa tất cả các mô hình cho một nông sản cụ thể"""
    return get_forecast_comparison(db, commodity_id=commodity_id)
