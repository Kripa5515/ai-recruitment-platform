from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.data.database import Base

class CandidateProject(Base):
    __tablename__ = "candidate_projects"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("candidates.id"),
        nullable=False,
    )

    project: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    candidate: Mapped["Candidate"] = relationship(
        "Candidate",
        back_populates="projects",
    )