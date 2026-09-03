from sqlalchemy.orm import Session

from app.api.schemas.candidate import CandidateProfile
from app.data.models.candidate import Candidate
from app.data.repositories.candidate_repository import CandidateRepository
from app.data.repositories.candidate_certification_repository import (
    CandidateCertificationRepository,
)
from app.data.repositories.candidate_education_repository import (
    CandidateEducationRepository,
)
from app.data.repositories.candidate_project_repository import (
    CandidateProjectRepository,
)
from app.data.repositories.candidate_skill_repository import (
    CandidateSkillRepository,
)


class CandidateService:
    def __init__(self, db: Session):
        self.repository = CandidateRepository(db)

        self.skill_repository = CandidateSkillRepository(db)
        self.education_repository = CandidateEducationRepository(db)
        self.project_repository = CandidateProjectRepository(db)
        self.certification_repository = (
            CandidateCertificationRepository(db)
        )

    def create_candidate(
        self,
        profile: CandidateProfile,
    ) -> Candidate:
        return self.repository.create(
            name=profile.name,
            email=profile.email,
            phone=profile.phone,
            total_experience_years=profile.total_experience_years,
        )

    def create_candidate_profile(
    self,
    profile: CandidateProfile,
    ) -> Candidate:

        try:
            candidate = self.repository.create(
                name=profile.name,
                email=profile.email,
                phone=profile.phone,
                total_experience_years=profile.total_experience_years,
            )

            for skill in profile.skills:
                self.skill_repository.create(
                    candidate_id=candidate.id,
                    skill_name=skill,
                )

            for education in profile.education:
                self.education_repository.create(
                    candidate_id=candidate.id,
                    education=education,
                )

            for project in profile.projects:
                self.project_repository.create(
                    candidate_id=candidate.id,
                    project=project,
                )

            for certification in profile.certifications:
                self.certification_repository.create(
                    candidate_id=candidate.id,
                    certification=certification,
                )

            self.repository.db.commit()
            self.repository.db.refresh(candidate)

            return candidate

        except Exception:
            self.repository.db.rollback()
            raise

    def get_candidate(
        self,
        candidate_id: int,
    ) -> Candidate | None:
        return self.repository.get_by_id(candidate_id)

    def get_all_candidates(self) -> list[Candidate]:
        return self.repository.get_all()

    def get_candidate_by_email(
        self,
        email: str,
    ) -> Candidate | None:
        return self.repository.get_by_email(email)