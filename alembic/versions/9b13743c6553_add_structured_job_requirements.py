from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9b13743c6553"
down_revision: Union[str, Sequence[str], None] = "ac21d4eff97e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # =========================================================
    # Add columns as nullable first
    # =========================================================

    op.add_column(
        "jobs",
        sa.Column(
            "required_experience_years",
            sa.Float(),
            nullable=True,
        ),
    )

    op.add_column(
        "jobs",
        sa.Column(
            "required_skills",
            sa.JSON(),
            nullable=True,
        ),
    )

    op.add_column(
        "jobs",
        sa.Column(
            "preferred_skills",
            sa.JSON(),
            nullable=True,
        ),
    )

    op.add_column(
        "jobs",
        sa.Column(
            "education_requirements",
            sa.JSON(),
            nullable=True,
        ),
    )

    op.add_column(
        "jobs",
        sa.Column(
            "other_constraints",
            sa.JSON(),
            nullable=True,
        ),
    )

    # =========================================================
    # Populate existing records
    # =========================================================

    op.execute(
        """
        UPDATE jobs
        SET required_skills = '[]'
        WHERE required_skills IS NULL
        """
    )

    op.execute(
        """
        UPDATE jobs
        SET preferred_skills = '[]'
        WHERE preferred_skills IS NULL
        """
    )

    op.execute(
        """
        UPDATE jobs
        SET education_requirements = '[]'
        WHERE education_requirements IS NULL
        """
    )

    op.execute(
        """
        UPDATE jobs
        SET other_constraints = '[]'
        WHERE other_constraints IS NULL
        """
    )

    # =========================================================
    # Make list fields NOT NULL
    # =========================================================

    op.alter_column(
        "jobs",
        "required_skills",
        existing_type=sa.JSON(),
        nullable=False,
    )

    op.alter_column(
        "jobs",
        "preferred_skills",
        existing_type=sa.JSON(),
        nullable=False,
    )

    op.alter_column(
        "jobs",
        "education_requirements",
        existing_type=sa.JSON(),
        nullable=False,
    )

    op.alter_column(
        "jobs",
        "other_constraints",
        existing_type=sa.JSON(),
        nullable=False,
    )


def downgrade() -> None:
    # =========================================================
    # Remove structured JD requirement columns
    # =========================================================

    op.drop_column(
        "jobs",
        "other_constraints",
    )

    op.drop_column(
        "jobs",
        "education_requirements",
    )

    op.drop_column(
        "jobs",
        "preferred_skills",
    )

    op.drop_column(
        "jobs",
        "required_skills",
    )

    op.drop_column(
        "jobs",
        "required_experience_years",
    )