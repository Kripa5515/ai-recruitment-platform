import requests


API_BASE_URL = "http://127.0.0.1:8000/api/v1"


def get_candidates(
    page: int = 1,
    page_size: int = 20,
    search: str = "",
) -> dict:
    """
    Fetch candidates from FastAPI.

    Returns paginated candidate data.
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


def get_candidate(
    candidate_id: int,
) -> dict:
    """
    Fetch complete candidate details.
    """

    response = requests.get(
        f"{API_BASE_URL}/candidates/{candidate_id}",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_candidate_resumes(
    candidate_id: int,
) -> list:
    """
    Fetch all resume versions belonging to a candidate.
    """

    response = requests.get(
        f"{API_BASE_URL}/candidates/{candidate_id}/resumes",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_candidates_error_message(
    exc: Exception,
) -> str:
    """
    Convert API exceptions into user-friendly messages.
    """

    if isinstance(
        exc,
        requests.exceptions.ConnectionError,
    ):
        return (
            "Could not connect to the FastAPI server. "
            "Please make sure Uvicorn is running on "
            "http://127.0.0.1:8000."
        )

    if isinstance(
        exc,
        requests.exceptions.Timeout,
    ):
        return (
            "The request timed out. "
            "Please try again."
        )

    if isinstance(
        exc,
        requests.exceptions.HTTPError,
    ):

        response = exc.response

        if response is not None:

            try:

                error_data = response.json()

                if isinstance(
                    error_data,
                    dict,
                ):

                    detail = error_data.get(
                        "detail"
                    )

                    if detail:

                        return (
                            f"API error: {detail}"
                        )

            except ValueError:
                pass

            return (
                "Candidate API request failed "
                f"with HTTP {response.status_code}."
            )

    return f"Unexpected error: {exc}"