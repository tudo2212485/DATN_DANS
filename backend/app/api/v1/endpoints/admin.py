import io
import csv
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Query, File, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime, date
import math

from app.core.database import get_db, SessionLocal
from app.core.deps import require_role
from app.core.security import get_password_hash
from app.models.models import User, Commodity, PriceHistory, Forecast, AlertRule, BackgroundJob, SystemSetting
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

from app.services.job_service import create_job, run_job, job_response, active_model, MODEL_NAMES

router = APIRouter()


# ---------------------------------------------------------
# 1. Thống kê hệ thống
# ---------------------------------------------------------
@router.get("/stats", response_model=AdminStatsResponse)
def get_admin_system_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "analyst"]))
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
    current_user: User = Depends(require_role(["admin", "analyst"]))
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
    offset: int = Query(0, ge=0),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "analyst"]))
):
    """Lấy danh sách các bản ghi giá gần nhất để quản lý và kiểm tra dữ liệu"""
    query = (
        db.query(PriceHistory, Commodity.name.label("commodity_name"))
        .join(Commodity, PriceHistory.commodity_id == Commodity.id)
    )
    if commodity_id:
        query = query.filter(PriceHistory.commodity_id == commodity_id)
    
    if start_date and end_date and start_date > end_date:
        raise HTTPException(400, "Ngày bắt đầu phải trước ngày kết thúc")
    if start_date:
        query = query.filter(PriceHistory.record_date >= start_date)
    if end_date:
        query = query.filter(PriceHistory.record_date <= end_date)
    records = query.order_by(desc(PriceHistory.record_date), desc(PriceHistory.id)).offset(offset).limit(limit).all()

    result = []
    for ph, c_name in records:
        result.append(AdminPriceItem(
            provenance=ph.provenance,
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
        from app.services.history_service import archive_price
        archive_price(db, existing)
        existing.provenance = "reviewed" if item.reviewed else "unverified"
        existing.source_details = None
        existing.price = item.price
        existing.price_min = item.price_min
        existing.price_max = item.price_max
        existing.volume = item.volume or 0.0
        existing.source = item.source or "Cập nhật thủ công bởi Quản trị viên"
        db.commit()
        db.refresh(existing)
        target = existing
    else:
        new_price = PriceHistory(
            provenance="reviewed" if item.reviewed else "unverified",
            commodity_id=item.commodity_id,
            record_date=item.record_date,
            price=item.price,
            price_min=item.price_min,
            price_max=item.price_max,
            volume=item.volume or 0.0,
            source=item.source or "Nhập thủ công bởi Quản trị viên"
        )
        db.add(new_price)
        db.commit()
        db.refresh(new_price)
        target = new_price

    return AdminPriceItem(
        provenance=target.provenance,
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
@router.post("/tasks/scrape", response_model=TaskRunResponse)
def admin_trigger_scrape(background_tasks: BackgroundTasks, days: int = Query(30, ge=1, le=365),
                        commodity_id: Optional[int] = Query(None), start_date: Optional[date] = Query(None),
                        end_date: Optional[date] = Query(None),
                        db: Session = Depends(get_db), current_user: User = Depends(require_role(["admin"]))):
    if bool(start_date) != bool(end_date) or (start_date and (start_date > end_date or end_date > date.today() or (end_date - start_date).days > 1826)):
        raise HTTPException(400, "Cần ngày bắt đầu/kết thúc hợp lệ trong quá khứ, tối đa 5 năm")
    if commodity_id:
        commodity = db.get(Commodity, commodity_id)
        from ml_pipeline.source_catalog import SOURCES
        if not commodity or commodity.code not in SOURCES:
            raise HTTPException(400, "Chưa có nguồn thu thập lịch sử tự động cho nông sản này")
    job = create_job(db, "scrape")
    background_tasks.add_task(run_job, job.id, "scrape", dict(days=days, commodity_id=commodity_id,
                              start_date=start_date, end_date=end_date))
    return job_response(job)


@router.post("/tasks/retrain", response_model=TaskRunResponse)
def admin_trigger_retrain(background_tasks: BackgroundTasks, commodity_id: Optional[int] = Query(None),
                         db: Session = Depends(get_db), current_user: User = Depends(require_role(["admin"]))):
    if commodity_id and not db.get(Commodity, commodity_id):
        raise HTTPException(404, "Không tìm thấy nông sản")
    job = create_job(db, "retrain")
    background_tasks.add_task(run_job, job.id, "retrain", commodity_id)
    return job_response(job)


@router.get("/tasks", response_model=List[TaskRunResponse])
def admin_tasks(kind: Optional[str] = None, db: Session = Depends(get_db),
                current_user: User = Depends(require_role(["admin", "analyst"]))):
    query = db.query(BackgroundJob)
    if kind:
        query = query.filter(BackgroundJob.kind == kind)
    return [job_response(job) for job in query.order_by(BackgroundJob.id.desc()).limit(20).all()]


@router.get("/tasks/{task_id}", response_model=TaskRunResponse)
def admin_task(task_id: int, db: Session = Depends(get_db),
               current_user: User = Depends(require_role(["admin", "analyst"]))):
    job = db.get(BackgroundJob, task_id)
    if not job:
        raise HTTPException(404, "Không tìm thấy tác vụ")
    return job_response(job)

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
    exist = db.query(User).filter(User.email.ilike(item.email.strip())).first()
    if exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{item.email}' đã được đăng ký trong hệ thống."
        )
    
    new_user = User(
        email=item.email.strip().lower(),
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
        
    if user.id == current_user.id and item.role != "admin":
        raise HTTPException(400, "Không thể tự hạ quyền tài khoản quản trị đang đăng nhập")
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
        
    user.is_active = not user.is_active
    # Normalize accounts locked by the previous implementation.
    if user.role.endswith("_disabled"):
        user.role = user.role.removesuffix("_disabled")
        user.is_active = True
    db.commit()
    return {"message": "Đã kích hoạt lại tài khoản" if user.is_active else "Đã khóa tài khoản thành công",
            "user_id": user.id, "current_role": user.role, "is_active": user.is_active}

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
    if not (file.filename or '').lower().endswith(('.csv', '.txt')):
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận file định dạng CSV (.csv)")
    
    content = await file.read(5 * 1024 * 1024 + 1)
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(400, "File CSV tối đa 5 MB")
    try:
        decoded = content.decode('utf-8-sig')
    except Exception:
        decoded = content.decode('latin-1')
        
    reader = csv.DictReader(io.StringIO(decoded))
    created_count = 0
    updated_count = 0
    errors = []
    
    if not reader.fieldnames:
        raise HTTPException(400, "File CSV trống hoặc thiếu dòng tiêu đề")
    for row_idx, row in enumerate(reader, start=2):
        savepoint = db.begin_nested()
        try:
            # Map columns
            raw_date = row.get("record_date") or row.get("date") or row.get("Ngày")
            raw_price = row.get("price") or row.get("Giá")
            raw_code = row.get("commodity_code") or row.get("code") or row.get("Mã")
            raw_cid = row.get("commodity_id")
            
            if not raw_date or not raw_price:
                errors.append(f"Dòng {row_idx}: Thiếu ngày hoặc giá")
                savepoint.rollback()
                continue
                
            # Tìm commodity
            commodity = None
            if raw_cid and raw_cid.isdigit():
                commodity = db.query(Commodity).filter(Commodity.id == int(raw_cid)).first()
            elif raw_code:
                commodity = db.query(Commodity).filter(Commodity.code.ilike(raw_code.strip())).first()
            else:
                commodity = None
                
            if not commodity:
                errors.append(f"Dòng {row_idx}: Không xác định được nông sản")
                savepoint.rollback()
                continue
                
            p_val = float(str(raw_price).replace(',', ''))
            r_date = datetime.strptime(raw_date.strip()[:10], "%Y-%m-%d").date()
            
            p_min = float(row["price_min"]) if row.get("price_min") else None
            p_max = float(row["price_max"]) if row.get("price_max") else None
            vol = float(row.get("volume") or 0.0)
            src = row.get("source") or "Import từ CSV"
            reviewed = str(row.get("reviewed", "false")).strip().lower() in ("true", "1", "yes")
            PriceCreateManual(commodity_id=commodity.id, record_date=r_date, price=p_val,
                              price_min=p_min, price_max=p_max, volume=vol, source=src, reviewed=reviewed)
            
            existing = (
                db.query(PriceHistory)
                .filter(PriceHistory.commodity_id == commodity.id, PriceHistory.record_date == r_date)
                .first()
            )
            if existing:
                from app.services.history_service import archive_price
                archive_price(db, existing)
                existing.provenance = "reviewed" if reviewed else "unverified"
                existing.source_details = None
                existing.price = p_val
                existing.price_min = p_min
                existing.price_max = p_max
                existing.volume = vol
                existing.source = src
            else:
                new_ph = PriceHistory(
                    provenance="reviewed" if reviewed else "unverified",
                    commodity_id=commodity.id,
                    record_date=r_date,
                    price=p_val,
                    price_min=p_min,
                    price_max=p_max,
                    volume=vol,
                    source=src
                )
                db.add(new_ph)
            db.flush()
            savepoint.commit()
            if existing:
                updated_count += 1
            else:
                created_count += 1
        except Exception as e:
            savepoint.rollback()
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
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
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
        
    if start_date and end_date and start_date > end_date:
        raise HTTPException(400, "Khoảng ngày không hợp lệ")
    if start_date:
        query = query.filter(PriceHistory.record_date >= start_date)
    if end_date:
        query = query.filter(PriceHistory.record_date <= end_date)
    records = query.order_by(desc(PriceHistory.record_date)).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "commodity_id", "commodity_code", "commodity_name", "record_date", "price", "price_min", "price_max", "volume", "source", "provenance", "reviewed"])
    
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
            ph.source or "",
            ph.provenance,
            "true" if ph.provenance == "reviewed" else "false"
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
    jobs = db.query(BackgroundJob).filter(BackgroundJob.kind == "scrape").order_by(BackgroundJob.id.desc()).limit(limit).all()
    return [CrawlerLogItem(id=j.id, crawler_name="Thu thập lịch sử nông sản Việt Nam", target_source="Xem chi tiết tác vụ và nguồn từng bản ghi",
                          records_extracted=j.records_processed, status=j.status,
                          duration_sec=max(0, ((j.finished_at or datetime.now()) - j.created_at).total_seconds()),
                          timestamp=j.created_at.isoformat(), details=j.message) for j in jobs]

# ---------------------------------------------------------
# 8. Cấu hình Mô hình Hoạt động (Model Switcher)
# ---------------------------------------------------------
@router.get("/models/active", response_model=ActiveModelSetting)
def admin_get_active_model(db: Session = Depends(get_db),
                          current_user: User = Depends(require_role(["admin", "analyst"]))):
    setting = db.get(SystemSetting, "active_model")
    return ActiveModelSetting(active_model=active_model(db).upper(), description="Mô hình mặc định khi API không chỉ định thuật toán",
                              updated_at=setting.updated_at.isoformat() if setting else None)


@router.post("/models/active", response_model=ActiveModelSetting)
def admin_set_active_model(setting: ActiveModelSetting, db: Session = Depends(get_db),
                          current_user: User = Depends(require_role(["admin"]))):
    name = setting.active_model.strip().upper()
    if name not in MODEL_NAMES:
        raise HTTPException(400, "Thuật toán không được hỗ trợ")
    row = db.get(SystemSetting, "active_model")
    if row:
        row.value = name
    else:
        db.add(SystemSetting(key="active_model", value=name))
    db.commit()
    return admin_get_active_model(db, current_user)
