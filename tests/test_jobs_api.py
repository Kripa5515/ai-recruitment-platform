from fastapi.testclient import TestClient

from app.api.main import app


client = TestClient(app)


def test_create_job_api():
    response = client.post(
        "/jobs/",
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


def test_get_all_jobs_api():
    response = client.get("/jobs/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_job_api():
    create_response = client.post(
        "/jobs/",
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

    response = client.get(f"/jobs/{job_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == job_id
    assert data["title"] == "AI Engineer"
    assert data["company"] == "AI Solutions"
    assert data["location"] == "Bangalore"


def test_get_job_not_found():
    response = client.get("/jobs/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Job not found"
    }


def test_update_job_api():
    create_response = client.post(
        "/jobs/",
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
        f"/jobs/{job_id}",
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


def test_update_job_not_found():
    response = client.put(
        "/jobs/999999",
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


def test_delete_job_api():
    create_response = client.post(
        "/jobs/",
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

    response = client.delete(f"/jobs/{job_id}")

    assert response.status_code == 204

    get_response = client.get(f"/jobs/{job_id}")

    assert get_response.status_code == 404


def test_delete_job_not_found():
    response = client.delete("/jobs/999999")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Job not found"
    }