from datetime import datetime

from pydantic import BaseModel, Field


# ----------------------------------------------------------------------
# Candidate Profile
# ----------------------------------------------------------------------


class CandidateProfile(BaseModel):
    name: str | None = None

    email: str | None = None
    phone: str | None = None
    whatsapp_number: str | None = None

    linkedin_url: str | None = None
    github_url: str | None = None
    portfolio_url: str | None = None

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


# ----------------------------------------------------------------------
# Candidate Skill Response
# ----------------------------------------------------------------------


class CandidateSkillResponse(BaseModel):
    id: int
    candidate_id: int
    skill_name: str

    model_config = {
        "from_attributes": True,
    }


# ----------------------------------------------------------------------
# Candidate Education Response
# ----------------------------------------------------------------------


class CandidateEducationResponse(BaseModel):
    id: int
    candidate_id: int
    education: str

    model_config = {
        "from_attributes": True,
    }


# ----------------------------------------------------------------------
# Candidate Project Response
# ----------------------------------------------------------------------


class CandidateProjectResponse(BaseModel):
    id: int
    candidate_id: int
    project: str

    model_config = {
        "from_attributes": True,
    }


# ----------------------------------------------------------------------
# Candidate Certification Response
# ----------------------------------------------------------------------


class CandidateCertificationResponse(BaseModel):
    id: int
    candidate_id: int
    certification: str

    model_config = {
        "from_attributes": True,
    }


# ----------------------------------------------------------------------
# Candidate List Response
# ----------------------------------------------------------------------


class CandidateListItem(BaseModel):
    id: int

    name: str | None = None
    email: str | None = None
    phone: str | None = None

    whatsapp_number: str | None = None

    linkedin_url: str | None = None
    github_url: str | None = None
    portfolio_url: str | None = None

    total_experience_years: float | None = None

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }


class CandidateListResponse(BaseModel):
    items: list[CandidateListItem]

    total: int
    page: int
    page_size: int
    total_pages: int


# ----------------------------------------------------------------------
# Candidate Resume Summary
# ----------------------------------------------------------------------


class CandidateResumeSummary(BaseModel):
    id: int

    original_filename: str
    file_type: str
    file_size: int

    file_hash: str

    storage_path: str

    source_type: str
    source_reference: str | None = None

    extraction_status: str

    candidate_id: int | None = None

    version: int | None = None
    is_current: bool

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }


# ----------------------------------------------------------------------
# Candidate Detail Response
# ----------------------------------------------------------------------


class CandidateDetailResponse(BaseModel):
    id: int

    name: str | None = None

    email: str | None = None
    phone: str | None = None
    whatsapp_number: str | None = None

    linkedin_url: str | None = None
    github_url: str | None = None
    portfolio_url: str | None = None

    total_experience_years: float | None = None

    skills: list[CandidateSkillResponse] = Field(
        default_factory=list,
    )

    education: list[CandidateEducationResponse] = Field(
        default_factory=list,
    )

    projects: list[CandidateProjectResponse] = Field(
        default_factory=list,
    )

    certifications: list[CandidateCertificationResponse] = Field(
        default_factory=list,
    )

    resumes: list[CandidateResumeSummary] = Field(
        default_factory=list,
    )

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }