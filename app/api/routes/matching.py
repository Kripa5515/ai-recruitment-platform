from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai.matching.matching_service import MatchingService
from app.api.dependencies.database import get_db
from app.api.schemas.candidate import CandidateProfile
from app.api.schemas.job_requirements import JobRequirements
from app.api.schemas.matching import (
    MatchingCandidateResponse,
    MatchingResponse,
)
from app.data.repositories.candidate_repository import (
    CandidateRepository,
)
from app.data.repositories.job_repository import JobRepository
from app.data.repositories.resume_repository import ResumeRepository


router = APIRouter(
    prefix="/matching",
    tags=["Matching"],
)


@router.post(
    "/jobs/{job_id}/candidates",
    response_model=MatchingResponse,
)
def match_candidates_for_job(
    job_id: int,
    db: Session = Depends(get_db),
):

    job_repository = JobRepository(db)

    candidate_repository = CandidateRepository(db)

    resume_repository = ResumeRepository(db)

    job = job_repository.get_by_id(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail=f"Job with id {job_id} not found.",
        )

    job_requirements = JobRequirements(
        required_experience_years=job.required_experience_years,
        required_skills=job.required_skills or [],
        preferred_skills=job.preferred_skills or [],
        education_requirements=job.education_requirements or [],
        location=job.location,
        employment_type=job.employment_type,
        other_constraints=job.other_constraints or [],
    )

    candidates = candidate_repository.get_all()

    matching_service = MatchingService()

    results = []

    for candidate in candidates:

        candidate_skills = [
            skill.skill_name
            for skill in candidate.skills
            if skill.skill_name
        ]

        candidate_education = [
            education.education
            for education in candidate.education
            if education.education
        ]

        candidate_projects = [
            project.project
            for project in candidate.projects
            if project.project
        ]

        candidate_certifications = [
            certification.certification
            for certification in candidate.certifications
            if certification.certification
        ]

        candidate_profile = CandidateProfile(
            name=candidate.name,

            email=candidate.email,
            phone=candidate.phone,
            whatsapp_number=candidate.whatsapp_number,

            linkedin_url=candidate.linkedin_url,
            github_url=candidate.github_url,
            portfolio_url=candidate.portfolio_url,

            total_experience_years=(
                candidate.total_experience_years
            ),

            skills=candidate_skills,
            education=candidate_education,
            projects=candidate_projects,
            certifications=candidate_certifications,
        )

        current_resume = (
            resume_repository
            .get_current_resume_by_candidate_id(
                candidate.id
            )
        )

        candidate_text = (
            current_resume.extracted_text
            if current_resume is not None
            else None
        )

        match_result = matching_service.match(
            job=job_requirements,
            candidate=candidate_profile,
            candidate_id=candidate.id,
            job_text=job.description,
            candidate_text=candidate_text,
        )

        results.append(
            MatchingCandidateResponse(
                candidate_id=match_result.candidate_id,
                candidate_name=match_result.candidate_name,

                email=candidate.email,
                phone=candidate.phone,
                whatsapp_number=candidate.whatsapp_number,

                linkedin_url=candidate.linkedin_url,
                github_url=candidate.github_url,
                portfolio_url=candidate.portfolio_url,

                experience_score=(
                    match_result.experience_score
                ),

                required_skill_score=(
                    match_result.required_skill_score
                ),

                preferred_skill_score=(
                    match_result.preferred_skill_score
                ),

                semantic_score=(
                    match_result.semantic_score
                ),

                constraint_score=(
                    match_result.constraint_score
                ),

                deterministic_score=(
                    match_result.deterministic_score
                ),

                final_score=(
                    match_result.final_score
                ),

                reasons=match_result.reasons,

                warnings=match_result.warnings,
            )
        )

    results.sort(
        key=lambda item: (
            item.final_score
            if item.final_score is not None
            else item.deterministic_score
        ),
        reverse=True,
    )

    return MatchingResponse(
        job_id=job.id,
        job_title=job.title,
        total_candidates=len(candidates),
        matched_candidates=len(results),
        results=results,
    )