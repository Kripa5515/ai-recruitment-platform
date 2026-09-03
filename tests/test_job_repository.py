from app.data.repositories.job_repository import JobRepository
from app.data.database import SessionLocal

def test_create_job():
    db = SessionLocal()

    try:
        repository = JobRepository(db)

        job = repository.create(
            title="Python Developer",
            description="Looking for a Python developer.",
        )

        assert job.id is not None
        assert job.title == "Python Developer"
        assert job.description == "Looking for a Python developer."

    finally:
        db.close()

def test_get_all_jobs():
    db = SessionLocal()

    try:
        repository = JobRepository(db)

        repository.create(
            title="Python Developer",
            description="Python backend developer.",
        )

        repository.create(
            title="AI Engineer",
            description="GenAI and LLM developer.",
        )

        jobs = repository.get_all()

        assert len(jobs) >= 2
        assert jobs[-2].title == "Python Developer"
        assert jobs[-1].title == "AI Engineer"

    finally:
        db.close()


def test_get_job_by_id():
    db = SessionLocal()

    try:
        repository = JobRepository(db)

        created_job = repository.create(
            title="Senior AI Engineer",
            description="Python, LLM and RAG developer.",
        )

        job = repository.get_by_id(created_job.id)

        assert job is not None
        assert job.id == created_job.id
        assert job.title == "Senior AI Engineer"

    finally:
        db.close()

def test_get_job_by_id_not_found():
    db = SessionLocal()

    try:
        repository = JobRepository(db)

        job = repository.get_by_id(999999)

        assert job is None

    finally:
        db.close()

def test_update_job():
    db = SessionLocal()

    try:
        repository = JobRepository(db)

        created_job = repository.create(
            title="Python Developer",
            description="Python backend developer.",
        )

        updated_job = repository.update(
            job_id=created_job.id,
            title="Senior Python Developer",
            description="Python, FastAPI and PostgreSQL developer.",
        )

        assert updated_job is not None
        assert updated_job.id == created_job.id
        assert updated_job.title == "Senior Python Developer"
        assert updated_job.description == (
            "Python, FastAPI and PostgreSQL developer."
        )

    finally:
        db.close()

def test_update_job_not_found():
    db = SessionLocal()

    try:
        repository = JobRepository(db)
        updated_job = repository.update(
            job_id=999999,
            title="Senior Developer",
            description="Updated description.",
        )
        assert updated_job is None

    finally:
        db.close()

def test_delete_job():
    db = SessionLocal()

    try:
        repository = JobRepository(db)
        created_job = repository.create(
            title="Temporary Developer",
            description="This job will be deleted.",
        )

        deleted = repository.delete(created_job.id)
        assert deleted is True
        job = repository.get_by_id(created_job.id)
        assert job is None

    finally:
        db.close()

def test_delete_job_not_found():
    db = SessionLocal()
    try:
        repository = JobRepository(db)
        deleted = repository.delete(999999)
        assert deleted is False
    finally:
        db.close()