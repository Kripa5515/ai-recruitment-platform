import textwrap

import requests
import streamlit as st

from streamlit_app.api_client.dashboard import get_dashboard_stats
from streamlit_app.components.cards import metric_card


def render_html(html: str) -> None:
    """
    Render HTML directly using Streamlit's HTML renderer.

    textwrap.dedent() removes Python indentation so multiline
    HTML is rendered correctly instead of appearing as code.
    """
    st.html(textwrap.dedent(html).strip())


def get_match_status(
    matched_candidates: int,
    total_candidates: int,
) -> tuple[str, str]:
    """
    Return a simple dashboard-level matching status.

    This is only a UI indicator and is NOT a hiring decision.
    """

    if total_candidates <= 0:
        return "No matching data", "neutral"

    match_rate = (
        matched_candidates / total_candidates
    ) * 100

    if match_rate >= 70:
        return "Strong pipeline", "success"

    if match_rate >= 40:
        return "Active pipeline", "info"

    return "Needs review", "warning"


def render_dashboard() -> None:

    # =========================================================
    # FETCH DASHBOARD DATA
    # =========================================================

    try:
        stats = get_dashboard_stats()

    except requests.RequestException:
        st.error(
            "Unable to connect to the Recruitment API. "
            "Please make sure FastAPI is running on port 8000."
        )
        return

    # =========================================================
    # SAFE DATA EXTRACTION
    # =========================================================

    total_jobs = int(
        stats.get("total_jobs", 0)
    )

    total_candidates = int(
        stats.get("total_candidates", 0)
    )

    total_resumes = int(
        stats.get("total_resumes", 0)
    )

    matched_candidates = int(
        stats.get("matched_candidates", 0)
    )

    # =========================================================
    # MATCH RATE
    # =========================================================

    if total_candidates > 0:
        match_rate = (
            matched_candidates / total_candidates
        ) * 100
    else:
        match_rate = 0

    match_rate = min(
        100,
        round(match_rate, 1),
    )

    match_status, match_status_type = get_match_status(
        matched_candidates,
        total_candidates,
    )

    # =========================================================
    # PAGE HERO
    # =========================================================

    render_html(
        """
        <div class="dashboard-hero">

            <div class="dashboard-hero-content">

                <div class="dashboard-eyebrow">
                    AI RECRUITMENT PLATFORM
                </div>

                <div class="dashboard-hero-title">
                    Good morning 👋
                </div>

                <div class="dashboard-hero-subtitle">
                    Manage jobs, candidates and AI-powered matching
                    from one intelligent recruitment workspace.
                </div>

            </div>

            <div class="dashboard-hero-status">
                <span class="dashboard-status-dot"></span>
                Recruitment system online
            </div>

        </div>
        """
    )

    # =========================================================
    # RECRUITMENT OVERVIEW
    # =========================================================

    render_html(
        """
        <div class="dashboard-section-heading">
            <div class="dashboard-section-title">
                Recruitment Overview
            </div>

            <div class="dashboard-section-subtitle">
                Real-time recruitment workspace statistics
            </div>
        </div>
        """
    )

    # =========================================================
    # METRIC CARDS
    # =========================================================

    col1, col2, col3, col4 = st.columns(
        4,
        gap="medium",
    )

    with col1:
        metric_card(
            "💼",
            "Total Jobs",
            str(total_jobs),
        )

    with col2:
        metric_card(
            "👤",
            "Candidates",
            str(total_candidates),
        )

    with col3:
        metric_card(
            "📄",
            "Resumes",
            str(total_resumes),
        )

    with col4:
        metric_card(
            "🎯",
            "Matched Candidates",
            str(matched_candidates),
        )

    # =========================================================
    # INTELLIGENCE SECTION
    # =========================================================

    render_html(
        """
        <div class="dashboard-section-heading dashboard-section-spacing">

            <div class="dashboard-section-title">
                Recruitment Intelligence
            </div>

            <div class="dashboard-section-subtitle">
                Understand your current candidate pipeline and AI
                matching activity.
            </div>

        </div>
        """
    )

    intelligence_left, intelligence_right = st.columns(
        [1.65, 1],
        gap="medium",
    )

    # =========================================================
    # RECRUITMENT OVERVIEW CARD
    # =========================================================

    with intelligence_left:

        render_html(
            f"""
            <div class="dashboard-panel">

                <div class="dashboard-panel-header">

                    <div>

                        <div class="dashboard-panel-title">
                            Recruitment Overview
                        </div>

                        <div class="dashboard-panel-subtitle">
                            Current hiring pipeline at a glance
                        </div>

                    </div>

                    <div class="dashboard-panel-icon">
                        📊
                    </div>

                </div>


                <div class="overview-grid">

                    <div class="overview-item">

                        <div class="overview-label">
                            JOBS
                        </div>

                        <div class="overview-number">
                            {total_jobs}
                        </div>

                        <div class="overview-description">
                            Recruitment opportunities
                        </div>

                    </div>


                    <div class="overview-item">

                        <div class="overview-label">
                            CANDIDATES
                        </div>

                        <div class="overview-number">
                            {total_candidates}
                        </div>

                        <div class="overview-description">
                            Candidates available for review
                        </div>

                    </div>


                    <div class="overview-item">

                        <div class="overview-label">
                            RESUMES
                        </div>

                        <div class="overview-number">
                            {total_resumes}
                        </div>

                        <div class="overview-description">
                            Documents processed
                        </div>

                    </div>

                </div>


                <div class="overview-ai-footer">

                    <div class="overview-ai-icon">
                        ✨
                    </div>

                    <div>

                        <div class="overview-ai-title">
                            AI-assisted candidate intelligence
                        </div>

                        <div class="overview-ai-description">
                            Structured candidate data and matching
                            insights help recruiters review candidates
                            faster.
                        </div>

                    </div>

                </div>

            </div>
            """
        )

    # =========================================================
    # MATCHING HIGHLIGHT CARD
    # =========================================================

    with intelligence_right:

        render_html(
            f"""
            <div class="dashboard-panel matching-highlight">

                <div class="matching-highlight-header">

                    <div class="matching-icon">
                        🎯
                    </div>

                    <div class="matching-label">
                        CANDIDATE MATCHING
                    </div>

                </div>


                <div class="matching-number">
                    {matched_candidates}
                </div>


                <div class="matching-description">
                    candidates matched through the recruitment workflow
                </div>


                <div class="matching-progress-container">

                    <div class="matching-progress-track">

                        <div
                            class="matching-progress-fill"
                            style="width: {match_rate}%;">
                        </div>

                    </div>

                    <div class="matching-progress-meta">

                        <span>
                            Matching activity
                        </span>

                        <strong>
                            {match_rate}%
                        </strong>

                    </div>

                </div>


                <div class="matching-status status-{match_status_type}">
                    ● {match_status}
                </div>


                <div class="matching-note">
                    Matching scores support recruiter review.
                    Final hiring decisions remain with HR.
                </div>

            </div>
            """
        )

    # =========================================================
    # RECENT ACTIVITY
    # =========================================================

    render_html(
        """
        <div class="dashboard-section-heading dashboard-section-spacing">

            <div class="dashboard-section-title">
                Recent Activity
            </div>

            <div class="dashboard-section-subtitle">
                Latest recruitment activity across your workspace
            </div>

        </div>
        """
    )

    # =========================================================
    # EMPTY STATE
    # =========================================================

    if (
        total_jobs == 0
        and total_candidates == 0
        and total_resumes == 0
    ):

        render_html(
            """
            <div class="dashboard-empty-state">

                <div class="dashboard-empty-icon">
                    🌱
                </div>

                <div class="dashboard-empty-title">
                    Your recruitment workspace is ready
                </div>

                <div class="dashboard-empty-description">
                    Create your first job or upload resumes to start
                    building your candidate intelligence pipeline.
                </div>

            </div>
            """
        )

    # =========================================================
    # ACTIVITY CARDS
    # =========================================================

    else:

        activity_col1, activity_col2, activity_col3 = st.columns(
            3,
            gap="medium",
        )

        # -----------------------------------------------------
        # JOB ACTIVITY
        # -----------------------------------------------------

        with activity_col1:

            render_html(
                f"""
                <div class="activity-card">

                    <div class="activity-icon activity-green">
                        💼
                    </div>

                    <div class="activity-content">

                        <div class="activity-title">
                            Jobs
                        </div>

                        <div class="activity-value">
                            {total_jobs}
                        </div>

                        <div class="activity-description">
                            Job records in the recruitment system
                        </div>

                    </div>

                </div>
                """
            )

        # -----------------------------------------------------
        # CANDIDATE ACTIVITY
        # -----------------------------------------------------

        with activity_col2:

            render_html(
                f"""
                <div class="activity-card">

                    <div class="activity-icon activity-blue">
                        👥
                    </div>

                    <div class="activity-content">

                        <div class="activity-title">
                            Candidate Pool
                        </div>

                        <div class="activity-value">
                            {total_candidates}
                        </div>

                        <div class="activity-description">
                            Candidates available for matching
                        </div>

                    </div>

                </div>
                """
            )

        # -----------------------------------------------------
        # RESUME ACTIVITY
        # -----------------------------------------------------

        with activity_col3:

            render_html(
                f"""
                <div class="activity-card">

                    <div class="activity-icon activity-purple">
                        📄
                    </div>

                    <div class="activity-content">

                        <div class="activity-title">
                            Resume Repository
                        </div>

                        <div class="activity-value">
                            {total_resumes}
                        </div>

                        <div class="activity-description">
                            Resume documents stored in the system
                        </div>

                    </div>

                </div>
                """
            )

    # =========================================================
    # RECRUITMENT WORKFLOW
    # =========================================================

    render_html(
        """
        <div class="dashboard-section-heading dashboard-section-spacing">

            <div class="dashboard-section-title">
                Recruitment Workflow
            </div>

            <div class="dashboard-section-subtitle">
                From job creation to human-reviewed candidate selection
            </div>

        </div>
        """
    )

    workflow_steps = [
        (
            "01",
            "Create Job",
            "Define role and requirements",
        ),
        (
            "02",
            "Upload Resumes",
            "Add candidate documents",
        ),
        (
            "03",
            "Extract Candidates",
            "Build structured profiles",
        ),
        (
            "04",
            "Match Candidates",
            "Compare candidates with JD",
        ),
        (
            "05",
            "HR Review",
            "Review and make final decision",
        ),
    ]

    workflow_columns = st.columns(
        5,
        gap="small",
    )

    for column, (
        number,
        title,
        description,
    ) in zip(
        workflow_columns,
        workflow_steps,
    ):

        with column:

            render_html(
                f"""
                <div class="workflow-card">

                    <div class="workflow-number">
                        {number}
                    </div>

                    <div class="workflow-title">
                        {title}
                    </div>

                    <div class="workflow-description">
                        {description}
                    </div>

                </div>
                """
            )

    # =========================================================
    # RESPONSIBLE AI NOTE
    # =========================================================

    render_html(
        """
        <div class="dashboard-ai-note">

            <div class="dashboard-ai-note-icon">
                🛡️
            </div>

            <div>

                <div class="dashboard-ai-note-title">
                    Human-in-the-loop recruitment
                </div>

                <div class="dashboard-ai-note-text">
                    AI provides candidate intelligence, matching scores
                    and explanations. Recruiters retain control over
                    candidate selection and final hiring decisions.
                </div>

            </div>

        </div>
        """
    )