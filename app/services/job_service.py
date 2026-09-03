from sqlalchemy.orm import Session
from app.data.repositories.job_repository import JobRepository
from app.data.models.job import Job

class JobService:

    def __init__(self, db: Session):
        self.repository = JobRepository(db)

    def create_job(self, title: str, description: str, company: str, location: str, experience_required: str, employment_type: str,) -> Job:
        return self.repository.create(
            title=title,
            description=description,
            company=company,
            location=location,
            experience_required=experience_required,
            employment_type=employment_type,
        )

    def get_all_jobs(self) -> list[Job]:
        return self.repository.get_all()

    def get_job(self, job_id: int) -> Job | None:
        return self.repository.get_by_id(job_id)

    def update_job(self, job_id: int, title: str, description: str, company: str, location: str, experience_required: str, employment_type: str, status: str,) -> Job | None:
        return self.repository.update(
            job_id=job_id,
            title=title,
            description=description,
            company=company,
            location=location,
            experience_required=experience_required,
            employment_type=employment_type,
            status=status,
        )

    def delete_job(self, job_id: int) -> bool:
        return self.repository.delete(job_id)