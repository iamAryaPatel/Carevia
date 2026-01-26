from fastapi import APIRouter
from app.database import job_collection
from app.services.job_aggregator import fetch_all_jobs

router = APIRouter()

@router.get("/jobs")
def get_jobs():
    return list(job_collection.find({}, {"_id": 0}))

@router.get("/jobs/fetch")
def fetch_jobs():
    jobs = fetch_all_jobs()
    inserted = 0

    for job in jobs:
        if not job_collection.find_one({"url": job["url"]}):
            job_collection.insert_one(job)
            inserted += 1

    return {"inserted": inserted}
