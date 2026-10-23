
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
        "The experiment showed that advertising increased purchases overall. "
        "But does it work equally well for everyone? Uplift modeling helps "
        "identify users who are more likely to purchase because of advertising, "
        "so we can target ads more effectively."
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

    st.markdown(
        "**Why the top 10%?** We divided the 300,000 test users into "
        "10 equally sized groups based on predicted uplift and selected "
        "the highest-ranked group (30,000 users). "
        "The 10% cutoff was chosen as a starting point, "
        "not because it was proven to be optimal."
    )

    st.caption(
        "Predicted uplift ranks users by their estimated response to advertising. "
        "Observed lift is the actual difference between treatment and control."
    )

    # Load experiment results
    results = load_experiment_results()

    top = results.loc[
        results["segment"] == "Top 10% predicted uplift"
    ].iloc[0]

    control_rate = float(top["control_conversion_pct"])
    treatment_rate = float(top["treatment_conversion_pct"])
    lift = float(top["lift_pp"])
    lower = float(top["ci_lower_pp"])
    upper = float(top["ci_upper_pp"])

    # Test 1: Treatment effect within the top 10%
    st.subheader("💡 Test 1: Did Advertising Work in the Top 10%?")

    st.write(
        "We compared actual purchase rates between treatment and "
        "control users within the selected 30,000 users."
    )

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
        "**Yes. Advertising significantly increased conversions in the top 10%.** "
        f"The estimated lift represents about {lift * 10:.1f} additional purchases "
        "per 1,000 users assigned to treatment in this group. "
        "The confidence interval is entirely above zero."
    )

    # Test 2: Compare the top 10% with the remaining 90%
    st.subheader("🔎 Test 2: Did the Top 10% Benefit More?")

    st.write(
        "Test 1 showed that advertising worked for the top 10%. "
        "Now we compare its effect with the remaining 90% to see "
        "whether the model identified users who respond more strongly."
    )

    comparison = pd.DataFrame({
        "User group": ["Top 10%", "Other 90%"],
        "Conversion lift": ["+0.8234 pp", "+0.0191 pp"],
    })

    st.dataframe(
        comparison,
        hide_index=True,
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Difference in lift",
        "+0.8043 pp"
    )

    col2.metric(
        "95% confidence interval",
        "+0.3722 to +1.2365 pp"
    )

    col3.metric(
        "P-value",
        "0.000265"
    )

    st.caption(
        "Difference in lift = top 10% lift − other 90% lift."
    )

    st.write(
        "**Yes. The top 10% responded significantly more strongly to advertising.** "
        "The difference between the groups was statistically significant "
        "(p < 0.05), supporting the model's ability to identify users "
        "who benefit more from advertising."
    )

    # Business recommendation
    st.subheader("👤 What Does This Mean for the Business?")

    takeaway(
        "The uplift model identified users who responded significantly "
        "better to advertising. The top 10% showed a conversion lift "
        "of 0.82 percentage points, compared with just 0.02 percentage "
        "points for the remaining users."
    )

    st.write(
        "**Recommendation:** Prioritize this group for further targeting "
        "experiments. Focusing on users who benefit most could improve "
        "advertising efficiency. Before rollout, we should validate "
        "performance on new data and compare advertising costs with "
        "the value of additional purchases."
    )

    # Technical methodology
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
            "- **Test 1:** Two-sided two-proportion z-test and 95% confidence "
            "interval for conversion lift within the top 10%.\n"
            "- **Test 2:** Two-sided z-test comparing the treatment effects "
            "of the top 10% and remaining 90%, with a 95% confidence interval "
            "for the difference.\n"
            "- **Limitation:** The results support differences in advertising "
            "response on this test sample, but do not establish the "
            "most profitable targeting strategy.\n"
            "- **Next step:** Validate targeting performance using fresh "
            "data before deployment."
        )

    st.markdown(
        "[Criteo dataset documentation]"
        "(https://huggingface.co/datasets/criteo/criteo-uplift)"
    )
