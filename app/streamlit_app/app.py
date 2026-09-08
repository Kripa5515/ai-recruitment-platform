import streamlit as st


st.set_page_config(
    page_title="AI Recruitment Platform",
    page_icon="🤖",
    layout="wide",
)


st.title("🤖 AI Recruitment Platform")
st.caption("AI-powered Candidate Intelligence Dashboard")


st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Dashboard",
        "Jobs",
        "Resumes",
        "Candidates",
    ],
)


if page == "Dashboard":
    st.header("Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Jobs", 0)

    with col2:
        st.metric("Total Candidates", 0)

    with col3:
        st.metric("Total Resumes", 0)


elif page == "Jobs":
    st.header("💼 Jobs")
    st.info("Job management will be connected here.")


elif page == "Resumes":
    st.header("📄 Resumes")
    st.info("Resume management will be connected here.")


elif page == "Candidates":
    st.header("👤 Candidates")
    st.info("Candidate management will be connected here.")