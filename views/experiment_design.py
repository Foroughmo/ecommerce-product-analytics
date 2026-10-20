import pandas as pd
import streamlit as st

from shared.styling import insight_card, page_header, takeaway


def render():
    page_header(
        title="Can Better Product-Page Information Increase Sales?",
        subtitle=(
            "Designing an A/B test to determine whether clearer "
            "shipping and return information increases purchases "
            "among first-time product viewers."
        ),
        eyebrow="Experiment Design · Proposed, not yet run",
    )


    st.write(
        "The funnel analysis found that only 18–19% of product-view "
        "sessions lead to adding an item to the cart. This suggests "
        "an opportunity to improve the product-page experience. "
        "One possible explanation is that customers need clearer "
        "shipping and return information before deciding to buy. "
        "This experiment is designed to test that hypothesis."
    )


    st.subheader(" 🧭 From Insight to Experiment")
    
    steps = [
        ("01", "Opportunity", "Low product-view-to-cart conversion"),
        ("02", "Hypothesis", "Clearer information may reduce hesitation"),
        ("03", "Experiment", "A/B test measuring purchase conversion"),
        ("04", "Decision", "Assess conversion lift and business impact"),
    ]
    
    cols = st.columns([1, 0.12, 1, 0.12, 1, 0.12, 1], gap="small")
    
    for i, (number, title, description) in enumerate(steps):
        with cols[i * 2]:
            st.markdown(
                f"""
                <div style="
                    background: #FFFFFF;
                    border: 1px solid #DDE4EE;
                    border-radius: 12px;
                    padding: 18px;
                    min-height: 155px;
                ">
                    <div style="color:#6683B0; font-size:14px; font-weight:700;">
                        STEP {number}
                    </div>
                    <div style="
                        color:#172B4D;
                        font-size:19px;
                        font-weight:700;
                        margin:9px 0;
                    ">{title}</div>
                    <div style="color:#526480; font-size:15px; line-height:1.5;">
                        {description}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    
        if i < 3:
            with cols[i * 2 + 1]:
                st.markdown(
                    "<div style='text-align:center; padding-top:57px; "
                    "color:#6683B0; font-size:23px;'>→</div>",
                    unsafe_allow_html=True,
                )


    
    st.subheader("🔀 Two Experiences to Compare")

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
        "**Participants:** First-time visitors who view a product.  \n"
        "**Assignment:** Random 50/50 split; each user keeps the same version.  \n"
        "**Primary metric:** Percentage of eligible users who purchase."
    )

    st.subheader("📏 Sample Size and Duration")

    col1, col2, col3 = st.columns(3)

    col1.metric("Participants needed", "24,696")
    col2.metric("Minimum Detectable Lift", "20% relative")
    col3.metric("Estimated Experiment Duration.", "≈45 days")

    
    st.caption(
        "Why 20%? Detecting smaller improvements would require "
        "a much longer experiment. A 20% relative lift offers a "
        "practical balance between sensitivity and duration. "
        "This is the improvement the test is designed to detect, "
        "not a prediction of the outcome."
    )

    takeaway(
        "The test is planned to detect an increase from 3.36% "
        "to 4.032% purchase conversion—about 7 additional "
        "purchasers per 1,000 eligible users."
    )

    st.subheader("How Would We Decide?")

    st.write(
        "If the revised page produces a statistically reliable "
        "and commercially meaningful increase in purchases, "
        "it would be a candidate for rollout."
    )

    with st.expander("Sample size, duration, and planning assumptions"):
        st.markdown("#### Key Metrics from the GA4 SQL Analysis")

        st.markdown(
            "- **Population:** 50,940 first-time visitors who viewed "
            "a product, identified in the GA4 BigQuery analysis.\n"
            "- **Current purchase rate:** 1,713 of 50,940 eligible "
            "visitors purchased (3.36%).\n"
            "- **Average daily eligible users:** 50,940 ÷ 92 = **553.6**, "
            "measured across 92 days."
        )

        st.markdown("#### Selected Experiment Design")

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
        st.caption(
            "The 45-day estimate assumes future eligible traffic "
            "remains similar to the historical average of 553.6 users "
            "per day. It excludes any additional purchase follow-up "
            "period and assumes all eligible users can participate."
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
            "**Hypothesis:** Clearer shipping and return information "
            "may increase purchases. The funnel identifies "
            "drop-off, but does not establish its cause."
        )
