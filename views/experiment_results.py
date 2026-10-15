import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from shared.data import load_experiment_results
from shared.styling import insight_card, page_header, takeaway


def render():
    page_header(
        title="Did advertising increase purchases?",
        subtitle=(
            "Compare users assigned to advertising treatment with "
            "users assigned to control in the Criteo public benchmark."
        ),
        eyebrow="Experiment results · Criteo",
    )

    st.write(
        "Some people would purchase even without advertising. "
        "Comparing treatment and control helps estimate the additional "
        "conversions associated with assignment to advertising."
    )

    results = load_experiment_results()
    overall = results.loc[
        results["segment"] == "Overall"
    ].iloc[0]

    control_rate = float(overall["control_conversion_pct"])
    treatment_rate = float(overall["treatment_conversion_pct"])
    lift = float(overall["lift_pp"])
    lower = float(overall["ci_lower_pp"])
    upper = float(overall["ci_upper_pp"])

    # Convert percentage-point differences into counts per 100,000.
    extra_per_100k = lift / 100 * 100_000
    lower_per_100k = lower / 100 * 100_000
    upper_per_100k = upper / 100 * 100_000

    col1, col2, col3 = st.columns(3)
    col1.metric("Control conversion", f"{control_rate:.4f}%")
    col2.metric("Treatment conversion", f"{treatment_rate:.4f}%")
    col3.metric("Absolute lift", f"+{lift:.4f} pp")

    st.caption(
        "Conversion means the share of users who purchased. "
        "pp means percentage points."
    )

    results_tab, business_tab, method_tab = st.tabs(
        ["Results", "Business interpretation", "Method & limitations"]
    )

    with results_tab:
        chart_col, explanation_col = st.columns([3, 2])

        with chart_col:
            st.subheader("Higher conversion in the treatment group")

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
                    f"{control_rate:.4f}%",
                    f"{treatment_rate:.4f}%",
                ],
                padding=7,
            )
            ax.set_ylim(0, max(control_rate, treatment_rate) * 1.3)
            ax.set_ylabel("Users who converted (%)")
            ax.spines[["top", "right"]].set_visible(False)
            fig.tight_layout()

            st.pyplot(fig)
            plt.close(fig)

        with explanation_col:
            insight_card(
                "Estimated difference",
                f"+{lift:.4f} percentage points",
                "Treatment conversion minus control conversion. "
                "This is the absolute increase in the public "
                "benchmark sample.",
            )

            insight_card(
                "95% confidence interval",
                f"+{lower:.4f} to +{upper:.4f} pp",
                "The approximate interval is entirely above zero, "
                "providing evidence of a positive difference "
                "under the analysis assumptions.",
            )

        takeaway(
            f"The observed difference corresponds to about "
            f"{extra_per_100k:.0f} additional conversions per "
            "100,000 users assigned to treatment in this benchmark."
        )

        with st.expander("See the verified group counts"):
            counts = pd.DataFrame({
                "Group": ["Control", "Treatment"],
                "Users": [149825, 850175],
                "Conversions": [281, 2540],
                "Conversion rate": [
                    f"{control_rate:.4f}%",
                    f"{treatment_rate:.4f}%",
                ],
            })
            st.dataframe(counts, hide_index=True)

            st.caption(
                "Total sample: 1,000,000 users. Groups are unequal "
                "in size; the comparison uses each group's own "
                "conversion rate and sample size."
            )

    with business_tab:
        left, right = st.columns(2)

        with left:
            insight_card(
                "Illustrative scale",
                f"About {extra_per_100k:.0f} extra conversions",
                "Per 100,000 users assigned to treatment, using "
                "the observed benchmark difference. This is a "
                "rescaling of the estimate, not a production forecast.",
            )

        with right:
            insight_card(
                "Uncertainty at the same scale",
                f"About {lower_per_100k:.0f}–{upper_per_100k:.0f}",
                "The approximate 95% confidence interval expressed "
                "as additional conversions per 100,000 users.",
            )

        st.subheader("Would we recommend deployment?")

        st.write(
            "The conversion result is positive. A business decision "
            "would also need the cost of advertising, the value of "
            "incremental conversions, and relevant guardrail outcomes."
        )

        st.write(
            "The uplift analysis explores whether a selected group "
            "responds more strongly. It does not yet establish "
            "the most profitable targeting policy."
        )

        takeaway(
            "Recommendation: use this as evidence from a benchmark "
            "and a demonstration of the decision process. Validate "
            "impact and economics in the intended production setting."
        )

    with method_tab:
        st.subheader("How the comparison was made")

        st.write(
            "- **Outcome:** Binary purchase conversion.\n"
            "- **Comparison:** Treatment assignment versus control "
            "assignment, regardless of actual ad exposure.\n"
            "- **Estimate:** Treatment conversion rate minus control "
            "conversion rate.\n"
            "- **Test:** Two-sided, two-proportion z-test.\n"
            "- **95% interval:** Approximate normal interval using "
            "the unpooled standard error.\n"
            "- **Verified p-value:** Approximately 7.24 × 10⁻¹⁴."
        )

        st.write(
            "**Intention-to-treat:** Users are compared according to "
            "their assigned group. Filtering only to people who "
            "actually saw an ad would change the comparison."
        )

        st.write(
            "**Statistical versus business significance:** A small "
            "p-value provides evidence against equal conversion "
            "rates under the test assumptions. It does not measure "
            "profitability or guarantee a valuable business outcome."
        )

        st.subheader("Limits of the public dataset")

        st.info(
            "Criteo non-uniformly subsampled the public dataset "
            "to conceal original advertising incrementality. "
            "These estimates describe the released benchmark; "
            "they should not be interpreted as actual advertiser "
            "lift or production ROI."
        )

        st.write(
            "The data originated from randomized advertising "
            "experiments. Its privacy-related subsampling limits "
            "how directly these released-data estimates can be "
            "translated to the original experimental population."
        )

        st.markdown(
            "[Source: Criteo public dataset documentation]"
            "(https://huggingface.co/datasets/criteo/criteo-uplift)"
        )

    st.caption(
        "Source: completed Criteo analysis. Displayed rates and "
        "confidence limits are rounded. The GA4 product-page "
        "experiment is a separate proposal and has not been run."
    )
