from app.api.schemas.job_requirements import JobRequirements

def test_job_requirements():
    requirements = JobRequirements(
        required_experience_years=5,
        required_skills=["PHP", "Laravel"],
        preferred_skills=["Python", "AI"],
        education_requirements=["B.Tech"],
        location="Remote",
        employment_type="Full-time",
        other_constraints=["Good communication"],
    )

    assert requirements.required_experience_years == 5
    assert "Laravel" in requirements.required_skills
    assert "Python" in requirements.preferred_skills


def test_job_requirements_defaults():
    requirements = JobRequirements()

    assert requirements.required_skills == []
    assert requirements.preferred_skills == []
    assert requirements.education_requirements == []
    assert requirements.other_constraints == []