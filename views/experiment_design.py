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

    with st.expander("Sample size, duration, and planning assumptions"):
        st.markdown("#### Inputs from the SQL analysis")

        st.markdown(
            "- **Population:** 50,940 first-time visitors who viewed "
            "a product, identified in the GA4 BigQuery analysis.\n"
            "- **Baseline conversion:** 1,713 purchasing users ÷ "
            "50,940 eligible users = **3.36%**.\n"
            "- **Average daily eligible users:** **553.6**, "
            "measured across 92 days."
        )

        st.markdown("#### Selected design")

        st.markdown(
            "- **Minimum detectable lift:** **20% relative**, "
            "equivalent to conversion increasing from "
            "3.36% to **4.032%**.\n"
            "- **Sample size:** **24,696 users**, "
            "split equally between the two groups.\n"
            "- **Estimated experiment duration:** "
            "24,696 ÷ 553.6 ≈ **45 days** to reach the sample "
            "size, plus purchase follow-up."
        )

        st.write(
            "Sample size was calculated in Python using "
            "statsmodels, with 80% power, a 5% significance "
            "level, and a two-sided test."
        )

        st.markdown("#### Alternative scenarios")

        st.write(
            "Detecting smaller improvements requires more users "
            "and a longer experiment. The 20% option balances "
            "sensitivity with duration."
        )

        scenarios = pd.DataFrame({
            "Minimum detectable lift": ["10%", "15%", "20%", "25%"],
            "Conversion at that lift": [
                "3.696%", "3.864%", "4.032%", "4.200%"
            ],
            "Users per group": [47299, 21490, 12348, 8068],
            "Total users": [94598, 42980, 24696, 16136],
            "Days to reach sample size": [170.9, 77.6, 44.6, 29.1],
        })

        st.dataframe(scenarios, hide_index=True)

    with st.expander("Launch criteria and checks"):
        st.markdown("#### Before the experiment")

        st.markdown(
            "- Confirm user eligibility and define the purchase "
            "measurement window; align the baseline with both.\n"
            "- Set acceptable limits for changes in engagement, "
            "page speed, and refunds or returns where available.\n"
            "- Allow purchase follow-up after the final users "
            "enter the experiment."
        )

        st.markdown("#### After the experiment")

        st.markdown(
            "- Compare purchase conversion and the confidence "
            "interval for the difference.\n"
            "- Assess whether the improvement justifies "
            "implementation costs.\n"
            "- Check that engagement, page speed, and purchase "
            "quality remain within the agreed limits."
        )

        st.write(
            "Launch when the evidence, business value, and "
            "guardrails support the change."
        )

    with st.expander("Statistical definitions and measurement"):
        st.markdown(
            "- **Minimum detectable lift:** The improvement used "
            "to calculate sample size, not a predicted result.\n"
            "- **Percentage points:** Moving from 3.36% to "
            "4.032% adds 0.672 percentage points—a 20% relative lift.\n"
            "- **80% power:** An 80% chance of detecting the planned "
            "lift if it is real and the assumptions hold.\n"
            "- **5% significance level:** A 5% false-positive rate "
            "when there is no effect, under the test assumptions.\n"
            "- **Two-sided test:** Detects either an increase "
            "or a decrease in conversion."
        )

        st.write(
            "**Calculation method:** statsmodels "
            "`NormalIndPower` and `proportion_effectsize`, "
            "with equal groups and sample sizes rounded up."
        )

        st.write(
            "**Measurement:** The experiment compares purchases "
            "per assigned user. The Product Analytics funnel "
            "measures ordered steps within a session."
        )

        st.write(
            "**Hypothesis:** Clearer shipping and return information "
            "may increase purchases. The funnel identifies "
            "drop-off, but does not establish its cause."
        )
