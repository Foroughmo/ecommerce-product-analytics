import pandas as pd
import streamlit as st

from shared.data import load_experiment_results
from shared.styling import page_header, takeaway


def render():
    page_header(
        title="Can we identify users more responsive to advertising?",
        subtitle="Uplift modeling to prioritize incremental conversions.",
        eyebrow="Uplift modeling · Criteo",
    )

    st.subheader("Why model uplift?")
    st.write(
        "The experiment results summarize the average response across all users. "
        "For targeting, the next question is whether we can identify users whose "
        "conversion probability increases more under treatment. "
        "Uplift modeling estimates that incremental response, rather than "
        "conversion probability alone."
    )

    st.subheader("How was the segment selected?")
    st.markdown(
        "1. **Train:** Fit a T-learner on 700,000 users using two logistic "
        "regressions: one for treatment users and one for control users.\n"
        "2. **Rank:** For each of the 300,000 test users, predict conversion "
        "under both conditions. Rank users by the difference, and select "
        "the highest-scoring 10% (30,000 users).\n"
        "3. **Evaluate:** Compare actual treatment and control conversion "
        "rates within that selected segment."
    )
    st.caption(
        "Predicted uplift determines the ranking. Observed lift is the "
        "treatment–control difference measured during evaluation. "
        "The top 10% is a ranking cutoff, not a conversion probability."
    )

    results = load_experiment_results()
    top = results.loc[results["segment"] == "Top 10% predicted uplift"].iloc[0]
    control_rate = float(top["control_conversion_pct"])
    treatment_rate = float(top["treatment_conversion_pct"])
    lift = float(top["lift_pp"])
    lower = float(top["ci_lower_pp"])
    upper = float(top["ci_upper_pp"])

    st.subheader("What did we observe in the top 10%?")
    st.dataframe(
        pd.DataFrame({
            "Assignment": ["Control", "Treatment"],
            "Users": [4_228, 25_772],
            "Conversions": [71, 645],
            "Conversion rate": [
                f"{control_rate:.4f}%",
                f"{treatment_rate:.4f}%",
            ],
        }),
        hide_index=True,
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Observed lift", f"{lift:+.4f} pp")
    col2.metric("95% confidence interval", f"{lower:+.4f} to {upper:+.4f} pp")
    col3.metric("P-value", "0.00115")
    st.caption("Observed lift = treatment conversion − control conversion; pp = percentage points.")

    st.write(
        "**Treatment conversion exceeded control within the selected segment.** "
        f"The observed difference corresponds to about {lift * 10:.1f} additional "
        "conversions per 1,000 users assigned to treatment in this segment. "
        "Its confidence interval excludes zero."
    )

    st.subheader("What does this support?")
    takeaway(
        "The top-ranked segment is a candidate for a follow-up targeting "
        "experiment. This exploratory result does not establish that "
        "targeting 10% is optimal or more profitable than broader targeting."
    )
    st.write(
        "The segment's estimated lift is numerically higher than the overall "
        "estimate, but those estimates use different evaluation populations. "
        "The reported p-value tests the treatment–control difference within "
        "the segment; it does not test whether the segment responds more "
        "strongly than other users."
    )

    with st.expander("Model and evaluation details"):
        st.markdown(
            "- **Features:** 12 anonymized numeric variables, f0–f11. Their "
            "business meanings are unavailable.\n"
            "- **Preprocessing:** A separate StandardScaler in each logistic "
            "regression pipeline, fitted on training data only.\n"
            "- **Split:** 70% training / 30% test, jointly stratified by "
            "treatment and conversion.\n"
            "- **Model settings:** Logistic regression, max_iter = 1,000.\n"
            "- **Ranking:** Test users grouped into predicted-uplift deciles; "
            "the highest decile is evaluated here.\n"
            "- **Inference:** Two-sided two-proportion z-test and a normal "
            "95% confidence interval using the unpooled standard error.\n"
            "- **Validation:** Model or cutoff changes informed by these "
            "results require fresh evaluation data."
        )
    st.markdown(
        "[Criteo dataset documentation]"
        "(https://huggingface.co/datasets/criteo/criteo-uplift)"
    )
