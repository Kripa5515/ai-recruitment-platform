from sqlalchemy import select
from sqlalchemy.orm import Session
from app.data.models.candidate_certification import CandidateCertification

class CandidateCertificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
    self,
    candidate_id: int,
    certification: str,
    ) -> CandidateCertification:
        certification_record = CandidateCertification(
            candidate_id=candidate_id,
            certification=certification,
        )

        self.db.add(certification_record)
        self.db.flush()

        return certification_record

    def get_by_candidate_id(
        self,
        candidate_id: int,
    ) -> list[CandidateCertification]:
        statement = (
            select(CandidateCertification)
            .where(
                CandidateCertification.candidate_id == candidate_id
            )
            .order_by(CandidateCertification.id)
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