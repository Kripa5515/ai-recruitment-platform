import streamlit as st

from streamlit_app.components.styles import load_custom_css
from streamlit_app.views.candidates import render_candidates
from streamlit_app.views.dashboard import render_dashboard
from streamlit_app.views.jobs import render_jobs
from streamlit_app.views.matching import render_matching
from streamlit_app.views.resumes import render_resume_page


def run_app() -> None:

    st.set_page_config(
        page_title="AI Recruiter",
        page_icon="🌿",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Load global application theme
    load_custom_css()

    # =========================================================
    # SIDEBAR
    # =========================================================

    with st.sidebar:

        st.markdown(
            """
            <div class="brand">
                🌿 AI Recruiter
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="brand-subtitle">
                Candidate Intelligence Platform
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            "**NAVIGATION**"
        )

        page = st.radio(
            "Navigation",
            [
                "🏠 Dashboard",
                "💼 Jobs",
                "📄 Resumes",
                "👤 Candidates",
                "🎯 Matching",
            ],
            label_visibility="collapsed",
        )

        st.divider()

        st.markdown(
            """
            <div class="status-online">
                ● System Online
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption(
            "AI Recruitment Platform"
        )

        st.caption(
            "v1.0.0"
        )

    # =========================================================
    # PAGE ROUTING
    # =========================================================

    if page == "🏠 Dashboard":

        render_dashboard()

    elif page == "💼 Jobs":

        render_jobs()

    elif page == "📄 Resumes":

        render_resume_page()

    elif page == "👤 Candidates":

        render_candidates()

    elif page == "🎯 Matching":

        render_matching()


if __name__ == "__main__":
    run_app()