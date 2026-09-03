from sqlalchemy import select
from sqlalchemy.orm import Session
from app.data.models.candidate_skill import CandidateSkill

class CandidateSkillRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
    self,
    candidate_id: int,
    skill_name: str,
    ) -> CandidateSkill:
        skill = CandidateSkill(
            candidate_id=candidate_id,
            skill_name=skill_name,
        )

        self.db.add(skill)
        self.db.flush()

        return skill

    def get_by_candidate_id(
        self,
        candidate_id: int,
    ) -> list[CandidateSkill]:
        statement = (
            select(CandidateSkill)
            .where(CandidateSkill.candidate_id == candidate_id)
            .order_by(CandidateSkill.id)
        )

        result = self.db.execute(statement)

        return list(result.scalars().all())

    def delete_by_candidate_id(
        self,
        candidate_id: int,
    ) -> int:
        skills = self.get_by_candidate_id(candidate_id)

        for skill in skills:
            self.db.delete(skill)

        self.db.commit()

        return len(skills)