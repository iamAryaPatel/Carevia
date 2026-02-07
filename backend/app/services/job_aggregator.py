from app.services.remotive_service import fetch_remotive_jobs
from app.services.adzuna_service import fetch_adzuna_jobs
import logging

logger = logging.getLogger(__name__)


def fetch_all_jobs():
    """
    Fetch jobs from all configured sources.
    
    Returns:
        list: Combined list of jobs from all sources
    """
    jobs = []
    
    # Fetch from Remotive
    try:
        remotive_jobs = fetch_remotive_jobs()
        jobs.extend(remotive_jobs)
        logger.info(f"Added {len(remotive_jobs)} jobs from Remotive")
    except Exception as e:
        logger.error(f"Failed to fetch from Remotive: {e}", exc_info=True)
    
    # Fetch from Adzuna
    try:
        adzuna_jobs = fetch_adzuna_jobs()
        jobs.extend(adzuna_jobs)
        logger.info(f"Added {len(adzuna_jobs)} jobs from Adzuna")
    except Exception as e:
        logger.error(f"Failed to fetch from Adzuna: {e}", exc_info=True)
    
    logger.info(f"Total jobs fetched from all sources: {len(jobs)}")
    return jobs


