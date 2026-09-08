import html
import re
import textwrap
import streamlit as st

from streamlit_app.api_client.jobs import (
    analyze_jd,
    create_job,
    delete_job,
    get_job,
    get_jobs,
    update_job,
    upload_jd,
)


# ============================================================
# HELPERS
# ============================================================


def render_html(html_str: str) -> None:
    """
    Safely render multiline HTML inside Streamlit.
    Removes leading whitespace from all lines so Streamlit markdown
    doesn't misinterpret HTML as a code block.
    """
    clean_html = re.sub(
        r"^[ \t]+", "", textwrap.dedent(html_str), flags=re.MULTILINE
    ).strip()
    st.markdown(
        clean_html,
        unsafe_allow_html=True,
    )


def _to_lines(values: list[str] | None) -> str:
    """Convert a list of strings into multiline text."""
    return "\n".join(values or [])


def _to_list(value: str) -> list[str]:
    """Convert multiline text into a clean list."""
    return [
        item.strip()
        for item in value.splitlines()
        if item.strip()
    ]


def _show_api_error(exc: Exception) -> None:
    """Display a readable API error."""
    st.error(f"API Error: {exc}")


def _job_status_class(status: str) -> str:
    """Return CSS class for job status."""
    normalized = (status or "draft").lower()

    if normalized == "open":
        return "status-open"

    if normalized == "closed":
        return "status-closed"

    return "status-draft"


def _job_status_label(status: str) -> str:
    """Return readable job status."""
    normalized = (status or "draft").lower()

    return {
        "open": "OPEN",
        "closed": "CLOSED",
        "draft": "DRAFT",
    }.get(normalized, normalized.upper())


# ============================================================
# CREATE JOB - COMMON
# ============================================================


def _create_job_from_requirements(
    requirements: dict,
    mode_key: str,
) -> None:
    """
    Show AI extracted requirements and allow HR to review/edit
    before creating the job.
    """

    render_html(
        """
        <div class="ai-result-card">
            <div class="ai-result-header">
                <div>
                    <div class="ai-result-title">
                        AI Extracted Requirements
                    </div>
                    <div class="ai-result-description">
                        Review the extracted information before creating
                        the job. HR remains in control of the final data.
                    </div>
                </div>
                <div class="ai-badge">
                    AI ANALYZED
                </div>
            </div>
        </div>
        """
    )

    render_html(
        """
        <div class="ai-complete-banner">
            <span>✓</span>
            <div>
                <strong>AI analysis completed</strong>
                <small>
                    Review and edit any field before creating the job.
                </small>
            </div>
        </div>
        """
    )

    # --------------------------------------------------------
    # BASIC INFORMATION
    # --------------------------------------------------------

    render_html(
        """
        <div class="form-section-label">
            Basic Information
        </div>
        """
    )

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        title = st.text_input(
            "Job Title",
            value=requirements.get("title") or "",
            placeholder="e.g. Senior Backend Developer",
            key=f"{mode_key}_title",
        )

        company = st.text_input(
            "Company",
            value=requirements.get("company") or "",
            placeholder="e.g. ABC Technologies",
            key=f"{mode_key}_company",
        )

        location = st.text_input(
            "Location",
            value=requirements.get("location") or "",
            placeholder="e.g. New Delhi / Remote",
            key=f"{mode_key}_location",
        )

    with col2:
        employment_type = st.text_input(
            "Employment Type",
            value=requirements.get("employment_type") or "",
            placeholder="e.g. Full Time",
            key=f"{mode_key}_employment_type",
        )

        experience = requirements.get("required_experience_years")

        experience_value = st.number_input(
            "Required Experience (Years)",
            min_value=0.0,
            value=float(experience or 0),
            step=0.5,
            key=f"{mode_key}_experience",
        )

    # --------------------------------------------------------
    # JOB DESCRIPTION
    # --------------------------------------------------------

    render_html(
        """
        <div class="form-section-label">
            Job Description
        </div>
        """
    )

    description = st.session_state.get(
        f"{mode_key}_description",
        "",
    )

    description = st.text_area(
        "Job Description",
        value=description,
        height=200,
        placeholder=(
            "Enter the complete job description, "
            "responsibilities, requirements and expectations..."
        ),
        key=f"{mode_key}_description_input",
        label_visibility="collapsed",
    )

    st.session_state[f"{mode_key}_description"] = description

    # --------------------------------------------------------
    # SKILLS
    # --------------------------------------------------------

    render_html(
        """
        <div class="form-section-label">
            Skills & Requirements
        </div>
        """
    )

    skill_col1, skill_col2 = st.columns(2, gap="medium")

    with skill_col1:
        required_skills = st.text_area(
            "Required Skills",
            value=_to_lines(requirements.get("required_skills")),
            height=120,
            placeholder="Python\nFastAPI\nPostgreSQL\nREST API",
            help="Enter one skill per line.",
            key=f"{mode_key}_required_skills",
        )

    with skill_col2:
        preferred_skills = st.text_area(
            "Preferred Skills",
            value=_to_lines(requirements.get("preferred_skills")),
            height=120,
            placeholder="Docker\nAWS\nRedis",
            help="Enter one skill per line.",
            key=f"{mode_key}_preferred_skills",
        )

    # --------------------------------------------------------
    # OTHER REQUIREMENTS
    # --------------------------------------------------------

    education_requirements = st.text_area(
        "Education Requirements",
        value=_to_lines(requirements.get("education_requirements")),
        height=80,
        placeholder="Bachelor's degree in Computer Science or equivalent",
        key=f"{mode_key}_education",
    )

    other_constraints = st.text_area(
        "Other Constraints",
        value=_to_lines(requirements.get("other_constraints")),
        height=80,
        placeholder="Work from office\nImmediate joiner preferred",
        key=f"{mode_key}_constraints",
    )

    # --------------------------------------------------------
    # CREATE
    # --------------------------------------------------------

    render_html('<div class="form-action-row"></div>')

    if st.button(
        "🚀 Create Job",
        type="primary",
        key=f"{mode_key}_create_job",
        use_container_width=True,
    ):
        if not title.strip():
            st.error("Job Title is required.")
            return

        if not company.strip():
            st.error("Company is required.")
            return

        if not description.strip():
            st.error("Job Description is required.")
            return

        job_data = {
            "title": title.strip(),
            "company": company.strip(),
            "description": description.strip(),
            "location": location.strip(),
            "experience_required": (
                f"{experience_value:g}+" if experience_value > 0 else ""
            ),
            "employment_type": employment_type.strip(),
            "status": "draft",
            "required_experience_years": (
                experience_value if experience_value > 0 else None
            ),
            "required_skills": _to_list(required_skills),
            "preferred_skills": _to_list(preferred_skills),
            "education_requirements": _to_list(education_requirements),
            "other_constraints": _to_list(other_constraints),
        }

        try:
            created_job = create_job(job_data)

            st.session_state.job_created_message = (
                f"Job '{title.strip()}' created successfully. "
                f"Job ID: {created_job.get('id')}"
            )

            st.session_state.jobs_page = 1

            st.session_state.pop(f"{mode_key}_requirements", None)
            st.session_state.pop(f"{mode_key}_description", None)

            st.rerun()

        except Exception as exc:
            _show_api_error(exc)


# ============================================================
# PASTE JD
# ============================================================


def _render_paste_jd() -> None:
    """Paste JD → AI analyze → editable requirements."""

    render_html(
        """
        <div class="input-card">
            <div class="input-card-title">
                📋 Paste Job Description
            </div>
            <div class="input-card-description">
                Paste the complete JD and let AI extract
                structured recruitment requirements.
            </div>
        </div>
        """
    )

    job_description = st.text_area(
        "Paste Job Description",
        height=220,
        placeholder=(
            "Paste the complete job description here...\n\n"
            "Example:\n"
            "We are looking for a Senior Backend Developer with "
            "4+ years of experience in Python and FastAPI..."
        ),
        key="paste_jd_description",
        label_visibility="collapsed",
    )

    if st.button(
        "🤖 Analyze JD with AI",
        type="primary",
        key="analyze_paste_jd",
        use_container_width=True,
    ):
        if not job_description.strip():
            st.warning("Please enter a job description first.")
            return

        with st.spinner("AI is analyzing the job description..."):
            try:
                requirements = analyze_jd(job_description.strip())
                st.session_state["paste_jd_requirements"] = requirements
                st.session_state["paste_jd_description"] = job_description.strip()
                st.success("JD analyzed successfully.")
            except Exception as exc:
                _show_api_error(exc)

    requirements = st.session_state.get("paste_jd_requirements")
    if requirements:
        _create_job_from_requirements(requirements, "paste_jd")


# ============================================================
# UPLOAD JD
# ============================================================


def _render_upload_jd() -> None:
    """Upload JD → AI analyze → editable requirements."""

    render_html(
        """
        <div class="input-card upload-input-card">
            <div class="upload-icon">
                📄
            </div>
            <div class="input-card-title">
                Upload Job Description
            </div>
            <div class="input-card-description">
                Upload TXT, PDF or DOCX and let AI extract
                structured job requirements.
            </div>
        </div>
        """
    )

    uploaded_file = st.file_uploader(
        "Upload Job Description",
        type=["txt", "pdf", "docx"],
        help="Supported formats: TXT, PDF and DOCX. Maximum file size: 10 MB.",
        key="jd_file_uploader",
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        render_html(
            f"""
            <div class="selected-file">
                <span>📄</span>
                <div>
                    <strong>{html.escape(uploaded_file.name)}</strong>
                    <small>{uploaded_file.size / 1024:.1f} KB</small>
                </div>
            </div>
            """
        )

        if st.button(
            "🤖 Analyze Uploaded JD",
            type="primary",
            key="analyze_uploaded_jd",
            use_container_width=True,
        ):
            with st.spinner("Reading file and analyzing JD with AI..."):
                try:
                    requirements = upload_jd(uploaded_file)
                    st.session_state["upload_jd_requirements"] = requirements
                    st.session_state["upload_jd_description"] = requirements.get(
                        "extracted_text", ""
                    )
                    st.success("JD uploaded and analyzed successfully.")
                except Exception as exc:
                    _show_api_error(exc)

    requirements = st.session_state.get("upload_jd_requirements")
    if requirements:
        extracted_text = requirements.get("extracted_text", "")
        if extracted_text:
            with st.expander("📄 View Extracted Job Description", expanded=False):
                st.text_area(
                    "Original JD Text",
                    value=extracted_text,
                    height=200,
                    disabled=True,
                    key="upload_jd_extracted_preview",
                )

        _create_job_from_requirements(requirements, "upload_jd")


# ============================================================
# MANUAL JOB CREATION
# ============================================================


def _render_manual_job() -> None:
    """Render manual job creation form."""

    render_html(
        """
        <div class="input-card">
            <div class="input-card-title">
                ✍️ Manual Job Creation
            </div>
            <div class="input-card-description">
                Enter job information manually and define
                structured matching requirements.
            </div>
        </div>
        """
    )

    render_html(
        """
        <div class="form-section-label">
            Basic Information
        </div>
        """
    )

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        title = st.text_input(
            "Job Title",
            placeholder="e.g. Backend Developer",
            key="manual_title",
        )

        company = st.text_input(
            "Company",
            placeholder="e.g. Infotech Solutions",
            key="manual_company",
        )

        location = st.text_input(
            "Location",
            placeholder="e.g. New Delhi / Remote",
            key="manual_location",
        )

    with col2:
        experience_required = st.text_input(
            "Experience Required",
            placeholder="e.g. 4+ years",
            key="manual_experience",
        )

        employment_type = st.text_input(
            "Employment Type",
            placeholder="e.g. Full Time",
            key="manual_employment",
        )

        status = st.selectbox(
            "Status",
            options=["draft", "open", "closed"],
            key="manual_status",
        )

    render_html(
        """
        <div class="form-section-label">
            Job Description
        </div>
        """
    )

    description = st.text_area(
        "Job Description",
        height=200,
        placeholder=(
            "Enter complete job description, "
            "responsibilities, skills and requirements..."
        ),
        key="manual_description",
        label_visibility="collapsed",
    )

    render_html(
        """
        <div class="form-section-label">
            Structured Requirements
        </div>
        """
    )

    required_experience_years = st.number_input(
        "Required Experience (Years)",
        min_value=0.0,
        value=0.0,
        step=0.5,
        key="manual_required_experience",
    )

    skill_col1, skill_col2 = st.columns(2, gap="medium")

    with skill_col1:
        required_skills = st.text_area(
            "Required Skills",
            placeholder="Python\nFastAPI\nPostgreSQL\nREST API",
            height=120,
            help="Enter one skill per line.",
            key="manual_required_skills",
        )

    with skill_col2:
        preferred_skills = st.text_area(
            "Preferred Skills",
            placeholder="Docker\nAWS\nRedis",
            height=120,
            help="Enter one skill per line.",
            key="manual_preferred_skills",
        )

    education_requirements = st.text_area(
        "Education Requirements",
        height=80,
        placeholder="Bachelor's degree in Computer Science or related field",
        key="manual_education",
    )

    other_constraints = st.text_area(
        "Other Constraints",
        height=80,
        placeholder="Work from office\nImmediate joiner preferred",
        key="manual_constraints",
    )

    render_html('<div class="form-action-row"></div>')

    if st.button(
        "🚀 Create Job",
        type="primary",
        key="manual_create_job",
        use_container_width=True,
    ):
        if not title.strip():
            st.error("Job Title is required.")
            return

        if not company.strip():
            st.error("Company is required.")
            return

        if not description.strip():
            st.error("Job Description is required.")
            return

        job_data = {
            "title": title.strip(),
            "company": company.strip(),
            "description": description.strip(),
            "location": location.strip(),
            "experience_required": experience_required.strip(),
            "employment_type": employment_type.strip(),
            "status": status,
            "required_experience_years": (
                required_experience_years if required_experience_years > 0 else None
            ),
            "required_skills": _to_list(required_skills),
            "preferred_skills": _to_list(preferred_skills),
            "education_requirements": _to_list(education_requirements),
            "other_constraints": _to_list(other_constraints),
        }

        try:
            created_job = create_job(job_data)
            st.session_state.job_created_message = (
                f"Job '{title.strip()}' created successfully. "
                f"Job ID: {created_job.get('id')}"
            )
            st.session_state.jobs_page = 1
            st.rerun()

        except Exception as exc:
            _show_api_error(exc)


# ============================================================
# CREATE JOB MODAL
# ============================================================


@st.dialog("Create New Job", width="large")
def _create_job_dialog() -> None:
    render_html(
        """
        <div class="modal-header">
            <div class="modal-eyebrow">
                AI RECRUITMENT WORKSPACE
            </div>
            <div class="modal-title">
                Build your next opportunity
            </div>
            <div class="modal-description">
                Create a job manually, paste a JD or upload
                a document. AI can convert the JD into
                structured matching requirements.
            </div>
        </div>
        """
    )

    mode = st.radio(
        "Choose creation method",
        options=[
            "✍️ Manual",
            "📋 Paste JD",
            "📄 Upload JD",
        ],
        horizontal=True,
        key="job_creation_mode",
        label_visibility="collapsed",
    )

    render_html('<div class="creation-method-spacer"></div>')

    if mode == "✍️ Manual":
        _render_manual_job()
    elif mode == "📋 Paste JD":
        _render_paste_jd()
    elif mode == "📄 Upload JD":
        _render_upload_jd()


# ============================================================
# EDIT JOB MODAL
# ============================================================


@st.dialog("Edit Job", width="large")
def _edit_job_dialog(job_id: int) -> None:
    """Render edit form for selected job inside a dialog modal."""
    try:
        job = get_job(job_id)
    except Exception as exc:
        _show_api_error(exc)
        return

    job_title = job.get("title", "") or ""

    render_html(
        f"""
        <div class="modal-header">
            <div class="modal-eyebrow">
                JOB MANAGEMENT · ID #{job_id}
            </div>
            <div class="modal-title">
                Edit: {html.escape(str(job_title))}
            </div>
            <div class="modal-description">
                Update job details, requirements, and matching criteria.
            </div>
        </div>
        """
    )

    with st.form(f"edit_job_dialog_form_{job_id}"):
        col1, col2 = st.columns(2, gap="medium")

        with col1:
            title = st.text_input(
                "Job Title",
                value=job.get("title", "") or "",
            )
            company = st.text_input(
                "Company",
                value=job.get("company", "") or "",
            )
            location = st.text_input(
                "Location",
                value=job.get("location", "") or "",
            )

        with col2:
            experience_required = st.text_input(
                "Experience Required",
                value=job.get("experience_required", "") or "",
            )
            employment_type = st.text_input(
                "Employment Type",
                value=job.get("employment_type", "") or "",
            )
            status_options = ["draft", "open", "closed"]
            current_status = job.get("status", "draft")
            status_index = (
                status_options.index(current_status)
                if current_status in status_options
                else 0
            )
            status = st.selectbox(
                "Status",
                options=status_options,
                index=status_index,
            )

        description = st.text_area(
            "Job Description",
            value=job.get("description", "") or "",
            height=200,
        )

        required_experience_years = st.number_input(
            "Required Experience (Years)",
            min_value=0.0,
            value=float(job.get("required_experience_years", 0) or 0),
            step=0.5,
        )

        skill_col1, skill_col2 = st.columns(2, gap="medium")
        with skill_col1:
            required_skills = st.text_area(
                "Required Skills",
                value=_to_lines(job.get("required_skills")),
                height=120,
                help="One skill per line",
            )
        with skill_col2:
            preferred_skills = st.text_area(
                "Preferred Skills",
                value=_to_lines(job.get("preferred_skills")),
                height=120,
                help="One skill per line",
            )

        education_requirements = st.text_area(
            "Education Requirements",
            value=_to_lines(job.get("education_requirements")),
            height=80,
            help="One requirement per line",
        )

        other_constraints = st.text_area(
            "Other Constraints",
            value=_to_lines(job.get("other_constraints")),
            height=80,
            help="One constraint per line",
        )

        action_col1, action_col2 = st.columns(2, gap="small")
        with action_col1:
            save = st.form_submit_button(
                "💾 Save Changes",
                type="primary",
                use_container_width=True,
            )
        with action_col2:
            cancel = st.form_submit_button(
                "Cancel",
                key=f"neutral_cancel_edit_{job_id}",
                use_container_width=True,
            )

    if cancel:
        st.rerun()

    if save:
        if not title.strip():
            st.error("Job Title is required.")
            return

        if not company.strip():
            st.error("Company is required.")
            return

        if not description.strip():
            st.error("Job Description is required.")
            return

        job_data = {
            "title": title.strip(),
            "company": company.strip(),
            "description": description.strip(),
            "location": location.strip(),
            "experience_required": experience_required.strip(),
            "employment_type": employment_type.strip(),
            "status": status,
            "required_experience_years": (
                required_experience_years if required_experience_years > 0 else None
            ),
            "required_skills": _to_list(required_skills),
            "preferred_skills": _to_list(preferred_skills),
            "education_requirements": _to_list(education_requirements),
            "other_constraints": _to_list(other_constraints),
        }

        try:
            update_job(job_id, job_data)
            st.session_state["job_created_message"] = (
                f"Job '{title.strip()}' updated successfully."
            )
            st.rerun()
        except Exception as exc:
            _show_api_error(exc)


# ============================================================
# DELETE JOB MODAL
# ============================================================


@st.dialog("Delete Job?", width="small")
def _delete_job_dialog(job_id: int, job_title: str) -> None:
    """Confirmation modal dialog before deleting a job."""
    safe_title = html.escape(str(job_title))

    render_html(
        f"""
        <div style="padding: 4px 0 16px 0;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                <div style="width: 40px; height: 40px; border-radius: 12px; background: #fde8e8; border: 1.5px solid #f5c4c4; display: flex; align-items: center; justify-content: center; font-size: 20px;">
                    🗑️
                </div>
                <div>
                    <div style="color: #a13b3b; font-size: 10px; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase;">CONFIRM DELETION</div>
                    <div style="color: #14382b; font-size: 18px; font-weight: 800;">Delete Job?</div>
                </div>
            </div>
            <div style="color: #556c62; font-size: 13px; line-height: 1.5; margin-bottom: 12px;">
                Are you sure you want to delete <strong>"{safe_title}"</strong> (Job ID #{job_id})?
            </div>
            <div style="padding: 10px 14px; background: #fdf2f2; border: 1px solid #f2c7c7; border-radius: 12px; color: #a13b3b; font-size: 11px; line-height: 1.45;">
                ⚠️ This action cannot be undone. Matching rankings and pipelines associated with this role may be affected.
            </div>
        </div>
        """
    )

    confirm_col1, confirm_col2 = st.columns(2, gap="small")
    with confirm_col1:
        if st.button("Cancel", key=f"dlg_cancel_del_{job_id}", use_container_width=True):
            st.rerun()

    with confirm_col2:
        if st.button(
            "Delete Job",
            key=f"dlg_confirm_del_{job_id}",
            type="primary",
            use_container_width=True,
        ):
            try:
                delete_job(job_id)
                st.session_state["job_created_message"] = (
                    f"Job '{job_title}' deleted successfully."
                )
                st.rerun()
            except Exception as exc:
                _show_api_error(exc)


# ============================================================
# JOB CARD
# ============================================================


def _render_job_card(job: dict) -> None:
    """Render a single modern job card matching the SaaS design system."""
    job_id = job.get("id", "-")
    title = job.get("title", "Untitled Job")
    company = job.get("company", "-")
    location = job.get("location", "-")
    experience = job.get("experience_required", "-")
    employment = job.get("employment_type", "-")
    status = job.get("status", "draft")

    status_class = _job_status_class(status)
    status_label = _job_status_label(status)

    required_skills = job.get("required_skills", [])
    preferred_skills = job.get("preferred_skills", [])
    education_reqs = job.get("education_requirements", [])
    constraints = job.get("other_constraints", [])
    description = job.get("description", "")

    safe_title = html.escape(str(title))
    safe_company = html.escape(str(company))
    safe_location = html.escape(str(location))
    safe_exp = html.escape(str(experience))
    safe_emp = html.escape(str(employment))
    safe_id = html.escape(str(job_id))

    with st.container(border=True):
        # Card Header & Meta Grid
        render_html(
            f"""
            <div class="job-card-top">
                <div>
                    <div class="job-card-eyebrow">
                        JOB · ID #{safe_id}
                    </div>
                    <div class="job-card-title">
                        💼 {safe_title}
                    </div>
                    <div class="job-card-company">
                        {safe_company}
                    </div>
                </div>

                <div class="job-status {status_class}">
                    {status_label}
                </div>
            </div>

            <div class="job-meta-grid">
                <div class="job-meta-item">
                    <span>📍</span>
                    <div>
                        <small>Location</small>
                        <strong>{safe_location}</strong>
                    </div>
                </div>

                <div class="job-meta-item">
                    <span>⏱️</span>
                    <div>
                        <small>Experience</small>
                        <strong>{safe_exp}</strong>
                    </div>
                </div>

                <div class="job-meta-item">
                    <span>💼</span>
                    <div>
                        <small>Employment</small>
                        <strong>{safe_emp}</strong>
                    </div>
                </div>
            </div>
            """
        )

        # Required Skills
        if required_skills:
            skills_html = "".join(
                f'<span class="skill-pill">{html.escape(str(skill))}</span>'
                for skill in required_skills
            )
            render_html(
                f"""
                <div class="job-skills-section">
                    <div class="job-card-label">Required Skills</div>
                    <div class="skill-pills">
                        {skills_html}
                    </div>
                </div>
                """
            )

        # Preferred Skills
        if preferred_skills:
            preferred_html = "".join(
                f'<span class="skill-pill preferred-pill">{html.escape(str(skill))}</span>'
                for skill in preferred_skills
            )
            render_html(
                f"""
                <div class="job-skills-section preferred-section">
                    <div class="job-card-label preferred-label">Preferred Skills</div>
                    <div class="skill-pills">
                        {preferred_html}
                    </div>
                </div>
                """
            )

        # Education & Constraints pills if present
        extra_badges = []
        if education_reqs:
            for edu in education_reqs:
                safe_edu = html.escape(str(edu))
                extra_badges.append(
                    f'<span class="contact-pill" style="font-size: 11px;">🎓 {safe_edu}</span>'
                )
        if constraints:
            for con in constraints:
                safe_con = html.escape(str(con))
                extra_badges.append(
                    f'<span class="contact-pill" style="font-size: 11px;">📌 {safe_con}</span>'
                )

        if extra_badges:
            badges_str = "".join(extra_badges)
            render_html(
                f"""
                <div style="margin-top: 14px; display: flex; flex-wrap: wrap; gap: 8px;">
                    {badges_str}
                </div>
                """
            )

        # Description expander
        if description:
            with st.expander("📄 Review Full Job Description", expanded=False):
                st.markdown(description)

        # Action bar with Edit & Delete
        st.markdown('<div class="candidate-card-action-bar"></div>', unsafe_allow_html=True)
        col_info, col_edit, col_del = st.columns([3.2, 0.9, 0.9])

        with col_info:
            render_html(
                """
                <div style="color: #648075; font-size: 11px; padding-top: 8px;">
                    ✓ Active recruitment pipeline opportunity
                </div>
                """
            )

        with col_edit:
            try:
                numeric_job_id = int(job_id)
            except (ValueError, TypeError):
                numeric_job_id = None

            if numeric_job_id is not None:
                if st.button(
                    "✏️ Edit",
                    key=f"edit_job_btn_{numeric_job_id}",
                    use_container_width=True,
                ):
                    _edit_job_dialog(numeric_job_id)

        with col_del:
            if numeric_job_id is not None:
                if st.button(
                    "🗑️ Delete",
                    key=f"del_job_btn_{numeric_job_id}",
                    use_container_width=True,
                ):
                    _delete_job_dialog(numeric_job_id, str(title))


# ============================================================
# JOB LIST
# ============================================================


def _render_job_list() -> None:
    """Render existing jobs with search, pagination, and modern cards."""

    render_html(
        """
        <div class="jobs-list-header">
            <div>
                <div class="jobs-section-title">
                    Job Listings
                </div>
                <div class="jobs-section-description">
                    Manage your recruitment opportunities, requirements, and candidate matching pipelines.
                </div>
            </div>
        </div>
        """
    )

    search_col, size_col = st.columns([4, 1], gap="medium")

    with search_col:
        search = st.text_input(
            "Search Jobs",
            placeholder="Search by title, company, or keywords...",
            key="job_search",
            label_visibility="collapsed",
        )

    with size_col:
        page_size = st.selectbox(
            "Jobs per page",
            options=[5, 10, 20, 50],
            index=1,
            key="jobs_page_size",
            label_visibility="collapsed",
        )

    if "jobs_page" not in st.session_state:
        st.session_state.jobs_page = 1

    try:
        data = get_jobs(
            page=st.session_state.jobs_page,
            page_size=page_size,
            search=search,
        )
    except Exception as exc:
        _show_api_error(exc)
        return

    jobs = data.get("items", [])
    total = data.get("total", 0)
    total_pages = data.get("total_pages", 0)

    if not jobs:
        render_html(
            """
            <div class="empty-state">
                <div class="empty-state-icon">
                    💼
                </div>
                <div class="empty-state-title">
                    No jobs found
                </div>
                <div class="empty-state-description">
                    Create your first opportunity to start matching candidates against structured requirements.
                </div>
            </div>
            """
        )
        return

    render_html(
        f"""
        <div class="results-count">
            Showing <strong>{len(jobs)}</strong> of <strong>{total}</strong> jobs
        </div>
        """
    )

    for job in jobs:
        _render_job_card(job)

    # --------------------------------------------------------
    # PAGINATION
    # --------------------------------------------------------

    if total_pages > 1:
        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            if st.button(
                "⬅️ Previous",
                key="jobs_previous",
                disabled=(st.session_state.jobs_page <= 1),
                use_container_width=True,
            ):
                st.session_state.jobs_page -= 1
                st.rerun()

        with col2:
            render_html(
                f"""
                <div class="pagination-label">
                    Page {st.session_state.jobs_page} of {total_pages}
                </div>
                """
            )

        with col3:
            if st.button(
                "Next ➡️",
                key="jobs_next",
                disabled=(st.session_state.jobs_page >= total_pages),
                use_container_width=True,
            ):
                st.session_state.jobs_page += 1
                st.rerun()


# ============================================================
# MAIN JOB PAGE
# ============================================================


def render_jobs_page() -> None:
    """Main Jobs page matching the AI Recruitment SaaS visual language."""

    # --------------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------------

    render_html(
        """
        <div class="jobs-page-header">
            <div>
                <div class="jobs-eyebrow">
                    JOBS INTELLIGENCE
                </div>
                <div class="jobs-page-title">
                    Manage your recruitment pipeline
                </div>
                <div class="jobs-page-subtitle">
                    Create, analyze and manage job opportunities.
                </div>
            </div>
            <div class="jobs-header-icon">
                💼
            </div>
        </div>
        """
    )

    # --------------------------------------------------------
    # SUCCESS MESSAGE
    # --------------------------------------------------------

    if "job_created_message" in st.session_state:
        st.success(st.session_state.job_created_message)
        del st.session_state["job_created_message"]

    # --------------------------------------------------------
    # HEADER ACTION & OVERVIEW HEADING
    # --------------------------------------------------------

    head_col1, head_col2 = st.columns([4, 1.2])

    with head_col1:
        render_html(
            """
            <div class="jobs-stat-section" style="margin-top: 0; margin-bottom: 0;">
                <div class="jobs-stat-title">
                    Recruitment Overview
                </div>
                <div class="jobs-stat-subtitle">
                    Current job pipeline and opportunity status at a glance
                </div>
            </div>
            """
        )

    with head_col2:
        if st.button(
            "＋ Create Job",
            type="primary",
            key="open_create_job",
            use_container_width=True,
        ):
            _create_job_dialog()

    # --------------------------------------------------------
    # JOB STATISTICS CARDS
    # --------------------------------------------------------

    try:
        stats = get_jobs(
            page=1,
            page_size=100,
            search="",
        )
        all_jobs = stats.get("items", [])
        total_jobs = stats.get("total", len(all_jobs))
    except Exception:
        all_jobs = []
        total_jobs = 0

    open_jobs = sum(1 for j in all_jobs if j.get("status") == "open")
    draft_jobs = sum(1 for j in all_jobs if j.get("status") == "draft")
    closed_jobs = sum(1 for j in all_jobs if j.get("status") == "closed")

    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4, gap="medium")

    with stat_col1:
        render_html(
            f"""
            <div class="jobs-stat-card">
                <div class="jobs-stat-icon">
                    💼
                </div>
                <div class="jobs-stat-label">
                    TOTAL JOBS
                </div>
                <div class="jobs-stat-value">
                    {total_jobs}
                </div>
                <div class="jobs-stat-description">
                    Recruitment opportunities
                </div>
            </div>
            """
        )

    with stat_col2:
        render_html(
            f"""
            <div class="jobs-stat-card">
                <div class="jobs-stat-icon" style="background: #e3f7ea;">
                    🟢
                </div>
                <div class="jobs-stat-label">
                    OPEN
                </div>
                <div class="jobs-stat-value" style="color: #11794d;">
                    {open_jobs}
                </div>
                <div class="jobs-stat-description">
                    Active opportunities
                </div>
            </div>
            """
        )

    with stat_col3:
        render_html(
            f"""
            <div class="jobs-stat-card">
                <div class="jobs-stat-icon" style="background: #edf3f0;">
                    📝
                </div>
                <div class="jobs-stat-label">
                    DRAFT
                </div>
                <div class="jobs-stat-value" style="color: #556c62;">
                    {draft_jobs}
                </div>
                <div class="jobs-stat-description">
                    Jobs being prepared
                </div>
            </div>
            """
        )

    with stat_col4:
        render_html(
            f"""
            <div class="jobs-stat-card">
                <div class="jobs-stat-icon" style="background: #fde8e8;">
                    🛑
                </div>
                <div class="jobs-stat-label">
                    CLOSED
                </div>
                <div class="jobs-stat-value" style="color: #a13b3b;">
                    {closed_jobs}
                </div>
                <div class="jobs-stat-description">
                    Completed opportunities
                </div>
            </div>
            """
        )

    # --------------------------------------------------------
    # JOB LIST SECTION
    # --------------------------------------------------------

    _render_job_list()


def render_jobs() -> None:
    """Backward-compatible entry point."""
    render_jobs_page()