import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

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

    st.subheader("Conversion by experiment group")

    fig, ax = plt.subplots(figsize=(7, 3.5))

    rates = [
        overall["control_conversion_pct"],
        overall["treatment_conversion_pct"],
    ]

    bars = ax.bar(
        ["Control", "Treatment"],
        rates,
        color=["#94A3B8", "#2563EB"],
        width=0.5,
    )

    ax.bar_label(
        bars,
        labels=[f"{rate:.4f}%" for rate in rates],
        padding=5,
    )
    ax.set_ylabel("Conversion rate (%)")
    ax.set_ylim(0, max(rates) * 1.25)
    ax.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
elif section == "Uplift Modeling":
    results_path = (
        Path(__file__).parent / "data" / "experiment_results.csv"
    )
    results = pd.read_csv(results_path)
    top = results.loc[
        results["segment"] == "Top 10% predicted uplift"
    ].iloc[0]

    st.subheader("Who benefits most from treatment?")

    st.write(
        "A T-learner estimates conversion probability under treatment "
        "and under control. The difference is the predicted uplift. "
        "Users in the test set were ranked by this score, and the "
        "highest-scoring 10% were evaluated as a group."
    )

    col1, col2 = st.columns(2)
    col1.metric(
        "Top 10%: control conversion",
        f"{top['control_conversion_pct']:.4f}%",
    )
    col2.metric(
        "Top 10%: treatment conversion",
        f"{top['treatment_conversion_pct']:.4f}%",
    )

    st.metric(
        "Estimated treatment effect in this group",
        f"{top['lift_pp']:+.4f} percentage points",
    )

    st.write(
        f"**95% confidence interval:** "
        f"{top['ci_lower_pp']:+.4f} to "
        f"{top['ci_upper_pp']:+.4f} percentage points."
    )

    st.write(
        "**Interpretation:** The estimated effect corresponds to about "
        "8.2 additional conversions per 1,000 treated users in this "
        "selected group."
    )

    st.write(
        "**Business implication:** This group is a candidate for "
        "targeted advertising. Profitability and whether targeting "
        "outperforms broader deployment still require evaluation."
    )

    st.caption(
        "The top 10% refers to predicted uplift rank, not a 10% "
        "conversion probability. Effects are estimated for the group; "
        "individual treatment effects are not directly observed."
    )

else:
    st.info("Report content will be added after the app setup is verified.")

st.caption(
    "GA4 and Criteo are separate datasets. "
    "The Criteo experiment does not test changes to the GA4 store."
)
