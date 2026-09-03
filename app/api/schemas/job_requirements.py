from pydantic import BaseModel, Field

class JobRequirements(BaseModel):
    required_experience_years: float | None = Field(
        default=None,
        ge=0,
    )

    required_skills: list[str] = Field(
        default_factory=list,
    )

    preferred_skills: list[str] = Field(
        default_factory=list,
    )

    education_requirements: list[str] = Field(
        default_factory=list,
    )

    location: str | None = None

    employment_type: str | None = None

    other_constraints: list[str] = Field(
        default_factory=list,
    )