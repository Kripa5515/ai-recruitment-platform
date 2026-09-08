import streamlit as st


def render_sidebar() -> str:

    with st.sidebar:

        st.markdown(
            """
            <div class="brand">🤖 AI Recruiter</div>
            <div class="brand-subtitle">
                Candidate Intelligence Platform
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### Navigation")

        page = st.radio(
            "Navigation",
            [
                "🏠 Dashboard",
                "💼 Jobs",
                "📄 Resumes",
                "👤 Candidates",
            ],
            label_visibility="collapsed",
        )

        st.markdown("---")

        st.caption("AI Recruitment Platform")
        st.caption("v1.0.0")

    return page