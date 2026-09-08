import pytest

from app.api.schemas.candidate import CandidateProfile
from app.api.schemas.job_requirements import JobRequirements
from app.ai.matching.matching_service import MatchingService


@pytest.fixture
def matching_service() -> MatchingService:
    return MatchingService()


def test_experience_match_when_candidate_meets_requirement(
    matching_service: MatchingService,
):
    result = matching_service.match_experience(
        required_experience_years=5,
        candidate_experience_years=6,
    )

    assert result.meets_requirement is True
    assert result.score == 100.0


def test_experience_match_when_candidate_has_less_experience(
    matching_service: MatchingService,
):
    result = matching_service.match_experience(
        required_experience_years=5,
        candidate_experience_years=3,
    )

    assert result.meets_requirement is False
    assert result.score == 60.0


def test_experience_match_when_requirement_is_missing(
    matching_service: MatchingService,
):
    result = matching_service.match_experience(
        required_experience_years=None,
        candidate_experience_years=6,
    )

    assert result.meets_requirement is None
    assert result.score == 100.0


def test_experience_match_when_candidate_experience_is_missing(
    matching_service: MatchingService,
):
    result = matching_service.match_experience(
        required_experience_years=5,
        candidate_experience_years=None,
    )

    assert result.meets_requirement is False
    assert result.score == 0.0


def test_required_skills_full_match(
    matching_service: MatchingService,
):
    result = matching_service.match_skills(
        required_skills=[
            "Python",
            "FastAPI",
            "PostgreSQL",
        ],
        preferred_skills=[],
        candidate_skills=[
            "Python",
            "FastAPI",
            "PostgreSQL",
        ],
    )

    assert result.required_skill_score == 100.0

    assert result.matched_required_skills == [
        "Python",
        "FastAPI",
        "PostgreSQL",
    ]

    assert result.missing_required_skills == []


def test_required_skills_partial_match(
    matching_service: MatchingService,
):
    result = matching_service.match_skills(
        required_skills=[
            "Python",
            "FastAPI",
            "PostgreSQL",
            "Docker",
        ],
        preferred_skills=[],
        candidate_skills=[
            "Python",
            "FastAPI",
        ],
    )

    assert result.required_skill_score == 50.0

    assert result.matched_required_skills == [
        "Python",
        "FastAPI",
    ]

    assert result.missing_required_skills == [
        "PostgreSQL",
        "Docker",
    ]


def test_preferred_skills_match(
    matching_service: MatchingService,
):
    result = matching_service.match_skills(
        required_skills=[
            "Python",
        ],
        preferred_skills=[
            "LangChain",
            "React",
        ],
        candidate_skills=[
            "Python",
            "LangChain",
        ],
    )

    assert result.required_skill_score == 100.0
    assert result.preferred_skill_score == 50.0

    assert result.matched_preferred_skills == [
        "LangChain",
    ]


def test_no_required_skills_returns_full_score(
    matching_service: MatchingService,
):
    result = matching_service.match_skills(
        required_skills=[],
        preferred_skills=[
            "React",
        ],
        candidate_skills=[
            "Python",
        ],
    )

    assert result.required_skill_score == 100.0


def test_skill_normalization(
    matching_service: MatchingService,
):
    result = matching_service.match_skills(
        required_skills=[
            "  Python  ",
            "FASTAPI",
        ],
        preferred_skills=[],
        candidate_skills=[
            "python",
            " fastapi ",
        ],
    )

    assert result.required_skill_score == 100.0
    assert result.missing_required_skills == []


def test_deterministic_score(
    matching_service: MatchingService,
):
    score = matching_service.calculate_deterministic_score(
        experience_score=100.0,
        required_skill_score=100.0,
        constraint_score=100.0,
    )

    assert score == 100.0


def test_full_candidate_matching(
    matching_service: MatchingService,
):
    job = JobRequirements(
        required_experience_years=5,
        required_skills=[
            "Python",
            "FastAPI",
            "PostgreSQL",
        ],
        preferred_skills=[
            "LangChain",
            "React",
        ],
        education_requirements=[],
        location=None,
        employment_type=None,
        other_constraints=[],
    )

    candidate = CandidateProfile(
        name="Test Candidate",
        email="candidate@example.com",
        phone="9999999999",
        total_experience_years=6,
        skills=[
            "Python",
            "FastAPI",
            "PostgreSQL",
            "LangChain",
        ],
        education=[
            "B.Tech",
        ],
        projects=[
            "AI Recruitment Platform",
        ],
        certifications=[],
    )

    result = matching_service.match(
        job=job,
        candidate=candidate,
        candidate_id=1,
    )

    assert result.candidate_id == 1
    assert result.candidate_name == "Test Candidate"

    assert result.experience_score == 100.0
    assert result.required_skill_score == 100.0
    assert result.preferred_skill_score == 50.0

    assert result.semantic_score is None
    assert result.deterministic_score == 100.0

    assert (
        "Candidate meets the required experience."
        in result.reasons
    )

    assert any(
        "Python" in reason
        for reason in result.reasons
    )


def test_missing_required_skills_generate_warning(
    matching_service: MatchingService,
):
    job = JobRequirements(
        required_experience_years=5,
        required_skills=[
            "Python",
            "FastAPI",
            "PostgreSQL",
        ],
        preferred_skills=[],
        education_requirements=[],
        location=None,
        employment_type=None,
        other_constraints=[],
    )

    candidate = CandidateProfile(
        name="Partial Match",
        email="partial@example.com",
        phone=None,
        total_experience_years=3,
        skills=[
            "Python",
        ],
        education=[],
        projects=[],
        certifications=[],
    )

    result = matching_service.match(
        job=job,
        candidate=candidate,
        candidate_id=2,
    )

    assert result.experience_match.meets_requirement is False

    assert result.skill_match.missing_required_skills == [
        "FastAPI",
        "PostgreSQL",
    ]

    assert any(
        "Missing required skills" in warning
        for warning in result.warnings
    )

    assert any(
        "less experience" in warning
        for warning in result.warnings
    )