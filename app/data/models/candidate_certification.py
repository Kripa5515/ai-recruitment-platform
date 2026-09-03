from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.data.database import Base

class CandidateCertification(Base):
    __tablename__ = "candidate_certifications"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("candidates.id"),
        nullable=False,
    )

    certification: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    candidate: Mapped["Candidate"] = relationship(
        "Candidate",
        back_populates="certifications",
    )