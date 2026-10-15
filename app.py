import streamlit as st

from shared.styling import apply_style
from views import (
    experiment_design,
    experiment_results,
    overview,
    product_analytics,
    uplift_modeling,
)


st.set_page_config(
    page_title="E-commerce Product Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_style()

PAGES = {
    "Overview": overview.render,
    "Product Analytics": product_analytics.render,
    "Experiment Design": experiment_design.render,
    "Experiment Results": experiment_results.render,
    "Uplift Modeling": uplift_modeling.render,
}

with st.sidebar:
    st.markdown("### E-commerce Insights")
    st.caption("Product analytics & experimentation")

    section = st.radio(
        "Explore the report",
        list(PAGES),
        key="main_navigation",
    )

    st.divider()
    st.caption("By Forough · Independent portfolio project")
    st.caption("SQL / BigQuery · Python · Streamlit")

PAGES[section]()

st.divider()
st.caption(
    "GA4 and Criteo are independent datasets. "
    "The Criteo advertising analysis does not evaluate "
    "the proposed GA4 product-page change."
)
