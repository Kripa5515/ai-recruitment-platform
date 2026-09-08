import requests
API_BASE_URL = "http://127.0.0.1:8000/api/v1"

def get_dashboard_stats() -> dict:
    response = requests.get(
        f"{API_BASE_URL}/dashboard/stats",
        timeout=10,
    )
    response.raise_for_status()
    return response.json()