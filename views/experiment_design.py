import pandas as pd
import streamlit as st

from shared.styling import insight_card, page_header, takeaway


def render():
    page_header(
        title="Can better product-page information increase sales?",
        subtitle="Compare two product pages for first-time visitors.",
        eyebrow="Experiment design · Proposed, not yet run",
    )

    st.write(
        "Only about 18–19 in 100 product-view sessions reach the cart. "
        "Would clearer information help more shoppers take the next step?"
    )

    st.subheader("🔀 Two experiences to compare")

    control_col, treatment_col = st.columns(2)

    with control_col:
        insight_card(
            "A · Control",
            "Current page",
            "Keep the existing experience.",
            height=150,
        )

    with treatment_col:
        insight_card(
            "B · Treatment",
            "Revised page",
            "Make shipping estimates and return information "
            "more visible near Add to Cart.",
            height=150,
        )

    st.write(
        "**Participants:** : First-time visitors who view a product.  \n"
        "**Assignment:** Random 50/50 split; each user keeps the same version. \n"
        "**Primary metric** Percentage of assigned users who purchase. "
    )

    st.subheader("📏 Sample Size and Duration")

    col1, col2, col3 = st.columns(3)

    col1.metric("Participants needed", "24,696")
    col2.metric("Minimum Detectable Lift", "20% relative")
    col3.metric("Estimated Experiment Duration.", "≈45 days")

    takeaway(
        "The test is planned to detect an increase from 3.36% "
        "to 4.032% purchase conversion—about 7 additional "
        "purchasers per 1,000 eligible users."
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
            "return information, and reassurance near *Add to Cart* "
            "will increase purchase conversion among first-time "
            "product viewers."
        )

    with st.expander("Sample size, timing, and alternative scenarios"):
        st.markdown("#### Planning Inputs")

        st.markdown(
            "- **Source:** GA4 store data analyzed in BigQuery.\n"
            "- **Eligible users:** The eligibility query identified "
            "50,940 first-time visitors who viewed a product.\n"
            "- **Baseline purchase conversion:** 1,713 of those users "
            "purchased. Calculated as 1,713 ÷ 50,940 × 100 = **3.36%**.\n"
            "- **Average daily eligible users:** The daily traffic "
            "query measured **553.6 users per day** across 92 days."
        )

        st.markdown("#### Selected Experiment Design")

        st.markdown(
            "- **Minimum detectable lift:** A **20% relative increase**, "
            "selected for planning. This raises conversion from "
            "3.36% to **4.032%**: 3.36% × 1.20.\n"
            "- **Sample size:** **24,696 users—12,348 per group**, "
            "calculated in Python using the baseline, detectable lift, "
            "80% power, a 5% significance level, and a two-sided test.\n"
            "- **Estimated experiment duration:** "
            "24,696 ÷ 553.6 = **44.6 days**, rounded to **45 days** "
            "to reach the sample size, plus purchase follow-up."
        )

        st.markdown("#### Why a 20% Minimum Detectable Lift?")

        st.write(
            "The notebook compared detectable lifts of 10%, 15%, "
            "20%, and 25%. The 20% option balances the size of "
            "improvement we can detect with the estimated "
            "experiment duration."
        )

        st.write(
            "The table below shows how smaller detectable "
            "improvements require more users and more time."
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
