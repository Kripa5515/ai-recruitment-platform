from app.api.schemas.candidate import CandidateProfile
from app.api.schemas.job_requirements import JobRequirements
from app.ai.matching.schemas import (
    ExperienceMatchResult,
    MatchResult,
    SkillMatchResult,
)


class MatchingService:
    EXPERIENCE_WEIGHT = 20.0
    REQUIRED_SKILLS_WEIGHT = 40.0
    SEMANTIC_WEIGHT = 25.0
    CONSTRAINT_WEIGHT = 15.0

    def match(
        self,
        job: JobRequirements,
        candidate: CandidateProfile,
        candidate_id: int | None = None,
    ) -> MatchResult:
        experience_match = self.match_experience(
            required_experience_years=job.required_experience_years,
            candidate_experience_years=candidate.total_experience_years,
        )

        skill_match = self.match_skills(
            required_skills=job.required_skills,
            preferred_skills=job.preferred_skills,
            candidate_skills=candidate.skills,
        )

        deterministic_score = self.calculate_deterministic_score(
            experience_score=experience_match.score,
            required_skill_score=skill_match.required_skill_score,
            constraint_score=100.0,
        )

        reasons = self.build_reasons(
            experience_match,
            skill_match,
        )

        warnings = self.build_warnings(
            experience_match,
            skill_match,
        )

        return MatchResult(
            candidate_id=candidate_id,
            candidate_name=candidate.name,
            experience_score=experience_match.score,
            required_skill_score=skill_match.required_skill_score,
            preferred_skill_score=skill_match.preferred_skill_score,
            semantic_score=None,
            constraint_score=100.0,
            deterministic_score=deterministic_score,
            final_score=None,
            skill_match=skill_match,
            experience_match=experience_match,
            reasons=reasons,
            warnings=warnings,
        )

    def match_experience(
        self,
        required_experience_years: float | None,
        candidate_experience_years: float | None,
    ) -> ExperienceMatchResult:
        if required_experience_years is None:
            return ExperienceMatchResult(
                required_experience_years=None,
                candidate_experience_years=candidate_experience_years,
                meets_requirement=None,
                score=100.0,
                explanation=(
                    "No specific experience requirement "
                    "was provided."
                ),
            )

        if candidate_experience_years is None:
            return ExperienceMatchResult(
                required_experience_years=required_experience_years,
                candidate_experience_years=None,
                meets_requirement=False,
                score=0.0,
                explanation=(
                    "Candidate experience could not "
                    "be determined."
                ),
            )

        if candidate_experience_years >= required_experience_years:
            return ExperienceMatchResult(
                required_experience_years=required_experience_years,
                candidate_experience_years=candidate_experience_years,
                meets_requirement=True,
                score=100.0,
                explanation=(
                    "Candidate meets or exceeds the "
                    "required experience."
                ),
            )

        ratio = (
            candidate_experience_years
            / required_experience_years
        )

        score = min(
            100.0,
            max(0.0, ratio * 100.0),
        )

        return ExperienceMatchResult(
            required_experience_years=required_experience_years,
            candidate_experience_years=candidate_experience_years,
            meets_requirement=False,
            score=score,
            explanation=(
                "Candidate has less experience than required."
            ),
        )

    def match_skills(
        self,
        required_skills: list[str],
        preferred_skills: list[str],
        candidate_skills: list[str],
    ) -> SkillMatchResult:
        normalized_candidate_skills = {
            self.normalize_skill(skill)
            for skill in candidate_skills
            if skill
        }

        normalized_required = {
            self.normalize_skill(skill): skill
            for skill in required_skills
            if skill
        }

        normalized_preferred = {
            self.normalize_skill(skill): skill
            for skill in preferred_skills
            if skill
        }

        matched_required_keys = (
            set(normalized_required)
            & normalized_candidate_skills
        )

        matched_preferred_keys = (
            set(normalized_preferred)
            & normalized_candidate_skills
        )

        matched_required_skills = [
            normalized_required[key]
            for key in normalized_required
            if key in matched_required_keys
        ]

        missing_required_skills = [
            normalized_required[key]
            for key in normalized_required
            if key not in matched_required_keys
        ]

        matched_preferred_skills = [
            normalized_preferred[key]
            for key in normalized_preferred
            if key in matched_preferred_keys
        ]

        required_skill_score = self.calculate_skill_score(
            total=len(normalized_required),
            matched=len(matched_required_keys),
        )

        preferred_skill_score = self.calculate_skill_score(
            total=len(normalized_preferred),
            matched=len(matched_preferred_keys),
        )

        return SkillMatchResult(
            required_skills=required_skills,
            matched_required_skills=matched_required_skills,
            missing_required_skills=missing_required_skills,
            preferred_skills=preferred_skills,
            matched_preferred_skills=matched_preferred_skills,
            required_skill_score=required_skill_score,
            preferred_skill_score=preferred_skill_score,
        )

    @staticmethod
    def calculate_skill_score(
        total: int,
        matched: int,
    ) -> float:
        if total == 0:
            return 100.0

        score = (matched / total) * 100.0

        return round(
            min(100.0, max(0.0, score)),
            2,
        )

    @staticmethod
    def normalize_skill(skill: str) -> str:
        return " ".join(
            skill.lower().strip().split()
        )

    def calculate_deterministic_score(
        self,
        experience_score: float,
        required_skill_score: float,
        constraint_score: float,
    ) -> float:
        available_weight = (
            self.EXPERIENCE_WEIGHT
            + self.REQUIRED_SKILLS_WEIGHT
            + self.CONSTRAINT_WEIGHT
        )

        weighted_score = (
            experience_score
            * self.EXPERIENCE_WEIGHT
        ) + (
            required_skill_score
            * self.REQUIRED_SKILLS_WEIGHT
        ) + (
            constraint_score
            * self.CONSTRAINT_WEIGHT
        )

        score = weighted_score / available_weight

        return round(
            min(100.0, max(0.0, score)),
            2,
        )

    @staticmethod
    def build_reasons(
        experience_match: ExperienceMatchResult,
        skill_match: SkillMatchResult,
    ) -> list[str]:
        reasons: list[str] = []

        if experience_match.meets_requirement is True:
            reasons.append(
                "Candidate meets the required experience."
            )

        if skill_match.matched_required_skills:
            reasons.append(
                "Matched required skills: "
                + ", ".join(
                    skill_match.matched_required_skills
                )
                + "."
            )

        if skill_match.matched_preferred_skills:
            reasons.append(
                "Matched preferred skills: "
                + ", ".join(
                    skill_match.matched_preferred_skills
                )
                + "."
            )

        return reasons

    @staticmethod
    def build_warnings(
        experience_match: ExperienceMatchResult,
        skill_match: SkillMatchResult,
    ) -> list[str]:
        warnings: list[str] = []

        if experience_match.meets_requirement is False:
            warnings.append(
                experience_match.explanation
            )

        if skill_match.missing_required_skills:
            warnings.append(
                "Missing required skills: "
                + ", ".join(
                    skill_match.missing_required_skills
                )
                + "."
            )

        return warnings