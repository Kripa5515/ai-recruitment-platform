import html
import re
import textwrap
import requests
import streamlit as st

from streamlit_app.api_client.candidates import (
    get_candidates,
)
from streamlit_app.components.candidate_profile_modal import (
    open_candidate_profile_dialog,
)


PAGE_SIZE = 10


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


def _get_candidate_list(data: dict | list) -> list[dict]:
    """
    Normalize candidate list response.

    Supports:
    - direct list response
    - paginated response containing 'items'
    - response containing 'candidates'
    """
    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        items = data.get("items")
        if isinstance(items, list):
            return items

        candidates = data.get("candidates")
        if isinstance(candidates, list):
            return candidates

    return []


def _format_experience(value) -> str:
    if value is None:
        return "Not specified"

    try:
        return f"{float(value):g} years"
    except (TypeError, ValueError):
        return str(value)


def _render_candidate_card(candidate: dict) -> None:
    candidate_id = candidate.get("id")
    name = candidate.get("name") or "Unnamed Candidate"
    email = candidate.get("email") or "Email not available"
    phone = candidate.get("phone") or "Phone not available"
    experience = _format_experience(candidate.get("total_experience_years"))

    safe_name = html.escape(str(name))
    safe_email = html.escape(str(email))
    safe_phone = html.escape(str(phone))
    safe_exp = html.escape(str(experience))

    with st.container(border=True):
        render_html(
            f"""
            <div class="candidate-card-top">
                <div>
                    <div class="candidates-eyebrow">CANDIDATE · ID #{candidate_id}</div>
                    <div class="candidate-card-name">👤 {safe_name}</div>
                </div>
                <span class="job-status status-open">ACTIVE PROFILE</span>
            </div>
            <div class="candidate-meta-grid">
                <div class="candidate-meta-item">
                    <div class="icon-box icon-box-blue">📧</div>
                    <div>
                        <small>Email Address</small>
                        <strong>{safe_email}</strong>
                    </div>
                </div>
                <div class="candidate-meta-item">
                    <div class="icon-box icon-box-amber">💼</div>
                    <div>
                        <small>Experience</small>
                        <strong>{safe_exp}</strong>
                    </div>
                </div>
                <div class="candidate-meta-item">
                    <div class="icon-box icon-box-green">📱</div>
                    <div>
                        <small>Phone Number</small>
                        <strong>{safe_phone}</strong>
                    </div>
                </div>
            </div>
            """
        )

        st.markdown('<div class="candidate-card-action-bar"></div>', unsafe_allow_html=True)
        col_meta, col_btn = st.columns([3.5, 1.5])
        with col_meta:
            render_html(
                """
                <div style="color: #648075; font-size: 11px; padding-top: 6px;">
                    ✓ Verified candidate intelligence record
                </div>
                """
            )
        with col_btn:
            if candidate_id is not None:
                if st.button(
                    "View Profile →",
                    key=f"view_candidate_{candidate_id}",
                    use_container_width=True,
                ):
                    open_candidate_profile_dialog(candidate_id)


def render_candidates() -> None:
    # =========================================================
    # PAGE HEADER
    # =========================================================
    render_html(
        """
        <div class="candidates-page-header">
            <div>
                <div class="candidates-eyebrow">
                    CANDIDATE INTELLIGENCE
                </div>
                <div class="candidates-page-title">
                    Candidate Repository
                </div>
                <div class="candidates-page-subtitle">
                    Review candidate profiles, background experience,
                    extracted skills, and resume history.
                </div>
            </div>
            <div class="candidates-header-icon">
                👥
            </div>
        </div>
        """
    )

    # =========================================================
    # SEARCH BAR
    # =========================================================
    search = st.text_input(
        "Search candidates",
        placeholder="Search candidates by name, email, or keywords...",
        label_visibility="collapsed",
    )

    # =========================================================
    # DATA RETRIEVAL
    # =========================================================
    try:
        data = get_candidates(
            page=1,
            page_size=PAGE_SIZE,
            search=search,
        )
    except requests.RequestException as exc:
        st.error(
            "Unable to connect to the Candidate API. "
            "Please make sure FastAPI is running on port 8000."
        )
        st.caption(str(exc))
        return

    candidates = _get_candidate_list(data)

    total_candidates = (
        data.get("total", len(candidates))
        if isinstance(data, dict)
        else len(candidates)
    )

    # =========================================================
    # METRICS SUMMARY CARDS
    # =========================================================
    render_html(
        """
        <div class="jobs-stat-section">
            <div class="jobs-stat-title">
                Candidate Overview
            </div>
            <div class="jobs-stat-subtitle">
                Current talent repository statistics
            </div>
        </div>
        """
    )

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        render_html(
            f"""
            <div class="jobs-stat-card">
                <div class="jobs-stat-icon">
                    👤
                </div>
                <div class="jobs-stat-label">
                    CANDIDATES FOUND
                </div>
                <div class="jobs-stat-value">
                    {len(candidates)}
                </div>
                <div class="jobs-stat-description">
                    Matching current view criteria
                </div>
            </div>
            """
        )

    with col2:
        render_html(
            f"""
            <div class="jobs-stat-card">
                <div class="jobs-stat-icon">
                    📄
                </div>
                <div class="jobs-stat-label">
                    REPOSITORY STATUS
                </div>
                <div class="jobs-stat-value">
                    {total_candidates}
                </div>
                <div class="jobs-stat-description">
                    Total candidate profiles registered
                </div>
            </div>
            """
        )

    # =========================================================
    # CANDIDATE LIST SECTION
    # =========================================================
    render_html(
        """
        <div class="jobs-list-header">
            <div class="jobs-section-title">
                Talent Pool
            </div>
            <div class="jobs-section-description">
                Browse detailed candidate profiles, experience levels, and resume records.
            </div>
        </div>
        """
    )

    if not candidates:
        render_html(
            """
            <div class="empty-state">
                <div class="empty-state-icon">
                    👥
                </div>
                <div class="empty-state-title">
                    No candidates found
                </div>
                <div class="empty-state-description">
                    Upload resumes to build your recruitment intelligence repository.
                </div>
            </div>
            """
        )
        return

    for candidate in candidates:
        _render_candidate_card(candidate)