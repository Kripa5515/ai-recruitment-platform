from pydantic import BaseModel, Field


class SkillMatchResult(BaseModel):
    """
    Result of comparing candidate skills with job skills.
    """

    required_skills: list[str] = Field(
        default_factory=list
    )

    matched_required_skills: list[str] = Field(
        default_factory=list
    )

    missing_required_skills: list[str] = Field(
        default_factory=list
    )

    preferred_skills: list[str] = Field(
        default_factory=list
    )

    matched_preferred_skills: list[str] = Field(
        default_factory=list
    )

    required_skill_score: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
    )

    preferred_skill_score: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
    )


class ExperienceMatchResult(BaseModel):
    """
    Result of comparing candidate experience
    with the job requirement.
    """

    required_experience_years: float | None = None

    candidate_experience_years: float | None = None

    meets_requirement: bool | None = None

    score: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
    )

    explanation: str = ""


class MatchResult(BaseModel):
    """
    Overall deterministic candidate matching result.

    Semantic similarity will be added later.
    """

    candidate_id: int | None = None

    candidate_name: str | None = None

    experience_score: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
    )

    required_skill_score: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
    )

    preferred_skill_score: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
    )

    semantic_score: float | None = Field(
        default=None,
        ge=0.0,
        le=100.0,
    )

    constraint_score: float = Field(
        default=100.0,
        ge=0.0,
        le=100.0,
    )

    deterministic_score: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
    )

    final_score: float | None = Field(
        default=None,
        ge=0.0,
        le=100.0,
    )

    skill_match: SkillMatchResult

    experience_match: ExperienceMatchResult

    reasons: list[str] = Field(
        default_factory=list
    )

    warnings: list[str] = Field(
        default_factory=list
    )