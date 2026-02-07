from fastapi import APIRouter, Query, HTTPException, status
from typing import Optional
import logging

from app.database import job_collection
from app.services.job_aggregator import fetch_all_jobs
from app.models import JobResponse, JobListResponse, FetchJobsResponse
from app.middleware import DatabaseException

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("", response_model=JobListResponse)
def get_jobs(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search in title, company, or location"),
    source: Optional[str] = Query(None, description="Filter by job source"),
    category: Optional[str] = Query(None, description="Filter by category"),
):
    """
    Get paginated list of jobs with optional filtering.
    
    Args:
        page: Page number (starts at 1)
        page_size: Number of items per page (max 100)
        search: Search query for title, company, or location
        source: Filter by job source (e.g., "Remotive", "Adzuna")
        category: Filter by job category
    
    Returns:
        JobListResponse: Paginated list of jobs
    """
    try:
        # Build query filter
        query_filter = {}
        
        if search:
            query_filter["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"company": {"$regex": search, "$options": "i"}},
                {"location": {"$regex": search, "$options": "i"}},
            ]
        
        if source:
            query_filter["source"] = source
        
        if category:
            query_filter["category"] = category
        
        # Get total count
        total = job_collection.count_documents(query_filter)
        
        # Calculate skip
        skip = (page - 1) * page_size
        
        # Fetch jobs with pagination
        jobs_cursor = job_collection.find(
            query_filter,
            {"_id": 0}
        ).skip(skip).limit(page_size).sort("_id", -1)
        
        jobs = list(jobs_cursor)
        
        logger.info(
            f"Retrieved {len(jobs)} jobs (page {page}/{(total + page_size - 1) // page_size})"
        )
        
        return JobListResponse(
            jobs=jobs,
            total=total,
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        logger.error(f"Error fetching jobs: {e}", exc_info=True)
        raise DatabaseException("Failed to fetch jobs from database")


@router.get("/fetch", response_model=FetchJobsResponse)
def fetch_jobs():
    """
    Manually trigger job fetching from all sources.
    
    Returns:
        FetchJobsResponse: Statistics about fetched jobs
    """
    try:
        logger.info("Manual job fetch triggered")
        
        jobs = fetch_all_jobs()
        total_fetched = len(jobs)
        inserted = 0
        duplicates_skipped = 0
        
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
                continue
        
        logger.info(
            f"Job fetch complete: {inserted} inserted, "
            f"{duplicates_skipped} duplicates skipped, "
            f"{total_fetched} total fetched"
        )
        
        return FetchJobsResponse(
            inserted=inserted,
            total_fetched=total_fetched,
            duplicates_skipped=duplicates_skipped
        )
        
    except Exception as e:
        logger.error(f"Error in manual job fetch: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch jobs"
        )


@router.get("/sources", tags=["Jobs"])
def get_job_sources():
    """
    Get list of available job sources with job counts.
    
    Returns:
        dict: Job sources and their counts
    """
    try:
        pipeline = [
            {"$group": {"_id": "$source", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        
        sources = list(job_collection.aggregate(pipeline))
        
        return {
            "sources": [
                {"name": s["_id"], "count": s["count"]}
                for s in sources
            ],
            "total_sources": len(sources)
        }
        
    except Exception as e:
        logger.error(f"Error fetching job sources: {e}", exc_info=True)
        raise DatabaseException("Failed to fetch job sources")

