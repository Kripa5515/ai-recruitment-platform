from app.data.repositories.job_repository import JobRepository
from app.data.database import SessionLocal

def test_create_job():
    db = SessionLocal()
    try:
        repository = JobRepository(db)
        job = repository.create(
            title="Python Developer",
            description="Looking for a Python developer.",
            company="ABC Technologies",
            location="Noida",
            experience_required="5+ years",
            employment_type="Full-time",
        )

        assert job.id is not None
        assert job.title == "Python Developer"
        assert job.description == "Looking for a Python developer."
        assert job.company == "ABC Technologies"
        assert job.location == "Noida"
        assert job.experience_required == "5+ years"
        assert job.employment_type == "Full-time"
        assert job.status == "draft"

    finally:
        db.close()


def test_get_all_jobs():
    db = SessionLocal()
    try:
        repository = JobRepository(db)
        repository.create(
            title="Python Developer",
            description="Python backend developer.",
            company="ABC Technologies",
            location="Noida",
            experience_required="3+ years",
            employment_type="Full-time",
        )

        repository.create(
            title="AI Engineer",
            description="GenAI and LLM developer.",
            company="AI Solutions",
            location="Bangalore",
            experience_required="4+ years",
            employment_type="Full-time",
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
            company="AI Solutions",
            location="Bangalore",
            experience_required="5+ years",
            employment_type="Full-time",
        )
        job = repository.get_by_id(created_job.id)
        assert job is not None
        assert job.id == created_job.id
        assert job.title == "Senior AI Engineer"
        assert job.company == "AI Solutions"
        assert job.location == "Bangalore"
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
            company="ABC Technologies",
            location="Noida",
            experience_required="3+ years",
            employment_type="Full-time",
        )
        updated_job = repository.update(
            job_id=created_job.id,
            title="Senior Python Developer",
            description="Python, FastAPI and PostgreSQL developer.",
            company="XYZ Solutions",
            location="Bangalore",
            experience_required="6+ years",
            employment_type="Full-time",
            status="active",
        )
        assert updated_job is not None
        assert updated_job.id == created_job.id
        assert updated_job.title == "Senior Python Developer"
        assert updated_job.description == (
            "Python, FastAPI and PostgreSQL developer."
        )
        assert updated_job.company == "XYZ Solutions"
        assert updated_job.location == "Bangalore"
        assert updated_job.experience_required == "6+ years"
        assert updated_job.employment_type == "Full-time"
        assert updated_job.status == "active"

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
            company="ABC Technologies",
            location="Delhi",
            experience_required="5+ years",
            employment_type="Full-time",
            status="active",
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
            company="Temporary Company",
            location="Noida",
            experience_required="2+ years",
            employment_type="Full-time",
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