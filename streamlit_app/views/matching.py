import html
import re
import textwrap
import requests
import streamlit as st

from streamlit_app.api_client.jobs import get_jobs
from streamlit_app.api_client.matching import (
    match_candidates_for_job,
)
from streamlit_app.components.matching_cards import (
    render_candidate_match_card,
)


def render_html(html_str: str) -> None:
    """
    Safely render multiline HTML inside Streamlit.
    Removes leading whitespace from each line so Streamlit's markdown
    parser doesn't misinterpret the text as a code block.
    """
    clean_html = re.sub(
        r"^[ \t]+", "", textwrap.dedent(html_str), flags=re.MULTILINE
    ).strip()
    st.markdown(
        clean_html,
        unsafe_allow_html=True,
    )


def _get_score(
    result: dict,
) -> float:
    """
    Get the score used for match classification.
    """
    final_score = result.get("final_score")
    if final_score is not None:
        return float(final_score)

    return float(result.get("deterministic_score", 0))


def _get_job_label(
    job: dict,
) -> str:
    """
    Create a readable label for the job selector.
    """
    job_id = job.get("id", "-")
    title = job.get("title", "Untitled Job")
    company = job.get("company", "-")

    return f"{title} — {company} (Job ID: {job_id})"


def render_matching() -> None:
    """
    Render the recruiter candidate matching page.
    """

    # =========================================================
    # PAGE HEADER
    # =========================================================
    render_html(
        """
        <div class="matching-page-header">
            <div>
                <div class="matching-eyebrow">
                    AI INTELLIGENCE SUITE
                </div>
                <div class="matching-page-title">
                    Candidate Matching
                </div>
                <div class="matching-page-subtitle">
                    Rank candidates against job requirements using
                    experience, required skills, semantic similarity and constraint analysis.
                </div>
            </div>
            <div class="matching-header-badge">
                <span class="dashboard-status-dot"></span>
                AI Engine Online
            </div>
        </div>
        """
    )

    # =========================================================
    # Load Jobs
    # =========================================================
    try:
        jobs_response = get_jobs(
            page=1,
            page_size=100,
            search="",
        )
    except requests.RequestException as exc:
        st.error("Unable to load jobs from Recruitment API.")
        st.caption(str(exc))
        return

    jobs = jobs_response.get("items", [])
    if not jobs:
        render_html(
            """
            <div class="empty-state">
                <div class="empty-state-icon">
                    💼
                </div>
                <div class="empty-state-title">
                    No jobs available
                </div>
                <div class="empty-state-description">
                    Create a job posting first before running candidate matching.
                </div>
            </div>
            """
        )
        return

    # =========================================================
    # Job Selection Section
    # =========================================================
    render_html(
        """
        <div class="jobs-list-header">
            <div class="jobs-section-title">
                Target Role
            </div>
            <div class="jobs-section-description">
                Select an active job position to match candidate profiles against.
            </div>
        </div>
        """
    )

    job_options = {
        _get_job_label(job): job
        for job in jobs
    }

    selected_label = st.selectbox(
        "Select Job",
        options=list(job_options.keys()),
        label_visibility="collapsed",
    )

    selected_job = job_options[selected_label]
    selected_job_id = selected_job.get("id")

    # =========================================================
    # Selected Job Information Panel
    # =========================================================
    job_title = html.escape(str(selected_job.get("title", "Untitled Job")))
    company_name = html.escape(str(selected_job.get("company", "-")))
    exp_req = html.escape(str(selected_job.get("experience_required", "-")))
    loc_val = html.escape(str(selected_job.get("location", "Remote / Not specified")))

    render_html(
        f"""
        <div class="job-preview-panel">
            <div class="job-preview-header">
                <div>
                    <div class="job-card-eyebrow">SELECTED POSITION · ID {selected_job_id}</div>
                    <div class="job-preview-title">💼 {job_title}</div>
                    <div class="job-preview-company">{company_name} • {loc_val}</div>
                </div>
                <span class="job-status status-open">ACTIVE RECRUITMENT</span>
            </div>
            <div class="candidate-meta-grid">
                <div class="candidate-meta-item">
                    <div class="icon-box icon-box-blue">🏢</div>
                    <div>
                        <small>Company</small>
                        <strong>{company_name}</strong>
                    </div>
                </div>
                <div class="candidate-meta-item">
                    <div class="icon-box icon-box-amber">⏳</div>
                    <div>
                        <small>Experience Required</small>
                        <strong>{exp_req}</strong>
                    </div>
                </div>
                <div class="candidate-meta-item">
                    <div class="icon-box icon-box-green">📍</div>
                    <div>
                        <small>Location</small>
                        <strong>{loc_val}</strong>
                    </div>
                </div>
            </div>
        </div>
        """
    )

    # Job Description Expander
    with st.expander("📄 Review Full Job Description", expanded=False):
        st.write(
            selected_job.get(
                "description",
                "No description available.",
            )
        )

    # =========================================================
    # Matching Button
    # =========================================================
    run_matching = st.button(
        "✨ Find Best Candidates",
        use_container_width=True,
        type="primary",
    )

    # =========================================================
    # Execute Matching
    # =========================================================
    if run_matching:
        try:
            with st.spinner(
                "Analyzing candidate talent pool and computing explainable match scores..."
            ):
                response = match_candidates_for_job(int(selected_job_id))

            st.session_state["matching_response"] = response
            st.session_state["matching_job_id"] = selected_job_id
            st.session_state["matching_job_title"] = selected_job.get(
                "title",
                "Selected Job",
            )
            st.success("Candidate matching completed successfully.")
        except requests.RequestException as exc:
            st.error("Unable to run candidate matching.")
            st.caption(str(exc))
            return

    # =========================================================
    # Retrieve Matching Results from Session State
    # =========================================================
    response = st.session_state.get("matching_response")
    if not response:
        return

    # Validate Result Belongs to Selected Job
    response_job_id = response.get("job_id")
    if response_job_id != selected_job_id:
        return

    results = response.get("results", [])
    total_candidates = response.get("total_candidates", len(results))

    # =========================================================
    # Summary Cards
    # =========================================================
    strong_matches = 0
    good_matches = 0
    moderate_matches = 0
    low_matches = 0

    for result in results:
        score = _get_score(result)
        if score >= 80:
            strong_matches += 1
        elif score >= 60:
            good_matches += 1
        elif score >= 40:
            moderate_matches += 1
        else:
            low_matches += 1

    render_html(
        f"""
        <div class="jobs-list-header" style="margin-top: 36px;">
            <div class="jobs-section-title">
                Matching Intelligence Summary
            </div>
            <div class="jobs-section-description">
                AI match distribution across candidates for this role
            </div>
        </div>
        <div class="match-summary-grid">
            <div class="match-summary-card summary-analyzed">
                <div class="match-summary-lbl">Analyzed</div>
                <div class="match-summary-val" style="color: #14382b;">{total_candidates}</div>
            </div>
            <div class="match-summary-card summary-strong">
                <div class="match-summary-lbl">🟢 Strong</div>
                <div class="match-summary-val" style="color: #11794d;">{strong_matches}</div>
            </div>
            <div class="match-summary-card summary-good">
                <div class="match-summary-lbl">🔵 Good</div>
                <div class="match-summary-val" style="color: #1a6fb0;">{good_matches}</div>
            </div>
            <div class="match-summary-card summary-moderate">
                <div class="match-summary-lbl">🟡 Moderate</div>
                <div class="match-summary-val" style="color: #9c6c0c;">{moderate_matches}</div>
            </div>
            <div class="match-summary-card summary-low">
                <div class="match-summary-lbl">🔴 Low</div>
                <div class="match-summary-val" style="color: #b33939;">{low_matches}</div>
            </div>
        </div>
        """
    )

    # =========================================================
    # Candidate Ranking
    # =========================================================
    render_html(
        """
        <div class="jobs-list-header">
            <div class="jobs-section-title">
                Candidate Rankings
            </div>
            <div class="jobs-section-description">
                Ranked by hybrid matching algorithm (Experience + Skills + Semantic + Constraints)
            </div>
        </div>
        """
    )

    if not results:
        render_html(
            """
            <div class="empty-state">
                <div class="empty-state-icon">
                    🎯
                </div>
                <div class="empty-state-title">
                    No candidates found
                </div>
                <div class="empty-state-description">
                    No candidate records were available for matching against this position.
                </div>
            </div>
            """
        )
        return

    # Sort results defensively by score descending
    results = sorted(
        results,
        key=_get_score,
        reverse=True,
    )

    for rank, result in enumerate(results, start=1):
        render_candidate_match_card(
            result=result,
            rank=rank,
            job_title=selected_job.get("title"),
        )

    # =========================================================
    # Clear Results Action
    # =========================================================
    st.markdown('<div class="jobs-summary-divider"></div>', unsafe_allow_html=True)

    btn_col1, btn_col2 = st.columns([4, 1])
    with btn_col2:
        if st.button(
            "Clear Matching Results",
            key="neutral_clear_matching",
            use_container_width=True,
        ):
            st.session_state.pop("matching_response", None)
            st.session_state.pop("matching_job_id", None)
            st.session_state.pop("matching_job_title", None)
            st.rerun()