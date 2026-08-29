from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.schemas import ForecastDashboardResponse, ModelMetricsResponse
from app.services.forecast_service import get_forecast_dashboard, get_forecast_comparison
from typing import List

router = APIRouter()

@router.get("", response_model=ForecastDashboardResponse)
def read_forecast(
    commodity_id: int = Query(2, description="ID nông sản (mặc định Cà phê Robusta = 2)"),
    model_name: str = Query("LSTM", description="Mô hình (LSTM, Prophet, ARIMA)"),
    days: int = Query(10, description="Số ngày dự báo (7, 10, 14)"),
    db: Session = Depends(get_db)
):
    """Lấy dữ liệu dự báo giá, dải khoảng tin cậy 95% và các chỉ số sai số (MAE, RMSE, MAPE, R2)"""
    return get_forecast_dashboard(db, commodity_id=commodity_id, model_name=model_name, days=days)

@router.get("/compare/{commodity_id}", response_model=List[ModelMetricsResponse])
def compare_models(
    commodity_id: int,
    db: Session = Depends(get_db)
):
    """Lấy số liệu so sánh hiệu năng giữa tất cả các mô hình cho một nông sản cụ thể"""
    return get_forecast_comparison(db, commodity_id=commodity_id)
