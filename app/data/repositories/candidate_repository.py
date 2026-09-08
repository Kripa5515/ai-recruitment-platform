from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.data.models.candidate import Candidate
from app.data.models.resume import Resume


class CandidateRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        whatsapp_number: str | None = None,
        linkedin_url: str | None = None,
        github_url: str | None = None,
        portfolio_url: str | None = None,
        total_experience_years: float | None = None,
    ) -> Candidate:

        candidate = Candidate(
            name=name,
            email=email,
            phone=phone,
            whatsapp_number=whatsapp_number,
            linkedin_url=linkedin_url,
            github_url=github_url,
            portfolio_url=portfolio_url,
            total_experience_years=total_experience_years,
        )

        self.db.add(candidate)
        self.db.flush()

        return candidate

    def get_by_id(
        self,
        candidate_id: int,
    ) -> Candidate | None:

        return self.db.scalar(
            select(Candidate).where(
                Candidate.id == candidate_id
            )
        )

    def get_by_email(
        self,
        email: str,
    ) -> Candidate | None:

        return self.db.scalar(
            select(Candidate).where(
                Candidate.email == email
            )
        )

    def get_all(self) -> list[Candidate]:

        return list(
            self.db.scalars(
                select(Candidate).order_by(
                    Candidate.id.desc()
                )
            ).all()
        )

    def get_paginated(
        self,
        page: int = 1,
        page_size: int = 10,
        search: str | None = None,
    ):

        query = select(Candidate)

        if search:
            search_pattern = f"%{search}%"

            query = query.where(
                or_(
                    Candidate.name.ilike(search_pattern),
                    Candidate.email.ilike(search_pattern),
                    Candidate.phone.ilike(search_pattern),
                )
            )

        count_query = select(
            func.count()
        ).select_from(
            query.subquery()
        )

        total = self.db.scalar(count_query) or 0

        query = (
            query
            .order_by(Candidate.id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        items = list(self.db.scalars(query).all())

        return items, total

    def get_resumes(
        self,
        candidate_id: int,
    ):

        return list(
            self.db.scalars(
                select(Resume)
                .where(
                    Resume.candidate_id == candidate_id
                )
                .order_by(Resume.version.desc())
            ).all()
        )

    def get_candidate_with_resumes(
        self,
        candidate_id: int,
    ):

        candidate = self.get_by_id(candidate_id)

        if candidate is None:
            return None

        candidate.resumes

        return candidate