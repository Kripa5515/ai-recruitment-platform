import html
import re
import textwrap
import streamlit as st

from streamlit_app.components.candidate_profile_modal import (
    open_candidate_profile_dialog,
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


def get_match_level(
    score: float | None,
) -> tuple[str, str, str]:
    """
    Convert final score into a recruiter-friendly match category,
    icon, and CSS badge class.
    """
    if score is None:
        return "Not Available", "⚪", "badge-moderate"

    if score >= 80:
        return "Strong Match", "🟢", "badge-strong"

    if score >= 60:
        return "Good Match", "🔵", "badge-good"

    if score >= 40:
        return "Moderate Match", "🟡", "badge-moderate"

    return "Low Match", "🔴", "badge-low"


def _build_score_metrics_html(
    result: dict,
) -> str:
    """
    Build HTML for the main matching dimensions with clean visual score bars.
    """
    experience_score = float(result.get("experience_score", 0) or 0)
    required_skill_score = float(result.get("required_skill_score", 0) or 0)
    semantic_score = result.get("semantic_score")
    constraint_score = float(result.get("constraint_score", 0) or 0)

    exp_pct = max(0.0, min(100.0, experience_score))
    skill_pct = max(0.0, min(100.0, required_skill_score))
    const_pct = max(0.0, min(100.0, constraint_score))

    if semantic_score is None:
        sem_val_str = "N/A"
        sem_pct = 0.0
    else:
        sem_float = float(semantic_score)
        sem_val_str = f"{sem_float:.1f}%"
        sem_pct = max(0.0, min(100.0, sem_float))

    return f"""
    <div class="match-dimension-container">
        <div class="dimension-header">📊 Score Breakdown by Dimension</div>
        <div class="score-bars-grid">
            <div class="score-bar-box">
                <div class="score-bar-lbl">
                    <span>Experience</span>
                    <strong>{experience_score:.1f}%</strong>
                </div>
                <div class="score-bar-track">
                    <div class="score-bar-fill" style="width: {exp_pct}%;"></div>
                </div>
            </div>
            <div class="score-bar-box">
                <div class="score-bar-lbl">
                    <span>Required Skills</span>
                    <strong>{required_skill_score:.1f}%</strong>
                </div>
                <div class="score-bar-track">
                    <div class="score-bar-fill" style="width: {skill_pct}%;"></div>
                </div>
            </div>
            <div class="score-bar-box">
                <div class="score-bar-lbl">
                    <span>Semantic Match</span>
                    <strong>{sem_val_str}</strong>
                </div>
                <div class="score-bar-track">
                    <div class="score-bar-fill" style="width: {sem_pct}%;"></div>
                </div>
            </div>
            <div class="score-bar-box">
                <div class="score-bar-lbl">
                    <span>Constraints</span>
                    <strong>{constraint_score:.1f}%</strong>
                </div>
                <div class="score-bar-track">
                    <div class="score-bar-fill" style="width: {const_pct}%;"></div>
                </div>
            </div>
        </div>
    </div>
    """


def _build_contact_information_html(
    result: dict,
) -> str:
    """
    Build candidate contact and professional profile information HTML.
    Only displays fields that are actually present.
    """
    email = result.get("email")
    phone = result.get("phone")
    whatsapp = result.get("whatsapp_number") or result.get("whatsapp")
    linkedin = result.get("linkedin_url") or result.get("linkedin")
    github = result.get("github_url") or result.get("github")
    portfolio = result.get("portfolio_url") or result.get("portfolio")

    has_contact = any([email, phone, whatsapp, linkedin, github, portfolio])
    if not has_contact:
        return ""

    pills_html = '<div class="match-contact-bar"><span style="font-size: 11px; font-weight: 800; color: #527566; text-transform: uppercase; letter-spacing: 0.05em; margin-right: 4px;">CONTACT:</span>'

    if email:
        safe_email = html.escape(str(email))
        pills_html += f'<span class="contact-pill">📧 {safe_email}</span>'

    if phone:
        safe_phone = html.escape(str(phone))
        pills_html += f'<span class="contact-pill">📱 {safe_phone}</span>'

    if whatsapp:
        safe_wa = html.escape(str(whatsapp))
        pills_html += f'<span class="contact-pill">💬 {safe_wa}</span>'

    if linkedin:
        safe_li = html.escape(str(linkedin))
        pills_html += f'<a class="contact-pill" href="{safe_li}" target="_blank">🔗 LinkedIn</a>'

    if github:
        safe_gh = html.escape(str(github))
        pills_html += f'<a class="contact-pill" href="{safe_gh}" target="_blank">💻 GitHub</a>'

    if portfolio:
        safe_port = html.escape(str(portfolio))
        pills_html += f'<a class="contact-pill" href="{safe_port}" target="_blank">🌐 Portfolio</a>'

    pills_html += "</div>"
    return pills_html


def _build_reasons_html(
    result: dict,
) -> str:
    """
    Build explainable matching reasons HTML.
    """
    reasons = result.get("reasons", [])
    if not reasons:
        return ""

    reasons_html = """
    <div class="reasons-list">
        <div style="font-size: 11px; font-weight: 800; color: #175438; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.06em;">
            ✨ Why this candidate matches
        </div>
    """
    for reason in reasons:
        safe_reason = html.escape(str(reason))
        reasons_html += f"""
        <div class="reason-bullet">
            <span>✓</span>
            <span>{safe_reason}</span>
        </div>
        """
    reasons_html += "</div>"
    return reasons_html


def _build_warnings_html(
    result: dict,
) -> str:
    """
    Build recruiter review warnings HTML.
    """
    warnings = result.get("warnings", [])
    if not warnings:
        return ""

    warnings_html = """<div style="margin-top: 10px;">"""
    for warning in warnings:
        safe_warning = html.escape(str(warning))
        warnings_html += f"""
        <div class="warning-bullet">
            <span>⚠</span>
            <span>{safe_warning}</span>
        </div>
        """
    warnings_html += "</div>"
    return warnings_html


# Backward-compatible helper functions
def render_score_metrics(result: dict) -> None:
    html_content = _build_score_metrics_html(result)
    if html_content:
        render_html(html_content)


def render_contact_information(result: dict) -> None:
    html_content = _build_contact_information_html(result)
    if html_content:
        render_html(html_content)


def render_reasons(result: dict) -> None:
    html_content = _build_reasons_html(result)
    if html_content:
        render_html(html_content)


def render_warnings(result: dict) -> None:
    html_content = _build_warnings_html(result)
    if html_content:
        render_html(html_content)


def render_candidate_match_card(
    result: dict,
    rank: int,
    job_title: str | None = None,
) -> None:
    """
    Render a complete, modern candidate match card with View Candidate modal trigger.
    """
    candidate_name = result.get("candidate_name") or "Unknown Candidate"
    candidate_id = result.get("candidate_id", "-")
    final_score = result.get("final_score")
    deterministic_score = result.get("deterministic_score", 0)

    score = (
        final_score
        if final_score is not None
        else deterministic_score
    )

    level, icon, badge_class = get_match_level(score)

    score_display = f"{float(score):.1f}%" if score is not None else "N/A"
    safe_name = html.escape(str(candidate_name))
    safe_id = html.escape(str(candidate_id))

    contact_html = _build_contact_information_html(result)
    metrics_html = _build_score_metrics_html(result)
    reasons_html = _build_reasons_html(result)
    warnings_html = _build_warnings_html(result)

    with st.container(border=True):
        card_content_html = f"""
        <div class="match-card-header">
            <div class="match-card-candidate">
                <div class="match-rank-badge">
                    #{rank}
                </div>
                <div>
                    <div class="job-card-eyebrow">CANDIDATE ID: {safe_id}</div>
                    <div style="color: #14382b; font-size: 19px; font-weight: 800; letter-spacing: -0.02em;">
                        👤 {safe_name}
                    </div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 14px;">
                <div style="text-align: right;">
                    <div style="font-size: 26px; font-weight: 800; color: #14382b; line-height: 1;">
                        {score_display}
                    </div>
                    <small style="color: #6b8177; font-size: 10px; font-weight: 700; text-transform: uppercase;">Match Score</small>
                </div>
                <span class="match-score-badge {badge_class}">
                    {icon} {level}
                </span>
            </div>
        </div>
        {contact_html}
        {metrics_html}
        {reasons_html}
        {warnings_html}
        """
        render_html(card_content_html)

        st.markdown('<div class="candidate-card-action-bar"></div>', unsafe_allow_html=True)
        col_meta, col_btn = st.columns([3.2, 1.8])
        with col_meta:
            render_html(
                """
                <div style="color: #7f998d; font-size: 11px; padding-top: 8px; display: flex; align-items: center; gap: 6px;">
                    <span>🛡️</span> AI matching insight. Human recruiter makes the final hiring evaluation.
                </div>
                """
            )
        with col_btn:
            try:
                cand_id_int = int(candidate_id)
            except (ValueError, TypeError):
                cand_id_int = None

            if cand_id_int is not None:
                if st.button(
                    "View Candidate →",
                    key=f"view_match_cand_{cand_id_int}_{rank}",
                    use_container_width=True,
                ):
                    open_candidate_profile_dialog(
                        cand_id_int,
                        context=f"Matched for: {job_title}" if job_title else None,
                    )