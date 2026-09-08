from unittest.mock import Mock

from app.services.dashboard_service import DashboardService


def test_get_stats():
    repository = Mock()

    repository.count_jobs.return_value = 5
    repository.count_candidates.return_value = 10
    repository.count_resumes.return_value = 15

    service = DashboardService.__new__(DashboardService)
    service.repository = repository

    stats = service.get_stats()

    assert stats["total_jobs"] == 5
    assert stats["total_candidates"] == 10
    assert stats["total_resumes"] == 15
    assert stats["matched_candidates"] == 0