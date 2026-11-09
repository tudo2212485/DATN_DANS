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
    RegionInfo,
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


COMMODITY_REGIONS = {
    "COFFEE_ROBUSTA": [
        {"id": "all", "name": "Toàn vùng Tây Nguyên (Bình quân)", "basisSpread": 0.0, "description": "Giá bình quân giao dịch tại các tỉnh Tây Nguyên"},
        {"id": "daklak", "name": "Đắk Lắk (Cư M'gar, Buôn Hồ)", "basisSpread": 0.0, "description": "Thủ phủ cà phê Robusta, chất lượng cao, giá tham chiếu chuẩn"},
        {"id": "lamdong", "name": "Lâm Đồng (Bảo Lộc, Di Linh)", "basisSpread": -800.0, "description": "Độ ẩm cao hơn mùa mưa, chiết khấu vận chuyển -800 đ/kg"},
        {"id": "gialai", "name": "Gia Lai (Chư Prông, Pleiku)", "basisSpread": -300.0, "description": "Sát giá Đắk Lắk, chiết khấu cước vận tải -300 đ/kg"},
        {"id": "daknong", "name": "Đắk Nông (Gia Nghĩa)", "basisSpread": 200.0, "description": "Vùng chuyên canh mới, hạt chắc, thặng dư +200 đ/kg"},
    ],
    "PEPPER_BLACK": [
        {"id": "all", "name": "Toàn vùng (Bình quân)", "basisSpread": 0.0, "description": "Giá tiêu đen xô bình quân"},
        {"id": "daklak", "name": "Đắk Lắk / Đắk Nông", "basisSpread": 0.0, "description": "Giá tiêu chuẩn tại vùng Tây Nguyên"},
        {"id": "gialai", "name": "Gia Lai (Chư Sê)", "basisSpread": -500.0, "description": "Tiêu Chư Sê, chiết khấu -500 đ/kg"},
        {"id": "baria", "name": "Bà Rịa - Vũng Tàu (Châu Đức)", "basisSpread": 1500.0, "description": "Dung trọng hạt cao (550-570g/l), thặng dư +1.500 đ/kg"},
        {"id": "binhphuoc", "name": "Bình Phước (Lộc Ninh)", "basisSpread": -500.0, "description": "Tiêu đen Đông Nam Bộ, chiết khấu -500 đ/kg"},
    ],
    "RICE_IR504": [
        {"id": "all", "name": "Toàn ĐBSCL (Bình quân)", "basisSpread": 0.0, "description": "Giá lúa gạo bình quân vùng ĐBSCL"},
        {"id": "angiang", "name": "An Giang (Lúa tươi tại ruộng)", "basisSpread": -200.0, "description": "Lúa tươi thu hoạch tại ruộng An Giang"},
        {"id": "dongthap", "name": "Đồng Tháp (Lúa kho / Bán buôn)", "basisSpread": 150.0, "description": "Lúa khô tại kho Đồng Tháp, đã qua sơ chế"},
        {"id": "tiengiang", "name": "Tiền Giang / Long An", "basisSpread": 50.0, "description": "Gần cảng xuất khẩu, chi phí logistics thấp"},
    ],
    "STRAWBERRY": [
        {"id": "all", "name": "Toàn quốc (Bình quân)", "basisSpread": 0.0, "description": "Giá dâu tây tươi bình quân"},
        {"id": "dalat", "name": "Đà Lạt (Lâm Đồng - Loại 1)", "basisSpread": 0.0, "description": "Dâu giống New Zealand trồng nhà kính Đà Lạt"},
        {"id": "mocchau", "name": "Sơn La (Mộc Châu)", "basisSpread": -15000.0, "description": "Dâu Mộc Châu, chiết khấu phẩm cấp -15.000 đ/kg"},
    ],
    "SWEET_POTATO": [
        {"id": "all", "name": "ĐBSCL (Bình quân)", "basisSpread": 0.0, "description": "Giá khoai lang tím bình quân"},
        {"id": "binhtan", "name": "Bình Tân (Vĩnh Long - Loại 1)", "basisSpread": 0.0, "description": "Thủ phủ khoai lang tím Vĩnh Long xuất khẩu"},
        {"id": "dongthap", "name": "Đồng Tháp / Hậu Giang", "basisSpread": -400.0, "description": "Vùng trồng phụ cận ĐBSCL"},
    ],
    "POTATO": [
        {"id": "all", "name": "Lâm Đồng (Bình quân)", "basisSpread": 0.0, "description": "Khoai tây Đà Lạt bình quân"},
        {"id": "dalat", "name": "Đà Lạt (Khoai tây hồng loại 1)", "basisSpread": 0.0, "description": "Khoai tây củ to, vỏ hồng ruột vàng Đà Lạt"},
        {"id": "donduong", "name": "Đơn Dương / Đức Trọng", "basisSpread": -1000.0, "description": "Khoai tây thương phẩm loại 2"},
    ],
    "CASHEW_NUT": [
        {"id": "all", "name": "Đông Nam Bộ (Bình quân)", "basisSpread": 0.0, "description": "Giá hạt điều thô bình quân"},
        {"id": "binhphuoc", "name": "Bình Phước (Thủ phủ điều)", "basisSpread": 0.0, "description": "Điều thô vườn Bình Phước thu mua tại nông hộ"},
        {"id": "dongnai", "name": "Đồng Nai", "basisSpread": -400.0, "description": "Điều thô Đồng Nai"},
        {"id": "gialai", "name": "Gia Lai / Tây Nguyên", "basisSpread": -800.0, "description": "Điều Tây Nguyên, chiết khấu vận chuyển"},
    ],
    "SUGARCANE": [
        {"id": "all", "name": "Miền Trung & TNB (Bình quân)", "basisSpread": 0.0, "description": "Giá mía nguyên liệu bình quân"},
        {"id": "phuyen", "name": "Phú Yên (Nhà máy đường)", "basisSpread": 0.0, "description": "Mía 10 CCS tại Nhà máy đường KCP Phú Yên"},
        {"id": "khanhhoa", "name": "Khánh Hòa / Tây Ninh", "basisSpread": -10000.0, "description": "Mía nguyên liệu phụ cận"},
    ]
}

def get_forecast_dashboard(
    db: Session, commodity_id: int = 2, model_name: str = "LSTM", days: int = 10, region: str = None
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

    # Calculate Regional Basis Spread
    regions_list = COMMODITY_REGIONS.get(commodity.code, [
        {"id": "all", "name": "Vùng chuẩn (Bình quân)", "basisSpread": 0.0, "description": "Giá tham chiếu chuẩn"}
    ])
    matched_region = regions_list[0]
    if region:
        for r_item in regions_list:
            if r_item["id"].lower() == region.lower():
                matched_region = r_item
                break
    spread = float(matched_region.get("basisSpread", 0.0))

    forecast_data = []

    # Add historical points with regional spread
    for p in history:
        p_val = max(0.0, round(float(p.price) + spread, 2))
        forecast_data.append(
            ForecastPointResponse(
                date=p.record_date.strftime("%d/%m"),
                actualPrice=p_val,
                predictedPrice=p_val,
                lowerCI=p_val,
                upperCI=p_val,
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
            pred_val = max(0.0, round(float(f.predicted_price) + spread, 2))
            lower_val = max(0.0, round(float(f.lower_ci) + spread, 2))
            upper_val = max(0.0, round(float(f.upper_ci) + spread, 2))
            forecast_data.append(
                ForecastPointResponse(
                    date=f.forecast_date.isoformat(),
                    predictedPrice=pred_val,
                    lowerCI=lower_val,
                    upperCI=upper_val,
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
        training=training,
        availableRegions=[RegionInfo(**r) for r in regions_list],
        selectedRegion=matched_region["id"]
    )

