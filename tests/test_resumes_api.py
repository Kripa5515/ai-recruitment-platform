import io
from pathlib import Path

import pymupdf
from fastapi.testclient import TestClient

from app.api.dependencies.database import get_db
from app.api.main import app


def create_test_pdf(
    text: str = (
        "Kripa Kumar\n"
        "Senior PHP Laravel Developer\n"
        "Python GenAI RAG Developer"
    ),
) -> bytes:
    """
    Create a real PDF file in memory for API testing.
    """

    document = pymupdf.open()

    page = document.new_page()

    page.insert_text(
        (50, 50),
        text,
    )

    file_content = document.tobytes()

    document.close()

    return file_content


from app.api.schemas.candidate import CandidateProfile


def test_upload_resume_api(
    db_session,
    tmp_path,
    monkeypatch,
):
    """
    Test successful PDF resume upload through API.
    """

    monkeypatch.setattr(
        "app.core.storage.settings.STORAGE_ROOT",
        str(tmp_path),
    )

    dummy_profile = CandidateProfile(
        name="Kripa Kumar",
        email="kripa@example.com",
        phone="9876543210",
        total_experience_years=6.5,
        skills=["PHP", "Laravel", "Python"],
    )
    monkeypatch.setattr(
        "app.services.resume_service.ResumeService.extract_candidate_profile",
        lambda self, text: dummy_profile,
    )

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        client = TestClient(app)

        file_content = create_test_pdf()

        response = client.post(
            "/api/v1/resumes/upload",
            files=[
                (
                    "files",
                    (
                        "kripa_resume.pdf",
                        io.BytesIO(file_content),
                        "application/pdf",
                    ),
                )
            ],
        )

        assert response.status_code == 200

        data = response.json()

        assert data["total_files"] == 1
        assert data["successful"] == 1
        assert data["duplicates"] == 0
        assert data["failed"] == 0
        assert len(data["items"]) == 1

        item = data["items"][0]
        assert item["status"] == "success"
        assert item["filename"] == "kripa_resume.pdf"
        assert item["candidate_name"] == "Kripa Kumar"

        resume = item["resume"]
        assert resume["id"] is not None
        assert resume["original_filename"] == "kripa_resume.pdf"
        assert resume["file_type"] == "pdf"
        assert resume["file_size"] == len(file_content)
        assert len(resume["file_hash"]) == 64
        assert resume["storage_path"].endswith(".pdf")
        assert resume["extracted_text"] is not None
        assert "Kripa Kumar" in resume["extracted_text"]
        assert "Senior PHP Laravel Developer" in resume["extracted_text"]
        assert "Python GenAI RAG Developer" in resume["extracted_text"]
        assert resume["extraction_status"] == "completed"

        saved_file = (
            tmp_path
            / Path(resume["storage_path"]).name
        )

        assert saved_file.exists()
        assert saved_file.read_bytes() == file_content

    finally:
        app.dependency_overrides.clear()


def test_upload_duplicate_resume_api(
    db_session,
    tmp_path,
    monkeypatch,
):
    """
    Same resume uploaded twice should be detected as duplicate.
    """

    monkeypatch.setattr(
        "app.core.storage.settings.STORAGE_ROOT",
        str(tmp_path),
    )

    dummy_profile = CandidateProfile(
        name="Duplicate Test",
        email="dup@example.com",
    )
    monkeypatch.setattr(
        "app.services.resume_service.ResumeService.extract_candidate_profile",
        lambda self, text: dummy_profile,
    )

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        client = TestClient(app)

        file_content = create_test_pdf(
            "Duplicate Resume Test"
        )

        # First upload
        first_response = client.post(
            "/api/v1/resumes/upload",
            files=[
                (
                    "files",
                    (
                        "kripa_resume.pdf",
                        io.BytesIO(file_content),
                        "application/pdf",
                    ),
                )
            ],
        )

        assert first_response.status_code == 200
        first_data = first_response.json()
        assert first_data["successful"] == 1
        assert first_data["duplicates"] == 0

        # Second upload with same content
        second_response = client.post(
            "/api/v1/resumes/upload",
            files=[
                (
                    "files",
                    (
                        "another_name.pdf",
                        io.BytesIO(file_content),
                        "application/pdf",
                    ),
                )
            ],
        )

        assert second_response.status_code == 200
        second_data = second_response.json()

        assert second_data["successful"] == 0
        assert second_data["duplicates"] == 1
        assert second_data["items"][0]["status"] == "duplicate"
        assert (
            "Duplicate resume"
            in second_data["items"][0]["message"]
        )

        # Only one physical file should exist
        stored_files = list(tmp_path.iterdir())
        assert len(stored_files) == 1

    finally:
        app.dependency_overrides.clear()


def test_upload_unsupported_file_api(
    db_session,
    tmp_path,
    monkeypatch,
):
    """
    Unsupported file extension should result in a failed upload item.
    """

    monkeypatch.setattr(
        "app.core.storage.settings.STORAGE_ROOT",
        str(tmp_path),
    )

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/resumes/upload",
            files=[
                (
                    "files",
                    (
                        "resume.txt",
                        io.BytesIO(b"plain text resume"),
                        "text/plain",
                    ),
                )
            ],
        )

        assert response.status_code == 200

        data = response.json()
        assert data["successful"] == 0
        assert data["failed"] == 1
        assert data["items"][0]["status"] == "failed"
        assert (
            "Unsupported file type"
            in data["items"][0]["message"]
        )

        # Nothing should be stored
        assert list(tmp_path.iterdir()) == []

    finally:
        app.dependency_overrides.clear()


def test_upload_invalid_pdf_api(
    db_session,
    tmp_path,
    monkeypatch,
):
    """
    PDF extension with invalid content should report failed item.
    """

    monkeypatch.setattr(
        "app.core.storage.settings.STORAGE_ROOT",
        str(tmp_path),
    )

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/resumes/upload",
            files=[
                (
                    "files",
                    (
                        "resume.pdf",
                        io.BytesIO(b"This is not a real PDF file"),
                        "application/pdf",
                    ),
                )
            ],
        )

        assert response.status_code == 200

        data = response.json()
        assert data["successful"] == 0
        assert data["failed"] == 1
        assert data["items"][0]["status"] == "failed"
        assert (
            "Invalid PDF"
            in data["items"][0]["message"]
        )

        # Nothing should be stored
        assert list(tmp_path.iterdir()) == []

    finally:
        app.dependency_overrides.clear()


def test_upload_malformed_docx_api(
    db_session,
    tmp_path,
    monkeypatch,
):
    """
    DOCX signature passes initial validation, but malformed DOCX
    fails during extraction and reports failed item.
    """

    monkeypatch.setattr(
        "app.core.storage.settings.STORAGE_ROOT",
        str(tmp_path),
    )

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        client = TestClient(app)

        file_content = (
            b"PK\x03\x04"
            + b"invalid docx content"
        )

        response = client.post(
            "/api/v1/resumes/upload",
            files=[
                (
                    "files",
                    (
                        "resume.docx",
                        io.BytesIO(file_content),
                        (
                            "application/vnd.openxmlformats-officedocument"
                            ".wordprocessingml.document"
                        ),
                    ),
                )
            ],
        )

        assert response.status_code == 200

        data = response.json()
        assert data["successful"] == 0
        assert data["failed"] == 1
        assert data["items"][0]["status"] == "failed"
        assert (
            "Failed to extract text from DOCX"
            in data["items"][0]["message"]
        )

        # Nothing should be stored
        assert list(tmp_path.iterdir()) == []

    finally:
        app.dependency_overrides.clear()