from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.schemas.candidate import (
    CandidateDetailResponse,
    CandidateListResponse,
    CandidateResumeSummary,
)
from app.services.candidate_service import CandidateService


router = APIRouter(
    prefix="/candidates",
    tags=["Candidates"],
)


# ----------------------------------------------------------------------
# Candidate List
# ----------------------------------------------------------------------


@router.get(
    "/",
    response_model=CandidateListResponse,
)
def get_candidates(
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    search: str | None = Query(
        default=None,
    ),
    db: Session = Depends(get_db),
):
    service = CandidateService(db)

    candidates, total = service.get_candidates(
        page=page,
        page_size=page_size,
        search=search,
    )

    total_pages = (
        ceil(total / page_size)
        if total > 0
        else 0
    )

    return CandidateListResponse(
        items=candidates,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


# ----------------------------------------------------------------------
# Candidate Detail
# ----------------------------------------------------------------------


@router.get(
    "/{candidate_id}",
    response_model=CandidateDetailResponse,
)
def get_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
):
    service = CandidateService(db)

    candidate = service.get_candidate(
        candidate_id
    )

    if candidate is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found.",
        )

    skills = service.skill_repository.get_by_candidate_id(
        candidate_id
    )

    education = (
        service.education_repository
        .get_by_candidate_id(candidate_id)
    )

    projects = (
        service.project_repository
        .get_by_candidate_id(candidate_id)
    )

    certifications = (
        service.certification_repository
        .get_by_candidate_id(candidate_id)
    )

    resumes = service.get_candidate_resumes(
        candidate_id
    )

    return CandidateDetailResponse(
        id=candidate.id,
        name=candidate.name,
        email=candidate.email,
        phone=candidate.phone,
        total_experience_years=(
            candidate.total_experience_years
        ),
        skills=skills,
        education=education,
        projects=projects,
        certifications=certifications,
        resumes=resumes,
        created_at=candidate.created_at,
        updated_at=candidate.updated_at,
    )


# ----------------------------------------------------------------------
# Candidate Resume History
# ----------------------------------------------------------------------


@router.get(
    "/{candidate_id}/resumes",
    response_model=list[CandidateResumeSummary],
)
def get_candidate_resumes(
    candidate_id: int,
    db: Session = Depends(get_db),
):
    service = CandidateService(db)

    candidate = service.get_candidate(
        candidate_id
    )

    if candidate is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found.",
        )

    return service.get_candidate_resumes(
        candidate_id
    )