import pytest

from app.ai.matching.matching_service import MatchingService
from app.ai.matching.schemas import (
    ExperienceMatchResult,
    MatchResult,
    SkillMatchResult,
)
from app.api.schemas.candidate import CandidateProfile
from app.api.schemas.job_requirements import JobRequirements


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def job_requirements() -> JobRequirements:
    return JobRequirements(
        required_experience_years=5.0,
        required_skills=[
            "Python",
            "FastAPI",
            "PostgreSQL",
        ],
        preferred_skills=[
            "Docker",
            "AWS",
        ],
        education_requirements=[],
        location="Delhi",
        employment_type="Full-time",
        other_constraints=[],
    )


@pytest.fixture
def candidate_profile() -> CandidateProfile:
    return CandidateProfile(
        name="John Doe",
        email="john@example.com",
        phone="9999999999",
        total_experience_years=6.0,
        skills=[
            "Python",
            "FastAPI",
            "PostgreSQL",
            "Docker",
        ],
        education=[
            "B.Tech Computer Science",
        ],
        projects=[
            "AI Recruitment Platform",
        ],
        certifications=[],
    )


# ============================================================
# Basic Matching
# ============================================================


def test_matching_all_required_skills(
    job_requirements: JobRequirements,
    candidate_profile: CandidateProfile,
):
    service = MatchingService()

    result = service.match(
        job=job_requirements,
        candidate=candidate_profile,
    )

    assert result.required_skill_score == 100.0

    assert result.skill_match.missing_required_skills == []

    assert set(result.skill_match.matched_required_skills) == {
        "python",
        "fastapi",
        "postgresql",
    }


def test_matching_partial_required_skills(
    job_requirements: JobRequirements,
    candidate_profile: CandidateProfile,
):
    candidate_profile.skills = [
        "Python",
        "FastAPI",
    ]

    service = MatchingService()

    result = service.match(
        job=job_requirements,
        candidate=candidate_profile,
    )

    assert result.required_skill_score == pytest.approx(66.67, abs=0.01)

    assert result.skill_match.missing_required_skills == [
        "postgresql"
    ]

    assert set(result.skill_match.matched_required_skills) == {
        "python",
        "fastapi",
    }


def test_matching_no_required_skills(
    candidate_profile: CandidateProfile,
):
    job = JobRequirements(
        required_experience_years=5.0,
        required_skills=[],
        preferred_skills=[],
        education_requirements=[],
        location=None,
        employment_type=None,
        other_constraints=[],
    )

    service = MatchingService()

    result = service.match(
        job=job,
        candidate=candidate_profile,
    )

    assert result.required_skill_score == 100.0
    assert result.skill_match.missing_required_skills == []
    assert result.skill_match.matched_required_skills == []


def test_preferred_skill_matching(
    job_requirements: JobRequirements,
    candidate_profile: CandidateProfile,
):
    service = MatchingService()

    result = service.match(
        job=job_requirements,
        candidate=candidate_profile,
    )

    assert result.preferred_skill_score == 50.0

    assert result.skill_match.matched_preferred_skills == [
        "docker"
    ]


def test_no_preferred_skill_match(
    job_requirements: JobRequirements,
    candidate_profile: CandidateProfile,
):
    candidate_profile.skills = [
        "Python",
        "FastAPI",
        "PostgreSQL",
    ]

    service = MatchingService()

    result = service.match(
        job=job_requirements,
        candidate=candidate_profile,
    )

    assert result.preferred_skill_score == 0.0

    assert result.skill_match.matched_preferred_skills == []


# ============================================================
# Case Insensitive Skill Matching
# ============================================================


def test_skill_matching_is_case_insensitive(
    candidate_profile: CandidateProfile,
):
    job = JobRequirements(
        required_experience_years=5.0,
        required_skills=[
            "python",
            "FASTAPI",
            "PostgreSQL",
        ],
        preferred_skills=[],
        education_requirements=[],
        location=None,
        employment_type=None,
        other_constraints=[],
    )

    candidate_profile.skills = [
        "Python",
        "fastapi",
        "POSTGRESQL",
    ]

    service = MatchingService()

    result = service.match(
        job=job,
        candidate=candidate_profile,
    )

    assert result.required_skill_score == 100.0
    assert result.skill_match.missing_required_skills == []


# ============================================================
# Experience Matching
# ============================================================


def test_matching_experience_meets_requirement(
    job_requirements: JobRequirements,
    candidate_profile: CandidateProfile,
):
    service = MatchingService()

    result = service.match(
        job=job_requirements,
        candidate=candidate_profile,
    )

    assert result.experience_score == 100.0
    assert result.experience_match.meets_requirement is True


def test_matching_experience_below_requirement(
    job_requirements: JobRequirements,
    candidate_profile: CandidateProfile,
):
    candidate_profile.total_experience_years = 3.0

    service = MatchingService()

    result = service.match(
        job=job_requirements,
        candidate=candidate_profile,
    )

    assert result.experience_score == 60.0
    assert result.experience_match.meets_requirement is False


def test_matching_missing_candidate_experience(
    job_requirements: JobRequirements,
    candidate_profile: CandidateProfile,
):
    candidate_profile.total_experience_years = None

    service = MatchingService()

    result = service.match(
        job=job_requirements,
        candidate=candidate_profile,
    )

    assert result.experience_score == 0.0
    assert result.experience_match.meets_requirement is False


def test_matching_without_experience_requirement(
    candidate_profile: CandidateProfile,
):
    job = JobRequirements(
        required_experience_years=None,
        required_skills=[],
        preferred_skills=[],
        education_requirements=[],
        location=None,
        employment_type=None,
        other_constraints=[],
    )

    service = MatchingService()

    result = service.match(
        job=job,
        candidate=candidate_profile,
    )

    assert result.experience_score == 100.0
    assert result.experience_match.meets_requirement is True


# ============================================================
# Deterministic Score
# ============================================================


def test_deterministic_score_is_generated(
    job_requirements: JobRequirements,
    candidate_profile: CandidateProfile,
):
    service = MatchingService()

    result = service.match(
        job=job_requirements,
        candidate=candidate_profile,
    )

    assert result.deterministic_score is not None
    assert 0.0 <= result.deterministic_score <= 100.0


def test_deterministic_mode_has_no_semantic_score(
    job_requirements: JobRequirements,
    candidate_profile: CandidateProfile,
):
    service = MatchingService()

    result = service.match(
        job=job_requirements,
        candidate=candidate_profile,
    )

    assert result.semantic_score is None
    assert result.final_score is None


# ============================================================
# Constraint Matching
# ============================================================


def test_no_constraints_get_full_constraint_score(
    job_requirements: JobRequirements,
    candidate_profile: CandidateProfile,
):
    service = MatchingService()

    result = service.match(
        job=job_requirements,
        candidate=candidate_profile,
    )

    assert result.constraint_score == 100.0


def test_explicit_constraints_get_mvp_constraint_score(
    job_requirements: JobRequirements,
    candidate_profile: CandidateProfile,
):
    job_requirements.other_constraints = [
        "Must be available for hybrid work."
    ]

    service = MatchingService()

    result = service.match(
        job=job_requirements,
        candidate=candidate_profile,
    )

    assert result.constraint_score == 50.0


# ============================================================
# Explainability
# ============================================================


def test_reasons_are_generated_for_matching_candidate(
    job_requirements: JobRequirements,
    candidate_profile: CandidateProfile,
):
    service = MatchingService()

    result = service.match(
        job=job_requirements,
        candidate=candidate_profile,
    )

    assert result.reasons

    assert any(
        "6 years of experience" in reason
        for reason in result.reasons
    )

    assert any(
        "5 years required" in reason
        for reason in result.reasons
    )

    assert any(
        "matches all 3 required skills" in reason
        for reason in result.reasons
    )


def test_warning_generated_for_missing_required_skill(
    job_requirements: JobRequirements,
    candidate_profile: CandidateProfile,
):
    candidate_profile.skills = [
        "Python",
    ]

    service = MatchingService()

    result = service.match(
        job=job_requirements,
        candidate=candidate_profile,
    )

    assert result.warnings

    assert any(
        "missing required skills:" in warning.lower()
        for warning in result.warnings
    )

    assert any(
        "fastapi" in warning.lower()
        for warning in result.warnings
    )

    assert any(
        "postgresql" in warning.lower()
        for warning in result.warnings
    )


# ============================================================
# Semantic / Hybrid Matching
# ============================================================


class FakeSemanticMatchingService:
    """
    Fake semantic service used for unit testing.

    It prevents the test from calling OpenAI.
    """

    def __init__(self, score: float = 80.0):
        self.score = score
        self.called = False
        self.received_text_a = None
        self.received_text_b = None

    def calculate_score(
        self,
        text_a: str,
        text_b: str,
    ) -> float:
        self.called = True
        self.received_text_a = text_a
        self.received_text_b = text_b

        return self.score


def test_semantic_matching_is_called_when_texts_are_available(
    job_requirements: JobRequirements,
    candidate_profile: CandidateProfile,
):
    fake_semantic_service = FakeSemanticMatchingService(
        score=80.0
    )

    service = MatchingService(
        semantic_matching_service=fake_semantic_service
    )

    result = service.match(
        job=job_requirements,
        candidate=candidate_profile,
        job_text="Python FastAPI backend developer",
        candidate_text="Python FastAPI developer with PostgreSQL",
    )

    assert fake_semantic_service.called is True

    assert (
        fake_semantic_service.received_text_a
        == "Python FastAPI backend developer"
    )

    assert (
        fake_semantic_service.received_text_b
        == "Python FastAPI developer with PostgreSQL"
    )

    assert result.semantic_score == 80.0


def test_hybrid_final_score_is_generated(
    job_requirements: JobRequirements,
    candidate_profile: CandidateProfile,
):
    fake_semantic_service = FakeSemanticMatchingService(
        score=80.0
    )

    service = MatchingService(
        semantic_matching_service=fake_semantic_service
    )

    result = service.match(
        job=job_requirements,
        candidate=candidate_profile,
        job_text="Python FastAPI backend developer",
        candidate_text="Python FastAPI developer with PostgreSQL",
    )

    assert result.final_score is not None
    assert 0.0 <= result.final_score <= 100.0


def test_hybrid_score_uses_all_weights(
    job_requirements: JobRequirements,
    candidate_profile: CandidateProfile,
):
    fake_semantic_service = FakeSemanticMatchingService(
        score=80.0
    )

    service = MatchingService(
        semantic_matching_service=fake_semantic_service
    )

    result = service.match(
        job=job_requirements,
        candidate=candidate_profile,
        job_text="Job description",
        candidate_text="Candidate resume",
    )

    # Experience = 100
    # Required skills = 100
    # Semantic = 80
    # Constraint = 100
    #
    # Final:
    #
    # (100*20 + 100*40 + 80*25 + 100*15) / 100
    #
    # = 95
    assert result.final_score == 95.0


def test_semantic_matching_not_called_without_texts(
    job_requirements: JobRequirements,
    candidate_profile: CandidateProfile,
):
    fake_semantic_service = FakeSemanticMatchingService(
        score=90.0
    )

    service = MatchingService(
        semantic_matching_service=fake_semantic_service
    )

    result = service.match(
        job=job_requirements,
        candidate=candidate_profile,
    )

    assert fake_semantic_service.called is False
    assert result.semantic_score is None
    assert result.final_score is None