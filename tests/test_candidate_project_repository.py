from app.data.models.candidate import Candidate
from app.data.repositories.candidate_project_repository import (
    CandidateProjectRepository,
)

def test_create_project(db_session):
    candidate = Candidate(
        name="Test Candidate",
        email="project-test@example.com",
    )

    db_session.add(candidate)
    db_session.commit()
    db_session.refresh(candidate)

    repository = CandidateProjectRepository(db_session)

    project = repository.create(
        candidate_id=candidate.id,
        project="AI Recruitment Platform",
    )

    assert project.id is not None
    assert project.candidate_id == candidate.id
    assert project.project == "AI Recruitment Platform"


def test_get_by_candidate_id(db_session):
    candidate = Candidate(
        name="Test Candidate",
        email="get-projects@example.com",
    )

    db_session.add(candidate)
    db_session.commit()
    db_session.refresh(candidate)

    repository = CandidateProjectRepository(db_session)

    repository.create(candidate.id, "AI Recruitment Platform")
    repository.create(candidate.id, "School Management System")
    repository.create(candidate.id, "E-commerce Application")

    projects = repository.get_by_candidate_id(candidate.id)

    assert len(projects) == 3
    assert projects[0].project == "AI Recruitment Platform"
    assert projects[1].project == "School Management System"
    assert projects[2].project == "E-commerce Application"


def test_get_by_candidate_id_returns_empty_list(db_session):
    candidate = Candidate(
        name="Test Candidate",
        email="empty-projects@example.com",
    )

    db_session.add(candidate)
    db_session.commit()
    db_session.refresh(candidate)

    repository = CandidateProjectRepository(db_session)

    projects = repository.get_by_candidate_id(candidate.id)

    assert projects == []


def test_delete_by_candidate_id(db_session):
    candidate = Candidate(
        name="Test Candidate",
        email="delete-projects@example.com",
    )

    db_session.add(candidate)
    db_session.commit()
    db_session.refresh(candidate)

    repository = CandidateProjectRepository(db_session)

    repository.create(candidate.id, "Project A")
    repository.create(candidate.id, "Project B")

    deleted_count = repository.delete_by_candidate_id(
        candidate.id
    )

    assert deleted_count == 2
    assert repository.get_by_candidate_id(candidate.id) == []