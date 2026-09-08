import requests


API_BASE_URL = "http://127.0.0.1:8000/api/v1"


def match_candidates_for_job(job_id: int) -> dict:
    """
    Run candidate matching for a selected job.

    The backend performs:
    - Experience matching
    - Required skill matching
    - Constraint matching
    - Semantic similarity
    - Hybrid final scoring
    - Explainable reasons and warnings
    """

    response = requests.post(
        f"{API_BASE_URL}/matching/jobs/{job_id}/candidates",
        timeout=120,
    )

    response.raise_for_status()

    return response.json()