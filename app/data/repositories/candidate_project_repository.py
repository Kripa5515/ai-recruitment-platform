from sqlalchemy import select
from sqlalchemy.orm import Session
from app.data.models.candidate_project import CandidateProject

class CandidateProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
    self,
    candidate_id: int,
    project: str,
    ) -> CandidateProject:
        project_record = CandidateProject(
            candidate_id=candidate_id,
            project=project,
        )

        self.db.add(project_record)
        self.db.flush()

        return project_record

    def get_by_candidate_id(
        self,
        candidate_id: int,
    ) -> list[CandidateProject]:
        statement = (
            select(CandidateProject)
            .where(CandidateProject.candidate_id == candidate_id)
            .order_by(CandidateProject.id)
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