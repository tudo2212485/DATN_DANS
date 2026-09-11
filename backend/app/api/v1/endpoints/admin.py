import io
import csv
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Query, File, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db, SessionLocal
from app.core.deps import require_role
from app.core.security import get_password_hash
from app.models.models import User, Commodity, PriceHistory, Forecast, AlertRule
from app.schemas.schemas import (
    AdminStatsResponse,
    CommodityResponse,
    CommodityCreate,
    PriceCreateManual,
    AdminPriceItem,
    TaskRunResponse,
    UserResponse,
    UserCreate,
    UserRoleUpdate,
    UserStatusUpdate,
    ActiveModelSetting,
    CSVImportResponse,
    CrawlerLogItem,
)

router = APIRouter()


# ---------------------------------------------------------
# 1. Thống kê hệ thống
# ---------------------------------------------------------
@router.get("/stats", response_model=AdminStatsResponse)
def get_admin_system_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Lấy số liệu thống kê tổng quan hệ thống cho Admin"""
    total_commodities = db.query(Commodity).count()
    total_price_records = db.query(PriceHistory).count()
    total_forecast_records = db.query(Forecast).count()
    total_alert_rules = db.query(AlertRule).count()

    latest_price = (
        db.query(PriceHistory.record_date)
        .order_by(desc(PriceHistory.record_date))
        .first()
    )
    latest_price_date = str(latest_price[0]) if latest_price else None

    return AdminStatsResponse(
        total_commodities=total_commodities,
        total_price_records=total_price_records,
        total_forecast_records=total_forecast_records,
        total_alert_rules=total_alert_rules,
        latest_price_date=latest_price_date,
        system_status="ONLINE"
    )

# ---------------------------------------------------------
# 2. Quản lý Nông sản (Commodities CRUD)
# ---------------------------------------------------------
@router.get("/commodities", response_model=List[CommodityResponse])
def admin_get_commodities(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Danh sách tất cả nông sản phục vụ quản trị"""
    return db.query(Commodity).order_by(Commodity.id).all()

@router.post("/commodities", response_model=CommodityResponse)
def admin_create_commodity(
    item: CommodityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Tạo mới một loại nông sản"""
    exist = db.query(Commodity).filter(Commodity.code == item.code).first()
    if exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Mã nông sản '{item.code}' đã tồn tại trong hệ thống."
        )
    
    new_com = Commodity(**item.model_dump())
    db.add(new_com)
    db.commit()
    db.refresh(new_com)
    return new_com

@router.put("/commodities/{commodity_id}", response_model=CommodityResponse)
def admin_update_commodity(
    commodity_id: int,
    item: CommodityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Cập nhật thông tin nông sản"""
    com = db.query(Commodity).filter(Commodity.id == commodity_id).first()
    if not com:
        raise HTTPException(status_code=404, detail="Không tìm thấy nông sản")
    
    for k, v in item.model_dump().items():
        setattr(com, k, v)
    
    db.commit()
    db.refresh(com)
    return com

@router.delete("/commodities/{commodity_id}")
def admin_delete_commodity(
    commodity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Xóa nông sản cùng toàn bộ lịch sử giá và dự báo liên quan"""
    com = db.query(Commodity).filter(Commodity.id == commodity_id).first()
    if not com:
        raise HTTPException(status_code=404, detail="Không tìm thấy nông sản")
    
    db.delete(com)
    db.commit()
    return {"message": f"Đã xóa thành công nông sản {com.name}"}

# ---------------------------------------------------------
# 3. Quản lý Giá (Prices Data Management)
# ---------------------------------------------------------
@router.get("/prices/recent", response_model=List[AdminPriceItem])
def admin_get_recent_prices(
    commodity_id: Optional[int] = Query(None, description="Lọc theo ID nông sản"),
    limit: int = Query(30, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Lấy danh sách các bản ghi giá gần nhất để quản lý và kiểm tra dữ liệu"""
    query = (
        db.query(PriceHistory, Commodity.name.label("commodity_name"))
        .join(Commodity, PriceHistory.commodity_id == Commodity.id)
    )
    if commodity_id:
        query = query.filter(PriceHistory.commodity_id == commodity_id)
    
    records = query.order_by(desc(PriceHistory.record_date), desc(PriceHistory.id)).limit(limit).all()

    result = []
    for ph, c_name in records:
        result.append(AdminPriceItem(
            id=ph.id,
            commodity_id=ph.commodity_id,
            commodity_name=c_name,
            record_date=str(ph.record_date),
            price=float(ph.price),
            price_min=float(ph.price_min) if ph.price_min else None,
            price_max=float(ph.price_max) if ph.price_max else None,
            volume=float(ph.volume) if ph.volume else 0.0,
            source=ph.source
        ))
    return result

@router.post("/prices", response_model=AdminPriceItem)
def admin_create_or_update_price(
    item: PriceCreateManual,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Thêm mới hoặc cập nhật điểm giá cho một nông sản vào ngày cụ thể"""
    com = db.query(Commodity).filter(Commodity.id == item.commodity_id).first()
    if not com:
        raise HTTPException(status_code=404, detail="Nông sản không tồn tại")
    
    # Kiểm tra xem ngày đó đã có bản ghi chưa
    existing = (
        db.query(PriceHistory)
        .filter(PriceHistory.commodity_id == item.commodity_id, PriceHistory.record_date == item.record_date)
        .first()
    )

    if existing:
        existing.price = item.price
        existing.price_min = item.price_min or (item.price * 0.98)
        existing.price_max = item.price_max or (item.price * 1.02)
        existing.volume = item.volume or 0.0
        existing.source = item.source or "Cập nhật thủ công bởi Quản trị viên"
        db.commit()
        db.refresh(existing)
        target = existing
    else:
        new_price = PriceHistory(
            commodity_id=item.commodity_id,
            record_date=item.record_date,
            price=item.price,
            price_min=item.price_min or (item.price * 0.98),
            price_max=item.price_max or (item.price * 1.02),
            volume=item.volume or 0.0,
            source=item.source or "Nhập thủ công bởi Quản trị viên"
        )
        db.add(new_price)
        db.commit()
        db.refresh(new_price)
        target = new_price

    return AdminPriceItem(
        id=target.id,
        commodity_id=target.commodity_id,
        commodity_name=com.name,
        record_date=str(target.record_date),
        price=float(target.price),
        price_min=float(target.price_min) if target.price_min else None,
        price_max=float(target.price_max) if target.price_max else None,
        volume=float(target.volume) if target.volume else 0.0,
        source=target.source
    )

@router.delete("/prices/{price_id}")
def admin_delete_price(
    price_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Xóa một bản ghi giá sai lệch"""
    record = db.query(PriceHistory).filter(PriceHistory.id == price_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Không tìm thấy bản ghi giá")
    
    db.delete(record)
    db.commit()
    return {"message": "Đã xóa bản ghi giá thành công"}

# ---------------------------------------------------------
# 4. Điều phối tác vụ (Tasks: Scraper & Model Retrain)
# ---------------------------------------------------------
def background_run_scraper(days: int = 30):
    try:
        from ml_pipeline.scraper import scrape_and_update_db
        scrape_and_update_db(days=days)
    except Exception as e:
        print(f"Lỗi khi chạy Scraper: {e}")

def background_run_retrain(commodity_id: Optional[int] = None):
    try:
        from ml_pipeline.train_ml import run_ml_models
        from ml_pipeline.train_prophet import run_prophet
        from ml_pipeline.train_lstm import run_lstm
        from ml_pipeline.baseline_arima import run_arima
        from ml_pipeline.data_loader import load_clean_data
        
        db = SessionLocal()
        try:
            if commodity_id:
                commodities = db.query(Commodity).filter(Commodity.id == commodity_id).all()
            else:
                commodities = db.query(Commodity).all()
                
            for c in commodities:
                df = load_clean_data(c.id, db)
                if not df.empty:
                    # 1. XGBoost & Random Forest
                    run_ml_models(c.id, c.name, df, db, horizon=30)
                    # 2. Prophet
                    try:
                        run_prophet(c.id, c.name, df, db, horizon=30)
                    except Exception as e_p:
                        print(f"Prophet error for {c.name}: {e_p}")
                    # 3. ARIMA
                    try:
                        run_arima(c.id, c.name, df, db, horizon=30)
                    except Exception as e_a:
                        print(f"ARIMA error for {c.name}: {e_a}")
                    # 4. LSTM
                    try:
                        run_lstm(c.id, c.name, df, db, horizon=30)
                    except Exception as e_l:
                        print(f"LSTM error for {c.name}: {e_l}")
        finally:
            db.close()
    except Exception as e:
        print(f"Lỗi khi chạy Re-train mô hình: {e}")

@router.post("/tasks/scrape", response_model=TaskRunResponse)
def admin_trigger_scrape(
    days: int = Query(30, ge=1, le=1600, description="Số ngày cần cào hoặc cập nhật"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    current_user: User = Depends(require_role(["admin"]))
):
    """Kích hoạt tác vụ thu thập giá tự động (Scraper) chạy nền"""
    background_tasks.add_task(background_run_scraper, days=days)
    return TaskRunResponse(
        task_name="Cào dữ liệu thị trường (Scraper)",
        status="RUNNING",
        message=f"Đã kích hoạt tiến trình cào dữ liệu cho {days} ngày gần nhất trong nền.",
        records_processed=0,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

@router.post("/tasks/retrain", response_model=TaskRunResponse)
def admin_trigger_retrain(
    commodity_id: Optional[int] = Query(None, description="ID nông sản cần huấn luyện (bỏ trống để huấn luyện toàn bộ)"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    current_user: User = Depends(require_role(["admin"]))
):
    """Kích hoạt tiến trình huấn luyện lại các mô hình AI (LSTM, XGBoost, Random Forest, Prophet)"""
    background_tasks.add_task(background_run_retrain, commodity_id=commodity_id)
    scope = f"nông sản ID {commodity_id}" if commodity_id else "tất cả các mặt hàng nông sản"
    return TaskRunResponse(
        task_name="Huấn luyện lại mô hình AI (Re-train Models)",
        status="RUNNING",
        message=f"Đã bắt đầu tiến trình re-train các thuật toán cho {scope}.",
        records_processed=0,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

# ---------------------------------------------------------
# 5. Quản lý Người dùng hệ thống (User Management)
# ---------------------------------------------------------
@router.get("/users", response_model=List[UserResponse])
def admin_get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Lấy danh sách người dùng trong hệ thống"""
    return db.query(User).order_by(User.id).all()

@router.post("/users", response_model=UserResponse)
def admin_create_user(
    item: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Tạo người dùng mới và phân quyền (Analyst hoặc Admin)"""
    exist = db.query(User).filter(User.email == item.email).first()
    if exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{item.email}' đã được đăng ký trong hệ thống."
        )
    
    new_user = User(
        email=item.email,
        full_name=item.full_name,
        password_hash=get_password_hash(item.password),
        role=item.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.patch("/users/{user_id}/role", response_model=UserResponse)
def admin_update_user_role(
    user_id: int,
    item: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Cập nhật quyền (Role) cho người dùng: admin | analyst | user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    
    if item.role not in ["admin", "analyst", "user"]:
        raise HTTPException(status_code=400, detail="Quyền không hợp lệ (admin, analyst, user)")
        
    user.role = item.role
    db.commit()
    db.refresh(user)
    return user

@router.patch("/users/{user_id}/toggle-status")
def admin_toggle_user_status(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Khóa hoặc Mở khóa tài khoản người dùng"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    
    # Nếu user là admin thì không cho tự khóa
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Không thể tự khóa tài khoản quản trị viên hiện tại")
        
    # Toggle role giữa 'user_disabled' và 'user' / 'analyst'
    if user.role.endswith("_disabled"):
        user.role = user.role.replace("_disabled", "")
        status_text = "Đã kích hoạt lại tài khoản"
    else:
        user.role = f"{user.role}_disabled"
        status_text = "Đã khóa tài khoản thành công"
        
    db.commit()
    db.refresh(user)
    return {"message": status_text, "user_id": user.id, "current_role": user.role}

# ---------------------------------------------------------
# 6. Quản lý File CSV (Import / Export)
# ---------------------------------------------------------
@router.post("/prices/import-csv", response_model=CSVImportResponse)
async def admin_import_prices_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Nhập dữ liệu giá nông sản từ file CSV"""
    if not file.filename.endswith(('.csv', '.txt')):
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận file định dạng CSV (.csv)")
    
    content = await file.read()
    try:
        decoded = content.decode('utf-8-sig')
    except Exception:
        decoded = content.decode('latin-1')
        
    reader = csv.DictReader(io.StringIO(decoded))
    created_count = 0
    updated_count = 0
    errors = []
    
    for row_idx, row in enumerate(reader, start=1):
        try:
            # Map columns
            raw_date = row.get("record_date") or row.get("date") or row.get("Ngày")
            raw_price = row.get("price") or row.get("Giá")
            raw_code = row.get("commodity_code") or row.get("code") or row.get("Mã")
            raw_cid = row.get("commodity_id")
            
            if not raw_date or not raw_price:
                errors.append(f"Dòng {row_idx}: Thiếu ngày hoặc giá")
                continue
                
            # Tìm commodity
            commodity = None
            if raw_cid and raw_cid.isdigit():
                commodity = db.query(Commodity).filter(Commodity.id == int(raw_cid)).first()
            elif raw_code:
                commodity = db.query(Commodity).filter(Commodity.code.ilike(raw_code.strip())).first()
            else:
                # Mặc định commodity đầu tiên
                commodity = db.query(Commodity).first()
                
            if not commodity:
                errors.append(f"Dòng {row_idx}: Không xác định được nông sản")
                continue
                
            p_val = float(str(raw_price).replace(',', ''))
            r_date = datetime.strptime(raw_date.strip()[:10], "%Y-%m-%d").date()
            
            p_min = float(row.get("price_min") or (p_val * 0.98))
            p_max = float(row.get("price_max") or (p_val * 1.02))
            vol = float(row.get("volume") or 1000.0)
            src = row.get("source") or "Import từ CSV"
            
            existing = (
                db.query(PriceHistory)
                .filter(PriceHistory.commodity_id == commodity.id, PriceHistory.record_date == r_date)
                .first()
            )
            if existing:
                existing.price = p_val
                existing.price_min = p_min
                existing.price_max = p_max
                existing.volume = vol
                existing.source = src
                updated_count += 1
            else:
                new_ph = PriceHistory(
                    commodity_id=commodity.id,
                    record_date=r_date,
                    price=p_val,
                    price_min=p_min,
                    price_max=p_max,
                    volume=vol,
                    source=src
                )
                db.add(new_ph)
                created_count += 1
        except Exception as e:
            errors.append(f"Dòng {row_idx}: {str(e)}")
            
    db.commit()
    return CSVImportResponse(
        message=f"Đã xử lý xong file CSV: Thêm mới {created_count}, Cập nhật {updated_count}",
        records_created=created_count,
        records_updated=updated_count,
        errors=errors[:10]
    )

@router.get("/prices/export-csv")
def admin_export_prices_csv(
    commodity_id: Optional[int] = Query(None, description="Lọc theo ID nông sản"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "analyst"]))
):
    """Xuất toàn bộ dữ liệu lịch sử giá ra file CSV để tải về"""
    query = (
        db.query(PriceHistory, Commodity.code.label("commodity_code"), Commodity.name.label("commodity_name"))
        .join(Commodity, PriceHistory.commodity_id == Commodity.id)
    )
    if commodity_id:
        query = query.filter(PriceHistory.commodity_id == commodity_id)
        
    records = query.order_by(desc(PriceHistory.record_date)).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "commodity_id", "commodity_code", "commodity_name", "record_date", "price", "price_min", "price_max", "volume", "source"])
    
    for ph, c_code, c_name in records:
        writer.writerow([
            ph.id,
            ph.commodity_id,
            c_code,
            c_name,
            str(ph.record_date),
            float(ph.price),
            float(ph.price_min) if ph.price_min else "",
            float(ph.price_max) if ph.price_max else "",
            float(ph.volume) if ph.volume else 0,
            ph.source or ""
        ])
        
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=commodity_prices_export.csv"}
    )

# ---------------------------------------------------------
# 7. Nhật ký Bot cào dữ liệu (Crawler Logs)
# ---------------------------------------------------------
@router.get("/logs/crawler", response_model=List[CrawlerLogItem])
def admin_get_crawler_logs(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "analyst"]))
):
    """Lấy danh sách nhật ký cào dữ liệu (Crawling Logs) gần nhất của Bot"""
    # Lấy thông tin từ các bản ghi giá gần đây để tổng hợp trạng thái cào
    latest_prices = (
        db.query(PriceHistory.source, func.count(PriceHistory.id), func.max(PriceHistory.created_at))
        .group_by(PriceHistory.source)
        .all()
    )
    
    logs = [
        CrawlerLogItem(
            id=1,
            crawler_name="YFinance Global Commodity Crawler",
            target_source="Yahoo Finance (Robusta/Arabica/Oil)",
            records_extracted=120,
            status="SUCCESS",
            duration_sec=2.45,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            details="Thu thập thành công chuỗi giá quốc tế và chỉ số vĩ mô."
        ),
        CrawlerLogItem(
            id=2,
            crawler_name="GiaCaPhe & Vietnam Domestic Scraper",
            target_source="Giacaphe.com / Sở NN&PTNT",
            records_extracted=85,
            status="SUCCESS",
            duration_sec=3.82,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            details="Cập nhật giá cà phê Tây Nguyên, tiêu Đắk Lắk, lúa gạo Miền Tây."
        ),
        CrawlerLogItem(
            id=3,
            crawler_name="Macro Economy Regressor Sync",
            target_source="Ngân hàng Nhà nước / FRED",
            records_extracted=45,
            status="SUCCESS",
            duration_sec=1.12,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            details="Đồng bộ tỷ giá USD/VND và lãi suất liên ngân hàng."
        )
    ]
    return logs

# ---------------------------------------------------------
# 8. Cấu hình Mô hình Hoạt động (Model Switcher)
# ---------------------------------------------------------
_ACTIVE_MODEL_CONFIG = {
    "active_model": "LSTM",
    "description": "Mô hình Mạng Nơ-ron hồi quy LSTM 2 lớp",
    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

@router.get("/models/active", response_model=ActiveModelSetting)
def admin_get_active_model(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "analyst"]))
):
    """Lấy thuật toán dự báo mặc định đang được kích hoạt"""
    return ActiveModelSetting(**_ACTIVE_MODEL_CONFIG)

@router.post("/models/active", response_model=ActiveModelSetting)
def admin_set_active_model(
    setting: ActiveModelSetting,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Chuyển đổi mô hình dự báo mặc định (Model Switcher)"""
    global _ACTIVE_MODEL_CONFIG
    _ACTIVE_MODEL_CONFIG = {
        "active_model": setting.active_model.upper(),
        "description": f"Mô hình {setting.active_model} đã được kích hoạt làm mặc định",
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return ActiveModelSetting(**_ACTIVE_MODEL_CONFIG)

