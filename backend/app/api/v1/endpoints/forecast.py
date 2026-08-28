from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.schemas import ForecastDashboardResponse
from app.services.forecast_service import get_forecast_dashboard

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
