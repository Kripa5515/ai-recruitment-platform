from sqlalchemy import select
from sqlalchemy.orm import Session
from app.data.models.candidate import Candidate

class CandidateRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_resumes(
    self,
    candidate_id: int,
    ):
        candidate = self.get_by_id(candidate_id)

        if candidate is None:
            return None

        return candidate.resumes
    
    def create(
        self,
        name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        total_experience_years: float | None = None,
    ) -> Candidate:
        candidate = Candidate(
            name=name,
            email=email,
            phone=phone,
            total_experience_years=total_experience_years,
        )

        self.db.add(candidate)
        self.db.flush()
        return candidate

    def get_by_id(
        self,
        candidate_id: int,
    ) -> Candidate | None:
        statement = select(Candidate).where(
            Candidate.id == candidate_id
        )

        result = self.db.execute(statement)

        return result.scalar_one_or_none()

    def get_all(self) -> list[Candidate]:
        statement = select(Candidate).order_by(
            Candidate.id
        )

        result = self.db.execute(statement)

        return list(result.scalars().all())

    def get_by_email(
        self,
        email: str,
    ) -> Candidate | None:
        statement = select(Candidate).where(
            Candidate.email == email
        )

        result = self.db.execute(statement)

        return result.scalar_one_or_none()

