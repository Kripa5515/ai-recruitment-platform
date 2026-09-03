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

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        client = TestClient(app)

        file_content = create_test_pdf()

        response = client.post(
            "/resumes/upload",
            files={
                "file": (
                    "kripa_resume.pdf",
                    io.BytesIO(file_content),
                    "application/pdf",
                )
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["id"] is not None

        assert data["original_filename"] == "kripa_resume.pdf"

        assert data["file_type"] == "pdf"

        assert data["file_size"] == len(file_content)

        assert len(data["file_hash"]) == 64

        assert data["storage_path"].endswith(".pdf")

        assert data["extracted_text"] is not None

        assert "Kripa Kumar" in data["extracted_text"]

        assert (
            "Senior PHP Laravel Developer"
            in data["extracted_text"]
        )

        assert (
            "Python GenAI RAG Developer"
            in data["extracted_text"]
        )

        assert data["extraction_status"] == "completed"

        saved_file = (
            tmp_path
            / Path(data["storage_path"]).name
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
    Same resume uploaded twice should return 409 Conflict.
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

        file_content = create_test_pdf(
            "Duplicate Resume Test"
        )

        # -----------------------------------------------------
        # First upload
        # -----------------------------------------------------

        first_response = client.post(
            "/resumes/upload",
            files={
                "file": (
                    "kripa_resume.pdf",
                    io.BytesIO(file_content),
                    "application/pdf",
                )
            },
        )

        assert first_response.status_code == 200

        # -----------------------------------------------------
        # Second upload with same content
        # -----------------------------------------------------

        second_response = client.post(
            "/resumes/upload",
            files={
                "file": (
                    "another_name.pdf",
                    io.BytesIO(file_content),
                    "application/pdf",
                )
            },
        )

        assert second_response.status_code == 409

        data = second_response.json()

        assert data["detail"] == (
            "A resume with the same file already exists."
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
    Unsupported file extension should return 400 Bad Request.
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
            "/resumes/upload",
            files={
                "file": (
                    "resume.txt",
                    io.BytesIO(
                        b"plain text resume"
                    ),
                    "text/plain",
                )
            },
        )

        assert response.status_code == 400

        data = response.json()

        assert data["detail"] == (
            "Unsupported file type. "
            "Only PDF and DOCX files are allowed."
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
    PDF extension with invalid content should return 400.
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
            "/resumes/upload",
            files={
                "file": (
                    "resume.pdf",
                    io.BytesIO(
                        b"This is not a real PDF file"
                    ),
                    "application/pdf",
                )
            },
        )

        assert response.status_code == 400

        data = response.json()

        assert data["detail"] == (
            "Invalid PDF file content."
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
    DOCX signature may look valid, but malformed DOCX
    should fail during actual DOCX extraction.
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

        # PK signature passes initial validation,
        # but this is not a real DOCX file.
        file_content = (
            b"PK\x03\x04"
            + b"invalid docx content"
        )

        response = client.post(
            "/resumes/upload",
            files={
                "file": (
                    "resume.docx",
                    io.BytesIO(file_content),
                    (
                        "application/vnd.openxmlformats-officedocument"
                        ".wordprocessingml.document"
                    ),
                )
            },
        )

        assert response.status_code == 422

        data = response.json()

        assert data["detail"] == (
            "Failed to extract text from DOCX."
        )

        # Nothing should be stored
        assert list(tmp_path.iterdir()) == []

    finally:
        app.dependency_overrides.clear()