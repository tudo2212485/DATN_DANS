from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.models.models import Commodity, Forecast, TrainingRun
from app.services.history_service import fingerprint, training_context
import json
from datetime import date
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
        
    context = training_context(db, commodity)
    latest_run = db.query(func.max(Forecast.training_run_id)).filter(Forecast.commodity_id == commodity_id).scalar()
    run = db.get(TrainingRun, latest_run) if latest_run else None
    if not run or run.dataset_hash != fingerprint(context["rows"]):
        return []
    models = db.query(Forecast.model_name).filter(Forecast.commodity_id == commodity_id, Forecast.training_run_id == latest_run).distinct().all()
    
    result = []
    for (m_name,) in models:
        f = (
            db.query(Forecast)
            .filter(Forecast.commodity_id == commodity_id, Forecast.model_name == m_name, Forecast.training_run_id == latest_run)
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
    return sorted(result, key=lambda m: m.rmse)

def get_forecast_dashboard(
    db: Session, commodity_id: int = 2, model_name: str = "LSTM", days: int = 10
) -> ForecastDashboardResponse:
    commodity = db.query(Commodity).filter(Commodity.id == commodity_id).first()
    if not commodity:
        raise HTTPException(status_code=404, detail="Không tìm thấy nông sản")

    # Get recent historical prices
    context = training_context(db, commodity)
    history = context["rows"][-30:]
    quality = context["quality"]
    if not quality["ready"]:
        raise HTTPException(
            409,
            f"Chưa thể tạo biểu đồ dự báo cho {commodity.name}: {quality['reason']} "
            "Hệ thống vẫn tự thu thập dữ liệu theo lịch và sẽ tự huấn luyện khi chuỗi đủ điều kiện.",
        )

    from app.services.job_service import MODEL_NAMES
    if model_name.upper() not in MODEL_NAMES:
        raise HTTPException(400, "Thuật toán không được hỗ trợ")
    latest_training_date = db.query(func.max(Forecast.training_date)).filter(
        Forecast.commodity_id == commodity_id, Forecast.model_name.ilike(model_name)
    ).scalar()
    # Get forecasts for this model
    forecast_rows = (
        db.query(Forecast)
        .filter(
            Forecast.commodity_id == commodity_id,
            Forecast.model_name.ilike(model_name),
            Forecast.training_date == latest_training_date,
            Forecast.forecast_date > history[-1].record_date if history else True
        )
        .order_by(Forecast.forecast_date, desc(Forecast.training_date), desc(Forecast.id))
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
        run = db.get(TrainingRun, first_f.training_run_id) if first_f.training_run_id else None
        if not run or run.dataset_hash != fingerprint(context["rows"]):
            raise HTTPException(409, "Dữ liệu đã thay đổi hoặc dự báo cũ chưa có nguồn đầu vào được xác minh. Hãy thu thập đủ lịch sử và huấn luyện lại.")
        training = json.loads(run.metadata_json)
        training.pop("snapshot", None)
        training.update(run_id=run.id, dataset_hash=run.dataset_hash, trained_at=run.created_at.isoformat(),
                        stale_days=max(0, (date.today() - history[-1].record_date).days),
                        interval_note=("Dải ước lượng ±1,96 RMSE theo kỳ; chuỗi mía dùng giá mua trong báo cáo."
                                       if context["cadence"] == "periodic" else
                                       "Dải ước lượng ±1,96 RMSE theo mốc công bố AGROINFO."
                                       if context["cadence"] == "irregular" else
                                       "Dải ước lượng ±1,96 RMSE; chưa kiểm chứng độ bao phủ 95%."))
        if first_f.mae is not None:
            latest_metrics = ModelMetricsResponse(
                modelName=model_name,
                mae=float(first_f.mae),
                rmse=float(first_f.rmse) if first_f.rmse else 0.0,
                mape=float(first_f.mape) if first_f.mape else 0.0,
                r2=float(first_f.r2) if first_f.r2 else 0.0,
                trainDate=first_f.training_date.strftime("%d/%m/%Y") if first_f.training_date else "N/A"
            )

        for i, f in enumerate(forecast_rows):
            forecast_data.append(
                ForecastPointResponse(
                    date=f.forecast_date.isoformat(),
                    predictedPrice=float(f.predicted_price),
                    lowerCI=float(f.lower_ci),
                    upperCI=float(f.upper_ci),
                    isForecast=True
                )
            )
    else:
        raise HTTPException(409, "Chưa có dự báo phù hợp với dữ liệu mới nhất. Hãy huấn luyện lại mô hình trong trang quản trị.")

    return ForecastDashboardResponse(
        commodity=CommodityResponse.model_validate(commodity),
        modelName=model_name,
        metrics=latest_metrics,
        forecastData=forecast_data,
        training=training
    )

