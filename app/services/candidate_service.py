from sqlalchemy.orm import Session

from app.ai.extraction.candidate_extractor import CandidateExtractor
from app.api.schemas.candidate import CandidateProfile
from app.data.models.candidate import Candidate
from app.data.repositories.candidate_certification_repository import (
    CandidateCertificationRepository,
)
from app.data.repositories.candidate_education_repository import (
    CandidateEducationRepository,
)
from app.data.repositories.candidate_project_repository import (
    CandidateProjectRepository,
)
from app.data.repositories.candidate_repository import CandidateRepository
from app.data.repositories.candidate_skill_repository import (
    CandidateSkillRepository,
)


class CandidateService:
    def __init__(self, db: Session):
        self.db = db

        self.repository = CandidateRepository(db)

        self.skill_repository = CandidateSkillRepository(db)
        self.education_repository = CandidateEducationRepository(db)
        self.project_repository = CandidateProjectRepository(db)
        self.certification_repository = CandidateCertificationRepository(db)

        self.extractor = CandidateExtractor()

    def extract_profile(self, resume_text: str) -> CandidateProfile:
        return self.extractor.extract(resume_text)

    def create_candidate(self, profile: CandidateProfile) -> Candidate:
        return self.repository.create(
            name=profile.name,
            email=profile.email,
            phone=profile.phone,
            whatsapp_number=profile.whatsapp_number,
            linkedin_url=profile.linkedin_url,
            github_url=profile.github_url,
            portfolio_url=profile.portfolio_url,
            total_experience_years=profile.total_experience_years,
        )

    def create_candidate_profile_without_commit(
        self,
        profile: CandidateProfile,
    ) -> Candidate:

        candidate = self.repository.create(
            name=profile.name,
            email=profile.email,
            phone=profile.phone,
            whatsapp_number=profile.whatsapp_number,
            linkedin_url=profile.linkedin_url,
            github_url=profile.github_url,
            portfolio_url=profile.portfolio_url,
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

        return candidate

    def create_candidate_profile(
        self,
        profile: CandidateProfile,
    ) -> Candidate:

        try:
            candidate = self.create_candidate_profile_without_commit(
                profile
            )

            self.db.commit()
            self.db.refresh(candidate)

            return candidate

        except Exception:
            self.db.rollback()
            raise

    def get_candidate(self, candidate_id: int) -> Candidate | None:
        return self.repository.get_by_id(candidate_id)

    def get_all_candidates(self) -> list[Candidate]:
        return self.repository.get_all()

    def get_candidates(
        self,
        page: int = 1,
        page_size: int = 10,
        search: str | None = None,
    ):
        return self.repository.get_paginated(
            page=page,
            page_size=page_size,
            search=search,
        )

    def get_candidate_by_email(
        self,
        email: str,
    ) -> Candidate | None:
        return self.repository.get_by_email(email)

    def get_candidate_resumes(
        self,
        candidate_id: int,
    ):
        return self.repository.get_resumes(candidate_id)

    def get_or_create_candidate(
        self,
        profile: CandidateProfile,
    ) -> Candidate:

        if profile.email:
            existing = self.get_candidate_by_email(profile.email)

            if existing is not None:
                return existing

        return self.repository.create(
            name=profile.name,
            email=profile.email,
            phone=profile.phone,
            whatsapp_number=profile.whatsapp_number,
            linkedin_url=profile.linkedin_url,
            github_url=profile.github_url,
            portfolio_url=profile.portfolio_url,
            total_experience_years=profile.total_experience_years,
        )

    def get_or_create_candidate_profile_without_commit(
        self,
        profile: CandidateProfile,
    ) -> tuple[Candidate, bool]:

        if profile.email:
            existing = self.get_candidate_by_email(profile.email)

            if existing is not None:

                # Update newly extracted contact information
                # only when the new value is actually available.
                if profile.phone:
                    existing.phone = profile.phone

                if profile.whatsapp_number:
                    existing.whatsapp_number = (
                        profile.whatsapp_number
                    )

                if profile.linkedin_url:
                    existing.linkedin_url = profile.linkedin_url

                if profile.github_url:
                    existing.github_url = profile.github_url

                if profile.portfolio_url:
                    existing.portfolio_url = profile.portfolio_url

                if profile.name and not existing.name:
                    existing.name = profile.name

                if (
                    profile.total_experience_years is not None
                    and existing.total_experience_years is None
                ):
                    existing.total_experience_years = (
                        profile.total_experience_years
                    )

                self.db.flush()

                return existing, False

        candidate = self.create_candidate_profile_without_commit(
            profile
        )

        return candidate, True