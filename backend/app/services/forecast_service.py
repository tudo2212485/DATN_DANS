from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.models.models import Commodity, Forecast, TrainingRun
from app.services.history_service import fingerprint, training_context
import json
from datetime import date
from app.schemas.schemas import (
    ForecastDashboardResponse,
    ForecastPointResponse,
    LocationContextResponse,
    ModelMetricsResponse,
    CommodityResponse,
    RegionInfo,
)
from app.services.regional_pricing_service import (
    normalize_province_code,
    resolve_commodity_location_context,
)
from fastapi import HTTPException
from typing import List, Optional

def get_forecast_comparison(db: Session, commodity_id: int) -> List[ModelMetricsResponse]:
    commodity = db.query(Commodity).filter(Commodity.id == commodity_id).first()
    if not commodity:
        raise HTTPException(status_code=404, detail="Không tìm thấy nông sản")
        
    context = training_context(db, commodity)
    latest_run = db.query(func.max(Forecast.training_run_id)).filter(Forecast.commodity_id == commodity_id).scalar()
    run = db.get(TrainingRun, latest_run) if latest_run else None
    if latest_run is not None:
        if not run or run.dataset_hash != fingerprint(context["rows"]):
            return []
        models = db.query(Forecast.model_name).filter(Forecast.commodity_id == commodity_id, Forecast.training_run_id == latest_run).distinct().all()
    else:
        if not context["quality"]["ready"]:
            return []
        models = db.query(Forecast.model_name).filter(Forecast.commodity_id == commodity_id).distinct().all()
    
    run_meta = json.loads(run.metadata_json) if run and run.metadata_json else {}
    model_meta_map = run_meta.get("model_metrics") or {}

    result = []
    for (m_name,) in models:
        q = db.query(Forecast).filter(Forecast.commodity_id == commodity_id, Forecast.model_name == m_name)
        if latest_run is not None:
            q = q.filter(Forecast.training_run_id == latest_run)
        f = q.order_by(desc(Forecast.training_date), desc(Forecast.forecast_date)).first()
        if f and f.mae is not None:
            mape_val = float(f.mape) if f.mape is not None else 0.0
            m_extra = model_meta_map.get(m_name) or {}
            acc_val = m_extra.get("accuracy")
            if acc_val is None:
                acc_val = round(max(0.0, 100.0 - mape_val), 2)
            picp_val = m_extra.get("picp_95")
            result.append(
                ModelMetricsResponse(
                    modelName=m_name,
                    mae=float(f.mae),
                    rmse=float(f.rmse) if f.rmse is not None else 0.0,
                    mape=mape_val,
                    r2=float(f.r2) if f.r2 is not None else 0.0,
                    accuracy=float(acc_val),
                    picp95=float(picp_val) if picp_val is not None else None,
                    trainDate=f.training_date.strftime("%d/%m/%Y") if f.training_date else "N/A"
                )
            )
    return sorted(result, key=lambda m: (m.mape, m.rmse))


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
    db: Session,
    commodity_id: int = 2,
    model_name: str = "LSTM",
    days: int = 10,
    region: Optional[str] = None,
    province: Optional[str] = None,
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

    # Calculate Regional Basis Spread (prioritize Location-Aware `?province=`, preserve legacy `?region=`)
    regions_list = COMMODITY_REGIONS.get(commodity.code, [
        {"id": "all", "name": "Vùng chuẩn (Bình quân)", "basisSpread": 0.0, "description": "Giá tham chiếu chuẩn"}
    ])
    matched_region = regions_list[0]
    norm_prov = normalize_province_code(province)
    loc = resolve_commodity_location_context(db, commodity, province if norm_prov else None)

    if norm_prov:
        if loc.get("pricing_mode") == "direct" and loc.get("latest_direct_price") and history:
            spread = round(float(loc["latest_direct_price"]) - float(history[-1].price), 2)
        else:
            spread = float(loc.get("basis_offset", 0.0))
        selected_region_id = loc["province_code"]
    else:
        if region:
            for r_item in regions_list:
                if r_item["id"].lower() == region.lower():
                    matched_region = r_item
                    break
        spread = float(matched_region.get("basisSpread", 0.0))
        selected_region_id = matched_region["id"]

    forecast_data = []

    # Add historical points with regional spread (ISO YYYY-MM-DD for accurate tooltip & date formatting)
    for p in history:
        p_val = max(0.0, round(float(p.price) + spread, 2))
        forecast_data.append(
            ForecastPointResponse(
                date=p.record_date.strftime("%Y-%m-%d"),
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
        latest_run_id = db.query(func.max(TrainingRun.id)).filter(TrainingRun.commodity_id == commodity_id).scalar()
        run = db.get(TrainingRun, first_f.training_run_id or latest_run_id) if (first_f.training_run_id or latest_run_id) else None
        if (first_f.training_run_id or latest_run_id) and (not run or run.dataset_hash != fingerprint(context["rows"])):
            raise HTTPException(409, "Dữ liệu đã thay đổi hoặc dự báo cũ chưa có nguồn đầu vào được xác minh. Hãy thu thập đủ lịch sử và huấn luyện lại.")
        if run:
            training = json.loads(run.metadata_json)
            training.pop("snapshot", None)
            trained_at_iso = run.created_at.isoformat()
            run_id_val = run.id
            ds_hash_val = run.dataset_hash
        else:
            training = dict(
                quality,
                commodity_unit=commodity.unit,
                test_start=str(history[-min(10, len(history))].record_date) if history else None,
                test_end=str(history[-1].record_date) if history else None,
                test_count=min(10, len(history)),
                train_end=str(history[-min(10, len(history))].record_date) if history else None,
                filled_days=0,
                baseline={"mae": float(first_f.mae or 0), "rmse": float(first_f.rmse or 0), "mape": float(first_f.mape or 0), "r2": float(first_f.r2 or 0)},
                evaluation="Dự báo nhiều bước từ mốc lịch sử gần nhất.",
            )
            trained_at_iso = first_f.created_at.isoformat() if first_f.created_at else date.today().isoformat()
            run_id_val = 0
            ds_hash_val = fingerprint(context["rows"])
        model_extra_map = (training.get("model_metrics") or {}) if isinstance(training, dict) else {}
        matched_extra = {}
        for k_m, v_m in model_extra_map.items():
            if k_m.lower() == model_name.lower():
                matched_extra = v_m or {}
                break
        picp_val = matched_extra.get("picp_95")
        if picp_val is not None:
            ci_note = (
                f"Khoảng tin cậy 95% mở rộng theo chân trời (√h), hiệu chỉnh Conformal trên tập huấn luyện; "
                f"độ bao phủ thực nghiệm trên tập kiểm thử (PICP): {float(picp_val):.1f}%."
            )
        elif context["cadence"] == "periodic":
            ci_note = "Dải ước lượng ±1,96 RMSE theo kỳ; chuỗi mía dùng giá mua trong báo cáo."
        elif context["cadence"] == "irregular":
            ci_note = "Dải ước lượng ±1,96 RMSE theo mốc công bố AGROINFO."
        else:
            ci_note = "Dải ước lượng ±1,96 RMSE mở rộng theo chân trời."

        training.update(run_id=run_id_val, dataset_hash=ds_hash_val, trained_at=trained_at_iso,
                        stale_days=max(0, (date.today() - history[-1].record_date).days) if history else 0,
                        interval_note=ci_note)
        if first_f.mae is not None:
            mape_val = float(first_f.mape) if first_f.mape is not None else 0.0
            acc_val = matched_extra.get("accuracy")
            if acc_val is None:
                acc_val = round(max(0.0, 100.0 - mape_val), 2)
            latest_metrics = ModelMetricsResponse(
                modelName=model_name,
                mae=float(first_f.mae),
                rmse=float(first_f.rmse) if first_f.rmse is not None else 0.0,
                mape=mape_val,
                r2=float(first_f.r2) if first_f.r2 is not None else 0.0,
                accuracy=float(acc_val),
                picp95=float(picp_val) if picp_val is not None else None,
                trainDate=first_f.training_date.strftime("%d/%m/%Y") if first_f.training_date else "N/A"
            )

        for i, f in enumerate(forecast_rows):
            pred_val = max(0.0, round(float(f.predicted_price) + spread, 2))
            lower_val = max(0.0, min(pred_val, round(float(f.lower_ci) + spread, 2)))
            upper_val = max(pred_val, round(float(f.upper_ci) + spread, 2))
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
        selectedRegion=selected_region_id,
        location_context=LocationContextResponse(**{k: v for k, v in loc.items() if k in LocationContextResponse.model_fields}),
    )

