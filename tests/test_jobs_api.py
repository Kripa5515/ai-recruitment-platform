import pytest
from fastapi.testclient import TestClient

from app.api.dependencies.database import get_db
from app.api.main import app


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_create_job_api(client):
    response = client.post(
        "/api/v1/jobs/",
        json={
            "title": "GenAI Developer",
            "description": "Looking for a Python and GenAI developer.",
            "company": "ABC Technologies",
            "location": "Noida",
            "experience_required": "5+ years",
            "employment_type": "Full-time",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] is not None
    assert data["title"] == "GenAI Developer"
    assert data["description"] == (
        "Looking for a Python and GenAI developer."
    )
    assert data["company"] == "ABC Technologies"
    assert data["location"] == "Noida"
    assert data["experience_required"] == "5+ years"
    assert data["employment_type"] == "Full-time"
    assert data["status"] == "draft"


def test_get_all_jobs_api(client):
    client.post(
        "/api/v1/jobs/",
        json={
            "title": "Job For Listing",
            "description": "Job description.",
            "company": "ABC Corp",
            "location": "Noida",
            "experience_required": "3+ years",
            "employment_type": "Full-time",
        },
    )

    response = client.get("/api/v1/jobs/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)

    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert "total_pages" in data

    assert isinstance(data["items"], list)
    assert isinstance(data["total"], int)
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert data["total"] >= 1


def test_get_job_api(client):
    create_response = client.post(
        "/api/v1/jobs/",
        json={
            "title": "AI Engineer",
            "description": "Python, RAG and LLM developer.",
            "company": "AI Solutions",
            "location": "Bangalore",
            "experience_required": "4+ years",
            "employment_type": "Full-time",
        },
    )

    assert create_response.status_code == 200

    created_job = create_response.json()
    job_id = created_job["id"]

    response = client.get(f"/api/v1/jobs/{job_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == job_id
    assert data["title"] == "AI Engineer"
    assert data["company"] == "AI Solutions"
    assert data["location"] == "Bangalore"


def test_get_job_not_found(client):
    response = client.get("/api/v1/jobs/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Job not found"
    }


def test_update_job_api(client):
    create_response = client.post(
        "/api/v1/jobs/",
        json={
            "title": "Python Developer",
            "description": "Python backend developer.",
            "company": "ABC Technologies",
            "location": "Noida",
            "experience_required": "3+ years",
            "employment_type": "Full-time",
        },
    )

    assert create_response.status_code == 200

    created_job = create_response.json()
    job_id = created_job["id"]

    response = client.put(
        f"/api/v1/jobs/{job_id}",
        json={
            "title": "Senior Python Developer",
            "description": "Python, FastAPI and PostgreSQL developer.",
            "company": "XYZ Solutions",
            "location": "Bangalore",
            "experience_required": "6+ years",
            "employment_type": "Full-time",
            "status": "active",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == job_id
    assert data["title"] == "Senior Python Developer"
    assert data["description"] == (
        "Python, FastAPI and PostgreSQL developer."
    )
    assert data["company"] == "XYZ Solutions"
    assert data["location"] == "Bangalore"
    assert data["experience_required"] == "6+ years"
    assert data["employment_type"] == "Full-time"
    assert data["status"] == "active"


def test_update_job_not_found(client):
    response = client.put(
        "/api/v1/jobs/999999",
        json={
            "title": "Senior Developer",
            "description": "Updated description.",
            "company": "ABC Technologies",
            "location": "Delhi",
            "experience_required": "5+ years",
            "employment_type": "Full-time",
            "status": "active",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Job not found"
    }


def test_delete_job_api(client):
    create_response = client.post(
        "/api/v1/jobs/",
        json={
            "title": "Temporary Developer",
            "description": "This job will be deleted.",
            "company": "Temporary Company",
            "location": "Noida",
            "experience_required": "2+ years",
            "employment_type": "Full-time",
        },
    )

    assert create_response.status_code == 200

    created_job = create_response.json()
    job_id = created_job["id"]

    response = client.delete(f"/api/v1/jobs/{job_id}")

    assert response.status_code == 204

    get_response = client.get(f"/api/v1/jobs/{job_id}")

    assert get_response.status_code == 404


def test_delete_job_not_found(client):
    response = client.delete("/api/v1/jobs/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Job not found"
    }