import pandas as pd
import streamlit as st

from shared.styling import insight_card, page_header, takeaway


def render():
    page_header(
        title="Can clearer information help shoppers buy?",
        subtitle=(
            "Test shipping estimates and return information "
            "near Add to Cart."
        ),
        eyebrow="Experiment design · Proposed, not yet run",
    )

    st.write(
        "Only about 18–19 in 100 product-view sessions reach the cart. "
        "Could clearer shipping and return information help? "
        "This experiment would test that idea."
    )

    st.subheader("🔀 Two experiences to compare")

    control_col, treatment_col = st.columns(2)

    with control_col:
        insight_card(
            "A · Control",
            "Current product page",
            "Keep the existing experience.",
            height=220,
        )

    with treatment_col:
        insight_card(
            "B · Treatment",
            "Clearer purchase information",
            "Show shipping estimates, return information, and "
            "purchase reassurance near Add to Cart.",
            height=220,
        )

    st.write(
        "**Who:** First-time visitors, when they view a product.  \n"
        "**Assignment:** Randomly split users 50/50, keeping each "
        "person on the same version.  \n"
        "**Success measure:** The percentage of assigned users "
        "who purchase."
    )

    st.subheader("📏 How large would the test be?")

    col1, col2, col3 = st.columns(3)

    col1.metric("Participants needed", "24,696")
    col2.metric("Improvement to detect", "20% relative")
    col3.metric("Estimated recruitment", "≈45 days")

    takeaway(
        "The test is planned to detect an increase from 3.36% "
        "to 4.032% purchase conversion—about 7 additional "
        "purchasers per 1,000 eligible users."
    )

    st.write(
        "These are planning estimates, not predicted results. "
        "The baseline, eligible traffic, and purchase measurement "
        "window still need confirmation."
    )

    with st.expander("Why test this change?"):
        st.write(
            "The GA4 funnel shows its largest drop-off between "
            "viewing a product and adding it to the cart. "
            "Uncertainty about shipping or returns could contribute, "
            "but the funnel cannot establish the cause."
        )

        st.write(
            "**Hypothesis:** Clearer shipping estimates, visible "
            "return information, and reassurance near Add to Cart "
            "will increase purchase conversion among first-time "
            "product viewers."
        )

        st.write(
            "This experiment targets a narrower population than "
            "the device funnel, which describes shopping sessions "
            "across a broader group of visitors."
        )

    with st.expander("Sample size, timing, and alternative scenarios"):
        st.markdown("#### Selected plan")

        st.write(
            "**12,348 users per group**, or **24,696 total**. "
            "A 20% relative improvement on the 3.36% baseline "
            "equals **+0.672 percentage points**, giving a target "
            "conversion rate of **4.032%**."
        )

        st.write(
            "The notebook assumes **553.6 eligible users per day**. "
            "Recruitment would take **44.6 days**, approximately "
            "**45 days or 6.4 weeks**. The final decision would "
            "also require time for participants to complete "
            "the purchase measurement window."
        )

        st.markdown("#### Why plan for a 20% improvement?")

        st.write(
            "Smaller improvements require more participants. "
            "The notebook selected 20% as a compromise between "
            "sensitivity and recruitment time."
        )

        scenarios = pd.DataFrame({
            "Relative improvement": ["10%", "15%", "20%", "25%"],
            "Target conversion": [
                "3.696%", "3.864%", "4.032%", "4.200%"
            ],
            "Users per group": [47299, 21490, 12348, 8068],
            "Total users": [94598, 42980, 24696, 16136],
            "Recruitment days": [170.9, 77.6, 44.6, 29.1],
        })

        st.dataframe(scenarios, hide_index=True)

        st.write(
            "These are alternative planning scenarios, not four "
            "experiments or forecasts. Business value is still "
            "needed to determine what improvement is worthwhile."
        )

    with st.expander("How would we decide whether to launch?"):
        st.write(
            "After reaching the planned sample and completing "
            "purchase follow-up, compare conversion between "
            "groups and estimate a confidence interval for "
            "the difference."
        )

        st.markdown(
            "- **Business value:** Does the improvement justify "
            "the cost of the change?\n"
            "- **Engagement:** Do bounce and engagement measures "
            "suggest a worse experience?\n"
            "- **Page performance:** Does the revised page "
            "become slower?\n"
            "- **Purchase quality:** Do refunds or returns "
            "increase, if those data are available?"
        )

        st.write(
            "Launch only if the evidence and business value "
            "support it and the agreed guardrails are met. "
            "Statistical significance alone is not enough."
        )

    with st.expander("Technical design and definitions"):
        design = pd.DataFrame({
            "Parameter": [
                "Eligible population",
                "Randomization unit",
                "Allocation",
                "Primary metric",
                "Baseline conversion",
                "Minimum detectable effect",
                "Corresponding treatment conversion",
                "Absolute effect",
                "Significance level",
                "Statistical power",
                "Test direction",
                "Required users per group",
                "Required users total",
                "Eligible daily traffic assumption",
                "Estimated recruitment duration",
            ],
            "Value": [
                "First-time visitors who view a product",
                "User",
                "50/50",
                "User-level purchase conversion",
                "3.36%",
                "20% relative lift",
                "4.032%",
                "+0.672 percentage points",
                "5%",
                "80%",
                "Two-sided",
                "12,348",
                "24,696",
                "553.6 users",
                "44.6 days, approximately 6.4 weeks",
            ],
        })

        st.dataframe(design, hide_index=True)

        st.markdown(
            "- **Percentage points:** The difference between "
            "two percentages. Moving from 3.36% to 4.032% is "
            "+0.672 percentage points, or a 20% relative increase.\n"
            "- **Minimum detectable effect (MDE):** The improvement "
            "used to plan sample size. Smaller effects may exist "
            "even if the test cannot reliably detect them.\n"
            "- **80% power:** If the true improvement equals the "
            "planned MDE and assumptions hold, the test has about "
            "an 80% chance of detecting it.\n"
            "- **5% significance level:** When there is no effect, "
            "the test procedure has a 5% false-positive rate "
            "under its assumptions.\n"
            "- **Two-sided test:** Allows for either an increase "
            "or a decrease in conversion."
        )

        st.write(
            "Sample sizes were calculated with statsmodels "
            "`NormalIndPower` and `proportion_effectsize`, "
            "using equal group allocation and rounding up."
        )

        st.write(
            "**Metric distinction:** This test measures user-level "
            "purchase conversion. Product Analytics reports "
            "ordered, same-session funnel completion. "
            "The separate Criteo advertising analysis does not "
            "evaluate this proposed change."
        )

    with st.expander("What needs confirmation before launch?"):
        st.markdown(
            "- Confirm the source and eligibility definitions "
            "behind the 3.36% baseline and daily traffic estimate.\n"
            "- Define how long each assigned user has to purchase "
            "and align the baseline with that window.\n"
            "- Define acceptable guardrail changes before testing.\n"
            "- Include purchase follow-up in the timeline; "
            "45 days covers recruitment, not necessarily "
            "the full time to a decision."
        )
