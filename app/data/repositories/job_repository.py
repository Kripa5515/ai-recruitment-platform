from sqlalchemy import select
from sqlalchemy.orm import Session
from app.data.models.job import Job

class JobRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, title: str, description: str) -> Job:
        job = Job(
            title=title,
            description=description,
        )

        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)

        return job

    def get_all(self) -> list[Job]:
        statement = select(Job).order_by(Job.id)
        result = self.db.execute(statement)
        return list(result.scalars().all())

    def get_by_id(self, job_id: int) -> Job | None:
        statement = select(Job).where(Job.id == job_id)
        result = self.db.execute(statement)
        return result.scalar_one_or_none()

    def update(self, job_id: int, title: str, description: str,) -> Job | None:
        job = self.get_by_id(job_id)

        if job is None:
            return None

        job.title = title
        job.description = description

        self.db.commit()
        self.db.refresh(job)

        return job

    def delete(self, job_id: int) -> bool:
        job = self.get_by_id(job_id)

        if job is None:
            return False

        self.db.delete(job)
        self.db.commit()

        return True