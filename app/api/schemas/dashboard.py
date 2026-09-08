from pydantic import BaseModel


class DashboardStatsResponse(BaseModel):
    total_jobs: int
    total_candidates: int
    total_resumes: int
    matched_candidates: int