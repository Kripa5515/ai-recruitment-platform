from types import SimpleNamespace
import pytest
from app.ai.extraction.candidate_extractor import CandidateExtractor
from app.api.schemas.candidate import CandidateProfile


def test_candidate_extractor_returns_structured_profile(
    monkeypatch,
):
    expected_profile = CandidateProfile(
        name="Kripa Kumar",
        email="kripa@example.com",
        phone="9876543210",
        total_experience_years=6.5,
        skills=["PHP", "Laravel", "Python"],
        education=["B.Tech"],
        projects=["AI Recruitment Platform"],
        certifications=[],
    )

    fake_response = SimpleNamespace(
        output_parsed=expected_profile
    )

    class FakeResponses:
        def parse(self, **kwargs):
            return fake_response

    class FakeClient:
        responses = FakeResponses()

    extractor = CandidateExtractor.__new__(
        CandidateExtractor
    )

    extractor.llm = SimpleNamespace(
        client=FakeClient()
    )

    result = extractor.extract(
        "Kripa Kumar is a Senior Developer..."
    )

    assert isinstance(result, CandidateProfile)
    assert result.name == "Kripa Kumar"
    assert result.total_experience_years == 6.5
    assert "Laravel" in result.skills

def test_candidate_extractor_rejects_empty_text():
    extractor = CandidateExtractor.__new__(
        CandidateExtractor
    )

    with pytest.raises(ValueError, match="Resume text cannot be empty"):
        extractor.extract("   ")