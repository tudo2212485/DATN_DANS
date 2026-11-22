from datetime import datetime, timedelta, timezone
import logging
import threading

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import func

from app.core.database import SessionLocal
from ml_pipeline.scraper import scrape_and_update_db
from app.services.alert_service import evaluate_all_alert_rules

logger = logging.getLogger(__name__)
_scheduler_instance = None

try:
    from zoneinfo import ZoneInfo
    VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")
except Exception:
    VN_TZ = timezone(timedelta(hours=7))


def _vn_today():
    return datetime.now(VN_TZ).date()


def scheduled_scraper_task():
    logger.info("Starting scheduled scraper task...")
    try:
        # Refresh 7 recent days across all supported Vietnamese commodities (all 8 core items).
        from app.services.job_service import create_job, run_job
        with SessionLocal() as db:
            job = create_job(db, "scrape")
            job_id = job.id
        run_job(job_id, "scrape", dict(days=7))
        logger.info("Scheduled scraper task completed successfully.")
    except Exception as e:
        logger.error(f"Error in scheduled scraper task: {e}")


def scheduled_alert_evaluation_task():
    logger.info("Starting scheduled alert evaluation task...")
    db = SessionLocal()
    try:
        triggered = evaluate_all_alert_rules(db)
        logger.info(f"Scheduled alert evaluation completed. Triggered {triggered} rules.")
    except Exception as e:
        logger.error(f"Error in scheduled alert evaluation task: {e}")
    finally:
        db.close()


def run_startup_catchup_if_stale() -> bool:
    """
    Lightweight startup catch-up check (Asia/Ho_Chi_Minh):
    If MAX(price_history.record_date) < today_vn and no successful scrape finished in the last 2 hours,
    automatically trigger a background scrape + forecast sync.
    Returns True if catch-up job was launched, False otherwise.
    """
    try:
        from app.models.models import BackgroundJob, Commodity, PriceHistory
        from app.services.job_service import create_job, run_job

        today_vn = _vn_today()
        two_hours_ago = datetime.now() - timedelta(hours=2)

        with SessionLocal() as db:
            if db.query(Commodity).count() == 0:
                return False
            if db.query(BackgroundJob).filter(BackgroundJob.status == "RUNNING").first():
                return False
            recent_ok = (
                db.query(BackgroundJob)
                .filter(
                    BackgroundJob.kind == "scrape",
                    BackgroundJob.status == "SUCCESS",
                    BackgroundJob.finished_at >= two_hours_ago,
                )
                .first()
            )
            if recent_ok:
                return False

            max_date = db.query(func.max(PriceHistory.record_date)).scalar()
            if max_date is not None and max_date >= today_vn:
                return False

            job = create_job(db, "scrape")
            job_id = job.id

        logger.info(f"Startup auto catch-up triggered (max_date={max_date}, today_vn={today_vn}, job_id={job_id})")
        run_job(job_id, "scrape", dict(days=7))
        return True
    except Exception as exc:
        logger.warning(f"Startup auto catch-up skipped/failed safely: {exc}")
        return False


def start_scheduler():
    global _scheduler_instance
    if _scheduler_instance is not None:
        return _scheduler_instance

    _scheduler_instance = BackgroundScheduler(timezone=VN_TZ)

    # Refresh verified observations and stale eligible forecasts twice a day (06:00 & 18:00 GMT+7).
    _scheduler_instance.add_job(
        scheduled_scraper_task,
        trigger=CronTrigger(hour="6,18", minute=0, timezone=VN_TZ),
        id="daily_scraper",
        name="Daily Scraper",
        replace_existing=True,
        coalesce=True,
        misfire_grace_time=3600,
    )

    # Run alert evaluation every day at 06:30 and 18:30 GMT+7.
    _scheduler_instance.add_job(
        scheduled_alert_evaluation_task,
        trigger=CronTrigger(hour="6,18", minute=30, timezone=VN_TZ),
        id="daily_alert_evaluation",
        name="Daily Alert Evaluation",
        replace_existing=True,
        coalesce=True,
        misfire_grace_time=3600,
    )

    _scheduler_instance.start()
    logger.info("APScheduler started with background jobs (Asia/Ho_Chi_Minh, misfire_grace_time=3600, coalesce=True).")

    # Non-blocking startup catch-up check in a daemon thread
    threading.Thread(
        target=run_startup_catchup_if_stale,
        name="agro-startup-catchup",
        daemon=True,
    ).start()
    return _scheduler_instance


def stop_scheduler():
    global _scheduler_instance
    if _scheduler_instance is not None:
        _scheduler_instance.shutdown()
        logger.info("APScheduler stopped.")
        _scheduler_instance = None
