from types import SimpleNamespace

import pytest

from app.ai.extraction.job_extractor import JobExtractor
from app.api.schemas.job_requirements import JobRequirements


def test_job_extractor_returns_structured_requirements(
    monkeypatch,
):
    expected_requirements = JobRequirements(
        required_experience_years=5,
        required_skills=[
            "PHP",
            "Laravel",
            "PostgreSQL",
            "REST API",
        ],
        preferred_skills=[
            "React",
            "Docker",
        ],
        education_requirements=[],
        location="Remote",
        employment_type="Full-time",
        other_constraints=[],
    )

    fake_response = SimpleNamespace(
        output_parsed=expected_requirements
    )

    class FakeResponses:
        def parse(self, **kwargs):
            return fake_response

    class FakeClient:
        responses = FakeResponses()

    extractor = JobExtractor.__new__(JobExtractor)

    extractor.llm = SimpleNamespace(
        client=FakeClient()
    )

    result = extractor.extract(
        """
        Senior PHP Developer

        5+ years of experience required.

        Required:
        PHP, Laravel, PostgreSQL, REST API

        Good to have:
        React, Docker

        Location: Remote
        Employment: Full-time
        """
    )

    assert isinstance(result, JobRequirements)
    assert result.required_experience_years == 5
    assert "Laravel" in result.required_skills
    assert "React" in result.preferred_skills
    assert result.location == "Remote"
    assert result.employment_type == "Full-time"


def test_job_extractor_rejects_empty_text():
    extractor = JobExtractor.__new__(JobExtractor)

    with pytest.raises(
        ValueError,
        match="Job description cannot be empty",
    ):
        extractor.extract("   ")