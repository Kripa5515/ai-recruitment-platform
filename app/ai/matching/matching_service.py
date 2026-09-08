from app.ai.embeddings.semantic_matching_service import (
    SemanticMatchingService,
)
from app.api.schemas.candidate import CandidateProfile
from app.api.schemas.job_requirements import JobRequirements
from app.ai.matching.schemas import (
    ExperienceMatchResult,
    MatchResult,
    SkillMatchResult,
)


class MatchingService:
    """
    Hybrid candidate matching service.

    Matching strategy:

    1. Deterministic matching
       - Experience
       - Required skills
       - Job constraints

    2. Semantic matching
       - Job text vs candidate resume text
       - Embedding-based similarity

    3. Hybrid final score
       - Experience: 20%
       - Required skills: 40%
       - Semantic similarity: 25%
       - Constraints: 15%

    4. Explainable matching
       - Human-readable reasons
       - Missing skills
       - Experience explanation
       - Warnings
       - Overall assessment

    Important:
    The matching score is calculated by deterministic and
    semantic logic. Explanations are generated from the
    calculated results and do not use an LLM.
    """

    EXPERIENCE_WEIGHT = 20.0
    REQUIRED_SKILLS_WEIGHT = 40.0
    SEMANTIC_WEIGHT = 25.0
    CONSTRAINT_WEIGHT = 15.0

    def __init__(
        self,
        semantic_matching_service: SemanticMatchingService | None = None,
    ) -> None:
        """
        Initialize MatchingService.

        semantic_matching_service is injectable so that tests
        can provide a fake semantic service without calling
        the real OpenAI API.
        """
        self.semantic_matching_service = semantic_matching_service

    def match(
        self,
        job: JobRequirements,
        candidate: CandidateProfile,
        candidate_id: int | None = None,
        job_text: str | None = None,
        candidate_text: str | None = None,
    ) -> MatchResult:
        """
        Match a candidate against job requirements.

        If job_text and candidate_text are provided,
        semantic matching is also performed and final_score
        contains the hybrid score.

        Otherwise only deterministic matching is performed.
        """

        # ---------------------------------------------------------
        # 1. Experience matching
        # ---------------------------------------------------------
        experience_match = self._match_experience(
            required_experience=job.required_experience_years,
            candidate_experience=candidate.total_experience_years,
        )

        # ---------------------------------------------------------
        # 2. Skill matching
        # ---------------------------------------------------------
        skill_match = self._match_skills(
            required_skills=job.required_skills,
            preferred_skills=job.preferred_skills,
            candidate_skills=candidate.skills,
        )

        # ---------------------------------------------------------
        # 3. Constraint matching
        # ---------------------------------------------------------
        constraint_score = self._calculate_constraint_score(
            job=job,
            candidate=candidate,
        )

        # ---------------------------------------------------------
        # 4. Deterministic score
        # ---------------------------------------------------------
        deterministic_score = self._calculate_deterministic_score(
            experience_score=experience_match.score,
            required_skill_score=skill_match.required_skill_score,
            constraint_score=constraint_score,
        )

        # ---------------------------------------------------------
        # 5. Semantic matching
        # ---------------------------------------------------------
        semantic_score: float | None = None
        final_score: float | None = None

        # Semantic matching tabhi chalega jab dono texts available hon.
        if job_text is not None and candidate_text is not None:
            semantic_service = (
                self.semantic_matching_service
                or SemanticMatchingService()
            )

            semantic_score = semantic_service.calculate_score(
                text_a=job_text,
                text_b=candidate_text,
            )

            # -----------------------------------------------------
            # 6. Hybrid final score
            # -----------------------------------------------------
            final_score = self._calculate_hybrid_score(
                experience_score=experience_match.score,
                required_skill_score=skill_match.required_skill_score,
                semantic_score=semantic_score,
                constraint_score=constraint_score,
            )

        # ---------------------------------------------------------
        # 7. Explainable reasons
        # ---------------------------------------------------------
        reasons = self._build_reasons(
            experience_match=experience_match,
            skill_match=skill_match,
            semantic_score=semantic_score,
            constraint_score=constraint_score,
            final_score=final_score,
        )

        # ---------------------------------------------------------
        # 8. Warnings
        # ---------------------------------------------------------
        warnings = self._build_warnings(
            experience_match=experience_match,
            skill_match=skill_match,
            constraint_score=constraint_score,
        )

        # ---------------------------------------------------------
        # 9. Final result
        # ---------------------------------------------------------
        return MatchResult(
            candidate_id=candidate_id,
            candidate_name=candidate.name,
            experience_score=experience_match.score,
            required_skill_score=skill_match.required_skill_score,
            preferred_skill_score=skill_match.preferred_skill_score,
            semantic_score=semantic_score,
            constraint_score=constraint_score,
            deterministic_score=deterministic_score,
            final_score=final_score,
            skill_match=skill_match,
            experience_match=experience_match,
            reasons=reasons,
            warnings=warnings,
        )

    # =============================================================
    # EXPERIENCE MATCHING
    # =============================================================

    def _match_experience(
        self,
        required_experience: float | None,
        candidate_experience: float | None,
    ) -> ExperienceMatchResult:
        """
        Calculate experience match score.

        Rules:

        - No experience requirement -> 100
        - Missing candidate experience -> 0
        - Candidate meets/exceeds requirement -> 100
        - Otherwise proportional score

        Also generates a human-readable explanation.
        """

        # ---------------------------------------------------------
        # No experience requirement
        # ---------------------------------------------------------
        if required_experience is None:
            return ExperienceMatchResult(
                score=100.0,
                required_experience_years=None,
                candidate_experience_years=candidate_experience,
                meets_requirement=True,
                explanation=(
                    "No specific experience requirement was provided."
                ),
            )

        # ---------------------------------------------------------
        # Candidate experience is missing
        # ---------------------------------------------------------
        if candidate_experience is None:
            return ExperienceMatchResult(
                score=0.0,
                required_experience_years=required_experience,
                candidate_experience_years=None,
                meets_requirement=False,
                explanation=(
                    "Candidate experience information is not available."
                ),
            )

        # ---------------------------------------------------------
        # Candidate meets or exceeds requirement
        # ---------------------------------------------------------
        if candidate_experience >= required_experience:
            score = 100.0
            meets_requirement = True

            explanation = (
                f"Candidate has {candidate_experience:g} years of "
                f"experience; {required_experience:g} years required."
            )

        # ---------------------------------------------------------
        # Candidate is below requirement
        # ---------------------------------------------------------
        else:
            score = max(
                0.0,
                min(
                    100.0,
                    (candidate_experience / required_experience) * 100.0,
                ),
            )

            meets_requirement = False

            explanation = (
                f"Candidate has {candidate_experience:g} years of "
                f"experience; {required_experience:g} years required."
            )

        return ExperienceMatchResult(
            score=round(score, 2),
            required_experience_years=required_experience,
            candidate_experience_years=candidate_experience,
            meets_requirement=meets_requirement,
            explanation=explanation,
        )

    # =============================================================
    # SKILL MATCHING
    # =============================================================

    def _match_skills(
        self,
        required_skills: list[str],
        preferred_skills: list[str],
        candidate_skills: list[str],
    ) -> SkillMatchResult:
        """
        Match required and preferred skills.

        Matching is case-insensitive.

        Example:

        Job:
            Python
            FastAPI

        Candidate:
            python
            fastapi

        Both are considered matches.
        """

        # ---------------------------------------------------------
        # Normalize candidate skills
        # ---------------------------------------------------------
        candidate_skill_set = {
            skill.strip().lower()
            for skill in candidate_skills
            if skill.strip()
        }

        # ---------------------------------------------------------
        # Normalize required skills
        # ---------------------------------------------------------
        required_skill_set = {
            skill.strip().lower()
            for skill in required_skills
            if skill.strip()
        }

        # ---------------------------------------------------------
        # Normalize preferred skills
        # ---------------------------------------------------------
        preferred_skill_set = {
            skill.strip().lower()
            for skill in preferred_skills
            if skill.strip()
        }

        # ---------------------------------------------------------
        # Required skill matching
        # ---------------------------------------------------------
        matched_required = sorted(
            required_skill_set.intersection(candidate_skill_set)
        )

        missing_required = sorted(
            required_skill_set.difference(candidate_skill_set)
        )

        # ---------------------------------------------------------
        # Preferred skill matching
        # ---------------------------------------------------------
        matched_preferred = sorted(
            preferred_skill_set.intersection(candidate_skill_set)
        )

        # ---------------------------------------------------------
        # Required skill score
        # ---------------------------------------------------------
        if required_skill_set:
            required_score = (
                len(matched_required) / len(required_skill_set)
            ) * 100.0
        else:
            required_score = 100.0

        # ---------------------------------------------------------
        # Preferred skill score
        # ---------------------------------------------------------
        if preferred_skill_set:
            preferred_score = (
                len(matched_preferred) / len(preferred_skill_set)
            ) * 100.0
        else:
            preferred_score = 0.0

        return SkillMatchResult(
            required_skills=sorted(required_skill_set),
            matched_required_skills=matched_required,
            missing_required_skills=missing_required,
            preferred_skills=sorted(preferred_skill_set),
            matched_preferred_skills=matched_preferred,
            required_skill_score=round(required_score, 2),
            preferred_skill_score=round(preferred_score, 2),
        )

    # =============================================================
    # CONSTRAINT MATCHING
    # =============================================================

    def _calculate_constraint_score(
        self,
        job: JobRequirements,
        candidate: CandidateProfile,
    ) -> float:
        """
        MVP constraint scoring.

        Currently candidate-specific structured constraint
        fields are not available.

        Therefore:

        - No explicit constraints -> 100
        - Explicit constraints -> 50

        This is intentionally an MVP implementation and can
        later be replaced with proper deterministic constraint
        evaluation.
        """

        if not job.other_constraints:
            return 100.0

        return 50.0

    # =============================================================
    # DETERMINISTIC SCORE
    # =============================================================

    def _calculate_deterministic_score(
        self,
        experience_score: float,
        required_skill_score: float,
        constraint_score: float,
    ) -> float:
        """
        Calculate deterministic matching score.

        Since semantic score is not available in deterministic
        mode, the available weights are normalized.

        Available weights:

        Experience      = 20
        Required Skills = 40
        Constraints     = 15

        Total            = 75
        """

        available_weight = (
            self.EXPERIENCE_WEIGHT
            + self.REQUIRED_SKILLS_WEIGHT
            + self.CONSTRAINT_WEIGHT
        )

        weighted_score = (
            experience_score * self.EXPERIENCE_WEIGHT
            + required_skill_score * self.REQUIRED_SKILLS_WEIGHT
            + constraint_score * self.CONSTRAINT_WEIGHT
        )

        return round(weighted_score / available_weight, 2)

    # =============================================================
    # HYBRID SCORE
    # =============================================================

    def _calculate_hybrid_score(
        self,
        experience_score: float,
        required_skill_score: float,
        semantic_score: float,
        constraint_score: float,
    ) -> float:
        """
        Calculate final hybrid matching score.

        Experience        = 20%
        Required Skills   = 40%
        Semantic          = 25%
        Constraints       = 15%

        Total             = 100%
        """

        weighted_score = (
            experience_score * self.EXPERIENCE_WEIGHT
            + required_skill_score * self.REQUIRED_SKILLS_WEIGHT
            + semantic_score * self.SEMANTIC_WEIGHT
            + constraint_score * self.CONSTRAINT_WEIGHT
        )

        total_weight = (
            self.EXPERIENCE_WEIGHT
            + self.REQUIRED_SKILLS_WEIGHT
            + self.SEMANTIC_WEIGHT
            + self.CONSTRAINT_WEIGHT
        )

        return round(weighted_score / total_weight, 2)

    # =============================================================
    # EXPLAINABLE REASONS
    # =============================================================

    def _build_reasons(
        self,
        experience_match: ExperienceMatchResult,
        skill_match: SkillMatchResult,
        semantic_score: float | None,
        constraint_score: float,
        final_score: float | None,
    ) -> list[str]:
        """
        Build human-readable explanations for the match.

        These reasons are generated only from calculated matching
        results. No LLM is used.
        """

        reasons: list[str] = []

        # ---------------------------------------------------------
        # Experience reason
        # ---------------------------------------------------------
        reasons.append(experience_match.explanation)

        # ---------------------------------------------------------
        # Required skills reason
        # ---------------------------------------------------------
        total_required = len(skill_match.required_skills)
        matched_required = len(
            skill_match.matched_required_skills
        )

        if total_required == 0:
            reasons.append(
                "No required skills were specified."
            )
        elif not skill_match.missing_required_skills:
            reasons.append(
                f"Candidate matches all {total_required} "
                "required skills."
            )
        else:
            reasons.append(
                f"Candidate matches {matched_required} of "
                f"{total_required} required skills."
            )

        # ---------------------------------------------------------
        # Preferred skills reason
        # ---------------------------------------------------------
        total_preferred = len(skill_match.preferred_skills)
        matched_preferred = len(
            skill_match.matched_preferred_skills
        )

        if total_preferred:
            if matched_preferred == total_preferred:
                reasons.append(
                    f"Candidate matches all {total_preferred} "
                    "preferred skills."
                )
            elif matched_preferred:
                reasons.append(
                    f"Candidate matches {matched_preferred} of "
                    f"{total_preferred} preferred skills."
                )
            else:
                reasons.append(
                    "Candidate does not match any preferred skills."
                )

        # ---------------------------------------------------------
        # Semantic reason
        # ---------------------------------------------------------
        if semantic_score is not None:
            reasons.append(
                f"Resume and job description semantic similarity "
                f"is {semantic_score:.2f}%."
            )

        # ---------------------------------------------------------
        # Constraint reason
        # ---------------------------------------------------------
        if constraint_score >= 100:
            reasons.append(
                "No constraint mismatch was identified."
            )
        else:
            reasons.append(
                "Some job constraints may require review."
            )

        # ---------------------------------------------------------
        # Overall assessment
        # ---------------------------------------------------------
        if final_score is not None:
            reasons.append(
                self._build_overall_assessment(final_score)
            )

        return reasons

    # =============================================================
    # WARNINGS
    # =============================================================

    def _build_warnings(
        self,
        experience_match: ExperienceMatchResult,
        skill_match: SkillMatchResult,
        constraint_score: float,
    ) -> list[str]:
        """
        Build warnings that HR should review.
        """

        warnings: list[str] = []

        # ---------------------------------------------------------
        # Experience warning
        # ---------------------------------------------------------
        if not experience_match.meets_requirement:
            warnings.append(
                "Experience requirement is not fully satisfied."
            )

        # ---------------------------------------------------------
        # Missing required skills
        # ---------------------------------------------------------
        if skill_match.missing_required_skills:
            missing_skills = ", ".join(
                skill_match.missing_required_skills
            )

            warnings.append(
                f"Missing required skills: {missing_skills}."
            )

        # ---------------------------------------------------------
        # Constraint warning
        # ---------------------------------------------------------
        if constraint_score < 100:
            warnings.append(
                "Some job constraints may require HR review."
            )

        return warnings

    # =============================================================
    # OVERALL ASSESSMENT
    # =============================================================

    def _build_overall_assessment(
        self,
        final_score: float,
    ) -> str:
        """
        Convert the calculated score into a human-readable
        assessment.

        This is not a hiring decision. It is only a matching
        interpretation for recruiter review.
        """

        if final_score >= 80:
            return (
                f"Overall match assessment: Strong Match "
                f"({final_score:.2f}%)."
            )

        if final_score >= 60:
            return (
                f"Overall match assessment: Good Match "
                f"({final_score:.2f}%)."
            )

        if final_score >= 40:
            return (
                f"Overall match assessment: Moderate Match "
                f"({final_score:.2f}%)."
            )

        return (
            f"Overall match assessment: Low Match "
            f"({final_score:.2f}%)."
        )