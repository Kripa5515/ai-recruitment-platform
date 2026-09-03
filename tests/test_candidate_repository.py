from app.data.repositories.candidate_repository import CandidateRepository

def test_create_candidate(db_session):
    repository = CandidateRepository(db_session)

    candidate = repository.create(
        name="Kripa Kumar",
        email="kripa@example.com",
        phone="9876543210",
        total_experience_years=6.5,
    )

    assert candidate.id is not None
    assert candidate.name == "Kripa Kumar"
    assert candidate.email == "kripa@example.com"
    assert candidate.phone == "9876543210"
    assert candidate.total_experience_years == 6.5


def test_get_candidate_by_id(db_session):
    repository = CandidateRepository(db_session)

    created = repository.create(
        name="John Developer",
        email="john@example.com",
    )

    candidate = repository.get_by_id(created.id)

    assert candidate is not None
    assert candidate.id == created.id
    assert candidate.name == "John Developer"


def test_get_candidate_by_id_returns_none_for_missing_candidate(
    db_session,
):
    repository = CandidateRepository(db_session)

    candidate = repository.get_by_id(999999)

    assert candidate is None


def test_get_all_candidates(db_session):
    repository = CandidateRepository(db_session)

    repository.create(
        name="Candidate One",
        email="one@example.com",
    )

    repository.create(
        name="Candidate Two",
        email="two@example.com",
    )

    candidates = repository.get_all()

    assert len(candidates) == 2
    assert candidates[0].name == "Candidate One"
    assert candidates[1].name == "Candidate Two"


def test_get_candidate_by_email(db_session):
    repository = CandidateRepository(db_session)

    repository.create(
        name="Email Candidate",
        email="candidate@example.com",
    )

    candidate = repository.get_by_email(
        "candidate@example.com"
    )

    assert candidate is not None
    assert candidate.name == "Email Candidate"


def test_get_candidate_resumes(db_session):
    from app.data.repositories.resume_repository import (
        ResumeRepository,
    )

    candidate_repository = CandidateRepository(db_session)
    resume_repository = ResumeRepository(db_session)

    candidate = candidate_repository.create(
        name="Relationship Candidate",
        email="relationship@example.com",
    )

    resume_repository.create(
        original_filename="candidate.pdf",
        file_type="pdf",
        file_size=100,
        file_hash="b" * 64,
        storage_path="storage/resumes/b.pdf",
        source_type="upload",
    )

    resume = resume_repository.get_by_hash("b" * 64)
    resume.candidate_id = candidate.id
    db_session.commit()

    resumes = candidate_repository.get_resumes(
        candidate.id
    )

    assert resumes is not None
    assert len(resumes) == 1
    assert resumes[0].original_filename == "candidate.pdf"