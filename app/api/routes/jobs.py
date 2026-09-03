from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.services.job_service import JobService
from app.api.schemas.job import JobCreate, JobResponse, JobUpdate
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)

@router.post("/", response_model=JobResponse)
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
    )

@router.get("/", response_model=list[JobResponse])
def get_jobs(
    db: Session = Depends(get_db),
):
    service = JobService(db)
    return service.get_all_jobs()

@router.get("/{job_id}", response_model=JobResponse)
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

@router.put("/{job_id}", response_model=JobResponse)
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

@router.delete("/{job_id}", status_code=204)
def delete_job(job_id: int, db: Session = Depends(get_db),):
    service = JobService(db)
    deleted = service.delete_job(job_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )