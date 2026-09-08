from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.data.models.job import Job
from app.data.models.candidate import Candidate
from app.data.models.resume import Resume


class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db

    def count_jobs(self) -> int:
        statement = select(func.count(Job.id))
        return self.db.scalar(statement) or 0

    def count_candidates(self) -> int:
        statement = select(func.count(Candidate.id))
        return self.db.scalar(statement) or 0

    def count_resumes(self) -> int:
        statement = select(func.count(Resume.id))
        return self.db.scalar(statement) or 0