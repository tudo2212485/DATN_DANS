"""Persistent job status, shared by manual triggers and scheduled collection."""
from datetime import datetime
from fastapi import HTTPException
from app.core.database import SessionLocal
from app.models.models import BackgroundJob, SystemSetting

MODEL_NAMES = {"LSTM": "LSTM", "XGBOOST": "XGBoost", "PROPHET": "Prophet", "ARIMA": "ARIMA", "RANDOM FOREST": "Random Forest"}


def active_model(db):
    setting = db.get(SystemSetting, "active_model")
    return MODEL_NAMES.get(setting.value if setting else "LSTM", "LSTM")


def job_response(job):
    return dict(task_id=job.id, task_name="Cào dữ liệu" if job.kind == "scrape" else "Huấn luyện mô hình",
                status=job.status, message=job.message, progress=job.progress,
                records_processed=job.records_processed, timestamp=job.created_at.isoformat())


def create_job(db, kind):
    # Serialize triggers across processes without relying on a browser's disabled button.
    if db.bind.dialect.name == "postgresql":
        from sqlalchemy import text
        db.execute(text("SELECT pg_advisory_xact_lock(741852)"))
    if db.query(BackgroundJob).filter(BackgroundJob.status == "RUNNING").first():
        raise HTTPException(409, "Có tác vụ đang chạy. Vui lòng chờ hoàn tất.")
    job = BackgroundJob(kind=kind, message="Đã tiếp nhận tác vụ, đang xử lý.")
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def update_job(job_id, **values):
    with SessionLocal() as db:
        job = db.get(BackgroundJob, job_id)
        if job:
            for key, value in values.items():
                setattr(job, key, value)
            db.commit()


def run_job(job_id, kind, parameter):
    try:
        if kind == "scrape":
            from ml_pipeline.scraper import scrape_and_update_db
            options = parameter if isinstance(parameter, dict) else {"days": parameter}
            result = scrape_and_update_db(**options, progress=lambda done, total: update_job(
                job_id, progress=int(done * 100 / total), message=f"Đã xử lý {done}/{total} bước thu thập (ngày/trang/báo cáo tùy nguồn)."))
            update_job(job_id, status=result["status"], message=result["message"],
                       records_processed=result["count"], progress=100, finished_at=datetime.now())
        else:
            from app.services.training_service import retrain
            result = retrain(parameter, lambda percent, message: update_job(job_id, progress=percent, message=message))
            update_job(job_id, status=result["status"], progress=100, records_processed=result["count"],
                       message=result["message"], finished_at=datetime.now())
    except Exception as exc:
        update_job(job_id, status="FAILED", message=str(exc), finished_at=datetime.now())
