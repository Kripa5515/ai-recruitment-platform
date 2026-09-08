from pydantic import BaseModel, Field


class SkillMatchResult(BaseModel):
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
    candidate_id: int | None = None
    candidate_name: str | None = None

    email: str | None = None
    phone: str | None = None
    whatsapp_number: str | None = None

    linkedin_url: str | None = None
    github_url: str | None = None
    portfolio_url: str | None = None

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


class MatchingCandidateResponse(BaseModel):
    candidate_id: int
    candidate_name: str | None = None

    email: str | None = None
    phone: str | None = None
    whatsapp_number: str | None = None

    linkedin_url: str | None = None
    github_url: str | None = None
    portfolio_url: str | None = None

    experience_score: float
    required_skill_score: float
    preferred_skill_score: float
    semantic_score: float | None
    constraint_score: float
    deterministic_score: float
    final_score: float | None

    reasons: list[str] = Field(
        default_factory=list
    )

    warnings: list[str] = Field(
        default_factory=list
    )


class MatchingResponse(BaseModel):
    job_id: int
    job_title: str

    total_candidates: int
    matched_candidates: int

    results: list[MatchingCandidateResponse]