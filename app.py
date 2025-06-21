import streamlit as st

##--- Title ---
st.set_page_config(
    page_title="EMoNA Energy Monitoring & Analysis",
    page_icon=":material/dashboard:",
    layout="wide",
)

##--- PAGE SETUP ---
main_page = st.Page(
    page="pages/main.py",
    title="Home",
    icon="🏡",
    default=True,
)

report_page = st.Page(
    page="pages/reports.py",
    title="Reports",
    icon=":material/analytics:",
)

statistic_page = st.Page(
    page="pages/analysis/statistics.py",
    title="Statistics",
    icon="📈",
)

prediction_page = st.Page(
    page="pages/analysis/predictions.py",
    title="Machine Learning",
    icon="📊",
)

feedmill_motor_page = st.Page(
    page="pages/machines/feedmillmotors.py",
    title="Feed Mill Motors",
    icon=":material/manufacturing:",
)

compressor_page = st.Page(
    page="pages/machines/compressors.py",
    title="Compressors",
    icon=":material/multicooker:",
)

group_pages = {
    "🎛️ PT Central Panganpertiwi": [main_page],
    "🖥️ Live Tracking": [feedmill_motor_page, compressor_page],
    "📝 Reports & Analysis": [statistic_page, prediction_page],
}

pg = st.navigation(group_pages)

##--- SHARED ON ALL PAGES ---
st.logo("assets/g27.png")

##--- RUN NAVIGATION ---
pg.run()


st.sidebar.caption("EMoNA is a product of ©️ NetraMVA", unsafe_allow_html=True)
