from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

def test_create_job_api():
    response = client.post(
        "/jobs/",
        json={
            "title": "GenAI Developer",
            "description": "Looking for a Python and GenAI developer.",
        },
    )
    
    assert response.status_code == 200
    data = response.json()

    assert data["id"] is not None
    assert data["title"] == "GenAI Developer"
    assert data["description"] == (
        "Looking for a Python and GenAI developer."
    )
    assert "created_at" in data
    assert "updated_at" in data


def test_get_jobs_api():
    response = client.get("/jobs/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    assert "id" in data[0]
    assert "title" in data[0]
    assert "description" in data[0]
    assert "created_at" in data[0]
    assert "updated_at" in data[0]


def test_get_job_api():
    create_response = client.post(
        "/jobs/",
        json={
            "title": "AI Engineer",
            "description": "Python, RAG and LLM developer.",
        },
    )

    assert create_response.status_code == 200
    created_job = create_response.json()
    response = client.get(
        f"/jobs/{created_job['id']}"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_job["id"]
    assert data["title"] == "AI Engineer"
    assert data["description"] == "Python, RAG and LLM developer."

def test_get_job_not_found():
    response = client.get("/jobs/999999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Job not found"

def test_update_job_api():
    create_response = client.post(
        "/jobs/",
        json={
            "title": "Python Developer",
            "description": "Python backend developer.",
        },
    )

    assert create_response.status_code == 200
    created_job = create_response.json()

    response = client.put(
        f"/jobs/{created_job['id']}",
        json={
            "title": "Senior Python Developer",
            "description": "Python, FastAPI and PostgreSQL developer.",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_job["id"]
    assert data["title"] == "Senior Python Developer"
    assert data["description"] == (
        "Python, FastAPI and PostgreSQL developer."
    )

def test_update_job_not_found():
    response = client.put(
        "/jobs/999999",
        json={
            "title": "Senior Developer",
            "description": "Updated description.",
        },
    )

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Job not found"

def test_delete_job_api():
    create_response = client.post(
        "/jobs/",
        json={
            "title": "Temporary Developer",
            "description": "This job will be deleted.",
        },
    )

    assert create_response.status_code == 200
    created_job = create_response.json()
    response = client.delete(
        f"/jobs/{created_job['id']}"
    )

    assert response.status_code == 204
    assert response.content == b""

    get_response = client.get(
        f"/jobs/{created_job['id']}"
    )

    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Job not found"

def test_delete_job_not_found():
    response = client.delete("/jobs/999999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Job not found"