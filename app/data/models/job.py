from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.data.database import Base


class Job(Base):
    __tablename__ = "jobs"

    # =========================================================
    # Primary Key
    # =========================================================

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    # =========================================================
    # Basic Job Information
    # =========================================================

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    company: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    location: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    experience_required: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    employment_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="draft",
    )

    # =========================================================
    # Structured JD Requirements
    # =========================================================

    required_experience_years: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    required_skills: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    preferred_skills: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    education_requirements: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    other_constraints: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    # =========================================================
    # Timestamps
    # =========================================================

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