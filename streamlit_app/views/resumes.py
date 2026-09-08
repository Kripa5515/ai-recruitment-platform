import html
import re
import textwrap

import requests
import streamlit as st

from streamlit_app.api_client.candidates import (
    get_candidates,
)
from streamlit_app.api_client.resume_client import (
    get_resume_error_message,
    upload_resumes,
)
from streamlit_app.components.candidate_profile_modal import (
    open_candidate_profile_dialog,
)


def render_html(html_str: str) -> None:
    """
    Safely render multiline HTML inside Streamlit.

    Removes leading whitespace from each line so Streamlit's
    Markdown parser does not interpret the HTML as a code block.
    """
    clean_html = re.sub(
        r"^[ \t]+",
        "",
        textwrap.dedent(html_str),
        flags=re.MULTILINE,
    ).strip()

    st.markdown(
        clean_html,
        unsafe_allow_html=True,
    )


def _status_badge(status: str) -> str:
    status = (status or "unknown").lower()

    labels = {
        "success": "Processed",
        "duplicate": "Duplicate",
        "failed": "Failed",
        "error": "Failed",
    }

    return labels.get(
        status,
        status.replace("_", " ").title(),
    )


def _render_stat_card(
    icon: str,
    label: str,
    value: object,
    variant: str = "total",
) -> None:
    safe_icon = html.escape(str(icon))
    safe_label = html.escape(str(label))
    safe_value = html.escape(str(value))

    variant_classes = {
        "total": "stat-card-total",
        "success": "stat-card-success",
        "warning": "stat-card-warning",
        "danger": "stat-card-danger",
    }
    card_cls = variant_classes.get(variant, "stat-card-total")
    icon_cls = {
        "total": "icon-box-slate",
        "success": "icon-box-green",
        "warning": "icon-box-amber",
        "danger": "icon-box-red",
    }.get(variant, "icon-box-green")

    render_html(
        f"""
        <div class="resume-stat-card {card_cls}">
            <div class="icon-box {icon_cls}" style="width: 38px; height: 38px; font-size: 16px; margin-bottom: 8px;">
                {safe_icon}
            </div>

            <div class="resume-stat-label">
                {safe_label}
            </div>

            <div class="resume-stat-value">
                {safe_value}
            </div>
        </div>
        """
    )


def _render_resume_result(item: dict) -> None:
    filename = item.get(
        "filename",
        "Unknown file",
    )

    status = (
        item.get("status")
        or "unknown"
    ).lower()

    message = item.get("message") or ""

    candidate_id = item.get("candidate_id")

    candidate_name = item.get("candidate_name")

    resume = item.get("resume") or {}

    # ---------------------------------------------------------
    # Status styling
    # ---------------------------------------------------------

    if status == "success":
        badge_class = "resume-badge-success"
        icon = "✓"

    elif status == "duplicate":
        badge_class = "resume-badge-warning"
        icon = "↻"

    else:
        badge_class = "resume-badge-danger"
        icon = "!"

    # ---------------------------------------------------------
    # Resume information
    # ---------------------------------------------------------

    file_type = str(
        resume.get("file_type") or ""
    ).upper()

    version = resume.get("version")

    extraction_status = (
        resume.get("extraction_status")
        or "unknown"
    )

    is_current = resume.get(
        "is_current",
        False,
    )

    candidate_text = (
        candidate_name
        or "Candidate pending"
    )

    if candidate_id:
        candidate_text += f" · ID {candidate_id}"

    # Escape user/API supplied values before rendering HTML.
    safe_filename = html.escape(str(filename))
    safe_candidate_text = html.escape(str(candidate_text))
    safe_badge_text = html.escape(_status_badge(status))
    safe_icon = html.escape(icon)

    # ---------------------------------------------------------
    # Result card
    # ---------------------------------------------------------

    render_html(
        f"""
        <div class="resume-result-card">
            <div class="resume-result-top">

                <div class="resume-file-icon">
                    📄
                </div>

                <div class="resume-result-main">
                    <div class="resume-result-title">
                        {safe_filename}
                    </div>

                    <div class="resume-result-meta">
                        {safe_candidate_text}
                    </div>
                </div>

                <div class="{badge_class}">
                    {safe_icon}
                    {safe_badge_text}
                </div>

            </div>
        </div>
        """
    )

    # ---------------------------------------------------------
    # Resume metadata
    # ---------------------------------------------------------

    if resume:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.caption("File Type")
            st.write(
                file_type or "—"
            )

        with col2:
            st.caption("Version")
            st.write(
                version or "—"
            )

        with col3:
            st.caption("Resume State")
            st.write(
                "Current"
                if is_current
                else "Previous"
            )

        with col4:
            st.caption("Extraction")
            st.write(
                str(
                    extraction_status
                )
                .replace("_", " ")
                .title()
            )

    # ---------------------------------------------------------
    # Processing message
    # ---------------------------------------------------------

    if message:
        if status == "success":
            st.success(message)

        elif status == "duplicate":
            st.warning(message)

        else:
            st.error(message)


def _render_candidate_card(
    candidate: dict,
) -> None:
    candidate_id = candidate.get("id")

    candidate_name = (
        candidate.get("name")
        or "Unknown Candidate"
    )

    email = (
        candidate.get("email")
        or "No email available"
    )

    experience = candidate.get(
        "total_experience_years"
    )

    resume_count = candidate.get(
        "resume_count",
        0,
    )

    safe_name = html.escape(
        str(candidate_name)
    )

    safe_email = html.escape(
        str(email)
    )

    if isinstance(
        experience,
        (int, float),
    ):
        exp_text = f"{experience:g} yrs"
    else:
        exp_text = "Not available"

    safe_exp_text = html.escape(exp_text)

    with st.container(border=True):
        render_html(
            f"""
            <div class="candidate-card-top">
                <div>
                    <div class="job-card-eyebrow">
                        CANDIDATE · ID {candidate_id}
                    </div>

                    <div class="candidate-card-name">
                        👤 {safe_name}
                    </div>
                </div>
                <span class="job-status status-open">ACTIVE PROFILE</span>
            </div>

            <div class="candidate-meta-grid">

                <div class="candidate-meta-item">
                    <div class="icon-box icon-box-blue">📧</div>

                    <div>
                        <small>Email</small>
                        <strong>{safe_email}</strong>
                    </div>
                </div>

                <div class="candidate-meta-item">
                    <div class="icon-box icon-box-amber">💼</div>

                    <div>
                        <small>Experience</small>
                        <strong>{safe_exp_text}</strong>
                    </div>
                </div>

                <div class="candidate-meta-item">
                    <div class="icon-box icon-box-green">📄</div>

                    <div>
                        <small>Resumes</small>
                        <strong>
                            {resume_count} document(s)
                        </strong>
                    </div>
                </div>

            </div>
            """
        )

        # ---------------------------------------------------------
        # View Profile action bar
        # ---------------------------------------------------------
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
                    key=f"view_candidate_resume_{candidate_id}",
                    use_container_width=True,
                ):
                    open_candidate_profile_dialog(candidate_id)


def render_resume_page() -> None:
    """Render Resume Management page."""

    # =========================================================
    # PAGE HEADER
    # =========================================================

    render_html(
        """
        <div class="resume-page-header">

            <div>

                <div class="resume-eyebrow">
                    RESUME INTELLIGENCE
                </div>

                <div class="resume-page-title">
                    Resume Repository
                </div>

                <div class="resume-page-subtitle">
                    Upload, process and organize candidate
                    resumes for AI-powered recruitment matching.
                </div>

            </div>

            <div class="resume-header-badge">

                <span class="resume-online-dot"></span>

                Processing ready

            </div>

        </div>
        """
    )

    # =========================================================
    # UPLOAD SECTION
    # =========================================================

    render_html(
        """
        <div class="resume-section-heading">

            <div>

                <div class="resume-section-title">
                    Add resumes
                </div>

                <div class="resume-section-subtitle">
                    Upload one or multiple PDF/DOCX resumes.
                </div>

            </div>

        </div>
        """
    )

    with st.container(border=True):

        uploaded_files = st.file_uploader(
            "Drop resumes here or browse files",
            type=[
                "pdf",
                "docx",
            ],
            accept_multiple_files=True,
            help=(
                "Multiple PDF and DOCX files are supported. "
                "Each file is validated and processed by the "
                "recruitment API."
            ),
            label_visibility="visible",
        )

        # -----------------------------------------------------
        # Selected files
        # -----------------------------------------------------

        if uploaded_files:

            total_selected = len(
                uploaded_files
            )

            render_html(
                f"""
                <div class="resume-upload-summary">

                    <strong>
                        {total_selected}
                        resume(s) selected
                    </strong>

                    <span>
                        Maximum file size:
                        10 MB each
                    </span>

                </div>
                """
            )

            # -------------------------------------------------
            # File preview
            # -------------------------------------------------

            with st.expander(
                "Review selected files",
                expanded=False,
            ):

                for uploaded_file in uploaded_files:

                    size_mb = (
                        uploaded_file.size
                        / (1024 * 1024)
                    )

                    col1, col2 = st.columns(
                        [4, 1]
                    )

                    with col1:
                        st.write(
                            f"📄 {uploaded_file.name}"
                        )

                    with col2:
                        st.caption(
                            f"{size_mb:.2f} MB"
                        )

            # -------------------------------------------------
            # Process button
            # -------------------------------------------------

            if st.button(
                "Process Resumes",
                type="primary",
                use_container_width=True,
            ):

                progress = st.progress(0)

                status_placeholder = st.empty()

                try:

                    status_placeholder.info(
                        "Uploading and processing resumes..."
                    )

                    progress.progress(20)

                    response = upload_resumes(
                        uploaded_files
                    )

                    progress.progress(100)

                    status_placeholder.success(
                        "Resume processing completed."
                    )

                    st.session_state[
                        "last_resume_upload_result"
                    ] = response

                    st.rerun()

                except Exception as exc:

                    progress.empty()

                    status_placeholder.empty()

                    st.error(
                        get_resume_error_message(
                            exc
                        )
                    )

    # =========================================================
    # LATEST PROCESSING RESULT
    # =========================================================

    if (
        "last_resume_upload_result"
        in st.session_state
    ):

        response = st.session_state[
            "last_resume_upload_result"
        ]

        render_html(
            """
            <div class="resume-section-heading">

                <div>

                    <div class="resume-section-title">
                        Latest processing
                    </div>

                    <div class="resume-section-subtitle">
                        Results from the most recent resume upload.
                    </div>

                </div>

            </div>
            """
        )

        total_files = response.get(
            "total_files",
            0,
        )

        successful = response.get(
            "successful",
            0,
        )

        duplicates = response.get(
            "duplicates",
            0,
        )

        failed = response.get(
            "failed",
            0,
        )

        # -----------------------------------------------------
        # Statistics
        # -----------------------------------------------------

        col1, col2, col3, col4 = st.columns(
            4
        )

        with col1:
            _render_stat_card(
                "📄",
                "Files",
                total_files,
                variant="total",
            )

        with col2:
            _render_stat_card(
                "✓",
                "Processed",
                successful,
                variant="success",
            )

        with col3:
            _render_stat_card(
                "↻",
                "Duplicates",
                duplicates,
                variant="warning",
            )

        with col4:
            _render_stat_card(
                "!",
                "Failed",
                failed,
                variant="danger",
            )

        # -----------------------------------------------------
        # Detailed results
        # -----------------------------------------------------

        items = response.get(
            "items",
            [],
        )

        if items:

            st.markdown(
                "#### Processing details"
            )

            for item in items:
                _render_resume_result(
                    item
                )

        if st.button(
            "Clear Latest Result",
            key="neutral_clear_resume_result",
        ):

            st.session_state.pop(
                "last_resume_upload_result",
                None,
            )

            st.rerun()

    # =========================================================
    # CANDIDATE REPOSITORY
    # =========================================================

    render_html(
        """
        <div class="resume-section-heading repository-heading">

            <div>

                <div class="resume-section-title">
                    Candidate repository
                </div>

                <div class="resume-section-subtitle">
                    Search candidates and inspect their
                    resume history.
                </div>

            </div>

        </div>
        """
    )

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    search = st.text_input(
        "Search candidate",
        placeholder="Search by name or email...",
        label_visibility="collapsed",
    )

    try:

        candidates_response = get_candidates(
            page=1,
            page_size=50,
            search=search,
        )

        candidates = candidates_response.get(
            "items",
            [],
        )

        # -----------------------------------------------------
        # Empty state
        # -----------------------------------------------------

        if not candidates:

            render_html(
                """
                <div class="empty-state">

                    <div class="empty-state-icon">
                        📄
                    </div>

                    <div class="empty-state-title">
                        No resumes yet
                    </div>

                    <div class="empty-state-description">
                        Upload candidate resumes to start
                        building your recruitment intelligence
                        repository.
                    </div>

                </div>
                """
            )

            return

        total_candidates = candidates_response.get(
            "total",
            len(candidates),
        )

        st.caption(
            f"{total_candidates} candidate(s) available"
        )

        # -----------------------------------------------------
        # Candidate cards
        # -----------------------------------------------------

        for candidate in candidates:

            _render_candidate_card(
                candidate
            )

    except requests.RequestException:

        st.error(
            "Unable to connect to the Recruitment API. "
            "Please make sure FastAPI is running on port 8000."
        )

    except Exception as exc:

        st.error(
            get_resume_error_message(
                exc
            )
        )