from pydantic import BaseModel, Field

class CandidateProfile(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None

    total_experience_years: float | None = Field(
        default=None,
        ge=0,
    )

    skills: list[str] = Field(
        default_factory=list,
    )

    education: list[str] = Field(
        default_factory=list,
    )

    projects: list[str] = Field(
        default_factory=list,
    )

    certifications: list[str] = Field(
        default_factory=list,
    )