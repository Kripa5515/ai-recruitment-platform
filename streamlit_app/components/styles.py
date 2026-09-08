import streamlit as st


def load_custom_css() -> None:
    st.markdown(
        """
<style>

/* ============================================================
   DESIGN TOKENS
============================================================ */

:root {
    /* ============================================================
       BASE SAAS THEME
    ============================================================ */
    --primary-green: #18A56B;
    --primary-green-dark: #128A58;
    --primary-green-light: #EAF6EF;
    --page-bg: #F3FAF6;
    --card-bg: #FFFFFF;
    --border-main: #D8E9DE;
    --border-subtle: #EBF5EF;
    --border-strong: #A8D4BC;
    --text-main: #17352A;
    --text-secondary: #587469;
    --text-muted: #6B8177;

    /* ============================================================
       SEMANTIC COLORS
    ============================================================ */
    /* Success / Primary (Green) */
    --semantic-success: #18A56B;
    --semantic-success-dark: #11794D;
    --semantic-success-bg: #EAF7F0;
    --semantic-success-border: #BFE3CD;

    /* Info / View (Blue) */
    --semantic-info: #2383D9;
    --semantic-info-dark: #1967B2;
    --semantic-info-bg: #EEF6FF;
    --semantic-info-border: #C8E1F8;

    /* Edit (Light Blue) */
    --semantic-edit: #4F9FE8;
    --semantic-edit-text: #1967B2;
    --semantic-edit-bg: #EEF6FF;
    --semantic-edit-border: #C4DFF9;

    /* Warning / Moderate (Amber) */
    --semantic-warning: #C98200;
    --semantic-warning-dark: #A06400;
    --semantic-warning-bg: #FFF8E8;
    --semantic-warning-border: #F5DFB2;

    /* Danger / Delete / Low (Red) */
    --semantic-danger: #D94B4B;
    --semantic-danger-dark: #B92E2E;
    --semantic-danger-bg: #FFF1F1;
    --semantic-danger-border: #F2C7C7;

    /* Neutral / Cancel (Gray) */
    --semantic-neutral: #64748B;
    --semantic-neutral-dark: #334155;
    --semantic-neutral-bg: #F4F6F8;
    --semantic-neutral-border: #CBD5E1;

    /* Purple Accent */
    --accent-purple: #6941C6;
    --accent-purple-bg: #F5F0FF;
    --accent-purple-border: #D8C7F8;

    /* Backward compatibility mappings */
    --green-500: #18A56B;
    --green-600: #128A58;
    --green-700: #0F754B;
    --green-50: #F3FAF6;
    --green-100: #EAF6EF;
    --green-200: #D8E9DE;
    --green-300: #C3E4CF;
    --border: #D8E9DE;
    --card: #FFFFFF;
    --danger: #D94B4B;
    --danger-bg: #FFF1F1;
    --danger-border: #F2C7C7;

    --shadow-sm: 0 4px 18px rgba(18, 92, 58, 0.06);
    --shadow-md: 0 8px 28px rgba(18, 92, 58, 0.09);
    --shadow-lg: 0 18px 45px rgba(18, 92, 58, 0.12);
}


/* ============================================================
   GLOBAL
============================================================ */

html,
body,
[class*="css"] {
    font-family:
        "Manrope",
        "Inter",
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 82% 3%,
            rgba(190, 238, 207, 0.34),
            transparent 28%
        ),
        linear-gradient(
            180deg,
            #f7fcf9 0%,
            #f0f8f3 100%
        );

    color: var(--text-main);
}


/* ============================================================
   MAIN CONTENT
============================================================ */

.main .block-container {
    max-width: 1500px;

    padding-top: 2.3rem;
    padding-left: 3rem;
    padding-right: 3rem;
    padding-bottom: 4rem;
}


/* ============================================================
   STREAMLIT HEADER
============================================================ */

[data-testid="stHeader"] {
    background: rgba(
        247,
        252,
        249,
        0.86
    );

    backdrop-filter: blur(12px);
}


/* ============================================================
   SIDEBAR
============================================================ */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #edf9f2 0%,
            #e5f4ea 100%
        );

    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

section[data-testid="stSidebar"] * {
    font-family:
        "Manrope",
        "Inter",
        sans-serif;
}

section[data-testid="stSidebar"]
div[data-testid="stRadio"] label {
    border-radius: 12px;

    padding: 8px 10px;

    margin-bottom: 5px;

    transition:
        background 0.2s ease,
        transform 0.2s ease;
}

section[data-testid="stSidebar"]
div[data-testid="stRadio"] label:hover {
    background:
        rgba(
            25,
            168,
            107,
            0.08
        );
}


/* ============================================================
   BRAND
============================================================ */

.brand {
    color: #0f3d2c !important;

    font-size: 1.3rem;

    font-weight: 800;

    letter-spacing: -0.03em;
}

.brand-subtitle {
    color: var(--text-secondary) !important;

    font-size: 0.78rem;

    margin-top: 4px;

    margin-bottom: 2rem;
}


/* ============================================================
   PAGE TITLES
============================================================ */

.page-title {
    color: var(--text-main);

    font-size: 32px;

    font-weight: 800;

    line-height: 1.15;

    letter-spacing: -0.035em;
}

.page-subtitle {
    color: var(--text-secondary);

    font-size: 14px;

    line-height: 1.6;

    margin-top: 7px;

    margin-bottom: 26px;
}

.section-title {
    color: var(--text-main);

    font-size: 20px;

    font-weight: 800;

    letter-spacing: -0.02em;

    margin-top: 25px;

    margin-bottom: 10px;
}


/* ============================================================
   DASHBOARD HERO
============================================================ */

.dashboard-hero {
    display: flex;

    justify-content: space-between;

    align-items: flex-start;

    gap: 30px;

    padding: 30px 34px;

    margin-bottom: 26px;

    border: 1px solid var(--border);

    border-radius: 24px;

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.96),
            rgba(235,249,240,0.96)
        );

    box-shadow: var(--shadow-md);
}

.dashboard-eyebrow {
    color: var(--green-600);

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 0.12em;

    margin-bottom: 8px;
}

.dashboard-hero-title {
    color: var(--text-main);

    font-size: 34px;

    font-weight: 800;

    line-height: 1.15;

    letter-spacing: -0.035em;
}

.dashboard-hero-subtitle {
    max-width: 700px;

    color: var(--text-secondary);

    font-size: 15px;

    line-height: 1.6;

    margin-top: 8px;
}

.dashboard-hero-status {
    display: inline-flex;

    align-items: center;

    gap: 8px;

    white-space: nowrap;

    padding: 9px 14px;

    background: #e3f7eb;

    border: 1px solid #bfe5cd;

    border-radius: 999px;

    color: #16704a;

    font-size: 12px;

    font-weight: 700;
}

.dashboard-status-dot {
    width: 8px;
    height: 8px;

    background: var(--green-500);

    border-radius: 50%;

    box-shadow:
        0 0 0 4px
        rgba(25,168,107,0.12);
}


/* ============================================================
   DASHBOARD SECTIONS
============================================================ */

.dashboard-section-heading {
    margin-top: 20px;
    margin-bottom: 14px;
}

.dashboard-section-spacing {
    margin-top: 30px;
}

.dashboard-section-title {
    color: var(--text-main);

    font-size: 19px;

    font-weight: 800;
}

.dashboard-section-subtitle {
    color: var(--text-secondary);

    font-size: 12px;

    margin-top: 3px;
}


/* ============================================================
   METRIC CARDS
============================================================ */

.metric-card {
    position: relative;

    min-height: 125px;

    padding: 20px;

    background:
        rgba(255,255,255,0.96);

    border: 1px solid var(--border);

    border-radius: 18px;

    box-shadow: var(--shadow-sm);

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease,
        border-color 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-3px);

    border-color: #b9dcc7;

    box-shadow: var(--shadow-md);
}

.metric-title {
    color: var(--text-secondary);

    font-size: 13px;

    font-weight: 600;

    margin-top: 5px;
}

.metric-value {
    color: var(--text-main);

    font-size: 30px;

    font-weight: 800;

    margin-top: 5px;
}

.metric-icon {
    font-size: 22px;

    margin-bottom: 4px;
}


/* ============================================================
   DASHBOARD PANELS
============================================================ */

.dashboard-panel {
    background:
        rgba(255,255,255,0.96);

    border: 1px solid var(--border);

    border-radius: 20px;

    padding: 22px;

    min-height: 310px;

    box-shadow: var(--shadow-sm);
}

.dashboard-panel-header {
    display: flex;

    justify-content: space-between;

    align-items: flex-start;

    margin-bottom: 24px;
}

.dashboard-panel-title {
    color: var(--text-main);

    font-size: 17px;

    font-weight: 800;
}

.dashboard-panel-subtitle {
    color: var(--text-secondary);

    font-size: 12px;

    margin-top: 4px;
}

.dashboard-panel-icon {
    width: 40px;
    height: 40px;

    display: flex;

    align-items: center;

    justify-content: center;

    background: var(--green-100);

    border: 1px solid var(--green-200);

    border-radius: 12px;

    font-size: 19px;
}


/* ============================================================
   OVERVIEW
============================================================ */

.overview-grid {
    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 12px;
}

.overview-item {
    padding: 16px;

    background: #f7fcf9;

    border: 1px solid #e2efe7;

    border-radius: 14px;
}

.overview-label {
    color: var(--text-muted);

    font-size: 9px;

    font-weight: 800;

    letter-spacing: 0.1em;
}

.overview-number {
    color: var(--text-main);

    font-size: 25px;

    font-weight: 800;

    margin-top: 5px;
}

.overview-description {
    color: var(--text-secondary);

    font-size: 11px;

    line-height: 1.4;

    margin-top: 5px;
}

.overview-ai-footer {
    display: flex;

    align-items: flex-start;

    gap: 12px;

    margin-top: 18px;

    padding: 14px 16px;

    background:
        linear-gradient(
            135deg,
            #eefaf2,
            #e5f6eb
        );

    border: 1px solid #d4ebdd;

    border-radius: 14px;
}

.overview-ai-icon {
    font-size: 20px;
}

.overview-ai-title {
    color: #176545;

    font-size: 12px;

    font-weight: 800;
}

.overview-ai-description {
    color: var(--text-secondary);

    font-size: 11px;

    line-height: 1.45;

    margin-top: 3px;
}


/* ============================================================
   MATCHING
============================================================ */

.matching-highlight {
    position: relative;

    overflow: hidden;

    background:
        radial-gradient(
            circle at 90% 0%,
            rgba(89,207,114,0.38),
            transparent 35%
        ),
        linear-gradient(
            145deg,
            #f0fbf4,
            #dff4e6
        );
}

.matching-highlight-header {
    display: flex;

    align-items: center;

    gap: 10px;
}

.matching-icon {
    width: 38px;
    height: 38px;

    display: flex;

    align-items: center;

    justify-content: center;

    background: #d5f1df;

    border: 1px solid #bce3ca;

    border-radius: 12px;

    font-size: 18px;
}

.matching-label {
    color: #26704f;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 0.1em;
}

.matching-number {
    color: #0f5e3d;

    font-size: 50px;

    font-weight: 800;

    line-height: 1;

    margin-top: 30px;
}

.matching-description {
    max-width: 280px;

    color: #527466;

    font-size: 12px;

    line-height: 1.5;

    margin-top: 8px;
}

.matching-progress-container {
    margin-top: 25px;
}

.matching-progress-track {
    width: 100%;

    height: 8px;

    background: #cfe8d8;

    border-radius: 999px;

    overflow: hidden;
}

.matching-progress-fill {
    height: 100%;

    background:
        linear-gradient(
            90deg,
            #18a96b,
            #5acb70
        );

    border-radius: 999px;
}

.matching-progress-meta {
    display: flex;

    justify-content: space-between;

    margin-top: 7px;

    color: #668174;

    font-size: 10px;
}


/* ============================================================
   ACTIVITY
============================================================ */

.activity-card {
    display: flex;

    align-items: flex-start;

    gap: 14px;

    min-height: 125px;

    padding: 18px;

    background:
        rgba(255,255,255,0.96);

    border: 1px solid var(--border);

    border-radius: 18px;

    box-shadow: var(--shadow-sm);

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}

.activity-card:hover {
    transform: translateY(-2px);

    box-shadow: var(--shadow-md);
}

.activity-icon {
    width: 42px;
    height: 42px;

    flex-shrink: 0;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 12px;

    font-size: 19px;
}

.activity-green {
    background: #e2f6e9;
}

.activity-blue {
    background: #e4f1fb;
}

.activity-purple {
    background: #eee9fb;
}

.activity-title {
    color: var(--text-secondary);

    font-size: 12px;

    font-weight: 600;
}

.activity-value {
    color: var(--text-main);

    font-size: 24px;

    font-weight: 800;

    margin-top: 3px;
}

.activity-description {
    color: var(--text-muted);

    font-size: 10px;

    line-height: 1.4;

    margin-top: 3px;
}


/* ============================================================
   WORKFLOW
============================================================ */

.workflow-card {
    position: relative;

    min-height: 145px;

    padding: 18px;

    background:
        rgba(255,255,255,0.96);

    border: 1px solid var(--border);

    border-radius: 17px;

    box-shadow: var(--shadow-sm);

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}

.workflow-card:hover {
    transform: translateY(-3px);

    box-shadow: var(--shadow-md);
}

.workflow-number {
    color: var(--green-600);

    font-size: 11px;

    font-weight: 800;

    margin-bottom: 25px;
}

.workflow-title {
    color: var(--text-main);

    font-size: 13px;

    font-weight: 800;
}

.workflow-description {
    color: var(--text-secondary);

    font-size: 10px;

    line-height: 1.4;

    margin-top: 5px;
}


/* ============================================================
   JOBS PAGE
============================================================ */

.jobs-page-header {
    display: flex;

    align-items: center;

    justify-content: space-between;

    gap: 30px;

    padding: 30px 32px;

    margin-bottom: 24px;

    border: 1px solid var(--border);

    border-radius: 24px;

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.98),
            #eaf7ef
        );

    box-shadow: var(--shadow-md);
}

.jobs-eyebrow {
    color: var(--green-600);

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 0.14em;

    margin-bottom: 7px;
}

.jobs-page-title {
    color: var(--text-main);

    font-size: 34px;

    font-weight: 800;

    line-height: 1.1;

    letter-spacing: -0.035em;
}

.jobs-page-subtitle {
    color: var(--text-secondary);

    font-size: 14px;

    line-height: 1.5;

    margin-top: 8px;
}

.jobs-header-icon {
    width: 60px;
    height: 60px;

    display: flex;

    align-items: center;

    justify-content: center;

    flex-shrink: 0;

    background: var(--green-100);

    border: 1px solid var(--green-200);

    border-radius: 18px;

    font-size: 28px;
}


/* ============================================================
   JOB STATISTICS
============================================================ */

.jobs-stat-section {
    margin-top: 8px;

    margin-bottom: 15px;
}

.jobs-stat-title {
    color: var(--text-main);

    font-size: 19px;

    font-weight: 800;
}

.jobs-stat-subtitle {
    color: var(--text-secondary);

    font-size: 12px;

    margin-top: 3px;
}

.jobs-stat-card {
    min-height: 135px;

    padding: 18px;

    background:
        rgba(255,255,255,0.97);

    border: 1px solid var(--border);

    border-radius: 18px;

    box-shadow: var(--shadow-sm);

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}

.jobs-stat-card:hover {
    transform: translateY(-2px);

    box-shadow: var(--shadow-md);
}

.jobs-stat-icon {
    width: 38px;
    height: 38px;

    display: flex;

    align-items: center;

    justify-content: center;

    background: var(--green-100);

    border-radius: 11px;

    font-size: 18px;

    margin-bottom: 13px;
}

.jobs-stat-label {
    color: var(--text-muted);

    font-size: 9px;

    font-weight: 800;

    letter-spacing: 0.1em;
}

.jobs-stat-value {
    color: var(--text-main);

    font-size: 27px;

    font-weight: 800;

    margin-top: 4px;
}

.jobs-stat-description {
    color: var(--text-secondary);

    font-size: 10px;

    margin-top: 4px;
}


/* ============================================================
   JOB LIST HEADER
============================================================ */

.jobs-list-header {
    margin-top: 32px;

    margin-bottom: 15px;
}

.jobs-section-title {
    color: var(--text-main);

    font-size: 22px;

    font-weight: 800;

    letter-spacing: -0.02em;
}

.jobs-section-description {
    color: var(--text-secondary);

    font-size: 12px;

    line-height: 1.5;

    margin-top: 4px;
}


/* ============================================================
   JOB CARD
============================================================ */

.job-card {
    padding: 22px;

    background:
        rgba(255,255,255,0.97);

    border: 1px solid var(--border);

    border-radius: 20px;

    box-shadow: var(--shadow-sm);

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease,
        border-color 0.2s ease;
}

.job-card:hover {
    transform: translateY(-2px);

    border-color: #b9dcc7;

    box-shadow: var(--shadow-md);
}

.job-card-top {
    display: flex;

    align-items: flex-start;

    justify-content: space-between;

    gap: 20px;
}

.job-card-eyebrow {
    color: var(--text-muted);

    font-size: 9px;

    font-weight: 800;

    letter-spacing: 0.1em;

    margin-bottom: 6px;
}

.job-card-title {
    color: var(--text-main);

    font-size: 21px;

    font-weight: 800;

    line-height: 1.2;

    letter-spacing: -0.02em;
}

.job-card-company {
    color: var(--text-secondary);

    font-size: 13px;

    margin-top: 5px;
}


/* ============================================================
   JOB & GENERAL STATUS BADGES
============================================================ */

.job-status,
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.06em;
    white-space: nowrap;
    text-transform: uppercase;
}

.status-open,
.status-active,
.status-success,
.status-processed,
.status-current {
    color: var(--semantic-success-dark) !important;
    background: var(--semantic-success-bg) !important;
    border: 1.5px solid var(--semantic-success-border) !important;
}

.status-draft,
.status-previous,
.status-archived,
.status-neutral {
    color: var(--semantic-neutral) !important;
    background: var(--semantic-neutral-bg) !important;
    border: 1.5px solid var(--semantic-neutral-border) !important;
}

.status-closed,
.status-failed,
.status-danger {
    color: var(--semantic-danger) !important;
    background: var(--semantic-danger-bg) !important;
    border: 1.5px solid var(--semantic-danger-border) !important;
}

.status-duplicate,
.status-warning,
.status-moderate {
    color: var(--semantic-warning-dark) !important;
    background: var(--semantic-warning-bg) !important;
    border: 1.5px solid var(--semantic-warning-border) !important;
}

.status-info,
.status-good {
    color: var(--semantic-info-dark) !important;
    background: var(--semantic-info-bg) !important;
    border: 1.5px solid var(--semantic-info-border) !important;
}


/* ============================================================
   JOB META
============================================================ */

.job-meta-grid {
    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 12px;

    margin-top: 22px;

    padding-top: 18px;

    border-top: 1px solid #edf2ee;
}

.job-meta-item {
    display: flex;

    align-items: center;

    gap: 9px;
}

.job-meta-item > span {
    width: 34px;
    height: 34px;

    display: flex;

    align-items: center;

    justify-content: center;

    background: #eaf7ef;

    border-radius: 10px;

    font-size: 15px;
}

.job-meta-item small {
    display: block;

    color: var(--text-muted);

    font-size: 9px;
}

.job-meta-item strong {
    display: block;

    color: #365347;

    font-size: 11px;

    margin-top: 2px;
}


/* ============================================================
   SKILLS
============================================================ */

.job-skills-section {
    margin-top: 17px;
}

.preferred-section {
    margin-top: 19px;
}

.job-card-label {
    color: #657a70;

    font-size: 10px;

    font-weight: 800;

    text-transform: uppercase;

    letter-spacing: 0.07em;

    margin-bottom: 9px;
}

.preferred-label {
    margin-top: 0;
}

.skill-pills {
    display: flex;

    flex-wrap: wrap;

    gap: 7px;
}

.skill-pill {
    display: inline-flex;

    align-items: center;

    padding: 6px 10px;

    border: 1px solid #cfe6d8;

    border-radius: 999px;

    background: #f1faf5;

    color: #287254;

    font-size: 10px;

    font-weight: 650;

    line-height: 1.2;
}

.preferred-pill {
    background: #eef6ff;

    border-color: #c4dff9;

    color: #1967b2;
}


/* ============================================================
   JOB SPACING
============================================================ */

.job-card-spacing {
    height: 16px;
}

.jobs-summary-divider {
    height: 1px;

    margin: 20px 0;

    background: var(--border);
}


/* ============================================================
   RESULTS
============================================================ */

.results-count {
    margin: 5px 0 14px 0;

    color: var(--text-secondary);

    font-size: 12px;
}

.results-count strong {
    color: var(--text-main);
}


/* ============================================================
   EMPTY STATE
============================================================ */

.empty-state {
    padding: 55px 25px;

    margin-top: 12px;

    border: 1px dashed #c8ded1;

    border-radius: 20px;

    background:
        rgba(248,252,249,0.9);

    text-align: center;
}

.empty-state-icon {
    font-size: 34px;

    margin-bottom: 10px;
}

.empty-state-title {
    color: #294b3d;

    font-size: 18px;

    font-weight: 800;
}

.empty-state-description {
    color: #809188;

    font-size: 12px;

    line-height: 1.5;

    margin-top: 5px;
}


/* ============================================================
   STREAMLIT DIALOG / MODAL ENHANCEMENT
============================================================ */

div[data-testid="stDialog"] > div[role="dialog"] {
    background: #ffffff !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 24px !important;
    box-shadow: var(--shadow-lg) !important;
    padding: 24px 28px !important;
    max-height: 90vh !important;
}

div[data-testid="stDialog"] > div[role="dialog"] h2 {
    color: var(--text-main) !important;
    font-size: 22px !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
}

div[data-testid="stDialog"] button[aria-label="Close"] {
    color: var(--text-secondary) !important;
    border-radius: 10px !important;
    transition: background 0.15s ease !important;
}

div[data-testid="stDialog"] button[aria-label="Close"]:hover {
    background: var(--green-100) !important;
    color: var(--text-main) !important;
}

/* ============================================================
   CREATE / EDIT JOB MODAL
============================================================ */

.modal-header {
    padding: 5px 0 20px 0;
}

.modal-eyebrow {
    color: var(--green-600);

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 0.13em;

    margin-bottom: 7px;
}

.modal-title {
    color: var(--text-main);

    font-size: 27px;

    font-weight: 800;

    line-height: 1.15;

    letter-spacing: -0.03em;
}

.modal-description {
    max-width: 680px;

    color: var(--text-secondary);

    font-size: 12px;

    line-height: 1.55;

    margin-top: 7px;
}

.creation-method-spacer {
    height: 5px;
}


/* ============================================================
   INPUT CARDS
============================================================ */

.input-card {
    padding: 22px;

    margin-bottom: 18px;

    border: 1px solid var(--border);

    border-radius: 18px;

    background:
        linear-gradient(
            135deg,
            #ffffff,
            #f2faf5
        );

    box-shadow: var(--shadow-sm);
}

.input-card-title {
    color: var(--text-main);

    font-size: 18px;

    font-weight: 800;
}

.input-card-description {
    color: var(--text-secondary);

    font-size: 12px;

    line-height: 1.5;

    margin-top: 5px;
}

.upload-input-card {
    text-align: center;
}

.upload-icon {
    width: 50px;
    height: 50px;

    display: flex;

    align-items: center;

    justify-content: center;

    margin: 0 auto 10px;

    background: var(--green-100);

    border-radius: 14px;

    font-size: 23px;
}

.selected-file {
    display: flex;

    align-items: center;

    gap: 12px;

    padding: 13px 15px;

    margin: 14px 0;

    border: 1px solid #cde5d6;

    border-radius: 13px;

    background: #f5fbf7;
}

.selected-file > span {
    font-size: 22px;
}

.selected-file strong {
    display: block;

    color: var(--text-main);

    font-size: 12px;
}

.selected-file small {
    display: block;

    color: var(--text-muted);

    font-size: 10px;

    margin-top: 2px;
}


/* ============================================================
   AI RESULT
============================================================ */

.ai-result-card {
    padding: 19px;

    margin-bottom: 15px;

    border: 1px solid #cfe8d8;

    border-radius: 18px;

    background:
        linear-gradient(
            135deg,
            #f7fcf9,
            #eaf7ef
        );
}

.ai-result-header {
    display: flex;

    align-items: center;

    justify-content: space-between;

    gap: 20px;
}

.ai-result-title {
    color: var(--text-main);

    font-size: 18px;

    font-weight: 800;
}

.ai-result-description {
    color: var(--text-secondary);

    font-size: 12px;

    margin-top: 4px;
}

.ai-badge {
    flex-shrink: 0;

    padding: 7px 11px;

    border: 1px solid #bfe2cc;

    border-radius: 999px;

    background: #ddf4e6;

    color: #11794d;

    font-size: 9px;

    font-weight: 800;
}

.ai-complete-banner {
    display: flex;

    align-items: center;

    gap: 11px;

    padding: 12px 14px;

    margin-bottom: 16px;

    border: 1px solid #c6e8d2;

    border-radius: 14px;

    background: #eaf8ef;
}

.ai-complete-banner > span {
    width: 28px;
    height: 28px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 50%;

    background: #bfe8cd;

    color: #087645;

    font-weight: 800;
}

.ai-complete-banner strong {
    display: block;

    color: #17643f;

    font-size: 12px;
}

.ai-complete-banner small {
    display: block;

    color: #6f8a7c;

    font-size: 10px;

    margin-top: 2px;
}


/* ============================================================
   FORM
============================================================ */

.form-section-label {
    margin: 20px 0 11px 0;

    padding-bottom: 7px;

    border-bottom: 1px solid #e1eee6;

    color: #3d5e4f;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 0.1em;

    text-transform: uppercase;
}

.form-action-row {
    height: 5px;
}


/* ============================================================
   STREAMLIT INPUTS
============================================================ */

div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div,
div[data-baseweb="select"] > div {
    background: #ffffff;

    border: 1px solid #d1e5d8;

    border-radius: 12px;

    transition:
        border-color 0.2s ease,
        box-shadow 0.2s ease;
}

div[data-baseweb="input"] > div:focus-within,
div[data-baseweb="textarea"] > div:focus-within,
div[data-baseweb="select"] > div:focus-within {
    border-color: var(--green-500);

    box-shadow:
        0 0 0 3px
        rgba(25,168,107,0.10);
}

textarea {
    line-height: 1.55 !important;
}

[data-testid="stTextArea"] label {
    margin-bottom: 5px;
}

[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label {
    margin-bottom: 4px;
}


/* ============================================================
   FILE UPLOADER
============================================================ */

[data-testid="stFileUploader"] section {
    background: #f7fcf9;

    border: 1px dashed #abd6ba;

    border-radius: 16px;

    padding: 15px;
}


/* ============================================================
   BUTTONS - GLOBAL SEMANTIC HIERARCHY
============================================================ */

/* 1. DEFAULT / SECONDARY BUTTONS */
div.stButton > button,
div[data-testid="stFormSubmitButton"] > button {
    min-height: 40px;
    border-radius: 12px;
    border: 1.5px solid var(--border-main);
    background: #ffffff;
    color: var(--text-main);
    font-family: "Manrope", "Inter", sans-serif;
    font-weight: 700;
    font-size: 13px;
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease, background 0.18s ease, color 0.18s ease;
}

div.stButton > button:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-1px);
    border-color: var(--primary-green);
    color: var(--primary-green);
    box-shadow: 0 4px 14px rgba(24, 165, 107, 0.12);
}

/* 2. PRIMARY ACTION BUTTONS (GREEN)
   Create Job, Process Resumes, Run Matching, Save Changes, etc. */
div.stButton > button[kind="primary"],
div[data-testid="stFormSubmitButton"] > button[kind="primary"] {
    border: none !important;
    color: #ffffff !important;
    background: linear-gradient(135deg, #18A56B 0%, #128A58 100%) !important;
    box-shadow: 0 6px 18px rgba(24, 165, 107, 0.22) !important;
}

div.stButton > button[kind="primary"]:hover,
div[data-testid="stFormSubmitButton"] > button[kind="primary"]:hover {
    color: #ffffff !important;
    transform: translateY(-1px) !important;
    background: linear-gradient(135deg, #1cb676 0%, #0f784c 100%) !important;
    box-shadow: 0 10px 24px rgba(24, 165, 107, 0.30) !important;
}

/* 3. VIEW / PROFILE ACTIONS (BLUE)
   View Profile, View Candidate, Open Profile */
div[class*="st-key-view_"] button,
div[class*="st-key-candidate_profile_"] button {
    background: #2383D9 !important;
    border: 1.5px solid #1C75C5 !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 14px rgba(35, 131, 217, 0.20) !important;
}

div[class*="st-key-view_"] button:hover,
div[class*="st-key-candidate_profile_"] button:hover {
    background: #1C75C5 !important;
    border-color: #1565AB !important;
    color: #FFFFFF !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 20px rgba(35, 131, 217, 0.28) !important;
}

/* 4. EDIT ACTIONS (LIGHT BLUE)
   Edit Job, Edit Candidate, Edit Details */
div[class*="st-key-edit_"] button {
    background: #EEF6FF !important;
    border: 1.5px solid #BBD8F6 !important;
    color: #1967B2 !important;
    font-weight: 700 !important;
}

div[class*="st-key-edit_"] button:hover {
    background: #DDECFC !important;
    border-color: #2383D9 !important;
    color: #0F5394 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(35, 131, 217, 0.16) !important;
}

/* 5. DELETE ACTIONS (SOFT RED)
   Delete Job, Delete Resume, Remove */
div[class*="st-key-del_"] button,
div[class*="st-key-delete_"] button {
    background: #FFF1F1 !important;
    border: 1.5px solid #F5C6C6 !important;
    color: #D94B4B !important;
    font-weight: 700 !important;
}

div[class*="st-key-del_"] button:hover,
div[class*="st-key-delete_"] button:hover {
    background: #FEE4E4 !important;
    border-color: #D94B4B !important;
    color: #B92E2E !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(217, 75, 75, 0.18) !important;
}

/* 6. DESTRUCTIVE CONFIRM DELETE BUTTON (STRONG RED) */
div[class*="st-key-dlg_confirm_del_"] button {
    background: linear-gradient(135deg, #D94B4B 0%, #B92E2E 100%) !important;
    border: none !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    box-shadow: 0 6px 18px rgba(217, 75, 75, 0.25) !important;
}

div[class*="st-key-dlg_confirm_del_"] button:hover {
    background: linear-gradient(135deg, #C73838 0%, #A32020 100%) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 10px 24px rgba(217, 75, 75, 0.32) !important;
}

/* 7. CANCEL / CLOSE / NEUTRAL BUTTONS (NEUTRAL GRAY)
   Cancel, Close Profile, Clear Results, Back */
div[class*="st-key-dlg_cancel_"] button,
div[class*="st-key-dlg_close_"] button,
div[class*="st-key-cancel_"] button,
div[class*="st-key-close_"] button,
div[class*="st-key-neutral_"] button {
    background: #F4F6F8 !important;
    border: 1.5px solid #CBD5E1 !important;
    color: #475569 !important;
    font-weight: 700 !important;
}

div[class*="st-key-dlg_cancel_"] button:hover,
div[class*="st-key-dlg_close_"] button:hover,
div[class*="st-key-cancel_"] button:hover,
div[class*="st-key-close_"] button:hover,
div[class*="st-key-neutral_"] button:hover {
    background: #E2E8F0 !important;
    border-color: #94A3B8 !important;
    color: #1E293B !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(100, 116, 139, 0.12) !important;
}


/*
   Streamlit does not expose button keys as CSS attributes
   consistently across versions. The following nth-child
   fallback keeps the action buttons visually distinct
   without affecting primary buttons.
*/

.delete-confirmation {
    display: flex;

    flex-direction: column;

    gap: 3px;

    margin-top: 10px;

    padding: 12px 14px;

    border: 1px solid var(--danger-border);

    border-radius: 12px;

    background: var(--danger-bg);

    color: var(--danger);
}

.delete-confirmation strong {
    font-size: 12px;
}

.delete-confirmation span {
    font-size: 10px;

    color: #9c6b6b;
}


/* ============================================================
   EXPANDERS
============================================================ */

[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;

    border-radius: 14px !important;

    background:
        rgba(255,255,255,0.72) !important;
}

[data-testid="stExpander"] summary {
    color: var(--text-main) !important;

    font-weight: 700 !important;
}


/* ============================================================
   ALERTS
============================================================ */

div[data-testid="stAlert"] {
    border-radius: 14px;

    border-width: 1px;
}


/* ============================================================
   PAGINATION
============================================================ */

.pagination-label {
    padding: 10px;

    color: var(--text-secondary);

    font-size: 12px;

    text-align: center;
}


/* ============================================================
   EDIT JOB
============================================================ */

.edit-job-header {
    padding: 20px 22px;

    margin: 25px 0 18px;

    border: 1px solid var(--border);

    border-radius: 18px;

    background:
        linear-gradient(
            135deg,
            #ffffff,
            #eef9f3
        );
}


/* ============================================================
   EMPTY DASHBOARD
============================================================ */

.dashboard-empty-state {
    text-align: center;

    padding: 45px 20px;

    background:
        rgba(255,255,255,0.95);

    border: 1px dashed #b9dcc7;

    border-radius: 20px;
}

.dashboard-empty-icon {
    font-size: 32px;
}

.dashboard-empty-title {
    color: var(--text-main);

    font-size: 17px;

    font-weight: 800;

    margin-top: 8px;
}

.dashboard-empty-description {
    max-width: 550px;

    margin: 7px auto 0;

    color: var(--text-secondary);

    font-size: 12px;

    line-height: 1.5;
}


/* ============================================================
   RESPONSIBLE AI
============================================================ */

.dashboard-ai-note {
    display: flex;

    align-items: flex-start;

    gap: 14px;

    margin-top: 30px;

    padding: 18px 20px;

    background:
        linear-gradient(
            135deg,
            #effaf3,
            #e6f6ec
        );

    border: 1px solid #d2eadb;

    border-radius: 18px;
}

.dashboard-ai-note-icon {
    font-size: 22px;
}

.dashboard-ai-note-title {
    color: #176545;

    font-size: 13px;

    font-weight: 800;
}

.dashboard-ai-note-text {
    color: var(--text-secondary);

    font-size: 11px;

    line-height: 1.5;

    margin-top: 4px;
}


/* ============================================================
   SCROLLBAR
============================================================ */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #eef7f1;
}

::-webkit-scrollbar-thumb {
    background: #b9d9c5;

    border-radius: 999px;
}

::-webkit-scrollbar-thumb:hover {
    background: #8fc5a4;
}


/* ============================================================
   HIDE DEFAULT STREAMLIT UI
============================================================ */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* ============================================================
   RESPONSIVE
============================================================ */

/* ============================================================
   RESUME PAGE
============================================================ */

.resume-page-header {
    display: flex;

    align-items: flex-start;

    justify-content: space-between;

    gap: 24px;

    padding: 30px 32px;

    margin-bottom: 30px;

    border: 1px solid #d8e9df;

    border-radius: 22px;

    background:
        radial-gradient(
            circle at 90% 20%,
            rgba(84, 201, 137, 0.14),
            transparent 32%
        ),
        #ffffff;

    box-shadow:
        0 10px 32px
        rgba(20, 90, 58, 0.06);
}


    /* ---------------------------------------------------------
    Header
    --------------------------------------------------------- */

    .resume-eyebrow {
        color: #0f965d;

        font-size: 11px;
        font-weight: 800;

        letter-spacing: 1.5px;

        margin-bottom: 7px;
    }


    .resume-page-title {
        color: #14382b;

        font-size: 32px;
        line-height: 1.1;

        font-weight: 800;

        letter-spacing: -1.2px;
    }


    .resume-page-subtitle {
        color: #6b8177;

        font-size: 14px;
        line-height: 1.55;

        margin-top: 9px;

        max-width: 700px;
    }


    .resume-header-badge {
        display: inline-flex;

        align-items: center;
        gap: 7px;

        flex-shrink: 0;

        padding: 9px 14px;

        border: 1px solid #bfe7ce;
        border-radius: 999px;

        background: #e8f8ee;

        color: #087a4b;

        font-size: 12px;
        font-weight: 700;
    }


    .resume-online-dot {
        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: #18a86b;

        display: inline-block;
    }


    /* ---------------------------------------------------------
    Section headings
    --------------------------------------------------------- */

    .resume-section-heading {
        display: flex;

        align-items: center;
        justify-content: space-between;

        margin: 28px 0 12px;
    }


    .resume-section-title {
        color: #14382b;

        font-size: 18px;

        font-weight: 800;

        letter-spacing: -0.3px;
    }


    .resume-section-subtitle {
        color: #71867c;

        font-size: 12px;

        margin-top: 3px;
    }


    .repository-heading {
        margin-top: 36px;
    }


    /* ---------------------------------------------------------
    Upload
    --------------------------------------------------------- */

    .resume-upload-summary {
        display: flex;

        justify-content: space-between;

        gap: 16px;

        margin-top: 12px;

        padding: 12px 14px;

        border: 1px solid #d8e9df;

        border-radius: 12px;

        background: #f5fbf7;

        color: #466257;

        font-size: 12px;
    }


    /* ---------------------------------------------------------
    Statistics
    --------------------------------------------------------- */

    .resume-stat-card {
        min-height: 125px;

        padding: 18px;

        border: 1px solid #d8e9df;

        border-radius: 17px;

        background: #ffffff;

        box-shadow:
            0 7px 22px
            rgba(20, 90, 58, 0.045);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }


    .resume-stat-card:hover {
        transform: translateY(-2px);

        box-shadow:
            0 12px 28px
            rgba(20, 90, 58, 0.09);
    }


    .resume-stat-icon {
        width: 36px;
        height: 36px;

        display: flex;

        align-items: center;
        justify-content: center;

        border-radius: 11px;

        background: #e4f7eb;

        font-size: 16px;

        margin-bottom: 11px;
    }


    .resume-stat-label {
        color: #71867c;

        font-size: 12px;

        font-weight: 650;
    }


    .resume-stat-value {
        color: #14382b;

        font-size: 27px;

        font-weight: 800;

        line-height: 1.1;

        margin-top: 4px;
    }


    /* ---------------------------------------------------------
    Processing result
    --------------------------------------------------------- */

    .resume-result-card {
        padding: 15px 16px;

        margin-top: 10px;

        border: 1px solid #d8e9df;

        border-radius: 15px;

        background: #ffffff;
    }


    .resume-result-top {
        display: flex;

        align-items: center;

        gap: 12px;
    }


    .resume-file-icon {
        width: 40px;
        height: 40px;

        display: flex;

        align-items: center;
        justify-content: center;

        flex-shrink: 0;

        border-radius: 11px;

        background: #e8f8ee;
    }


    .resume-result-main {
        flex: 1;

        min-width: 0;
    }


    .resume-result-title {
        color: #14382b;

        font-size: 13px;

        font-weight: 750;

        overflow-wrap: anywhere;
    }


    .resume-result-meta {
        color: #71867c;

        font-size: 11px;

        margin-top: 3px;
    }


    /* ---------------------------------------------------------
    Status badges
    --------------------------------------------------------- */

    .resume-badge-success,
    .resume-badge-warning,
    .resume-badge-danger {
        flex-shrink: 0;

        padding: 6px 10px;

        border-radius: 999px;

        font-size: 10px;

        font-weight: 750;
    }


    .resume-badge-success {
        color: #11794d;

        background: #eaf7f0;

        border: 1px solid #bfe5cc;
    }


    .resume-badge-warning {
        color: #9c6c0c;

        background: #fef9ee;

        border: 1px solid #f9de9b;
    }


    .resume-badge-danger {
        color: #b33939;

        background: #fdf2f2;

        border: 1px solid #f8c8c8;
    }


    /* ---------------------------------------------------------
    Candidate cards
    --------------------------------------------------------- */

    .candidate-card-name {
        color: #14382b;

        font-size: 14px;

        font-weight: 750;
    }


    .resume-history-row {
        display: flex;

        align-items: center;

        flex-wrap: wrap;

        gap: 9px;

        padding: 10px 0;

        border-bottom: 1px solid #e7f0ea;

        color: #526b60;

        font-size: 11px;
    }


    .resume-history-row strong {
        color: #14382b;

        margin-right: auto;
    }


    /* ---------------------------------------------------------
    Streamlit file uploader
    --------------------------------------------------------- */

    [data-testid="stFileUploader"] section {
        background: #f7fcf9 !important;

        border: 1px dashed #9fd5b5 !important;

        border-radius: 16px !important;

        padding: 22px !important;

        transition:
            border-color 0.2s ease,
            background 0.2s ease;
    }


    [data-testid="stFileUploader"] section:hover {
        border-color: #18a86b !important;

        background: #f1faf5 !important;
    }


    /* ---------------------------------------------------------
    Resume page buttons
    --------------------------------------------------------- */

    div.stButton > button {
        border-radius: 11px;

        font-weight: 650;

        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease;
    }


    div.stButton > button:hover {
        transform: translateY(-1px);
    }


    /* Primary process button */

    div.stButton > button[kind="primary"] {
        background:
            linear-gradient(
                135deg,
                #19a86d,
                #128a58
            );

        color: #ffffff;

        border: none;

        box-shadow:
            0 7px 18px
            rgba(24, 165, 107, 0.20);
    }


    div.stButton > button[kind="primary"]:hover {
        background:
            linear-gradient(
                135deg,
                #20b877,
                #0f8152
            );

        box-shadow:
            0 10px 24px
            rgba(24, 165, 107, 0.27);
    }


    /* ---------------------------------------------------------
    Inputs
    --------------------------------------------------------- */

    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div,
    div[data-baseweb="select"] > div {
        border-radius: 12px !important;

        border-color: #d1e5d8 !important;

        background: #ffffff !important;
    }


    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="textarea"] > div:focus-within,
    div[data-baseweb="select"] > div:focus-within {
        border-color: #18a56b !important;

        box-shadow:
            0 0 0 3px
            rgba(24, 165, 107, 0.10) !important;
    }


    @media (max-width: 800px) {

        .resume-page-header {
            flex-direction: column;
        }

        .resume-upload-summary {
            flex-direction: column;
        }

        .resume-result-top {
            align-items: flex-start;
        }

        .resume-badge-success,
        .resume-badge-warning,
        .resume-badge-danger {
            display: none;
        }
    }


/* ============================================================
   STREAMLIT CONTAINER & BLOCK STYLING
============================================================ */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff !important;
    border: 1.5px solid #c8e2d2 !important;
    border-radius: 20px !important;
    padding: 22px 24px !important;
    box-shadow: 0 4px 18px rgba(18, 92, 58, 0.06) !important;
    margin-bottom: 20px !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: #9fd4b6 !important;
    box-shadow: 0 8px 28px rgba(18, 92, 58, 0.10) !important;
}

/* Colored icon containers */
.icon-box {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 11px;
    font-size: 16px;
    flex-shrink: 0;
}

.icon-box-blue {
    background: #edf5fd;
    border: 1px solid #c8e1f8;
    color: #1976d2;
}

.icon-box-green {
    background: #eaf7ef;
    border: 1px solid #bfe5cc;
    color: #128a58;
}

.icon-box-amber {
    background: #fef8eb;
    border: 1px solid #f5dfb2;
    color: #b06a00;
}

.icon-box-purple {
    background: #f4f0fd;
    border: 1px solid #d8cbf7;
    color: #6941c6;
}

.icon-box-slate {
    background: #f0f4f8;
    border: 1px solid #d3dfea;
    color: #475569;
}

.icon-box-red {
    background: #fdf2f2;
    border: 1px solid #f8c8c8;
    color: #d94b4b;
}


/* ============================================================
   CANDIDATE INTELLIGENCE / REPOSITORY
============================================================ */

.candidates-page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    padding: 30px 32px;
    margin-bottom: 24px;
    border: 1.5px solid var(--border);
    border-radius: 24px;
    background: linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.98),
        #eaf7ef
    );
    box-shadow: var(--shadow-md);
}

.candidates-eyebrow {
    color: var(--green-600);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.14em;
    margin-bottom: 7px;
}

.candidates-page-title {
    color: var(--text-main);
    font-size: 34px;
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.035em;
}

.candidates-page-subtitle {
    color: var(--text-secondary);
    font-size: 14px;
    line-height: 1.5;
    margin-top: 8px;
}

.candidates-header-icon {
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    background: var(--green-100);
    border: 1.5px solid var(--green-200);
    border-radius: 18px;
    font-size: 28px;
}

.candidate-card {
    padding: 22px 24px;
    background: #ffffff;
    border: 1.5px solid var(--border);
    border-radius: 20px;
    box-shadow: var(--shadow-sm);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    margin-bottom: 20px;
}

.candidate-card:hover {
    transform: translateY(-2px);
    border-color: #98d4b0;
    box-shadow: var(--shadow-md);
}

.candidate-card-top {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 16px;
    padding-bottom: 14px;
    border-bottom: 1px solid #edf5ee;
}

.candidate-card-name {
    color: var(--text-main);
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.02em;
    display: flex;
    align-items: center;
    gap: 8px;
}

.candidate-meta-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-top: 14px;
}

.candidate-meta-item {
    display: flex;
    align-items: center;
    gap: 10px;
}

.candidate-meta-item small {
    display: block;
    color: var(--text-muted);
    font-size: 10px;
    font-weight: 750;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.candidate-meta-item strong {
    display: block;
    color: var(--text-main);
    font-size: 13px;
    font-weight: 700;
    margin-top: 2px;
    word-break: break-word;
}

.candidate-card-action-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 14px;
    margin-top: 14px;
    border-top: 1px dashed #dcefe3;
}

.candidate-profile-panel {
    background: linear-gradient(135deg, #ffffff 0%, #f4fbf7 100%);
    border: 1.5px solid var(--border);
    border-radius: 22px;
    padding: 28px;
    box-shadow: var(--shadow-md);
    margin-bottom: 26px;
}

.candidate-profile-hero {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    padding-bottom: 22px;
    border-bottom: 1.5px solid #edf5ee;
    margin-bottom: 22px;
}

.candidate-profile-avatar {
    width: 64px;
    height: 64px;
    border-radius: 20px;
    background: linear-gradient(135deg, #e4f7eb, #c3e8d2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    border: 1.5px solid #bce4cc;
    flex-shrink: 0;
}

.profile-group-card {
    background: #ffffff;
    border: 1.5px solid var(--border);
    border-radius: 20px;
    padding: 22px 24px;
    margin-bottom: 22px;
    box-shadow: var(--shadow-sm);
}

.profile-group-header {
    font-size: 16px;
    font-weight: 800;
    color: var(--text-main);
    display: flex;
    align-items: center;
    gap: 10px;
    padding-bottom: 12px;
    border-bottom: 1.5px solid #edf5ee;
    margin-bottom: 16px;
}

.profile-pill-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.profile-pill {
    display: inline-flex;
    align-items: center;
    padding: 7px 15px;
    border: 1.5px solid #bce5cb;
    border-radius: 999px;
    background: #edf8f2;
    color: #136c46;
    font-size: 12px;
    font-weight: 750;
    transition: all 0.15s ease;
}

.profile-pill:hover {
    border-color: #18a56b;
    background: #e3f6eb;
}

.profile-list-item {
    padding: 12px 16px;
    background: #f7fbf9;
    border: 1px solid #dcefe3;
    border-radius: 12px;
    margin-bottom: 10px;
    font-size: 13px;
    color: var(--text-main);
    display: flex;
    align-items: center;
    gap: 12px;
}

.resume-history-card {
    padding: 16px 20px;
    background: #ffffff;
    border: 1.5px solid var(--border);
    border-radius: 16px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 14px;
    box-shadow: 0 2px 10px rgba(18, 92, 58, 0.04);
}


/* ============================================================
   AI MATCHING MODULE
============================================================ */

.matching-page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    padding: 30px 32px;
    margin-bottom: 24px;
    border: 1.5px solid var(--border);
    border-radius: 24px;
    background: linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.98),
        #eaf7ef
    );
    box-shadow: var(--shadow-md);
}

.matching-eyebrow {
    color: var(--green-600);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.14em;
    margin-bottom: 7px;
}

.matching-page-title {
    color: var(--text-main);
    font-size: 34px;
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.035em;
}

.matching-page-subtitle {
    color: var(--text-secondary);
    font-size: 14px;
    line-height: 1.5;
    margin-top: 8px;
}

.matching-header-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 9px 16px;
    background: #e3f7eb;
    border: 1.5px solid #bfe5cd;
    border-radius: 999px;
    color: #16704a;
    font-size: 12px;
    font-weight: 750;
    flex-shrink: 0;
}

.job-preview-panel {
    background: linear-gradient(135deg, #ffffff 0%, #f6fbf8 100%);
    border: 1.5px solid var(--border);
    border-radius: 22px;
    padding: 26px 28px;
    box-shadow: var(--shadow-sm);
    margin-bottom: 24px;
}

.job-preview-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 16px;
    padding-bottom: 16px;
    border-bottom: 1.5px solid #edf5ee;
    margin-bottom: 16px;
}

.job-preview-title {
    color: var(--text-main);
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.02em;
}

.job-preview-company {
    color: var(--text-secondary);
    font-size: 13px;
    margin-top: 4px;
}

.match-summary-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 14px;
    margin: 20px 0 28px 0;
}

.match-summary-card {
    background: #ffffff;
    border: 1.5px solid var(--border);
    border-radius: 18px;
    padding: 18px 16px;
    text-align: center;
    box-shadow: var(--shadow-sm);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.match-summary-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.summary-analyzed {
    border-top: 4px solid #64748b;
    background: #f8fafc;
}

.summary-strong {
    border-top: 4px solid #18a56b;
    background: #eaf7f0;
}

.summary-good {
    border-top: 4px solid #2383d9;
    background: #eef6ff;
}

.summary-moderate {
    border-top: 4px solid #c98200;
    background: #fef9ee;
}

.summary-low {
    border-top: 4px solid #d94b4b;
    background: #fdf2f2;
}

.match-summary-val {
    font-size: 28px;
    font-weight: 800;
    line-height: 1.1;
    margin-top: 4px;
}

.match-summary-lbl {
    font-size: 10px;
    font-weight: 750;
    color: var(--text-secondary);
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.match-card {
    background: #ffffff;
    border: 1.5px solid #c5dfd0;
    border-radius: 24px;
    padding: 26px 28px;
    box-shadow: var(--shadow-sm);
    margin-bottom: 26px;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.match-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
    border-color: #98d4b0;
}

.match-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    flex-wrap: wrap;
    padding-bottom: 16px;
    border-bottom: 1.5px solid #edf5ee;
    margin-bottom: 16px;
}

.match-card-candidate {
    display: flex;
    align-items: center;
    gap: 14px;
}

.match-rank-badge {
    width: 38px;
    height: 38px;
    border-radius: 12px;
    background: #eaf7ef;
    color: var(--green-600);
    font-weight: 800;
    font-size: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1.5px solid #cce8d7;
    flex-shrink: 0;
}

.match-score-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.04em;
}

.badge-strong {
    background: #dcf5e7;
    color: #0e7747;
    border: 1.5px solid #9edab5;
}

.badge-good {
    background: #e4f1fd;
    color: #116cb0;
    border: 1.5px solid #aed6f8;
}

.badge-moderate {
    background: #fdf4e0;
    color: #946104;
    border: 1.5px solid #edd393;
}

.badge-low {
    background: #fde7e7;
    color: #b32c2c;
    border: 1.5px solid #f2b3b3;
}

.match-contact-bar {
    background: #f7fbf9;
    border: 1px solid #dcefe3;
    border-radius: 14px;
    padding: 10px 16px;
    margin-bottom: 18px;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 12px;
}

.match-dimension-container {
    background: #f7fbf9;
    border: 1.5px solid #d4eadc;
    border-radius: 18px;
    padding: 18px 20px;
    margin: 18px 0;
}

.dimension-header {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: var(--text-secondary);
    text-transform: uppercase;
    margin-bottom: 12px;
}

.score-bars-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
}

.score-bar-box {
    background: #ffffff;
    border: 1.5px solid #cce5d6;
    border-radius: 14px;
    padding: 14px 16px;
    box-shadow: 0 2px 10px rgba(18, 92, 58, 0.04);
}

.score-bar-lbl {
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    font-weight: 750;
    color: #4a685b;
    margin-bottom: 8px;
    text-transform: uppercase;
}

.score-bar-track {
    width: 100%;
    height: 7px;
    background: #d8eada;
    border-radius: 999px;
    overflow: hidden;
}

.score-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #18a96b, #3cc270);
}

.contact-pill-row {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 10px;
    font-size: 12px;
}

.contact-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    background: #ffffff;
    border: 1px solid #cce5d6;
    border-radius: 10px;
    color: #175438;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.15s ease;
}

.contact-pill:hover {
    border-color: #18a56b;
    background: #f1faf5;
    color: #11794d;
}

.reasons-list {
    margin-top: 18px;
    padding: 16px 20px;
    background: #f1f9f4;
    border: 1.5px solid #bfe4cb;
    border-radius: 16px;
}

.reason-bullet {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    font-size: 12px;
    color: #145336;
    line-height: 1.6;
    margin-bottom: 6px;
}

.reason-bullet:last-child {
    margin-bottom: 0;
}

.warning-bullet {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    font-size: 12px;
    color: #8c4d0a;
    line-height: 1.6;
    margin-top: 10px;
    background: #fef8ed;
    border: 1.5px solid #f5dfb2;
    border-radius: 14px;
    padding: 12px 16px;
}

/* Resume upload workspace */
.resume-upload-workspace {
    background: linear-gradient(135deg, #ffffff 0%, #f7fbf9 100%);
    border: 1.5px solid var(--border);
    border-radius: 22px;
    padding: 26px 28px;
    box-shadow: var(--shadow-sm);
    margin-bottom: 26px;
}

.stat-card-total {
    border-top: 4px solid #587469 !important;
}

.stat-card-success {
    border-top: 4px solid #18a86b !important;
    background: #f3faf6 !important;
}

.stat-card-warning {
    border-top: 4px solid #b06a00 !important;
    background: #fefbf3 !important;
}

.stat-card-danger {
    border-top: 4px solid #c94b4b !important;
    background: #fef4f4 !important;
}

@media (max-width: 900px) {
    .candidate-meta-grid {
        grid-template-columns: 1fr;
    }
    .score-bars-grid {
        grid-template-columns: 1fr 1fr;
    }
    .match-summary-grid {
        grid-template-columns: 1fr 1fr;
    }
}

</style>
        """,
        unsafe_allow_html=True,
    )
