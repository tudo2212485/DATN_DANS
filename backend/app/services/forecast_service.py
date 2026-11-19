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
        {"id": "all", "name": "Huyện Cư M'gar, Đắk Lắk (Tại vườn)", "basisSpread": 0.0, "description": "Giá cà phê nhân xô hộ dân bán ra tại vườn huyện Cư M'gar"},
        {"id": "buonho", "name": "Thị xã Buôn Hồ, Đắk Lắk (Tại vườn)", "basisSpread": -100.0, "description": "Giá thu mua tại sân phơi nông hộ thị xã Buôn Hồ, Krông Năng (-100 đ/kg)"},
        {"id": "dilinh", "name": "Huyện Di Linh, Lâm Đồng (Tại vườn)", "basisSpread": -800.0, "description": "Giá hộ trồng bán tại vườn huyện Di Linh, Bảo Lâm (-800 đ/kg)"},
        {"id": "chuprong", "name": "Huyện Chư Prông, Gia Lai (Tại vườn)", "basisSpread": -300.0, "description": "Giá thu mua tại vườn hộ dân huyện Chư Prông, Ia Grai (-300 đ/kg)"},
        {"id": "dakmil", "name": "Huyện Đắk Mil, Đắk Nông (Tại vườn)", "basisSpread": 200.0, "description": "Cà phê nhân xô hạt chắc bán tại vườn huyện Đắk Mil (+200 đ/kg)"},
    ],
    "PEPPER_BLACK": [
        {"id": "all", "name": "Huyện Chư Sê, Gia Lai (Tại vườn)", "basisSpread": 0.0, "description": "Giá tiêu đen phơi khô hộ dân bán tại vườn huyện Chư Sê"},
        {"id": "cukuin", "name": "Huyện Cư Kuin, Đắk Lắk (Tại vườn)", "basisSpread": 200.0, "description": "Giá tiêu đen bán tại hộ trồng huyện Cư Kuin, Ea H'leo (+200 đ/kg)"},
        {"id": "chauduc", "name": "Huyện Châu Đức, Bà Rịa - Vũng Tàu (Tại vườn)", "basisSpread": 1500.0, "description": "Tiêu hạt nặng dung trọng cao bán tại nhà vườn huyện Châu Đức (+1.500 đ/kg)"},
        {"id": "locninh", "name": "Huyện Lộc Ninh, Bình Phước (Tại vườn)", "basisSpread": -500.0, "description": "Giá tiêu đen thu mua tại vườn huyện Lộc Ninh, Bù Đốp (-500 đ/kg)"},
        {"id": "daksong", "name": "Huyện Đắk Song, Đắk Nông (Tại vườn)", "basisSpread": 100.0, "description": "Giá tiêu khô bán tại vườn nông hộ huyện Đắk Song (+100 đ/kg)"},
    ],
    "RICE_IR504": [
        {"id": "all", "name": "Huyện Châu Phú, An Giang (Tại ruộng)", "basisSpread": 0.0, "description": "Giá lúa tươi thương lái cân trực tiếp tại bờ ruộng huyện Châu Phú"},
        {"id": "thoaison", "name": "Huyện Thoại Sơn, An Giang (Tại ruộng)", "basisSpread": 50.0, "description": "Giá lúa tươi cắt tại ruộng huyện Thoại Sơn (+50 đ/kg)"},
        {"id": "thapmuoi", "name": "Huyện Tháp Mười, Đồng Tháp (Tại ruộng)", "basisSpread": 150.0, "description": "Giá lúa tươi bán tại bờ ruộng huyện Tháp Mười, Tam Nông (+150 đ/kg)"},
        {"id": "tanhiep", "name": "Huyện Tân Hiệp, Kiên Giang (Tại ruộng)", "basisSpread": -150.0, "description": "Giá lúa tươi gặt bán tại ruộng huyện Tân Hiệp, Hòn Đất (-150 đ/kg)"},
        {"id": "caibe", "name": "Huyện Cái Bè, Tiền Giang (Tại ruộng)", "basisSpread": 100.0, "description": "Giá lúa tươi nông dân bán tại ruộng huyện Cái Bè, Cai Lậy (+100 đ/kg)"},
    ],
    "STRAWBERRY": [
        {"id": "all", "name": "Phường 8, TP. Đà Lạt (Tại vườn)", "basisSpread": 0.0, "description": "Giá dâu tây tươi hái bán tại nhà vườn Phường 8, Phường 7 - Đà Lạt"},
        {"id": "lacduong", "name": "Huyện Lạc Dương, Lâm Đồng (Tại vườn)", "basisSpread": -3000.0, "description": "Giá dâu tây bán tại nhà vườn khu vực Langbiang - Lạc Dương (-3.000 đ/kg)"},
        {"id": "mocchau", "name": "Huyện Mộc Châu, Sơn La (Tại vườn)", "basisSpread": -15000.0, "description": "Giá dâu tây hái tại vườn xã Đông Sang, Mường Sang - Mộc Châu (-15.000 đ/kg)"},
    ],
    "SWEET_POTATO": [
        {"id": "all", "name": "Huyện Bình Tân, Vĩnh Long (Tại ruộng)", "basisSpread": 0.0, "description": "Giá khoai lang tím nhổ bán tại ruộng xã Tân Thành, Thành Trung - Bình Tân"},
        {"id": "chauthanh_dt", "name": "Huyện Châu Thành, Đồng Tháp (Tại ruộng)", "basisSpread": -400.0, "description": "Giá khoai lang thu mua tại ruộng huyện Châu Thành, Lai Vung (-400 đ/kg)"},
        {"id": "chauthanha_hg", "name": "Huyện Châu Thành A, Hậu Giang (Tại ruộng)", "basisSpread": -500.0, "description": "Giá khoai lang bán tại ruộng hộ dân huyện Châu Thành A (-500 đ/kg)"},
    ],
    "POTATO": [
        {"id": "all", "name": "Phường 7 (Thái Phiên), Đà Lạt (Tại vườn)", "basisSpread": 0.0, "description": "Giá khoai tây hồng loại 1 bán tại vườn làng hoa Thái Phiên, Đà Lạt"},
        {"id": "ductrong", "name": "Huyện Đức Trọng, Lâm Đồng (Tại vườn)", "basisSpread": -800.0, "description": "Giá khoai tây nhổ tại vườn xã Hiệp Thạnh, Liên Nghĩa - Đức Trọng (-800 đ/kg)"},
        {"id": "donduong", "name": "Huyện Đơn Dương, Lâm Đồng (Tại vườn)", "basisSpread": -1000.0, "description": "Giá khoai tây bán tại vườn xã Lạc Xuân, Thạnh Mỹ - Đơn Dương (-1.000 đ/kg)"},
    ],
    "CASHEW_NUT": [
        {"id": "all", "name": "Huyện Bù Đăng, Bình Phước (Tại vườn)", "basisSpread": 0.0, "description": "Giá hạt điều thô hộ dân bán trực tiếp tại vườn huyện Bù Đăng"},
        {"id": "phurieng", "name": "Huyện Phú Riềng, Bình Phước (Tại vườn)", "basisSpread": 200.0, "description": "Giá điều thô phơi ráo bán tại vườn huyện Phú Riềng, Đồng Phú (+200 đ/kg)"},
        {"id": "dinhquan", "name": "Huyện Định Quán, Đồng Nai (Tại vườn)", "basisSpread": -400.0, "description": "Giá điều tươi thu mua tại vườn hộ dân huyện Định Quán, Xuân Lộc (-400 đ/kg)"},
        {"id": "krongpa", "name": "Huyện Krông Pa, Gia Lai (Tại vườn)", "basisSpread": -800.0, "description": "Giá điều thô bán tại vườn nông hộ huyện Krông Pa (-800 đ/kg)"},
    ],
    "SUGARCANE": [
        {"id": "all", "name": "Huyện Tây Hòa, Phú Yên (Tại ruộng)", "basisSpread": 0.0, "description": "Giá mía 10 CCS thu mua tại ruộng huyện Tây Hòa, Sông Hinh - Phú Yên"},
        {"id": "tanchau", "name": "Huyện Tân Châu, Tây Ninh (Tại ruộng)", "basisSpread": -10000.0, "description": "Giá mía nguyên liệu bán tại ruộng huyện Tân Châu, Châu Thành (-10.000 đ/tấn)"},
        {"id": "ankhe", "name": "Thị xã An Khê, Gia Lai (Tại ruộng)", "basisSpread": -8000.0, "description": "Giá mía chặt bán tại ruộng khu vực An Khê, Kbang (-8.000 đ/tấn)"},
        {"id": "phunghiep", "name": "Huyện Phụng Hiệp, Hậu Giang (Tại ruộng)", "basisSpread": -15000.0, "description": "Giá mía nguyên liệu bán tại ruộng huyện Phụng Hiệp (-15.000 đ/tấn)"},
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

