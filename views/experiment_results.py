import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from shared.data import load_experiment_results
from shared.styling import insight_card, page_header, takeaway


def render():
    page_header(
        title="Did advertising increase conversion?",
        eyebrow="Experiment results · Criteo",
    )

    st.write(
        "This analysis uses a sample of 1 million users from Criteo’s "
        "public uplift dataset, derived from randomized advertising experiments. "
        "The objective is to estimate the difference in conversion between users "
        "assigned to advertising treatment and users assigned to control."
        "This is a separate analysis from the proposed GA4 product-page experiment."
    )

    st.subheader("Experiment setup")

    st.markdown(
        "- **Treatment:** Users eligible for advertising targeting.\n"
        "- **Control:** Users withheld from advertising targeting.\n"
        "- **Primary metric:** User conversion rate "
        "(converted users ÷ assigned users).\n"
        "- **Hypothesis:** Treatment assignment increases conversion."
    )

    results = load_experiment_results()
    overall = results.loc[results["segment"] == "Overall"].iloc[0]

    control_rate = float(overall["control_conversion_pct"])
    treatment_rate = float(overall["treatment_conversion_pct"])
    lift = float(overall["lift_pp"])
    lower = float(overall["ci_lower_pp"])
    upper = float(overall["ci_upper_pp"])

    # Convert percentage-point differences to conversions per 100,000 users.
    extra_per_100k = lift * 1_000
    lower_per_100k = lower * 1_000
    upper_per_100k = upper * 1_000

    st.subheader("Results")

    col1, col2, col3 = st.columns(3)
    col1.metric("Control conversion", f"{control_rate:.3f}%")
    col2.metric("Treatment conversion", f"{treatment_rate:.3f}%")
    col3.metric("Absolute lift", f"{lift:+.3f} pp")

    st.caption(
        "Absolute lift = treatment conversion − control conversion. "
        "pp = percentage points."
    )

    chart_col, inference_col = st.columns([3, 2])

    with chart_col:
        fig, ax = plt.subplots(figsize=(7, 3.8))
        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FFFFFF")

        bars = ax.bar(
            ["Control", "Treatment"],
            [control_rate, treatment_rate],
            color=["#94A3B8", "#087F8C"],
            width=0.5,
        )
        ax.bar_label(
            bars,
            labels=[
                f"{control_rate:.3f}%",
                f"{treatment_rate:.3f}%",
            ],
            padding=7,
        )
        ax.set_ylim(0, max(control_rate, treatment_rate) * 1.3)
        ax.set_ylabel("Conversion rate (%)")
        ax.spines[["top", "right"]].set_visible(False)
        fig.tight_layout()

        st.pyplot(fig)
        plt.close(fig)

    with inference_col:
        insight_card(
            "95% confidence interval",
            f"{lower:+.3f} to {upper:+.3f} pp",
            "The interval excludes zero, indicating a statistically "
            "significant positive difference in the benchmark sample.",
        )

        st.caption(
            "Two-sided two-proportion z-test: "
            "p ≈ 7.24 × 10⁻¹⁴."
        )

    st.subheader(" 🔎 Business interpretation")

    st.write(
        f"The estimated lift corresponds to approximately "
        f"**{extra_per_100k:.0f} additional conversions per 100,000 users** "
        f"assigned to treatment "
        f"(95% CI: {lower_per_100k:.0f}–{upper_per_100k:.0f}). "
        "This illustrates the scale of the benchmark estimate; "
        "it is not a production forecast."
    )

    takeaway(
        "Recommendation: validate the effect in a production experiment "
        "before scaling. A rollout decision also requires advertising costs, "
        "conversion value, and guardrail metrics to assess profitability."
    )

    with st.expander("Methodology and sample"):
        st.markdown(
            "- **Estimand:** Intention-to-treat difference in conversion rates; "
            "users remain in their assigned groups regardless of ad exposure.\n"
            "- **Hypothesis test:** Two-sided two-proportion z-test, α = 0.05.\n"
            "- **Confidence interval:** Normal approximation with an "
            "unpooled standard error."
        )

        counts = pd.DataFrame({
            "Group": ["Control", "Treatment"],
            "Users": [149_825, 850_175],
            "Conversions": [281, 2_540],
            "Conversion rate": [
                f"{control_rate:.3f}%",
                f"{treatment_rate:.3f}%",
            ],
        })
        st.dataframe(counts, hide_index=True)

        st.caption(
            "Unequal group sizes are accounted for through each group's "
            "conversion rate and sample size."
        )

    st.info(
        "Dataset limitation: Criteo non-uniformly subsampled the public data "
        "to conceal the original advertising incrementality. Estimates and "
        "statistical inference describe the released benchmark under the "
        "analysis assumptions, rather than the original advertiser population."
    )

    st.markdown(
        "[Source: Criteo uplift dataset documentation]"
        "(https://huggingface.co/datasets/criteo/criteo-uplift)"
    )
