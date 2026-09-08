from sqlalchemy.orm import Session

from app.data.repositories.dashboard_repository import DashboardRepository


class DashboardService:
    def __init__(self, db: Session):
        self.repository = DashboardRepository(db)

    def get_stats(self) -> dict[str, int]:
        return {
            "total_jobs": self.repository.count_jobs(),
            "total_candidates": self.repository.count_candidates(),
            "total_resumes": self.repository.count_resumes(),

            # Matching module will be implemented later.
            "matched_candidates": 0,
        }