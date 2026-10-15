import streamlit as st

from shared.data import load_experiment_results, load_funnel
from shared.styling import insight_card, page_header, takeaway


def render():
    page_header(
        title="From Browsing to Buying",
        subtitle=(
            "An e-commerce case study: identify where shoppers leave, "
            "design a product test, and explore whether advertising "
            "changes purchasing behavior."
        ),
        eyebrow="Overview · Business questions & findings",
    )

    # Introduce the business problem before displaying results.
    st.write(
        "An e-commerce team wants more visitors to become customers. "
        "Before investing in changes, it needs to understand where "
        "the shopping journey breaks down and how to measure whether "
        "an intervention actually helps."
    )

    left, right = st.columns(2)

    with left:
        insight_card(
            "01 · Understand the shopping journey",
            "Where do shoppers leave?",
            "GA4 store data describes product views, cart additions, "
            "checkout, and purchases. We use it to identify an "
            "opportunity and propose a product-page experiment.",
        )

    with right:
        insight_card(
            "02 · Evaluate an intervention",
            "Does advertising change behavior?",
            "A separate Criteo benchmark contains treatment and control "
            "groups. We evaluate overall conversion lift and explore "
            "which users may respond more strongly.",
        )

    st.caption(
        "Two independent datasets, two complementary questions. "
        "The Criteo analysis does not test the proposed GA4 store change."
    )

    funnel = load_funnel()
    results = load_experiment_results()

    overall = results.loc[
        results["segment"] == "Overall"
    ].iloc[0]

    top = results.loc[
        results["segment"] == "Top 10% predicted uplift"
    ].iloc[0]

    min_cart_rate = funnel["view_to_cart_rate"].min()
    max_cart_rate = funnel["view_to_cart_rate"].max()

    desktop_rate = funnel.loc[
        funnel["device_category"] == "desktop",
        "overall_conversion_rate",
    ].iloc[0]

    mobile_rate = funnel.loc[
        funnel["device_category"] == "mobile",
        "overall_conversion_rate",
    ].iloc[0]

    st.subheader("Three findings to take away")

    col1, col2, col3 = st.columns(3)

    with col1:
        insight_card(
            "GA4 · Observed shopping behavior",
            "About 18–19 in 100 reach the cart",
            "Across devices, this is the share of product-view sessions "
            "that progress to Add to Cart—the largest drop-off "
            "in the measured funnel.",
        )

    with col2:
        insight_card(
            "Criteo · Overall benchmark",
            f"+{overall['lift_pp']:.4f} percentage points",
            "The treatment group has a higher conversion rate than "
            "control. The confidence interval for the difference "
            "is entirely above zero.",
        )

    with col3:
        insight_card(
            "Criteo · Selected test-set group",
            f"+{top['lift_pp']:.4f} percentage points",
            "The highest-ranked 10% by predicted uplift show a positive "
            "effect. This supports further targeting evaluation; "
            "it does not establish an optimal policy.",
        )

    st.subheader("What's Next")

    product_tab, advertising_tab = st.tabs(
        ["Product experience", "Advertising & targeting"]
    )

    with product_tab:
        left, right = st.columns([3, 2])

        with left:
            st.markdown("#### Test clearer information near Add to Cart")
            st.write(
                "Show first-time product viewers clearer shipping "
                "estimates, return information, and purchase reassurance."
            )
            st.write(
                "The funnel shows where to investigate. It does not "
                "prove that uncertainty about shipping or returns "
                "causes visitors to leave."
            )

        with right:
            insight_card(
                "Proposed experiment · Not yet run",
                "24,696 participants",
                "12,348 users per group. About 45 days of recruitment "
                "at the earlier traffic estimate, plus any required "
                "outcome follow-up.",
            )

        takeaway(
            "Mobile full-funnel completion is "
            f"{mobile_rate:.2f}% versus {desktop_rate:.2f}% on desktop. "
        )

    with advertising_tab:
        left, right = st.columns([3, 2])

        with left:
            st.markdown("#### Evaluate value before deployment")
            st.write(
                "The benchmark shows positive conversion lift overall "
                "and within the selected high-uplift group."
            )
            st.write(
                "Before applying a targeting strategy in production, "
                "evaluate advertising costs, incremental conversion "
                "value, and performance on new data."
            )

        with right:
            insight_card(
                "Evidence status",
                "Promising, not deployment-ready",
                "Positive conversion lift alone does not establish "
                "profitability or prove that targeting the top 10% "
                "outperforms other policies.",
            )

        takeaway(
            "Criteo non-uniformly subsampled the public dataset to "
            "conceal original incrementality. These are benchmark "
            "findings, not estimates of actual advertiser ROI."
        )

    with st.expander("Supporting numbers and experiment assumptions"):
        st.markdown("#### GA4 shopping funnel")
        st.write(
            f"Product-view-to-cart rates range from "
            f"{min_cart_rate:.2f}% to {max_cart_rate:.2f}%. "
            "Counts represent sessions, not unique users. "
            "Full-funnel completion requires product view, cart, "
            "checkout, and purchase in that order within one session."
        )

        st.markdown("#### Proposed product-page test")
        st.write(
            "User-level 50/50 assignment; planning baseline 3.36%; "
            "20% relative minimum detectable effect; target conversion "
            "4.032%; 80% power; 5% significance level; two-sided test."
        )
        st.caption(
            "The baseline source, eligible traffic definition, and "
            "purchase measurement window still need confirmation. "
            "The detectable target is not a predicted result."
        )

        st.markdown("#### Criteo overall result")
        st.write(
            f"Control: {overall['control_conversion_pct']:.4f}%. "
            f"Treatment: {overall['treatment_conversion_pct']:.4f}%. "
            f"Absolute lift: {overall['lift_pp']:+.4f} percentage points. "
            f"95% CI: {overall['ci_lower_pp']:+.4f} to "
            f"{overall['ci_upper_pp']:+.4f} percentage points."
        )

        st.markdown("#### Criteo top-10% result")
        st.write(
            f"Estimated effect: {top['lift_pp']:+.4f} percentage points. "
            f"95% CI: {top['ci_lower_pp']:+.4f} to "
            f"{top['ci_upper_pp']:+.4f} percentage points."
        )
        st.caption(
            "Overall analysis: 1,000,000 sampled rows. "
            "Model training: 700,000 rows. "
            "Test-set evaluation: 300,000 rows. "
            "Top predicted-uplift decile: 30,000 test-set users."
        )

    with st.expander("Explore the report"):
        st.write(
            "- **Product Analytics:** Explore the session funnel "
            "using the device filter.\n"
            "- **Experiment Design:** Understand the proposed change, "
            "sample size, timing, and guardrails.\n"
            "- **Experiment Results:** Review overall advertising "
            "conversion lift and uncertainty.\n"
            "- **Uplift Modeling:** Understand how the model identifies "
            "users with higher predicted treatment effects."
        )
