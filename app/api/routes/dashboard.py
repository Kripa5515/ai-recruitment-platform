from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.schemas.dashboard import DashboardStatsResponse
from app.services.dashboard_service import DashboardService


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/stats",
    response_model=DashboardStatsResponse,
)
def get_dashboard_stats(
    db: Session = Depends(get_db),
):
    service = DashboardService(db)

    return service.get_stats()