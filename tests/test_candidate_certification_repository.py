from app.data.models.candidate import Candidate
from app.data.repositories.candidate_certification_repository import (
    CandidateCertificationRepository,
)

def test_create_certification(db_session):
    candidate = Candidate(
        name="Test Candidate",
        email="certification-test@example.com",
    )

    db_session.add(candidate)
    db_session.commit()
    db_session.refresh(candidate)

    repository = CandidateCertificationRepository(db_session)

    certification = repository.create(
        candidate_id=candidate.id,
        certification="AWS Certified Developer",
    )

    assert certification.id is not None
    assert certification.candidate_id == candidate.id
    assert certification.certification == "AWS Certified Developer"


def test_get_by_candidate_id(db_session):
    candidate = Candidate(
        name="Test Candidate",
        email="get-certifications@example.com",
    )

    db_session.add(candidate)
    db_session.commit()
    db_session.refresh(candidate)

    repository = CandidateCertificationRepository(db_session)

    repository.create(candidate.id, "AWS Certified Developer")
    repository.create(candidate.id, "Azure Developer Associate")

    certifications = repository.get_by_candidate_id(
        candidate.id
    )

    assert len(certifications) == 2
    assert (
        certifications[0].certification
        == "AWS Certified Developer"
    )
    assert (
        certifications[1].certification
        == "Azure Developer Associate"
    )


def test_get_by_candidate_id_returns_empty_list(db_session):
    candidate = Candidate(
        name="Test Candidate",
        email="empty-certifications@example.com",
    )

    db_session.add(candidate)
    db_session.commit()
    db_session.refresh(candidate)

    repository = CandidateCertificationRepository(db_session)

    certifications = repository.get_by_candidate_id(
        candidate.id
    )

    assert certifications == []


def test_delete_by_candidate_id(db_session):
    candidate = Candidate(
        name="Test Candidate",
        email="delete-certifications@example.com",
    )

    db_session.add(candidate)
    db_session.commit()
    db_session.refresh(candidate)

    repository = CandidateCertificationRepository(db_session)

    repository.create(candidate.id, "AWS Certified Developer")
    repository.create(candidate.id, "Azure Developer Associate")

    deleted_count = repository.delete_by_candidate_id(
        candidate.id
    )

    assert deleted_count == 2
    assert repository.get_by_candidate_id(candidate.id) == []