from apscheduler.schedulers.background import BackgroundScheduler
from app.services.job_aggregator import fetch_all_jobs
from app.database import job_collection

def start_scheduler():
    scheduler = BackgroundScheduler()

    def job_fetch_task():
        jobs = fetch_all_jobs()
        inserted = 0

        for job in jobs:
            if not job_collection.find_one({"url": job["url"]}):
                job_collection.insert_one(job)
                inserted += 1

        print(f"[Scheduler] Jobs inserted: {inserted}")

    scheduler.add_job(job_fetch_task, "interval", hours=12)
    scheduler.start()
