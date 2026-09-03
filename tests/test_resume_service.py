from app.services.resume_service import ResumeService
from app.services.exceptions import DuplicateResumeError
from pathlib import Path
import pytest

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

def test_upload_resume_creates_resume_and_saves_file(
    db_session,
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        "app.core.storage.settings.STORAGE_ROOT",
        str(tmp_path),
    )

    service = ResumeService(db_session)

    file_content = b"%PDF-1.7 sample resume content"

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
    assert resume.extraction_status == "uploaded"

    saved_file = tmp_path / resume.storage_path.split("/")[-1]

    assert saved_file.exists()
    assert saved_file.read_bytes() == file_content

def test_upload_duplicate_resume_is_rejected(
    db_session,
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        "app.core.storage.settings.STORAGE_ROOT",
        str(tmp_path),
    )

    service = ResumeService(db_session)

    file_content = b"%PDF-1.7 duplicate resume content"

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

    # Same physical file should be used
    stored_files = list(tmp_path.iterdir())

    assert len(stored_files) == 1
    assert stored_files[0].name == Path(first_resume.storage_path).name

def test_upload_resume_rejects_unsupported_file(
    db_session,
    tmp_path,
    monkeypatch,
):
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

    assert list(tmp_path.iterdir()) == []
    assert service.get_all_resumes() == []

def test_upload_resume_rejects_invalid_pdf(
    db_session,
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        "app.core.storage.settings.STORAGE_ROOT",
        str(tmp_path),
    )

    service = ResumeService(db_session)

    # PDF extension hai, lekin actual PDF content nahi hai
    file_content = b"This is not a real PDF file"

    with pytest.raises(ValueError):
        service.upload_resume(
            filename="resume.pdf",
            content_type="application/pdf",
            file_content=file_content,
        )

    assert list(tmp_path.iterdir()) == []
    assert service.get_all_resumes() == []

def test_upload_docx_resume_creates_resume_and_saves_file(
    db_session,
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        "app.core.storage.settings.STORAGE_ROOT",
        str(tmp_path),
    )

    service = ResumeService(db_session)

    # Minimal valid DOCX/ZIP signature.
    file_content = b"PK\x03\x04" + b"sample docx content"

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
    assert resume.extraction_status == "uploaded"

    saved_file = tmp_path / Path(resume.storage_path).name

    assert saved_file.exists()
    assert saved_file.read_bytes() == file_content