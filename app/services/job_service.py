from sqlalchemy.orm import Session
from app.data.repositories.job_repository import JobRepository
from app.data.models.job import Job

class JobService:

    def __init__(self, db: Session):
        self.repository = JobRepository(db)

    def create_job(self, title: str, description: str) -> Job:
        return self.repository.create(
            title=title,
            description=description,
        )

    def get_all_jobs(self) -> list[Job]:
        return self.repository.get_all()

    def get_job(self, job_id: int) -> Job | None:
        return self.repository.get_by_id(job_id)

    def update_job(self, job_id: int, title: str, description: str,) -> Job | None:
        return self.repository.update(
            job_id=job_id,
            title=title,
            description=description,
        )

    def delete_job(self, job_id: int) -> bool:
        return self.repository.delete(job_id)