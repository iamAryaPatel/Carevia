from app.services.remotive_service import fetch_remotive_jobs
from app.services.adzuna_service import fetch_adzuna_jobs

def fetch_all_jobs():
    jobs = []
    jobs.extend(fetch_remotive_jobs())
    jobs.extend(fetch_adzuna_jobs())
    return jobs
