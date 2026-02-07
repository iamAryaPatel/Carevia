import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging

from app.config import settings

logger = logging.getLogger(__name__)

ADZUNA_API_BASE_URL = "https://api.adzuna.com/v1/api/jobs"
REQUEST_TIMEOUT = 30  # seconds


def create_session_with_retries():
    """
    Create a requests session with retry logic.
    
    Returns:
        requests.Session: Configured session with retry strategy
    """
    session = requests.Session()
    
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


def fetch_adzuna_jobs():
    """
    Fetch job listings from Adzuna API.
    
    Returns:
        list: List of job dictionaries
    
    Note:
        Requires ADZUNA_APP_ID and ADZUNA_APP_KEY environment variables.
        If not configured, returns empty list.
    """
    # Check if API credentials are configured
    if not settings.adzuna_app_id or not settings.adzuna_app_key:
        logger.warning("Adzuna API credentials not configured, skipping")
        return []
    
    try:
        logger.info("Fetching jobs from Adzuna API...")
        
        # Adzuna API endpoint for India (you can make this configurable)
        url = f"{ADZUNA_API_BASE_URL}/in/search/1"
        
        params = {
            "app_id": settings.adzuna_app_id,
            "app_key": settings.adzuna_app_key,
            "results_per_page": 50,
            "what": "software developer",  # Can be made configurable
            "content-type": "application/json"
        }
        
        session = create_session_with_retries()
        response = session.get(url, params=params, timeout=REQUEST_TIMEOUT)
        
        if response.status_code != 200:
            logger.error(f"Adzuna API returned status {response.status_code}")
            return []
        
        data = response.json()
        jobs = []
        
        for job in data.get("results", []):
            try:
                jobs.append({
                    "title": job.get("title", "Unknown Title"),
                    "company": job.get("company", {}).get("display_name", "Unknown Company"),
                    "location": job.get("location", {}).get("display_name", "Remote"),
                    "category": job.get("category", {}).get("label", "Other"),
                    "url": job.get("redirect_url", ""),
                    "source": "Adzuna"
                })
            except Exception as e:
                logger.warning(f"Failed to parse Adzuna job: {e}")
                continue
        
        logger.info(f"Successfully fetched {len(jobs)} jobs from Adzuna")
        return jobs
        
    except requests.exceptions.Timeout:
        logger.error(f"Adzuna API request timed out after {REQUEST_TIMEOUT}s")
        return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Adzuna API request failed: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error fetching Adzuna jobs: {e}", exc_info=True)
        return []

