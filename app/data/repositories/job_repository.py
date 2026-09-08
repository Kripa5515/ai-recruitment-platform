from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.data.models.job import Job


class JobRepository:

    def __init__(self, db: Session):
        self.db = db

    # =========================================================
    # Create
    # =========================================================

    def create(
        self,
        title: str,
        description: str,
        company: str,
        location: str,
        experience_required: str,
        employment_type: str,
        status: str = "draft",
        required_experience_years: float | None = None,
        required_skills: list[str] | None = None,
        preferred_skills: list[str] | None = None,
        education_requirements: list[str] | None = None,
        other_constraints: list[str] | None = None,
    ) -> Job:

        job = Job(
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
                required_skills or []
            ),

            preferred_skills=(
                preferred_skills or []
            ),

            education_requirements=(
                education_requirements or []
            ),

            other_constraints=(
                other_constraints or []
            ),
        )

        self.db.add(job)
        self.db.flush()

        return job

    # =========================================================
    # Get All
    # =========================================================

    def get_all(self) -> list[Job]:

        statement = (
            select(Job)
            .order_by(Job.id.desc())
        )

        result = self.db.execute(statement)

        return list(result.scalars().all())

    # =========================================================
    # Get By ID
    # =========================================================

    def get_by_id(
        self,
        job_id: int,
    ) -> Job | None:

        statement = (
            select(Job)
            .where(Job.id == job_id)
        )

        result = self.db.execute(statement)

        return result.scalar_one_or_none()

    # =========================================================
    # Update
    # =========================================================

    def update(
        self,
        job_id: int,
        title: str,
        description: str,
        company: str,
        location: str,
        experience_required: str,
        employment_type: str,
        status: str,
        required_experience_years: float | None = None,
        required_skills: list[str] | None = None,
        preferred_skills: list[str] | None = None,
        education_requirements: list[str] | None = None,
        other_constraints: list[str] | None = None,
    ) -> Job | None:

        job = self.get_by_id(job_id)

        if job is None:
            return None

        job.title = title
        job.description = description
        job.company = company
        job.location = location
        job.experience_required = experience_required
        job.employment_type = employment_type
        job.status = status

        job.required_experience_years = (
            required_experience_years
        )

        job.required_skills = (
            required_skills or []
        )

        job.preferred_skills = (
            preferred_skills or []
        )

        job.education_requirements = (
            education_requirements or []
        )

        job.other_constraints = (
            other_constraints or []
        )

        self.db.commit()
        self.db.refresh(job)

        return job

    # =========================================================
    # Delete
    # =========================================================

    def delete(
        self,
        job_id: int,
    ) -> bool:

        job = self.get_by_id(job_id)

        if job is None:
            return False

        self.db.delete(job)
        self.db.commit()

        return True

    # =========================================================
    # Pagination
    # =========================================================

    def get_paginated(
        self,
        page: int,
        page_size: int,
        search: str | None = None,
    ) -> tuple[list[Job], int]:

        offset = (page - 1) * page_size

        jobs_statement = select(Job)
        count_statement = select(
            func.count(Job.id)
        )

        if search:
            search_pattern = (
                f"%{search.strip()}%"
            )

            search_filter = (
                Job.title.ilike(search_pattern)
                | Job.company.ilike(search_pattern)
                | Job.location.ilike(search_pattern)
                | Job.description.ilike(search_pattern)
            )

            jobs_statement = (
                jobs_statement.where(search_filter)
            )

            count_statement = (
                count_statement.where(search_filter)
            )

        jobs_statement = (
            jobs_statement
            .order_by(Job.id.desc())
            .offset(offset)
            .limit(page_size)
        )

        jobs = list(
            self.db.scalars(
                jobs_statement
            ).all()
        )

        total = (
            self.db.scalar(count_statement)
            or 0
        )

        return jobs, total