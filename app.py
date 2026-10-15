import streamlit as st

st.set_page_config(
    page_title="E-commerce Product Analytics",
    page_icon="📊",
    layout="wide",
)

st.title("E-commerce Product Analytics & Experimentation")
st.write(
    "Exploring shopping behavior with GA4 data and "
    "advertising treatment effects with Criteo data."
)

section = st.sidebar.radio(
    "Report sections",
    [
        "Overview",
        "Product Analytics",
        "Experiment Design",
        "Experiment Results",
        "Uplift Modeling",
    ],
)

st.header(section)
st.info("Report content will be added after the app setup is verified.")

st.caption(
    "GA4 and Criteo are separate datasets. "
    "The Criteo experiment does not test changes to the GA4 store."
)
