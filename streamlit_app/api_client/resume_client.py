import requests
API_BASE_URL = "http://127.0.0.1:8000/api/v1"

def upload_resumes(files) -> dict:
    """
    Upload multiple PDF/DOCX resume files to the FastAPI backend.
    """

    multipart_files = []

    for uploaded_file in files:
        multipart_files.append(
            (
                "files",
                (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type or "application/octet-stream",
                ),
            )
        )

    response = requests.post(
        f"{API_BASE_URL}/resumes/upload",
        files=multipart_files,
        timeout=300,
    )

    response.raise_for_status()

    return response.json()


def get_candidates(
    page: int = 1,
    page_size: int = 20,
    search: str = "",
) -> dict:
    """
    Get candidates from the backend.

    This is useful for displaying processed resumes
    along with their candidate information.
    """

    response = requests.get(
        f"{API_BASE_URL}/candidates/",
        params={
            "page": page,
            "page_size": page_size,
            "search": search.strip() or None,
        },
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_candidate(candidate_id: int) -> dict:
    """
    Get complete candidate details.
    """

    response = requests.get(
        f"{API_BASE_URL}/candidates/{candidate_id}",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_candidate_resumes(candidate_id: int) -> list:
    """
    Get all resume versions for a candidate.
    """

    response = requests.get(
        f"{API_BASE_URL}/candidates/{candidate_id}/resumes",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_resume_error_message(exc: Exception) -> str:
    """
    Convert API/request exceptions into a user-friendly message.
    """

    if isinstance(exc, requests.exceptions.ConnectionError):
        return (
            "Could not connect to the FastAPI server. "
            "Please make sure Uvicorn is running on "
            "http://127.0.0.1:8000."
        )

    if isinstance(exc, requests.exceptions.Timeout):
        return (
            "The request timed out. Resume processing may take "
            "longer because AI extraction is being performed."
        )

    if isinstance(exc, requests.exceptions.HTTPError):
        response = getattr(exc, "response", None)

        if response is not None:
            try:
                error_data = response.json()

                if isinstance(error_data, dict):
                    detail = error_data.get("detail")

                    if detail:
                        return f"API error: {detail}"

            except ValueError:
                pass

            return (
                f"API request failed with HTTP "
                f"{response.status_code}."
            )

    return f"Unexpected error: {exc}"