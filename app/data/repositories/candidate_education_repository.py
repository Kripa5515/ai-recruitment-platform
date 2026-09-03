from sqlalchemy import select
from sqlalchemy.orm import Session
from app.data.models.candidate_education import CandidateEducation

class CandidateEducationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
    self,
    candidate_id: int,
    education: str,
    ) -> CandidateEducation:
        education_record = CandidateEducation(
            candidate_id=candidate_id,
            education=education,
        )

        self.db.add(education_record)
        self.db.flush()

        return education_record

    def get_by_candidate_id(
        self,
        candidate_id: int,
    ) -> list[CandidateEducation]:
        statement = (
            select(CandidateEducation)
            .where(CandidateEducation.candidate_id == candidate_id)
            .order_by(CandidateEducation.id)
        )

        result = self.db.execute(statement)

        return list(result.scalars().all())

    def delete_by_candidate_id(
        self,
        candidate_id: int,
    ) -> int:
        records = self.get_by_candidate_id(candidate_id)

        for record in records:
            self.db.delete(record)

        self.db.commit()

        return len(records)