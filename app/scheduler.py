from datetime import date

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session

from app.config.database_config import sessionLocal
from app.services.status_resolver import expiry_sweep

scheduler = AsyncIOScheduler()


def run_expiry_sweep_job():
    db: Session = sessionLocal()
    try:
        updated = expiry_sweep(db)
        print(f"[{date.today()}] Sweep done — {updated} member(s) updated.")
    except Exception as e:
        db.rollback()
        print(f"[{date.today()}] Sweep failed: {e}")
    finally:
        db.close()


def sweep_scheduler():
    scheduler.add_job(
        run_expiry_sweep_job,
        trigger=CronTrigger(hour=0, minute=0),
        id="expiry_sweep",
        replace_existing=True,
    )
    scheduler.start()
