import io
from pathlib import Path

import pytest
import pymupdf
from docx import Document

from app.services.exceptions import DuplicateResumeError
from app.services.resume_service import ResumeService


def create_test_pdf(text: str) -> bytes:
    """
    Create a real PDF file in memory for testing.
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


def create_test_docx() -> bytes:
    """
    Create a real DOCX file in memory for testing.
    """

    document = Document()

    document.add_paragraph("Kripa Kumar")
    document.add_paragraph("Senior PHP Laravel Developer")
    document.add_paragraph("Python GenAI RAG Developer")
    document.add_paragraph(
        "Skills: PHP, Laravel, Python, PostgreSQL"
    )

    output = io.BytesIO()

    document.save(output)

    return output.getvalue()


def test_create_resume(db_session):
    service = ResumeService(db_session)

    resume = service.create_resume(
        original_filename="service_resume.pdf",
        file_type="pdf",
        file_size=1024,
        file_hash="1" * 64,
        storage_path="storage/resumes/service_resume.pdf",
    )

    assert resume.id is not None
    assert resume.original_filename == "service_resume.pdf"
    assert resume.file_type == "pdf"
    assert resume.file_size == 1024
    assert resume.file_hash == "1" * 64
    assert resume.source_type == "upload"
    assert resume.extraction_status == "uploaded"


def test_get_resume(db_session):
    service = ResumeService(db_session)

    created = service.create_resume(
        original_filename="resume.pdf",
        file_type="pdf",
        file_size=2000,
        file_hash="2" * 64,
        storage_path="storage/resumes/resume.pdf",
    )

    resume = service.get_resume(created.id)

    assert resume is not None
    assert resume.id == created.id


def test_get_resume_by_hash(db_session):
    service = ResumeService(db_session)

    file_hash = "3" * 64

    created = service.create_resume(
        original_filename="resume.pdf",
        file_type="pdf",
        file_size=3000,
        file_hash=file_hash,
        storage_path="storage/resumes/resume.pdf",
    )

    resume = service.get_resume_by_hash(file_hash)

    assert resume is not None
    assert resume.id == created.id


def test_get_unknown_resume(db_session):
    service = ResumeService(db_session)

    resume = service.get_resume(999999)

    assert resume is None


def test_get_all_resumes(db_session):
    service = ResumeService(db_session)

    service.create_resume(
        original_filename="resume1.pdf",
        file_type="pdf",
        file_size=1000,
        file_hash="4" * 64,
        storage_path="storage/resumes/resume1.pdf",
    )

    service.create_resume(
        original_filename="resume2.docx",
        file_type="docx",
        file_size=2000,
        file_hash="5" * 64,
        storage_path="storage/resumes/resume2.docx",
    )

    resumes = service.get_all_resumes()

    assert len(resumes) >= 2


def test_create_duplicate_resume_hash(db_session):
    service = ResumeService(db_session)

    file_hash = "duplicate" + ("b" * 55)

    service.create_resume(
        original_filename="resume1.pdf",
        file_type="pdf",
        file_size=1000,
        file_hash=file_hash,
        storage_path="storage/resumes/resume1.pdf",
    )

    with pytest.raises(DuplicateResumeError):
        service.create_resume(
            original_filename="resume2.pdf",
            file_type="pdf",
            file_size=2000,
            file_hash=file_hash,
            storage_path="storage/resumes/resume2.pdf",
        )


def test_upload_pdf_resume_creates_resume_and_extracts_text(
    db_session,
    tmp_path,
    monkeypatch,
):
    """
    Test complete PDF upload flow:

    validation
        ↓
    hash calculation
        ↓
    duplicate check
        ↓
    PDF text extraction
        ↓
    file storage
        ↓
    database record
    """

    monkeypatch.setattr(
        "app.core.storage.settings.STORAGE_ROOT",
        str(tmp_path),
    )

    service = ResumeService(db_session)

    file_content = create_test_pdf(
        "Kripa Kumar\n"
        "Senior PHP Laravel Developer\n"
        "Python GenAI RAG Developer"
    )

    resume = service.upload_resume(
        filename="kripa_resume.pdf",
        content_type="application/pdf",
        file_content=file_content,
    )

    assert resume.id is not None

    assert resume.original_filename == "kripa_resume.pdf"

    assert resume.file_type == "pdf"

    assert resume.file_size == len(file_content)

    assert len(resume.file_hash) == 64

    assert resume.storage_path.endswith(".pdf")

    # Verify extracted text
    assert resume.extracted_text is not None

    assert "Kripa Kumar" in resume.extracted_text

    assert "Senior PHP Laravel Developer" in resume.extracted_text

    assert "Python GenAI RAG Developer" in resume.extracted_text

    # Extraction should be completed
    assert resume.extraction_status == "completed"

    # Verify physical file exists
    saved_file = tmp_path / Path(resume.storage_path).name

    assert saved_file.exists()

    # Verify stored file is exactly the original bytes
    assert saved_file.read_bytes() == file_content


def test_upload_duplicate_pdf_resume_is_rejected(
    db_session,
    tmp_path,
    monkeypatch,
):
    """
    Same file content should produce the same SHA-256 hash
    and duplicate upload should be rejected.
    """

    monkeypatch.setattr(
        "app.core.storage.settings.STORAGE_ROOT",
        str(tmp_path),
    )

    service = ResumeService(db_session)

    file_content = create_test_pdf(
        "Duplicate Resume Test"
    )

    # First upload
    first_resume = service.upload_resume(
        filename="kripa_resume.pdf",
        content_type="application/pdf",
        file_content=file_content,
    )

    # Second upload with exactly same content
    with pytest.raises(DuplicateResumeError):
        service.upload_resume(
            filename="another_name.pdf",
            content_type="application/pdf",
            file_content=file_content,
        )

    # Only one physical file should exist
    stored_files = list(tmp_path.iterdir())

    assert len(stored_files) == 1

    # Physical filename should be hash based
    assert (
        stored_files[0].name
        == Path(first_resume.storage_path).name
    )


def test_upload_resume_rejects_unsupported_file(
    db_session,
    tmp_path,
    monkeypatch,
):
    """
    TXT files are not supported.
    """

    monkeypatch.setattr(
        "app.core.storage.settings.STORAGE_ROOT",
        str(tmp_path),
    )

    service = ResumeService(db_session)

    file_content = b"plain text resume"

    with pytest.raises(ValueError):
        service.upload_resume(
            filename="resume.txt",
            content_type="text/plain",
            file_content=file_content,
        )

    # No file should be saved
    assert list(tmp_path.iterdir()) == []

    # No database record should be created
    assert service.get_all_resumes() == []


def test_upload_resume_rejects_invalid_pdf(
    db_session,
    tmp_path,
    monkeypatch,
):
    """
    File has .pdf extension but does not contain
    valid PDF signature.
    """

    monkeypatch.setattr(
        "app.core.storage.settings.STORAGE_ROOT",
        str(tmp_path),
    )

    service = ResumeService(db_session)

    file_content = b"This is not a real PDF file"

    with pytest.raises(ValueError):
        service.upload_resume(
            filename="resume.pdf",
            content_type="application/pdf",
            file_content=file_content,
        )

    # No file should be saved
    assert list(tmp_path.iterdir()) == []

    # No database record should be created
    assert service.get_all_resumes() == []


def test_upload_docx_resume_creates_resume_and_extracts_text(
    db_session,
    tmp_path,
    monkeypatch,
):
    """
    Test complete DOCX upload and text extraction flow.
    """

    monkeypatch.setattr(
        "app.core.storage.settings.STORAGE_ROOT",
        str(tmp_path),
    )

    service = ResumeService(db_session)

    # Create a REAL DOCX file
    file_content = create_test_docx()

    resume = service.upload_resume(
        filename="kripa_resume.docx",
        content_type=(
            "application/vnd.openxmlformats-officedocument"
            ".wordprocessingml.document"
        ),
        file_content=file_content,
    )

    assert resume.id is not None

    assert resume.original_filename == "kripa_resume.docx"

    assert resume.file_type == "docx"

    assert resume.file_size == len(file_content)

    assert len(resume.file_hash) == 64

    assert resume.storage_path.endswith(".docx")

    # Verify extracted text
    assert resume.extracted_text is not None

    assert "Kripa Kumar" in resume.extracted_text

    assert "Senior PHP Laravel Developer" in resume.extracted_text

    assert "Python GenAI RAG Developer" in resume.extracted_text

    assert "PostgreSQL" in resume.extracted_text

    # Extraction should be completed
    assert resume.extraction_status == "completed"

    # Verify physical file exists
    saved_file = tmp_path / Path(resume.storage_path).name

    assert saved_file.exists()

    # Verify stored file is exactly the original bytes
    assert saved_file.read_bytes() == file_content


def test_upload_resume_rejects_invalid_docx(
    db_session,
    tmp_path,
    monkeypatch,
):
    """
    File has .docx extension and ZIP signature,
    but is not actually a valid DOCX document.
    """

    monkeypatch.setattr(
        "app.core.storage.settings.STORAGE_ROOT",
        str(tmp_path),
    )

    service = ResumeService(db_session)

    # ZIP signature exists, but this is not a valid DOCX
    file_content = b"PK\x03\x04" + b"invalid docx content"

    with pytest.raises(ValueError):
        service.upload_resume(
            filename="resume.docx",
            content_type=(
                "application/vnd.openxmlformats-officedocument"
                ".wordprocessingml.document"
            ),
            file_content=file_content,
        )

    # Nothing should be stored
    assert list(tmp_path.iterdir()) == []

    # No database record should be created
    assert service.get_all_resumes() == []


def test_get_resume_by_storage_path(db_session):
    service = ResumeService(db_session)

    resume = service.create_resume(
        original_filename="kripa_resume.pdf",
        file_type="pdf",
        file_size=1000,
        file_hash="b" * 64,
        storage_path="storage/resumes/" + "b" * 64 + ".pdf",
    )

    result = service.get_resume_by_storage_path(
        resume.storage_path
    )

    assert result is not None
    assert result.id == resume.id
    assert result.storage_path == resume.storage_path

def test_get_unknown_resume_by_storage_path(db_session):
    service = ResumeService(db_session)

    result = service.get_resume_by_storage_path(
        "storage/resumes/not-found.pdf"
    )

    assert result is None

def test_get_resume_by_source_reference(db_session):
    service = ResumeService(db_session)

    resume = service.create_resume(
        original_filename="kripa_resume.pdf",
        file_type="pdf",
        file_size=1000,
        file_hash="d" * 64,
        storage_path="storage/resumes/" + "d" * 64 + ".pdf",
        source_type="ats",
        source_reference="ATS-67890",
    )

    result = service.get_resume_by_source_reference(
        source_type="ats",
        source_reference="ATS-67890",
    )

    assert result is not None
    assert result.id == resume.id
    assert result.source_reference == "ATS-67890"

def test_get_unknown_resume_by_source_reference(db_session):
    service = ResumeService(db_session)

    result = service.get_resume_by_source_reference(
        source_type="ats",
        source_reference="NOT-FOUND",
    )

    assert result is None

def test_get_or_create_resume_creates_new_resume(
    db_session,
):
    service = ResumeService(db_session)

    resume, created = service.get_or_create_resume(
        original_filename="new_resume.pdf",
        file_type="pdf",
        file_size=1000,
        file_hash="e" * 64,
        storage_path=(
            "storage/resumes/"
            + "e" * 64
            + ".pdf"
        ),
    )

    assert created is True
    assert resume.id is not None
    assert resume.original_filename == "new_resume.pdf"

def test_get_or_create_resume_reuses_existing_resume(
    db_session,
):
    service = ResumeService(db_session)
    first_resume, first_created = (
        service.get_or_create_resume(
            original_filename="resume.pdf",
            file_type="pdf",
            file_size=1000,
            file_hash="f" * 64,
            storage_path=(
                "storage/resumes/"
                + "f" * 64
                + ".pdf"
            ),
        )
    )

    second_resume, second_created = (
        service.get_or_create_resume(
            original_filename="same_resume_different_name.pdf",
            file_type="pdf",
            file_size=1000,
            file_hash="f" * 64,
            storage_path=(
                "storage/resumes/"
                + "f" * 64
                + ".pdf"
            ),
        )
    )

    assert first_created is True
    assert second_created is False

    assert second_resume.id == first_resume.id