from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db, SessionLocal
from app.models.models import Commodity, Forecast
from app.schemas.schemas import (
    PredictionForecastResponse,
    PredictionMetricsResponse,
    PredictionModelMetric,
    TaskRunResponse,
)
from ml_pipeline.predictor import PricePredictor, clear_prediction_cache
from ml_pipeline.model_trainer import ModelTrainer
from ml_pipeline.data_loader import load_clean_data

router = APIRouter()


@router.get("/forecast", response_model=PredictionForecastResponse)
def get_prediction_forecast(
    symbol: Optional[str] = Query(None, description="Mã nông sản / hàng hóa (ví dụ: ROBUSTA, PEPPER, RICE, COPPER)"),
    commodity_id: Optional[int] = Query(None, description="Hoặc ID nông sản (ví dụ: 1, 2, 3)"),
    model: str = Query("LSTM", description="Mô hình Machine Learning (LSTM, Prophet, XGBoost, ARIMA)"),
    days: int = Query(7, ge=1, le=60, description="Số ngày dự báo trong tương lai (7, 14, 30)"),
    include_history: int = Query(5, ge=0, le=30, description="Số điểm lịch sử gần nhất để vẽ biểu đồ"),
    use_cache: bool = Query(True, description="Sử dụng In-Memory Cache để phản hồi <100ms"),
    db: Session = Depends(get_db)
):
    """
    Lấy kết quả dự báo giá hàng hóa trong tương lai (7 ngày, 30 ngày) kèm dải khoảng tin cậy 95% (yhat_lower, yhat_upper)
    và các chỉ số sai số của mô hình (MAE, RMSE, MAPE, R2 Score).
    """
    # Xác định commodity từ symbol hoặc commodity_id
    target_id_or_code = symbol or commodity_id or "ROBUSTA"
    
    # Tìm kiếm commodity trong db
    commodity = None
    if commodity_id:
        commodity = db.query(Commodity).filter(Commodity.id == commodity_id).first()
    elif symbol:
        commodity = db.query(Commodity).filter(Commodity.code.ilike(symbol.strip())).first()
    
    if not commodity:
        # Nếu chưa tìm thấy, lấy commodity đầu tiên mặc định
        commodity = db.query(Commodity).first()
        if not commodity and not symbol:
            raise HTTPException(status_code=404, detail="Không tìm thấy thông tin hàng hóa yêu cầu.")
            
    predictor = PricePredictor(commodity.code if commodity else target_id_or_code, db=db)
    
    try:
        result = predictor.forecast(
            model_name=model,
            days=days,
            include_history=include_history,
            use_cache=use_cache
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi thực hiện dự báo với mô hình {model}: {str(e)}"
        )


@router.get("/metrics", response_model=PredictionMetricsResponse)
def get_prediction_metrics(
    symbol: Optional[str] = Query(None, description="Mã nông sản (ví dụ: ROBUSTA, PEPPER, RICE, COPPER)"),
    commodity_id: Optional[int] = Query(None, description="Hoặc ID nông sản"),
    db: Session = Depends(get_db)
):
    """
    Lấy các chỉ số đánh giá độ chính xác mô hình (MAE, RMSE, MAPE, R2 Score, Trạng thái kiểm duyệt sai số)
    """
    target = symbol or commodity_id or "ROBUSTA"
    predictor = PricePredictor(target, db=db)
    metrics_summary = predictor.get_metrics_summary()

    models_list = []
    for m_name, data in metrics_summary.items():
        models_list.append(
            PredictionModelMetric(
                model_name=m_name,
                metrics=data.get("metrics", {}),
                trained_at=data.get("trained_at", "N/A"),
                passed_threshold=data.get("passed_threshold", True),
                threshold_reason=data.get("threshold_reason", "Passed Quality Check")
            )
        )

    return PredictionMetricsResponse(
        symbol=predictor.code,
        models=models_list
    )


def _async_retrain_task(commodity_id: Optional[int] = None):
    """Tiến trình huấn luyện lại mô hình trong background thread"""
    db = SessionLocal()
    try:
        if commodity_id:
            commodities = db.query(Commodity).filter(Commodity.id == commodity_id).all()
        else:
            commodities = db.query(Commodity).all()

        for c in commodities:
            df = load_clean_data(c.id, db)
            if not df.empty and len(df) >= 10:
                trainer = ModelTrainer(commodity_code=c.code)
                trainer.train_all(df)
        
        # Xóa cache sau khi retrain
        clear_prediction_cache()
    except Exception as e:
        print(f"Lỗi khi chạy background retrain task: {e}")
    finally:
        db.close()


@router.post("/retrain", response_model=TaskRunResponse)
def trigger_model_retrain(
    commodity_id: Optional[int] = Query(None, description="ID nông sản cần huấn luyện lại (bỏ trống để huấn luyện toàn bộ)"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    """
    Kích hoạt tiến trình huấn luyện lại toàn bộ mô hình (Prophet, XGBoost, LSTM)
    chạy nền (Async Execution) không làm nghẽn FastAPI Event Loop.
    """
    background_tasks.add_task(_async_retrain_task, commodity_id=commodity_id)
    target_str = f"nông sản ID {commodity_id}" if commodity_id else "toàn bộ danh mục nông sản"
    return TaskRunResponse(
        task_name="Huấn luyện mô hình Machine Learning (Retrain)",
        status="RUNNING",
        message=f"Đã bắt đầu tác vụ huấn luyện các mô hình (Prophet, XGBoost, PyTorch LSTM) cho {target_str}.",
        records_processed=0,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
