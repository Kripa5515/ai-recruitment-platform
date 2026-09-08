from datetime import datetime

from pydantic import BaseModel, Field


class JobCreate(BaseModel):
    title: str
    description: str
    company: str
    location: str
    experience_required: str
    employment_type: str
    status: str = "draft"


class JobUpdate(BaseModel):
    title: str
    description: str
    company: str
    location: str
    experience_required: str
    employment_type: str
    status: str


class JobResponse(BaseModel):
    id: int

    # =========================================================
    # Basic Job Information
    # =========================================================

    title: str
    description: str
    company: str
    location: str
    experience_required: str
    employment_type: str
    status: str

    # =========================================================
    # Structured JD Requirements
    # =========================================================

    required_experience_years: float | None = None

    required_skills: list[str] = Field(
        default_factory=list,
    )

    preferred_skills: list[str] = Field(
        default_factory=list,
    )

    education_requirements: list[str] = Field(
        default_factory=list,
    )

    other_constraints: list[str] = Field(
        default_factory=list,
    )

    # =========================================================
    # Timestamps
    # =========================================================

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }