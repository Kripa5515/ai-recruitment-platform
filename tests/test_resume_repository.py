from app.data.repositories.resume_repository import ResumeRepository
import pytest
from sqlalchemy.exc import IntegrityError
from app.data.models.resume import Resume

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

def test_get_resumes_by_candidate_id(db_session):
    from app.data.repositories.candidate_repository import (
        CandidateRepository,
    )
    from app.data.repositories.resume_repository import (
        ResumeRepository,
    )

    candidate_repository = CandidateRepository(db_session)
    resume_repository = ResumeRepository(db_session)

    candidate = candidate_repository.create(
        name="Kripa Kumar",
        email="kripa@example.com",
    )

    resume_repository.create(
        original_filename="resume_v1.pdf",
        file_type="pdf",
        file_size=100,
        file_hash="a" * 64,
        storage_path="storage/resumes/a.pdf",
        source_type="upload",
    )

    resume = resume_repository.get_by_hash("a" * 64)

    resume.candidate_id = candidate.id
    db_session.commit()

    resumes = resume_repository.get_by_candidate_id(
        candidate.id
    )

    assert len(resumes) == 1
    assert resumes[0].candidate_id == candidate.id


def test_get_latest_version_by_candidate_id(db_session):
    from app.data.repositories.candidate_repository import CandidateRepository

    candidate_repository = CandidateRepository(db_session)
    resume_repository = ResumeRepository(db_session)

    candidate = candidate_repository.create(
        name="Version Test",
        email="version@example.com",
    )

    resume1 = resume_repository.create(
        original_filename="resume_v1.pdf",
        file_type="pdf",
        file_size=100,
        file_hash="1" * 64,
        storage_path="storage/resumes/1.pdf",
    )
    resume1.candidate_id = candidate.id
    resume1.version = 1
    resume1.is_current = False
    db_session.commit()

    resume2 = resume_repository.create(
        original_filename="resume_v2.pdf",
        file_type="pdf",
        file_size=200,
        file_hash="2" * 64,
        storage_path="storage/resumes/2.pdf",
    )
    resume2.candidate_id = candidate.id
    resume2.version = 2
    resume2.is_current = True
    db_session.commit()

    latest_version = resume_repository.get_latest_version_by_candidate_id(
        candidate.id
    )

    assert latest_version == 2


def test_get_current_resume_by_candidate_id(db_session):
    from app.data.repositories.candidate_repository import CandidateRepository

    candidate_repository = CandidateRepository(db_session)
    resume_repository = ResumeRepository(db_session)

    candidate = candidate_repository.create(
        name="Current Resume Test",
        email="current@example.com",
    )

    old_resume = resume_repository.create(
        original_filename="old_resume.pdf",
        file_type="pdf",
        file_size=100,
        file_hash="3" * 64,
        storage_path="storage/resumes/3.pdf",
    )
    old_resume.candidate_id = candidate.id
    old_resume.version = 1
    old_resume.is_current = False
    db_session.commit()

    current_resume = resume_repository.create(
        original_filename="current_resume.pdf",
        file_type="pdf",
        file_size=200,
        file_hash="4" * 64,
        storage_path="storage/resumes/4.pdf",
    )
    current_resume.candidate_id = candidate.id
    current_resume.version = 2
    current_resume.is_current = True
    db_session.commit()

    result = resume_repository.get_current_resume_by_candidate_id(
        candidate.id
    )

    assert result is not None
    assert result.id == current_resume.id
    assert result.version == 2
    assert result.is_current is True


def test_get_next_version_by_candidate_id(db_session):
    from app.data.repositories.candidate_repository import CandidateRepository

    candidate_repository = CandidateRepository(db_session)
    resume_repository = ResumeRepository(db_session)

    candidate = candidate_repository.create(
        name="Next Version Test",
        email="next@example.com",
    )

    resume = resume_repository.create(
        original_filename="resume.pdf",
        file_type="pdf",
        file_size=100,
        file_hash="5" * 64,
        storage_path="storage/resumes/5.pdf",
    )
    resume.candidate_id = candidate.id
    resume.version = 3
    resume.is_current = True
    db_session.commit()

    next_version = resume_repository.get_next_version_by_candidate_id(
        candidate.id
    )

    assert next_version == 4


def test_get_resume_versions_by_candidate_id(db_session):
    from app.data.repositories.candidate_repository import CandidateRepository

    candidate_repository = CandidateRepository(db_session)
    resume_repository = ResumeRepository(db_session)

    candidate = candidate_repository.create(
        name="History Test",
        email="history@example.com",
    )

    resume1 = resume_repository.create(
        original_filename="resume_v1.pdf",
        file_type="pdf",
        file_size=100,
        file_hash="6" * 64,
        storage_path="storage/resumes/6.pdf",
    )
    resume1.candidate_id = candidate.id
    resume1.version = 1
    resume1.is_current = False
    db_session.commit()

    resume2 = resume_repository.create(
        original_filename="resume_v2.pdf",
        file_type="pdf",
        file_size=200,
        file_hash="7" * 64,
        storage_path="storage/resumes/7.pdf",
    )
    resume2.candidate_id = candidate.id
    resume2.version = 2
    resume2.is_current = False
    db_session.commit()

    resume3 = resume_repository.create(
        original_filename="resume_v3.pdf",
        file_type="pdf",
        file_size=300,
        file_hash="8" * 64,
        storage_path="storage/resumes/8.pdf",
    )
    resume3.candidate_id = candidate.id
    resume3.version = 3
    resume3.is_current = True
    db_session.commit()

    resumes = resume_repository.get_resume_versions_by_candidate_id(
        candidate.id
    )

    assert len(resumes) == 3
    assert resumes[0].version == 3
    assert resumes[1].version == 2
    assert resumes[2].version == 1


def test_get_latest_version_for_candidate_without_resumes(db_session):
    from app.data.repositories.candidate_repository import CandidateRepository

    candidate_repository = CandidateRepository(db_session)
    resume_repository = ResumeRepository(db_session)

    candidate = candidate_repository.create(
        name="No Resume",
        email="noresume@example.com",
    )

    latest_version = resume_repository.get_latest_version_by_candidate_id(
        candidate.id
    )

    assert latest_version == 0


def test_get_next_version_for_candidate_without_resumes(db_session):
    from app.data.repositories.candidate_repository import CandidateRepository

    candidate_repository = CandidateRepository(db_session)
    resume_repository = ResumeRepository(db_session)

    candidate = candidate_repository.create(
        name="First Resume",
        email="firstresume@example.com",
    )

    next_version = resume_repository.get_next_version_by_candidate_id(
        candidate.id
    )

    assert next_version == 1


def test_get_current_resume_returns_latest_current_version(db_session):
    from app.data.repositories.candidate_repository import CandidateRepository

    candidate_repository = CandidateRepository(db_session)
    resume_repository = ResumeRepository(db_session)

    candidate = candidate_repository.create(
        name="Current Version Test",
        email="current-version@example.com",
    )

    resume_v1 = Resume(
        original_filename="resume_v1.pdf",
        file_type="pdf",
        file_size=100,
        file_hash="a" * 64,
        storage_path="storage/resumes/a.pdf",
        source_type="upload",
        candidate_id=candidate.id,
        version=1,
        is_current=False,
    )

    resume_v2 = Resume(
        original_filename="resume_v2.pdf",
        file_type="pdf",
        file_size=200,
        file_hash="b" * 64,
        storage_path="storage/resumes/b.pdf",
        source_type="upload",
        candidate_id=candidate.id,
        version=2,
        is_current=False,
    )

    resume_v3 = Resume(
        original_filename="resume_v3.pdf",
        file_type="pdf",
        file_size=300,
        file_hash="c" * 64,
        storage_path="storage/resumes/c.pdf",
        source_type="upload",
        candidate_id=candidate.id,
        version=3,
        is_current=True,
    )

    db_session.add_all(
        [
            resume_v1,
            resume_v2,
            resume_v3,
        ]
    )

    db_session.commit()

    current_resume = (
        resume_repository.get_current_resume_by_candidate_id(
            candidate.id
        )
    )

    assert current_resume is not None
    assert current_resume.version == 3
    assert current_resume.is_current is True
    assert current_resume.original_filename == "resume_v3.pdf"



def test_only_one_current_resume_exists_after_version_creation(
    db_session,
):
    from app.data.repositories.candidate_repository import (
        CandidateRepository,
    )
    from app.services.resume_service import ResumeService

    candidate_repository = CandidateRepository(db_session)

    candidate = candidate_repository.create(
        name="Consistency Test",
        email="consistency@example.com",
    )

    resume_service = ResumeService(db_session)

    resume_v1, created_v1 = (
        resume_service.create_versioned_resume(
            original_filename="resume_v1.pdf",
            file_type="pdf",
            file_size=100,
            file_hash="d" * 64,
            storage_path="storage/resumes/d.pdf",
            candidate_id=candidate.id,
        )
    )

    resume_v2, created_v2 = (
        resume_service.create_versioned_resume(
            original_filename="resume_v2.pdf",
            file_type="pdf",
            file_size=200,
            file_hash="e" * 64,
            storage_path="storage/resumes/e.pdf",
            candidate_id=candidate.id,
        )
    )

    assert created_v1 is True
    assert created_v2 is True

    db_session.expire_all()

    current_resumes = (
        db_session.query(Resume)
        .filter(
            Resume.candidate_id == candidate.id,
            Resume.is_current.is_(True),
        )
        .all()
    )

    assert len(current_resumes) == 1
    assert current_resumes[0].version == 2
    assert current_resumes[0].id == resume_v2.id

    old_resume = db_session.get(Resume, resume_v1.id)

    assert old_resume is not None
    assert old_resume.is_current is False


def test_get_resume_versions_returns_history_in_descending_order(
    db_session,
):
    from app.data.repositories.candidate_repository import (
        CandidateRepository,
    )

    candidate_repository = CandidateRepository(db_session)
    resume_repository = ResumeRepository(db_session)

    candidate = candidate_repository.create(
        name="History Test",
        email="history@example.com",
    )

    resumes = [
        Resume(
            original_filename="resume_v1.pdf",
            file_type="pdf",
            file_size=100,
            file_hash="f" * 64,
            storage_path="storage/resumes/f.pdf",
            source_type="upload",
            candidate_id=candidate.id,
            version=1,
            is_current=False,
        ),
        Resume(
            original_filename="resume_v2.pdf",
            file_type="pdf",
            file_size=200,
            file_hash="g" * 64,
            storage_path="storage/resumes/g.pdf",
            source_type="upload",
            candidate_id=candidate.id,
            version=2,
            is_current=False,
        ),
        Resume(
            original_filename="resume_v3.pdf",
            file_type="pdf",
            file_size=300,
            file_hash="h" * 64,
            storage_path="storage/resumes/h.pdf",
            source_type="upload",
            candidate_id=candidate.id,
            version=3,
            is_current=True,
        ),
    ]

    db_session.add_all(resumes)
    db_session.commit()

    history = (
        resume_repository.get_resume_versions_by_candidate_id(
            candidate.id
        )
    )

    assert len(history) == 3

    assert [resume.version for resume in history] == [
        3,
        2,
        1,
    ]

    assert history[0].is_current is True
    assert history[1].is_current is False
    assert history[2].is_current is False

def test_get_current_resume_for_candidate_without_resumes(
    db_session,
):
    from app.data.repositories.candidate_repository import (
        CandidateRepository,
    )

    candidate_repository = CandidateRepository(db_session)
    resume_repository = ResumeRepository(db_session)

    candidate = candidate_repository.create(
        name="No Resume Candidate",
        email="no-resume@example.com",
    )

    current_resume = (
        resume_repository.get_current_resume_by_candidate_id(
            candidate.id
        )
    )

    assert current_resume is None


def test_resume_versions_are_isolated_per_candidate(
    db_session,
):
    from app.data.repositories.candidate_repository import (
        CandidateRepository,
    )
    from app.services.resume_service import ResumeService

    candidate_repository = CandidateRepository(db_session)

    candidate_1 = candidate_repository.create(
        name="Candidate One",
        email="candidate-one@example.com",
    )

    candidate_2 = candidate_repository.create(
        name="Candidate Two",
        email="candidate-two@example.com",
    )

    resume_service = ResumeService(db_session)

    resume_1, created_1 = (
        resume_service.create_versioned_resume(
            original_filename="candidate1_v1.pdf",
            file_type="pdf",
            file_size=100,
            file_hash="i" * 64,
            storage_path="storage/resumes/i.pdf",
            candidate_id=candidate_1.id,
        )
    )

    resume_2, created_2 = (
        resume_service.create_versioned_resume(
            original_filename="candidate2_v1.pdf",
            file_type="pdf",
            file_size=100,
            file_hash="j" * 64,
            storage_path="storage/resumes/j.pdf",
            candidate_id=candidate_2.id,
        )
    )

    assert created_1 is True
    assert created_2 is True

    assert resume_1.version == 1
    assert resume_2.version == 1

    assert resume_1.candidate_id == candidate_1.id
    assert resume_2.candidate_id == candidate_2.id

    assert resume_1.is_current is True
    assert resume_2.is_current is True
