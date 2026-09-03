from app.api.schemas.candidate import CandidateProfile
from app.services.candidate_service import CandidateService
import pytest

def test_create_candidate(db_session):
    service = CandidateService(db_session)

    profile = CandidateProfile(
        name="Kripa Kumar",
        email="kripa@example.com",
        phone="9876543210",
        total_experience_years=6.5,
    )

    candidate = service.create_candidate(profile)

    assert candidate.id is not None
    assert candidate.name == "Kripa Kumar"
    assert candidate.email == "kripa@example.com"
    assert candidate.phone == "9876543210"
    assert candidate.total_experience_years == 6.5


def test_get_candidate(db_session):
    service = CandidateService(db_session)

    profile = CandidateProfile(
        name="John Developer",
        email="john@example.com",
    )

    created = service.create_candidate(profile)

    candidate = service.get_candidate(created.id)

    assert candidate is not None
    assert candidate.id == created.id
    assert candidate.name == "John Developer"


def test_get_candidate_returns_none_for_missing_candidate(
    db_session,
):
    service = CandidateService(db_session)

    candidate = service.get_candidate(999999)

    assert candidate is None


def test_get_all_candidates(db_session):
    service = CandidateService(db_session)

    service.create_candidate(
        CandidateProfile(
            name="Candidate One",
            email="one@example.com",
        )
    )

    service.create_candidate(
        CandidateProfile(
            name="Candidate Two",
            email="two@example.com",
        )
    )

    candidates = service.get_all_candidates()

    assert len(candidates) == 2
    assert candidates[0].name == "Candidate One"
    assert candidates[1].name == "Candidate Two"


def test_get_candidate_by_email(db_session):
    service = CandidateService(db_session)

    service.create_candidate(
        CandidateProfile(
            name="Email Candidate",
            email="candidate@example.com",
        )
    )

    candidate = service.get_candidate_by_email(
        "candidate@example.com"
    )

    assert candidate is not None
    assert candidate.name == "Email Candidate"

def test_create_candidate_profile_persists_all_details(
    db_session,
):
    profile = CandidateProfile(
        name="Test Candidate",
        email="profile@example.com",
        phone="9876543210",
        total_experience_years=6.5,
        skills=["Python", "Laravel", "PostgreSQL"],
        education=["B.Tech Computer Science"],
        projects=[
            "AI Recruitment Platform",
            "School Management System",
        ],
        certifications=[
            "AWS Certified Developer",
        ],
    )

    service = CandidateService(db_session)

    candidate = service.create_candidate_profile(profile)

    assert candidate.id is not None
    assert candidate.name == "Test Candidate"
    assert candidate.email == "profile@example.com"
    assert candidate.phone == "9876543210"
    assert candidate.total_experience_years == 6.5

    assert [skill.skill_name for skill in candidate.skills] == [
        "Python",
        "Laravel",
        "PostgreSQL",
    ]

    assert [education.education for education in candidate.education] == [
        "B.Tech Computer Science",
    ]

    assert [project.project for project in candidate.projects] == [
        "AI Recruitment Platform",
        "School Management System",
    ]

    assert [
        certification.certification
        for certification in candidate.certifications
    ] == [
        "AWS Certified Developer",
    ]


def test_create_candidate_profile_with_empty_details(
    db_session,
):
    profile = CandidateProfile(
        name="Minimal Candidate",
        email="minimal@example.com",
        skills=[],
        education=[],
        projects=[],
        certifications=[],
    )

    service = CandidateService(db_session)

    candidate = service.create_candidate_profile(profile)

    assert candidate.id is not None
    assert candidate.name == "Minimal Candidate"
    assert candidate.skills == []
    assert candidate.education == []
    assert candidate.projects == []
    assert candidate.certifications == []


def test_create_candidate_profile_rolls_back_on_error(
    db_session,
    monkeypatch,
):
    profile = CandidateProfile(
        name="Rollback Candidate",
        email="rollback@example.com",
        phone="9876543210",
        total_experience_years=6.5,
        skills=["Python", "Laravel"],
        education=["B.Tech"],
        projects=["AI Recruitment Platform"],
        certifications=["AWS Certified Developer"],
    )

    service = CandidateService(db_session)

    def fail_create(*args, **kwargs):
        raise RuntimeError("Certification persistence failed")

    monkeypatch.setattr(
        service.certification_repository,
        "create",
        fail_create,
    )

    with pytest.raises(
        RuntimeError,
        match="Certification persistence failed",
    ):
        service.create_candidate_profile(profile)

    assert (
        service.repository.get_by_email(
            "rollback@example.com"
        )
        is None
    )