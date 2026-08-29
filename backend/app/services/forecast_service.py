from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.models import Commodity, Forecast, PriceHistory
from app.schemas.schemas import (
    ForecastDashboardResponse,
    ForecastPointResponse,
    ModelMetricsResponse,
    CommodityResponse,
)
from fastapi import HTTPException
from typing import List

def get_forecast_comparison(db: Session, commodity_id: int) -> List[ModelMetricsResponse]:
    commodity = db.query(Commodity).filter(Commodity.id == commodity_id).first()
    if not commodity:
        raise HTTPException(status_code=404, detail="Không tìm thấy nông sản")
        
    # Get distinct models and their latest metrics for this commodity
    # We query the forecast table, order by training_date/forecast_date descending to get the newest
    # For simplicity, we can get the first row for each model_name since training metrics (mae, rmse) 
    # are duplicated across the horizon rows of the same training session.
    
    models = db.query(Forecast.model_name).filter(Forecast.commodity_id == commodity_id).distinct().all()
    
    result = []
    for (m_name,) in models:
        f = (
            db.query(Forecast)
            .filter(Forecast.commodity_id == commodity_id, Forecast.model_name == m_name)
            .order_by(desc(Forecast.training_date), desc(Forecast.forecast_date))
            .first()
        )
        if f and f.mae is not None:
            result.append(
                ModelMetricsResponse(
                    modelName=m_name,
                    mae=float(f.mae),
                    rmse=float(f.rmse) if f.rmse else 0.0,
                    mape=float(f.mape) if f.mape else 0.0,
                    r2=float(f.r2) if f.r2 else 0.0,
                    trainDate=f.training_date.strftime("%d/%m/%Y") if f.training_date else "N/A"
                )
            )
            
    return result

def get_forecast_dashboard(
    db: Session, commodity_id: int = 2, model_name: str = "LSTM", days: int = 10
) -> ForecastDashboardResponse:
    commodity = db.query(Commodity).filter(Commodity.id == commodity_id).first()
    if not commodity:
        raise HTTPException(status_code=404, detail="Không tìm thấy nông sản")

    # Get recent historical prices
    history = (
        db.query(PriceHistory)
        .filter(PriceHistory.commodity_id == commodity_id)
        .order_by(desc(PriceHistory.record_date))
        .limit(4)
        .all()
    )
    history = list(reversed(history))

    # Get forecasts for this model
    forecast_rows = (
        db.query(Forecast)
        .filter(
            Forecast.commodity_id == commodity_id,
            Forecast.model_name.ilike(model_name)
        )
        .order_by(Forecast.forecast_date)
        .limit(days)
        .all()
    )

    forecast_data = []

    # Add historical points
    for p in history:
        forecast_data.append(
            ForecastPointResponse(
                date=p.record_date.strftime("%d/%m"),
                actualPrice=float(p.price),
                predictedPrice=float(p.price),
                lowerCI=float(p.price),
                upperCI=float(p.price),
                isForecast=False
            )
        )

    # Add future predicted points with 95% CI
    latest_metrics = ModelMetricsResponse(
        modelName=model_name,
        mae=0.0,
        rmse=0.0,
        mape=0.0,
        r2=0.0,
        trainDate="N/A"
    )

    if forecast_rows:
        first_f = forecast_rows[0]
        if first_f.mae is not None:
            latest_metrics = ModelMetricsResponse(
                modelName=model_name,
                mae=float(first_f.mae),
                rmse=float(first_f.rmse) if first_f.rmse else 0.0,
                mape=float(first_f.mape) if first_f.mape else 0.0,
                r2=float(first_f.r2) if first_f.r2 else 0.0,
                trainDate=first_f.training_date.strftime("%d/%m/%Y") if first_f.training_date else "28/08/2026"
            )

        for i, f in enumerate(forecast_rows):
            forecast_data.append(
                ForecastPointResponse(
                    date=f.forecast_date.strftime(f"%d/%m (T+{i+1})"),
                    predictedPrice=float(f.predicted_price),
                    lowerCI=float(f.lower_ci),
                    upperCI=float(f.upper_ci),
                    isForecast=True
                )
            )

    return ForecastDashboardResponse(
        commodity=CommodityResponse.model_validate(commodity),
        modelName=model_name,
        metrics=latest_metrics,
        forecastData=forecast_data
    )
