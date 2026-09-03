from app.data.database import SessionLocal
from app.services.job_service import JobService

def test_create_job():
    db = SessionLocal()

    try:
        service = JobService(db)

        job = service.create_job(
            title="AI Engineer",
            description="Looking for a GenAI developer.",
        )

        assert job.id is not None
        assert job.title == "AI Engineer"
        assert job.description == "Looking for a GenAI developer."

    finally:
        db.close()

def test_get_all_jobs():
    db = SessionLocal()

    try:
        service = JobService(db)

        service.create_job(
            title="Python Developer",
            description="Python backend developer.",
        )

        service.create_job(
            title="AI Engineer",
            description="GenAI and LLM developer.",
        )

        jobs = service.get_all_jobs()

        assert len(jobs) >= 2
        assert jobs[-2].title == "Python Developer"
        assert jobs[-1].title == "AI Engineer"

    finally:
        db.close()

def test_get_job():
    db = SessionLocal()

    try:
        service = JobService(db)

        created_job = service.create_job(
            title="Backend Developer",
            description="Python backend developer.",
        )

        job = service.get_job(created_job.id)

        assert job is not None
        assert job.id == created_job.id
        assert job.title == "Backend Developer"

    finally:
        db.close()

def test_get_job_not_found():
    db = SessionLocal()

    try:
        service = JobService(db)

        job = service.get_job(999999)

        assert job is None

    finally:
        db.close()

def test_update_job():
    db = SessionLocal()

    try:
        service = JobService(db)

        created_job = service.create_job(
            title="Python Developer",
            description="Python backend developer.",
        )

        updated_job = service.update_job(
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
        service = JobService(db)

        updated_job = service.update_job(
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
        service = JobService(db)
        created_job = service.create_job(
            title="Temporary Developer",
            description="This job will be deleted.",
        )
        deleted = service.delete_job(created_job.id)
        assert deleted is True
        job = service.get_job(created_job.id)
        assert job is None
    finally:
        db.close()

def test_delete_job_not_found():
    db = SessionLocal()

    try:
        service = JobService(db)
        deleted = service.delete_job(999999)
        assert deleted is False
    finally:
        db.close()