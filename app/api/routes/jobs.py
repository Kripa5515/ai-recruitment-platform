import math

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Query,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.schemas.job import (
    JobCreate,
    JobResponse,
    JobUpdate,
)
from app.api.schemas.job_requirements import JobRequirements
from app.services.job_document_service import JobDocumentService
from app.services.job_service import JobService


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


# =========================================================
# Analyze Job Description Text
# =========================================================

@router.post(
    "/analyze",
    response_model=JobRequirements,
)
def analyze_job_description(
    job_description: str,
    db: Session = Depends(get_db),
):
    """
    Analyze an unstructured job description.

    This endpoint does NOT create a Job in the database.
    """

    service = JobService(db)

    try:
        return service.analyze_jd(
            job_description=job_description,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze job description: {exc}",
        ) from exc


# =========================================================
# Analyze Uploaded Job Description
# =========================================================

@router.post(
    "/upload",
    response_model=JobRequirements,
)
async def analyze_uploaded_job_description(
    file: UploadFile = File(...),
):
    """
    Upload a TXT, PDF or DOCX job description.

    The file is validated and converted into structured
    job requirements.

    This endpoint does NOT create a Job in the database.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    try:
        file_content = await file.read()

        service = JobDocumentService()

        return service.analyze_file(
            filename=file.filename,
            file_content=file_content,
        )

    except (
        ValueError,
        PDFExtractionError,
        DOCXExtractionError,
    ) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process uploaded JD: {exc}",
        ) from exc


# =========================================================
# Create Job
# =========================================================

@router.post(
    "/",
    response_model=JobResponse,
)
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
):
    service = JobService(db)

    return service.create_job(
        title=job.title,
        description=job.description,
        company=job.company,
        location=job.location,
        experience_required=job.experience_required,
        employment_type=job.employment_type,
        status=job.status,
    )


# =========================================================
# Get Jobs - Pagination
# =========================================================

@router.get("/")
def get_jobs(
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
        description=(
            "Search jobs by title, company, "
            "location or description"
        ),
    ),
    db: Session = Depends(get_db),
):
    service = JobService(db)

    jobs, total = service.get_paginated_jobs(
        page=page,
        page_size=page_size,
        search=search,
    )

    total_pages = (
        math.ceil(total / page_size)
        if total > 0
        else 0
    )

    return {
        "items": jobs,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "search": search,
    }


# =========================================================
# Get Single Job
# =========================================================

@router.get(
    "/{job_id}",
    response_model=JobResponse,
)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
):
    service = JobService(db)

    job = service.get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return job


# =========================================================
# Update Job
# =========================================================

@router.put(
    "/{job_id}",
    response_model=JobResponse,
)
def update_job(
    job_id: int,
    job: JobUpdate,
    db: Session = Depends(get_db),
):
    service = JobService(db)

    updated_job = service.update_job(
        job_id=job_id,
        title=job.title,
        description=job.description,
        company=job.company,
        location=job.location,
        experience_required=job.experience_required,
        employment_type=job.employment_type,
        status=job.status,
    )

    if updated_job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return updated_job


# =========================================================
# Delete Job
# =========================================================

@router.delete(
    "/{job_id}",
    status_code=204,
)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
):
    service = JobService(db)

    deleted = service.delete_job(
        job_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )