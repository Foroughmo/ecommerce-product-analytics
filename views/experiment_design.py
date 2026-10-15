import pandas as pd
import streamlit as st

from shared.styling import insight_card, page_header, takeaway


def render():
    page_header(
        title="Test clearer information before purchase",
        subtitle=(
            "Would shipping estimates and visible return information "
            "help first-time product viewers become customers?"
        ),
        eyebrow="Experiment design · Proposed, not yet run",
    )

    takeaway(
        "Decision to inform: whether to introduce a revised product "
        "page. The experiment below is a plan; no results have "
        "been observed for this change."
    )

    context_col, opportunity_col = st.columns([3, 2])

    with context_col:
        st.subheader("Why this test?")
        st.write(
            "The GA4 funnel shows its largest drop-off between viewing "
            "a product and adding it to the cart. Across devices, "
            "only about 18–19 in 100 product-view sessions reach "
            "Add to Cart."
        )
        st.write(
            "Uncertainty about shipping or returns could contribute. "
            "The funnel cannot establish that explanation, so we "
            "propose testing it."
        )

    with opportunity_col:
        insight_card(
            "Hypothesis",
            "Clearer information may reduce uncertainty",
            "Providing shipping estimates, return-policy visibility, "
            "and reassurance near Add to Cart will increase purchase "
            "conversion among first-time product viewers.",
        )

    experience_tab, planning_tab, decision_tab = st.tabs(
        ["A/B experience", "Sample & timing", "Decision & safeguards"]
    )

    with experience_tab:
        st.subheader("One change, two experiences")

        control_col, treatment_col = st.columns(2)

        with control_col:
            insight_card(
                "A · Control",
                "Existing product page",
                "Eligible visitors see the current product page. "
                "This provides the comparison for evaluating "
                "the revised experience.",
            )

        with treatment_col:
            insight_card(
                "B · Treatment",
                "More visible purchase information",
                "Eligible visitors see clearer shipping estimates, "
                "return information, and purchase reassurance "
                "near Add to Cart.",
            )

        col1, col2, col3 = st.columns(3)

        with col1:
            insight_card(
                "Who participates?",
                "First-time product viewers",
                "First-time visitors become eligible when they "
                "view a product.",
            )

        with col2:
            insight_card(
                "How are groups assigned?",
                "50/50 random assignment",
                "Assignment is at the user level. Each participant "
                "should continue seeing the same assigned version.",
            )

        with col3:
            insight_card(
                "What do we measure?",
                "Purchase conversion",
                "Compare the percentage of eligible assigned "
                "users who purchase in each group.",
            )

        st.caption(
            "This experiment targets first-time product viewers. "
            "The device funnel describes a broader session population."
        )

    with planning_tab:
        st.subheader("What improvement are we planning to detect?")

        col1, col2, col3 = st.columns(3)
        col1.metric("Planning baseline", "3.36%")
        col2.metric("Detectable target", "4.032%")
        col3.metric("Absolute improvement", "+0.672 pp")

        takeaway(
            "Per 1,000 eligible users, the target corresponds to "
            "about 34 purchasers increasing to 40—approximately "
            "7 additional purchasers. This is a planning scenario, "
            "not a forecast."
        )

        st.caption(
            "pp means percentage points. A 20% relative increase "
            "on a 3.36% baseline equals +0.672 percentage points."
        )

        st.subheader("Participants and recruitment time")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total participants", "24,696")
        col2.metric("Users per group", "12,348")
        col3.metric("Recruitment estimate", "44.6 days")

        st.write(
            "The notebook assumes **553.6 eligible users per day**. "
            "At that rate, recruitment takes approximately "
            "**45 days, or 6.4 weeks**. The final decision may take "
            "longer because participants need time to complete "
            "the purchase measurement window."
        )

        with st.expander("Why choose a 20% relative improvement?"):
            st.write(
                "Smaller improvements require more participants "
                "to distinguish them from random variation. "
                "The notebook compared these planning scenarios "
                "and selected 20% as a compromise between "
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

            st.caption(
                "These are alternative planning scenarios, not "
                "four experiments or predicted outcomes. "
                "Business value is still needed to establish "
                "which improvement is commercially worthwhile."
            )

    with decision_tab:
        st.subheader("How would we decide whether to launch?")

        st.write(
            "After reaching the planned sample and completing "
            "outcome follow-up, compare purchase conversion "
            "between groups and quantify uncertainty around "
            "the difference."
        )
        st.write(
            "Consider both the evidence of improvement and its "
            "business value. Also check whether the revised "
            "experience creates problems elsewhere."
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            insight_card(
                "Guardrail · Engagement",
                "Are visitors disengaging?",
                "Monitor bounce and engagement for signs that "
                "the change makes the experience less useful.",
            )

        with col2:
            insight_card(
                "Guardrail · Performance",
                "Does the page become slower?",
                "Check whether the revised experience worsens "
                "page performance.",
            )

        with col3:
            insight_card(
                "Guardrail · Purchase quality",
                "Do refunds or returns increase?",
                "Monitor downstream refunds and returns "
                "if those data are available.",
            )

        takeaway(
            "Statistical significance alone is not a launch "
            "decision. The improvement must also justify its "
            "costs and meet the agreed guardrail criteria."
        )

    with st.expander("Technical design and plain-English definitions"):
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

        st.write(
            "**Minimum detectable effect (MDE):** The improvement "
            "used to plan the sample size. Smaller effects may "
            "exist even if the test cannot reliably detect them."
        )
        st.write(
            "**80% power:** If the true improvement equals the "
            "planned MDE and the assumptions hold, the test has "
            "about an 80% chance of detecting it."
        )
        st.write(
            "**5% significance level:** When there is truly no "
            "effect, the test procedure has a 5% false-positive "
            "rate under its assumptions."
        )
        st.write(
            "**Two-sided test:** The analysis allows for either "
            "an increase or a decrease in conversion."
        )
        st.caption(
            "Sample sizes were calculated with statsmodels "
            "NormalIndPower and proportion_effectsize, using "
            "equal group allocation and rounding up."
        )

    with st.expander("Planning details to confirm before launch"):
        st.write(
            "- Confirm the source and eligibility definitions "
            "behind the 3.36% baseline and daily traffic estimate.\n"
            "- Define how long each assigned user has to purchase "
            "and align the baseline with that window.\n"
            "- Define acceptable guardrail changes before the test.\n"
            "- Account for outcome follow-up after recruitment; "
            "45 days is not necessarily the full decision timeline."
        )

    st.caption(
        "This design uses a user-level metric. Product Analytics "
        "separately reports ordered, same-session funnel completion. "
        "The Criteo advertising analysis does not evaluate this "
        "proposed product-page change."
    )
