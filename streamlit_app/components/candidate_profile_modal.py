import html
import re
import textwrap
import requests
import streamlit as st

from streamlit_app.api_client.candidates import (
    get_candidate,
    get_candidate_resumes,
    get_candidates_error_message,
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


def _format_experience(value) -> str:
    if value is None:
        return "Not specified"
    try:
        return f"{float(value):g} years"
    except (TypeError, ValueError):
        return str(value)


def _extract_display_value(value, field_name: str) -> str:
    """Convert dictionary or primitive value into human-readable string."""
    if isinstance(value, dict):
        field_value = value.get(field_name)
        if field_value is not None:
            return str(field_value)
        return ""
    return str(value) if value is not None else ""


def _render_profile_section(
    title: str,
    icon: str,
    values: list,
    field_name: str,
) -> None:
    if not values:
        return

    icon_color_class = (
        "icon-box-blue"
        if "Education" in title
        else ("icon-box-purple" if "Projects" in title else "icon-box-amber")
    )

    items_html = ""
    for value in values:
        display_value = _extract_display_value(value, field_name)
        if display_value:
            safe_val = html.escape(display_value)
            items_html += f"""
            <div class="profile-list-item">
                <div class="icon-box {icon_color_class}" style="width: 28px; height: 28px; font-size: 13px;">
                    {icon}
                </div>
                <span style="font-weight: 600; color: #14382b;">{safe_val}</span>
            </div>
            """

    if items_html:
        render_html(
            f"""
            <div class="profile-group-card">
                <div class="profile-group-header">
                    <span>{icon}</span> {html.escape(title)}
                </div>
                {items_html}
            </div>
            """
        )


def _render_skills_section(skills: list) -> None:
    if not skills:
        return

    pills_html = ""
    for skill in skills:
        skill_name = _extract_display_value(skill, "skill_name")
        if skill_name:
            pills_html += f'<span class="profile-pill">{html.escape(skill_name)}</span>'

    if pills_html:
        render_html(
            f"""
            <div class="profile-group-card">
                <div class="profile-group-header">
                    <span>🛠️</span> Skills & Core Competencies
                </div>
                <div class="profile-pill-container">
                    {pills_html}
                </div>
            </div>
            """
        )


def _render_resume_history_section(resumes: list) -> None:
    if not resumes:
        return

    cards_html = ""
    for resume in resumes:
        filename = (
            resume.get("original_filename")
            or resume.get("filename")
            or "Unknown resume"
        )
        version = resume.get("version")
        is_current = resume.get("is_current", False)
        source_type = resume.get("source_type") or "upload"
        file_type = resume.get("file_type") or "doc"
        extraction_status = resume.get("extraction_status") or "processed"

        status_class = "status-open" if is_current else "status-draft"
        status_text = "CURRENT" if is_current else "PREVIOUS"
        version_text = f"v{version}" if version is not None else "v1.0"

        safe_filename = html.escape(str(filename))
        safe_source = html.escape(str(source_type).title())
        safe_file_type = html.escape(str(file_type).upper())
        safe_ext = html.escape(str(extraction_status).replace("_", " ").title())

        cards_html += f"""
        <div class="resume-history-card">
            <div style="display: flex; align-items: center; gap: 14px;">
                <div class="icon-box icon-box-green">
                    📄
                </div>
                <div>
                    <strong style="color: #14382b; font-size: 14px;">{safe_filename}</strong>
                    <div style="color: #648075; font-size: 12px; margin-top: 2px;">
                        {version_text} • {safe_file_type} • Source: {safe_source}
                    </div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 11px; font-weight: 600; color: #587469;">Status: {safe_ext}</span>
                <span class="job-status {status_class}">{status_text}</span>
            </div>
        </div>
        """

    render_html(
        f"""
        <div class="profile-group-card">
            <div class="profile-group-header">
                <span>📄</span> Resume Documents Timeline
            </div>
            {cards_html}
        </div>
        """
    )


@st.dialog("Candidate Profile", width="large")
def open_candidate_profile_dialog(candidate_id: int, context: str | None = None) -> None:
    """
    Open the candidate's complete profile inside a modern, reusable popup dialog.
    """
    try:
        candidate = get_candidate(candidate_id)
    except requests.RequestException as exc:
        st.error(get_candidates_error_message(exc))
        if st.button("Close", key=f"dlg_close_err_{candidate_id}", use_container_width=True):
            st.rerun()
        return

    # Fetch resumes timeline
    resumes = candidate.get("resumes") or []
    if not resumes:
        try:
            resumes = get_candidate_resumes(candidate_id)
        except Exception:
            resumes = []

    name = candidate.get("name") or "Unnamed Candidate"
    email = candidate.get("email") or "Not available"
    phone = candidate.get("phone") or "Not available"
    whatsapp = candidate.get("whatsapp_number") or candidate.get("whatsapp")
    linkedin = candidate.get("linkedin_url") or candidate.get("linkedin")
    github = candidate.get("github_url") or candidate.get("github")
    portfolio = candidate.get("portfolio_url") or candidate.get("portfolio")
    experience = _format_experience(candidate.get("total_experience_years"))

    safe_name = html.escape(str(name))
    safe_email = html.escape(str(email))
    safe_phone = html.escape(str(phone))
    safe_exp = html.escape(str(experience))

    # Optional context subtitle
    context_html = ""
    if context:
        safe_ctx = html.escape(str(context))
        context_html = f"""
        <div style="display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; background: #e8f5ed; border: 1px solid #bfe3cd; border-radius: 999px; color: #127a4e; font-size: 11px; font-weight: 700; margin-bottom: 8px;">
            <span>🎯</span> {safe_ctx}
        </div>
        """

    # Candidate Profile Hero Panel
    render_html(
        f"""
        <div class="candidate-profile-panel" style="margin-top: 4px; margin-bottom: 18px;">
            <div class="candidate-profile-hero">
                <div style="display: flex; align-items: center; gap: 18px;">
                    <div class="candidate-profile-avatar">
                        👤
                    </div>
                    <div>
                        {context_html}
                        <div class="candidates-eyebrow">CANDIDATE INTELLIGENCE · ID #{candidate_id}</div>
                        <div style="color: #14382b; font-size: 26px; font-weight: 800; letter-spacing: -0.02em;">
                            {safe_name}
                        </div>
                        <div style="color: #587469; font-size: 13px; margin-top: 4px;">
                            Verified talent record · Total Experience: <strong>{safe_exp}</strong>
                        </div>
                    </div>
                </div>
                <div class="dashboard-hero-status">
                    <span class="dashboard-status-dot"></span>
                    Active Profile
                </div>
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
                    <div class="icon-box icon-box-green">📱</div>
                    <div>
                        <small>Contact Phone</small>
                        <strong>{safe_phone}</strong>
                    </div>
                </div>
                <div class="candidate-meta-item">
                    <div class="icon-box icon-box-amber">💼</div>
                    <div>
                        <small>Experience</small>
                        <strong>{safe_exp}</strong>
                    </div>
                </div>
            </div>
        </div>
        """
    )

    # Contact & Social Links Section
    contact_pills = []
    if email and email != "Not available":
        contact_pills.append(f'<span class="contact-pill">📧 {safe_email}</span>')
    if phone and phone != "Not available":
        contact_pills.append(f'<span class="contact-pill">📱 {safe_phone}</span>')
    if whatsapp:
        safe_wa = html.escape(str(whatsapp))
        contact_pills.append(f'<span class="contact-pill">💬 WhatsApp: {safe_wa}</span>')
    if linkedin:
        safe_li = html.escape(str(linkedin))
        contact_pills.append(f'<a class="contact-pill" href="{safe_li}" target="_blank">🔗 LinkedIn</a>')
    if github:
        safe_gh = html.escape(str(github))
        contact_pills.append(f'<a class="contact-pill" href="{safe_gh}" target="_blank">💻 GitHub</a>')
    if portfolio:
        safe_port = html.escape(str(portfolio))
        contact_pills.append(f'<a class="contact-pill" href="{safe_port}" target="_blank">🌐 Portfolio</a>')

    if contact_pills:
        pills_str = "".join(contact_pills)
        render_html(
            f"""
            <div class="profile-group-card">
                <div class="profile-group-header">
                    <span>📇</span> Contact & Professional Links
                </div>
                <div class="contact-pill-row">
                    {pills_str}
                </div>
            </div>
            """
        )

    # Skills Section
    skills = candidate.get("skills") or []
    _render_skills_section(skills)

    # Education Section
    education = candidate.get("education") or []
    _render_profile_section(
        title="Education & Academic Background",
        icon="🎓",
        values=education,
        field_name="education",
    )

    # Projects Section
    projects = candidate.get("projects") or []
    _render_profile_section(
        title="Key Projects & Practical Experience",
        icon="🚀",
        values=projects,
        field_name="project",
    )

    # Certifications Section
    certifications = candidate.get("certifications") or []
    _render_profile_section(
        title="Certifications & Accreditations",
        icon="🏆",
        values=certifications,
        field_name="certification",
    )

    # Resume History Timeline
    _render_resume_history_section(resumes)

    # Dialog Footer with Close button
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    if st.button("Close Profile", key=f"dlg_close_btn_{candidate_id}", use_container_width=True):
        st.rerun()
