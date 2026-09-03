from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.data.database import Base

if TYPE_CHECKING:
    from app.data.models.candidate_certification import CandidateCertification
    from app.data.models.candidate_education import CandidateEducation
    from app.data.models.candidate_project import CandidateProject
    from app.data.models.candidate_skill import CandidateSkill
    from app.data.models.resume import Resume


class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    total_experience_years: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    resumes: Mapped[list["Resume"]] = relationship(
        "Resume",
        back_populates="candidate",
    )

    skills: Mapped[list["CandidateSkill"]] = relationship(
        "CandidateSkill",
        back_populates="candidate",
        cascade="all, delete-orphan",
    )

    education: Mapped[list["CandidateEducation"]] = relationship(
        "CandidateEducation",
        back_populates="candidate",
        cascade="all, delete-orphan",
    )

    projects: Mapped[list["CandidateProject"]] = relationship(
        "CandidateProject",
        back_populates="candidate",
        cascade="all, delete-orphan",
    )

    certifications: Mapped[list["CandidateCertification"]] = relationship(
        "CandidateCertification",
        back_populates="candidate",
        cascade="all, delete-orphan",
    )