import streamlit as st
import pandas as pd
from pathlib import Path

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
if section == "Experiment Results":
    results_path = (
        Path(__file__).parent / "data" / "experiment_results.csv"
    )
    results = pd.read_csv(results_path)
    overall = results.loc[results["segment"] == "Overall"].iloc[0]

    st.subheader("Did advertising increase conversion?")

    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Control conversion",
        f"{overall['control_conversion_pct']:.4f}%",
    )
    col2.metric(
        "Treatment conversion",
        f"{overall['treatment_conversion_pct']:.4f}%",
    )
    col3.metric(
        "Absolute lift",
        f"{overall['lift_pp']:+.4f} percentage points",
    )

    st.write(
        f"**95% confidence interval:** "
        f"{overall['ci_lower_pp']:+.4f} to "
        f"{overall['ci_upper_pp']:+.4f} percentage points."
    )

    st.write(
        "The estimated overall effect is positive, and the confidence "
        "interval excludes zero. A rollout decision also requires "
        "advertising costs and the value of incremental conversions."
    )

    st.caption(
        "Source: completed Criteo analysis. Displayed values are rounded. "
        "Segment results will be covered under Uplift Modeling."
    )
else:
    st.info("Report content will be added after the app setup is verified.")

st.caption(
    "GA4 and Criteo are separate datasets. "
    "The Criteo experiment does not test changes to the GA4 store."
)
