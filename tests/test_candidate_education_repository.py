from app.data.models.candidate import Candidate
from app.data.repositories.candidate_education_repository import (
    CandidateEducationRepository,
)

def test_create_education(db_session):
    candidate = Candidate(
        name="Test Candidate",
        email="education-test@example.com",
    )

    db_session.add(candidate)
    db_session.commit()
    db_session.refresh(candidate)

    repository = CandidateEducationRepository(db_session)

    education = repository.create(
        candidate_id=candidate.id,
        education="B.Tech Computer Science",
    )

    assert education.id is not None
    assert education.candidate_id == candidate.id
    assert education.education == "B.Tech Computer Science"


def test_get_by_candidate_id(db_session):
    candidate = Candidate(
        name="Test Candidate",
        email="get-education@example.com",
    )

    db_session.add(candidate)
    db_session.commit()
    db_session.refresh(candidate)

    repository = CandidateEducationRepository(db_session)

    repository.create(candidate.id, "B.Tech Computer Science")
    repository.create(candidate.id, "MBA")

    education_records = repository.get_by_candidate_id(candidate.id)

    assert len(education_records) == 2
    assert education_records[0].education == "B.Tech Computer Science"
    assert education_records[1].education == "MBA"


def test_get_by_candidate_id_returns_empty_list(db_session):
    candidate = Candidate(
        name="Test Candidate",
        email="empty-education@example.com",
    )

    db_session.add(candidate)
    db_session.commit()
    db_session.refresh(candidate)

    repository = CandidateEducationRepository(db_session)

    education_records = repository.get_by_candidate_id(candidate.id)

    assert education_records == []


def test_delete_by_candidate_id(db_session):
    candidate = Candidate(
        name="Test Candidate",
        email="delete-education@example.com",
    )

    db_session.add(candidate)
    db_session.commit()
    db_session.refresh(candidate)

    repository = CandidateEducationRepository(db_session)

    repository.create(candidate.id, "B.Tech")
    repository.create(candidate.id, "M.Tech")

    deleted_count = repository.delete_by_candidate_id(
        candidate.id
    )

    assert deleted_count == 2
    assert repository.get_by_candidate_id(candidate.id) == []