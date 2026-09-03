from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.data.database import Base

class CandidateEducation(Base):
    __tablename__ = "candidate_education"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("candidates.id"),
        nullable=False,
    )

    education: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    candidate: Mapped["Candidate"] = relationship(
        "Candidate",
        back_populates="education",
    )