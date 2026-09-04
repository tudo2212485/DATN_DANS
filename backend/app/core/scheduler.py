from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

from app.core.database import SessionLocal
from ml_pipeline.scraper import scrape_and_update_db
from app.services.alert_service import evaluate_all_alert_rules

logger = logging.getLogger(__name__)
_scheduler_instance = None

def scheduled_scraper_task():
    logger.info("Starting scheduled scraper task...")
    try:
        # Scrape data for the last 1 day
        scrape_and_update_db(days=1)
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

def start_scheduler():
    global _scheduler_instance
    if _scheduler_instance is not None:
        return _scheduler_instance
        
    _scheduler_instance = BackgroundScheduler()
    
    # Run scraper every day at 6:00 AM
    _scheduler_instance.add_job(
        scheduled_scraper_task,
        trigger=CronTrigger(hour=6, minute=0),
        id="daily_scraper",
        name="Daily Scraper",
        replace_existing=True,
    )
    
    # Run alert evaluation every day at 6:30 AM and 6:00 PM (18:00)
    _scheduler_instance.add_job(
        scheduled_alert_evaluation_task,
        trigger=CronTrigger(hour="6,18", minute=30),
        id="daily_alert_evaluation",
        name="Daily Alert Evaluation",
        replace_existing=True,
    )
    
    _scheduler_instance.start()
    logger.info("APScheduler started with background jobs.")
    return _scheduler_instance

def stop_scheduler():
    global _scheduler_instance
    if _scheduler_instance is not None:
        _scheduler_instance.shutdown()
        logger.info("APScheduler stopped.")
        _scheduler_instance = None
