"""Persistent job status, shared by manual triggers and scheduled collection."""
from datetime import datetime
from fastapi import HTTPException
from app.core.database import SessionLocal
from app.models.models import BackgroundJob, Commodity, Forecast, SystemSetting, TrainingRun

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


def sync_forecast_after_scrape(job_id, options):
    """Retrain a collected commodity only when its verified snapshot changed."""
    from app.services.history_service import fingerprint, training_context
    from app.services.training_service import retrain

    commodity_id = options.get("commodity_id") if isinstance(options, dict) else None
    with SessionLocal() as db:
        if commodity_id:
            commodities = db.query(Commodity).filter(Commodity.id == commodity_id).all()
        else:
            commodities = db.query(Commodity).filter(Commodity.code == "COFFEE_ROBUSTA").all()

        pending = []
        messages = []
        for commodity in commodities:
            context = training_context(db, commodity)
            quality = context["quality"]
            if not quality["ready"]:
                messages.append(f"{commodity.name}: chưa tự huấn luyện vì {quality['reason']}")
                continue
            current_hash = fingerprint(context["rows"])
            latest_run = (
                db.query(TrainingRun)
                .filter(TrainingRun.commodity_id == commodity.id)
                .order_by(TrainingRun.id.desc())
                .first()
            )
            trained_model_count = (
                db.query(Forecast.model_name)
                .filter(Forecast.training_run_id == latest_run.id)
                .distinct()
                .count()
                if latest_run else 0
            )
            if latest_run and latest_run.dataset_hash == current_hash and trained_model_count == len(MODEL_NAMES):
                messages.append(f"{commodity.name}: dự báo đã đồng bộ với dữ liệu mới nhất.")
            else:
                pending.append((commodity.id, commodity.name))

    failed = False
    for index, (target_id, target_name) in enumerate(pending):
        result = retrain(
            target_id,
            lambda percent, message, index=index: update_job(
                job_id,
                progress=min(99, 65 + int(((index + percent / 100) / max(1, len(pending))) * 34)),
                message=f"Đã thu thập dữ liệu. {message}",
            ),
        )
        failed = failed or result["status"] == "FAILED"
        messages.append(f"{target_name}: {result['message']}")

    return " ".join(messages), failed


def run_job(job_id, kind, parameter):
    try:
        if kind == "scrape":
            from ml_pipeline.scraper import scrape_and_update_db
            options = parameter if isinstance(parameter, dict) else {"days": parameter}
            result = scrape_and_update_db(**options, progress=lambda done, total: update_job(
                job_id, progress=int(done * 65 / total), message=f"Đã xử lý {done}/{total} bước thu thập (ngày/trang/báo cáo tùy nguồn)."))
            sync_message, sync_failed = sync_forecast_after_scrape(job_id, options)
            final_status = "PARTIAL" if sync_failed and result["status"] == "SUCCESS" else result["status"]
            update_job(job_id, status=final_status, message=f"{result['message']} {sync_message}".strip(),
                       records_processed=result["count"], progress=100, finished_at=datetime.now())
        else:
            from app.services.training_service import retrain
            result = retrain(parameter, lambda percent, message: update_job(job_id, progress=percent, message=message))
            update_job(job_id, status=result["status"], progress=100, records_processed=result["count"],
                       message=result["message"], finished_at=datetime.now())
    except Exception as exc:
        update_job(job_id, status="FAILED", message=str(exc), finished_at=datetime.now())
