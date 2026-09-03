from app.data.models.candidate import Candidate
from app.data.repositories.candidate_skill_repository import (
    CandidateSkillRepository,
)

def test_create_skill(db_session):
    candidate = Candidate(
        name="Test Candidate",
        email="skill-test@example.com",
    )

    db_session.add(candidate)
    db_session.commit()
    db_session.refresh(candidate)

    repository = CandidateSkillRepository(db_session)

    skill = repository.create(
        candidate_id=candidate.id,
        skill_name="Python",
    )

    assert skill.id is not None
    assert skill.candidate_id == candidate.id
    assert skill.skill_name == "Python"


def test_get_by_candidate_id(db_session):
    candidate = Candidate(
        name="Test Candidate",
        email="get-skills@example.com",
    )

    db_session.add(candidate)
    db_session.commit()
    db_session.refresh(candidate)

    repository = CandidateSkillRepository(db_session)

    repository.create(candidate.id, "Python")
    repository.create(candidate.id, "Laravel")
    repository.create(candidate.id, "PostgreSQL")

    skills = repository.get_by_candidate_id(candidate.id)

    assert len(skills) == 3
    assert skills[0].skill_name == "Python"
    assert skills[1].skill_name == "Laravel"
    assert skills[2].skill_name == "PostgreSQL"


def test_get_by_candidate_id_returns_empty_list(db_session):
    candidate = Candidate(
        name="Test Candidate",
        email="empty-skills@example.com",
    )

    db_session.add(candidate)
    db_session.commit()
    db_session.refresh(candidate)

    repository = CandidateSkillRepository(db_session)

    skills = repository.get_by_candidate_id(candidate.id)

    assert skills == []


def test_delete_by_candidate_id(db_session):
    candidate = Candidate(
        name="Test Candidate",
        email="delete-skills@example.com",
    )

    db_session.add(candidate)
    db_session.commit()
    db_session.refresh(candidate)

    repository = CandidateSkillRepository(db_session)

    repository.create(candidate.id, "Python")
    repository.create(candidate.id, "Laravel")

    deleted_count = repository.delete_by_candidate_id(
        candidate.id
    )

    assert deleted_count == 2
    assert repository.get_by_candidate_id(candidate.id) == []