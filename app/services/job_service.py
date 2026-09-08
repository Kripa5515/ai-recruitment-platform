import re

from sqlalchemy.orm import Session

from app.ai.extraction.job_extractor import JobExtractor
from app.api.schemas.job_requirements import JobRequirements
from app.data.models.job import Job
from app.data.repositories.job_repository import JobRepository


class JobService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = JobRepository(db)
        self.extractor = JobExtractor()

    # =========================================================
    # Experience Parser
    # =========================================================

    @staticmethod
    def parse_experience_years(
        experience_required: str | None,
    ) -> float | None:

        if not experience_required:
            return None

        value = experience_required.strip().lower()

        if not value:
            return None

        # -----------------------------------------------------
        # Examples:
        # "3+"
        # "3+ years"
        # "minimum 3 years"
        # "3 years"
        # -----------------------------------------------------

        minimum_match = re.search(
            r"(?:minimum|min|at\s*least)?\s*(\d+(?:\.\d+)?)\s*\+?",
            value,
        )

        if minimum_match:
            return float(minimum_match.group(1))

        # -----------------------------------------------------
        # Examples:
        # "5-7 years"
        # "5 to 7 years"
        # -----------------------------------------------------

        range_match = re.search(
            r"(\d+(?:\.\d+)?)\s*(?:-|to)\s*(\d+(?:\.\d+)?)",
            value,
        )

        if range_match:
            return float(range_match.group(1))

        return None

    # =========================================================
    # Job Requirement Extraction
    # =========================================================

    def extract_requirements(
        self,
        job_description: str,
    ) -> JobRequirements:

        return self.extractor.extract(job_description)

    # =========================================================
    # Analyze JD
    # =========================================================

    def analyze_jd(
        self,
        job_description: str,
    ) -> JobRequirements:

        """
        Analyze an unstructured JD and return structured
        requirements.

        IMPORTANT:
        This method does NOT create or update a database record.

        The extracted result can be reviewed and edited by HR
        before the final Job creation.
        """

        if not job_description or not job_description.strip():
            raise ValueError(
                "Job description cannot be empty."
            )

        return self.extract_requirements(
            job_description
        )

    # =========================================================
    # Create Job
    # =========================================================

    def create_job(
        self,
        title: str,
        description: str,
        company: str,
        location: str,
        experience_required: str,
        employment_type: str,
        status: str = "draft",
    ) -> Job:

        try:

            # -------------------------------------------------
            # 1. Deterministic experience extraction
            # -------------------------------------------------

            required_experience_years = (
                self.parse_experience_years(
                    experience_required
                )
            )

            # -------------------------------------------------
            # 2. AI-based JD requirement extraction
            # -------------------------------------------------

            requirements = self.extract_requirements(
                description
            )

            # -------------------------------------------------
            # 3. Save complete structured job
            # -------------------------------------------------

            job = self.repository.create(
                title=title,
                description=description,
                company=company,
                location=location,
                experience_required=experience_required,
                employment_type=employment_type,
                status=status,
                required_experience_years=(
                    required_experience_years
                ),
                required_skills=(
                    requirements.required_skills
                    or []
                ),
                preferred_skills=(
                    requirements.preferred_skills
                    or []
                ),
                education_requirements=(
                    requirements.education_requirements
                    or []
                ),
                other_constraints=(
                    requirements.other_constraints
                    or []
                ),
            )

            self.db.commit()
            self.db.refresh(job)

            return job

        except Exception:
            self.db.rollback()
            raise

    # =========================================================
    # Get All Jobs
    # =========================================================

    def get_all_jobs(self) -> list[Job]:

        return self.repository.get_all()

    # =========================================================
    # Get Single Job
    # =========================================================

    def get_job(
        self,
        job_id: int,
    ) -> Job | None:

        return self.repository.get_by_id(job_id)

    # =========================================================
    # Update Job
    # =========================================================

    def update_job(
        self,
        job_id: int,
        title: str,
        description: str,
        company: str,
        location: str,
        experience_required: str,
        employment_type: str,
        status: str,
    ) -> Job | None:

        try:

            # -------------------------------------------------
            # Recalculate structured requirements
            # -------------------------------------------------

            required_experience_years = (
                self.parse_experience_years(
                    experience_required
                )
            )

            requirements = self.extract_requirements(
                description
            )

            # -------------------------------------------------
            # Update complete job
            # -------------------------------------------------

            return self.repository.update(
                job_id=job_id,
                title=title,
                description=description,
                company=company,
                location=location,
                experience_required=experience_required,
                employment_type=employment_type,
                status=status,
                required_experience_years=(
                    required_experience_years
                ),
                required_skills=(
                    requirements.required_skills
                    or []
                ),
                preferred_skills=(
                    requirements.preferred_skills
                    or []
                ),
                education_requirements=(
                    requirements.education_requirements
                    or []
                ),
                other_constraints=(
                    requirements.other_constraints
                    or []
                ),
            )

        except Exception:
            self.db.rollback()
            raise

    # =========================================================
    # Delete Job
    # =========================================================

    def delete_job(
        self,
        job_id: int,
    ) -> bool:

        return self.repository.delete(job_id)

    # =========================================================
    # Paginated Jobs
    # =========================================================

    def get_paginated_jobs(
        self,
        page: int,
        page_size: int,
        search: str | None = None,
    ) -> tuple[list[Job], int]:

        return self.repository.get_paginated(
            page=page,
            page_size=page_size,
            search=search,
        )