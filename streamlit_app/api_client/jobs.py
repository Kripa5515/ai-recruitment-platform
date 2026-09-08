import requests


API_BASE_URL = "http://127.0.0.1:8000/api/v1"


# =========================================================
# Create Job
# =========================================================

def create_job(job_data: dict) -> dict:
    response = requests.post(
        f"{API_BASE_URL}/jobs/",
        json=job_data,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# Analyze Pasted Job Description
# =========================================================

def analyze_jd(job_description: str) -> dict:
    response = requests.post(
        f"{API_BASE_URL}/jobs/analyze",
        params={
            "job_description": job_description,
        },
        timeout=60,
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# Upload Job Description
# =========================================================

def upload_jd(
    file,
) -> dict:
    response = requests.post(
        f"{API_BASE_URL}/jobs/upload",
        files={
            "file": (
                file.name,
                file.getvalue(),
                file.type or "application/octet-stream",
            )
        },
        timeout=60,
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# Get Jobs
# =========================================================

def get_jobs(
    page: int = 1,
    page_size: int = 10,
    search: str = "",
) -> dict:
    response = requests.get(
        f"{API_BASE_URL}/jobs/",
        params={
            "page": page,
            "page_size": page_size,
            "search": search.strip() or None,
        },
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# Get Single Job
# =========================================================

def get_job(job_id: int) -> dict:
    response = requests.get(
        f"{API_BASE_URL}/jobs/{job_id}",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# Update Job
# =========================================================

def update_job(
    job_id: int,
    job_data: dict,
) -> dict:
    response = requests.put(
        f"{API_BASE_URL}/jobs/{job_id}",
        json=job_data,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# Delete Job
# =========================================================

def delete_job(job_id: int) -> None:
    response = requests.delete(
        f"{API_BASE_URL}/jobs/{job_id}",
        timeout=30,
    )

    response.raise_for_status()