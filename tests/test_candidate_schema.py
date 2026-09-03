from app.api.schemas.candidate import CandidateProfile

def test_candidate_profile():
    candidate = CandidateProfile(
        name="Kripa Kumar",
        email="kripa@example.com",
        phone="9876543210",
        total_experience_years=6.5,
        skills=["PHP", "Laravel", "Python"],
        education=["B.Tech"],
        projects=["AI Recruitment Platform"],
        certifications=["AWS"],
    )

    assert candidate.name == "Kripa Kumar"
    assert candidate.total_experience_years == 6.5
    assert "Laravel" in candidate.skills


def test_candidate_profile_defaults():
    candidate = CandidateProfile()

    assert candidate.name is None
    assert candidate.skills == []
    assert candidate.education == []
    assert candidate.projects == []
    assert candidate.certifications == []