from app.data.repositories.resume_repository import ResumeRepository
import pytest
from sqlalchemy.exc import IntegrityError

def test_create_resume(db_session):
    repository = ResumeRepository(db_session)
    resume = repository.create(
        original_filename="kripa_resume.pdf",
        file_type="pdf",
        file_size=1024,
        file_hash="a" * 64,
        storage_path="storage/resumes/test.pdf",
    )

    assert resume.id is not None
    assert resume.original_filename == "kripa_resume.pdf"
    assert resume.file_type == "pdf"
    assert resume.file_size == 1024
    assert resume.file_hash == "a" * 64
    assert resume.storage_path == "storage/resumes/test.pdf"
    assert resume.source_type == "upload"
    assert resume.extraction_status == "uploaded"


def test_get_resume_by_id(db_session):
    repository = ResumeRepository(db_session)
    created = repository.create(
        original_filename="resume.pdf",
        file_type="pdf",
        file_size=2048,
        file_hash="b" * 64,
        storage_path="storage/resumes/resume.pdf",
    )

    resume = repository.get_by_id(created.id)
    assert resume is not None
    assert resume.id == created.id


def test_get_resume_by_hash(db_session):
    repository = ResumeRepository(db_session)
    file_hash = "c" * 64
    created = repository.create(
        original_filename="resume.pdf",
        file_type="pdf",
        file_size=3000,
        file_hash=file_hash,
        storage_path="storage/resumes/resume.pdf",
    )

    resume = repository.get_by_hash(file_hash)

    assert resume is not None
    assert resume.id == created.id
    assert resume.file_hash == file_hash


def test_get_resume_by_unknown_hash(db_session):
    repository = ResumeRepository(db_session)
    resume = repository.get_by_hash("d" * 64)
    assert resume is None


def test_get_all_resumes(db_session):
    repository = ResumeRepository(db_session)
    repository.create(
        original_filename="resume1.pdf",
        file_type="pdf",
        file_size=1000,
        file_hash="e" * 64,
        storage_path="storage/resumes/resume1.pdf",
    )

    repository.create(
        original_filename="resume2.docx",
        file_type="docx",
        file_size=2000,
        file_hash="f" * 64,
        storage_path="storage/resumes/resume2.docx",
    )

    resumes = repository.get_all()
    assert len(resumes) >= 2

def test_create_duplicate_resume_hash(db_session):
    repository = ResumeRepository(db_session)
    file_hash = "duplicate" + ("a" * 55)
    repository.create(
        original_filename="resume1.pdf",
        file_type="pdf",
        file_size=1000,
        file_hash=file_hash,
        storage_path="storage/resumes/resume1.pdf",
    )

    with pytest.raises(IntegrityError):
        repository.create(
            original_filename="resume2.pdf",
            file_type="pdf",
            file_size=2000,
            file_hash=file_hash,
            storage_path="storage/resumes/resume2.pdf",
        )

def test_get_resume_by_storage_path(db_session):
    repository = ResumeRepository(db_session)

    resume = repository.create(
        original_filename="kripa_resume.pdf",
        file_type="pdf",
        file_size=1000,
        file_hash="a" * 64,
        storage_path="storage/resumes/" + "a" * 64 + ".pdf",
    )

    result = repository.get_by_storage_path(
        resume.storage_path
    )

    assert result is not None
    assert result.id == resume.id
    assert result.storage_path == resume.storage_path

def test_get_resume_by_unknown_storage_path(db_session):
    repository = ResumeRepository(db_session)

    result = repository.get_by_storage_path(
        "storage/resumes/not-found.pdf"
    )

    assert result is None

def test_get_resume_by_source_reference(db_session):
    repository = ResumeRepository(db_session)

    resume = repository.create(
        original_filename="kripa_resume.pdf",
        file_type="pdf",
        file_size=1000,
        file_hash="c" * 64,
        storage_path="storage/resumes/" + "c" * 64 + ".pdf",
        source_type="ats",
        source_reference="ATS-12345",
    )

    result = repository.get_by_source_reference(
        source_type="ats",
        source_reference="ATS-12345",
    )

    assert result is not None
    assert result.id == resume.id
    assert result.source_type == "ats"
    assert result.source_reference == "ATS-12345"

def test_get_resume_by_unknown_source_reference(db_session):
    repository = ResumeRepository(db_session)

    result = repository.get_by_source_reference(
        source_type="ats",
        source_reference="NOT-FOUND",
    )

    assert result is None