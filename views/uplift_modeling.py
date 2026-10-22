
import pandas as pd
import streamlit as st

from shared.data import load_experiment_results
from shared.styling import insight_card, page_header, takeaway


def render():
    page_header(
        title="Can We Identify Users More Responsive to Advertising?",
        subtitle="Using uplift modeling to identify users most likely to benefit from advertising.",
        eyebrow="Uplift modeling · Criteo",
    )

    st.subheader("🔗 Why Model Uplift?")
    st.write(
        "The experiment showed that advertising increased purchases "
        "overall. But does it work equally well for everyone? Uplift "
        "modeling helps identify users who are more likely to purchase "
        "because of advertising, so we can target ads more effectively."
    )


    
    st.subheader("🔍 How Did We Identify the Top 10%?")

    col1, col2, col3 = st.columns(3)

    
    with col1:
        insight_card(
            "01 · Train",
            "700,000 users",
            "Train two logistic regression models to predict "
            "purchases with and without advertising.",
            height=215,
        )

    with col2:
        insight_card(
            "02 · Rank",
            "300,000 test users",
            "Predict advertising's impact for each test user "
            "and rank them from lowest to highest uplift.",
            height=215,
        )

    with col3:
        insight_card(
            "03 · Evaluate",
            "Top 10% of test users",
            "Select 30,000 users from the test group and "
            "compare their actual treatment and control conversion rates.",
            height=215,
        )


    st.caption(
        "Predicted uplift is used to rank users. "
        "Observed lift measures the actual difference "
        "between treatment and control."
    )  
    
    results = load_experiment_results()
    top = results.loc[
        results["segment"] == "Top 10% predicted uplift"
    ].iloc[0]

    control_rate = float(top["control_conversion_pct"])
    treatment_rate = float(top["treatment_conversion_pct"])
    lift = float(top["lift_pp"])
    lower = float(top["ci_lower_pp"])
    upper = float(top["ci_upper_pp"])

    
    st.subheader("💡 What did we find in the top 10%?")

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

    col1.metric(
        "Conversion lift",
        f"{lift:+.4f} pp"
    )
    col2.metric(
        "95% confidence interval",
        f"{lower:+.4f} to {upper:+.4f} pp"
    )
    col3.metric(
        "P-value",
        "0.00115"
    )

    st.caption(
        "Lift = treatment conversion rate − control conversion rate. "
        "pp = percentage points."
    )

    st.write(
        "**Advertising significantly increased conversions in the top 10%.** "
        f"The estimated increase was about {lift * 10:.1f} additional purchases "
        "per 1,000 users assigned to treatment in this group. "
        "The confidence interval is entirely above zero."
    )

    st.subheader("What does this mean for the business?")

    takeaway(
        "The top 10% is a promising group for targeted advertising. "
        "Focusing on these users could improve advertising efficiency, "
        "but further testing is needed before recommending a targeted rollout."
    )

    st.write(
        "Although this group showed a larger estimated lift than the overall "
        "experiment, we still need to confirm whether it responds significantly "
        "better than the remaining 90%. We also need to consider advertising "
        "costs and the value of additional purchases."
    )

    with st.expander("Model and evaluation details"):
        st.markdown(
            "- **Features:** 12 anonymized user variables (f0–f11). "
            "Their business meanings are unknown.\n"
            "- **Preprocessing:** Features standardized separately for "
            "each model using training data only.\n"
            "- **Data split:** 70% training / 30% testing, stratified by "
            "treatment assignment and conversion.\n"
            "- **Model:** T-learner using two logistic regression models "
            "(max_iter=1,000).\n"
            "- **Ranking:** Test users divided into 10 groups based on "
            "predicted uplift; the highest-ranked 10% was selected.\n"
            "- **Statistical testing:** Two-sided two-proportion z-test "
            "and 95% confidence interval for the observed conversion lift.\n"
            "- **Limitation:** The significance test confirms a positive "
            "effect within the selected group, not that its effect is "
            "significantly larger than in the remaining users.\n"
            "- **Next step:** Validate targeting performance using fresh "
            "data before deployment."
        )

    st.markdown(
        "[Criteo dataset documentation]"
        "(https://huggingface.co/datasets/criteo/criteo-uplift)"
    )
