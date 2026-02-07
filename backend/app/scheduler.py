from apscheduler.schedulers.background import BackgroundScheduler
from app.services.job_aggregator import fetch_all_jobs
from app.database import job_collection
import logging

logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler = None


def job_fetch_task():
    """
    Background task to fetch jobs from all sources.
    """
    try:
        logger.info("Starting scheduled job fetch...")
        
        jobs = fetch_all_jobs()
        total_fetched = len(jobs)
        inserted = 0
        duplicates_skipped = 0
        errors = 0
        
        for job in jobs:
            try:
                # Check if job already exists
                if not job_collection.find_one({"url": job["url"]}):
                    job_collection.insert_one(job)
                    inserted += 1
                else:
                    duplicates_skipped += 1
            except Exception as e:
                logger.warning(f"Failed to insert job: {e}")
                errors += 1
                continue
        
        logger.info(
            f"Scheduled job fetch complete: {inserted} inserted, "
            f"{duplicates_skipped} duplicates, {errors} errors, "
            f"{total_fetched} total fetched"
        )
        
    except Exception as e:
        logger.error(f"Error in scheduled job fetch: {e}", exc_info=True)


def start_scheduler():
    """
    Start the background scheduler for periodic job fetching.
    """
    global scheduler
    
    try:
        scheduler = BackgroundScheduler()
        
        # Add job fetch task (runs every 12 hours)
        scheduler.add_job(
            job_fetch_task,
            "interval",
            hours=12,
            id="job_fetch_task",
            replace_existing=True,
            max_instances=1  # Prevent concurrent executions
        )
        
        scheduler.start()
        logger.info("Background scheduler started (job fetch every 12 hours)")
        
    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}", exc_info=True)
        raise


def stop_scheduler():
    """
    Stop the background scheduler gracefully.
    """
    global scheduler
    
    if scheduler and scheduler.running:
        try:
            scheduler.shutdown(wait=True)
            logger.info("Background scheduler stopped")
        except Exception as e:
            logger.error(f"Error stopping scheduler: {e}", exc_info=True)

