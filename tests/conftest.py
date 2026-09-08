import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.data.database import Base
# Ensure all models are registered in Base.metadata
from app.data.models.candidate import Candidate  # noqa: F401
from app.data.models.job import Job  # noqa: F401
from app.data.models.resume import Resume  # noqa: F401


@pytest.fixture
def db_session():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(test_engine)

    with Session(bind=test_engine) as session:
        yield session

    Base.metadata.drop_all(test_engine)
    test_engine.dispose()