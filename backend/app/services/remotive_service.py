import requests

REMOTIVE_API_URL = "https://remotive.com/api/remote-jobs"

def fetch_remotive_jobs():
    response = requests.get(REMOTIVE_API_URL)
    if response.status_code != 200:
        return []

    data = response.json()
    jobs = []

    for job in data.get("jobs", []):
        jobs.append({
            "title": job.get("title"),
            "company": job.get("company_name"),
            "location": job.get("candidate_required_location"),
            "category": job.get("category"),
            "url": job.get("url"),
            "source": "Remotive"
        })

    return jobs
