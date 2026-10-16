import pandas as pd
import streamlit as st

from shared.data import load_experiment_results
from shared.styling import page_header, takeaway


def render():
    page_header(
        title="Did advertising increase conversion?",
        subtitle="Overall treatment effect in the Criteo advertising benchmark.",
        eyebrow="Experiment results · Criteo",
    )

    st.subheader("What was tested?")
    st.write(
        "Criteo's dataset comes from randomized advertising experiments: "
        "the treatment group was eligible for advertising targeting, while "
        "the control group was withheld from targeting. This analysis compares "
        "conversion rates across a sample of 1 million users to estimate the "
        "incremental response to treatment assignment."
    )
    st.caption(
        "This advertising analysis is separate from the proposed GA4 "
        "product-page experiment. Conversion rate = converted users / assigned users."
    )

    results = load_experiment_results()
    overall = results.loc[results["segment"] == "Overall"].iloc[0]
    control_rate = float(overall["control_conversion_pct"])
    treatment_rate = float(overall["treatment_conversion_pct"])
    lift = float(overall["lift_pp"])
    lower = float(overall["ci_lower_pp"])
    upper = float(overall["ci_upper_pp"])
    relative_lift = lift / control_rate * 100 if control_rate else None

    st.subheader("What did we find?")
    st.dataframe(
        pd.DataFrame({
            "Assignment": ["Control", "Treatment"],
            "Users": [149_825, 850_175],
            "Conversions": [281, 2_540],
            "Conversion rate": [
                f"{control_rate:.4f}%",
                f"{treatment_rate:.4f}%",
            ],
        }),
        hide_index=True,
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Absolute lift", f"{lift:+.4f} pp")
    col2.metric("95% confidence interval", f"{lower:+.4f} to {upper:+.4f} pp")
    col3.metric("Relative lift", f"{relative_lift:+.1f}%" if relative_lift is not None else "N/A")
    st.caption(
        "Absolute lift = treatment rate − control rate; pp = percentage points. "
        "Relative lift expresses that difference as a percentage of the control rate."
    )

    st.write(
        "**Treatment conversion exceeded control in this benchmark sample.** "
        "The confidence interval excludes zero "
        "(two-sided two-proportion z-test: p ≈ 7.24 × 10⁻¹⁴). "
        f"The estimated difference is equivalent to approximately {lift * 1_000:.0f} "
        "additional conversions per 100,000 users assigned to treatment."
    )

    st.subheader("What is the decision?")
    takeaway(
        "The benchmark shows a positive overall response. Validate the effect "
        "in a production experiment and assess advertising cost, conversion "
        "value, and guardrails before recommending rollout."
    )
    st.write(
        "**Next question:** Can uplift modeling identify a segment "
        "with a larger incremental response to advertising?"
    )

    with st.expander("Statistical methodology"):
        st.markdown(
            "- **Estimand:** Intention-to-treat difference in user conversion rates; "
            "users are compared by assignment, regardless of actual ad exposure.\n"
            "- **Null hypothesis:** Treatment and control conversion rates are equal.\n"
            "- **Test:** Two-sided two-proportion z-test, α = 0.05.\n"
            "- **95% confidence interval:** Normal approximation using the "
            "unpooled standard error.\n"
            "- **Group sizes:** The comparison accounts for each group's "
            "conversion rate and sample size."
        )

    st.info(
        "Scope: Criteo non-uniformly subsampled the public data to conceal "
        "the original incrementality. These estimates describe the released "
        "benchmark under the analysis assumptions; they are not estimates "
        "of original advertiser lift or a production forecast."
    )
    st.markdown(
        "[Criteo dataset documentation]"
        "(https://huggingface.co/datasets/criteo/criteo-uplift)"
    )
