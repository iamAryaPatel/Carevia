import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging

from app.middleware import ExternalAPIException

logger = logging.getLogger(__name__)

REMOTIVE_API_URL = "https://remotive.com/api/remote-jobs"
REQUEST_TIMEOUT = 30  # seconds


def create_session_with_retries():
    """
    Create a requests session with retry logic.
    
    Returns:
        requests.Session: Configured session with retry strategy
    """
    session = requests.Session()
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session


def fetch_remotive_jobs():
    """
    Fetch job listings from Remotive API.
    
    Returns:
        list: List of job dictionaries
    
    Raises:
        ExternalAPIException: If API request fails
    """
    try:
        logger.info("Fetching jobs from Remotive API...")
        
        session = create_session_with_retries()
        response = session.get(REMOTIVE_API_URL, timeout=REQUEST_TIMEOUT)
        
        if response.status_code != 200:
            logger.error(f"Remotive API returned status {response.status_code}")
            return []
        
        data = response.json()
        jobs = []
        
        for job in data.get("jobs", []):
            try:
                jobs.append({
                    "title": job.get("title", "Unknown Title"),
                    "company": job.get("company_name", "Unknown Company"),
                    "location": job.get("candidate_required_location", "Remote"),
                    "category": job.get("category", "Other"),
                    "url": job.get("url", ""),
                    "source": "Remotive"
                })
            except Exception as e:
                logger.warning(f"Failed to parse Remotive job: {e}")
                continue
        
        logger.info(f"Successfully fetched {len(jobs)} jobs from Remotive")
        return jobs
        
    except requests.exceptions.Timeout:
        logger.error(f"Remotive API request timed out after {REQUEST_TIMEOUT}s")
        return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Remotive API request failed: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error fetching Remotive jobs: {e}", exc_info=True)
        return []

