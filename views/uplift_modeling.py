import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from shared.data import load_experiment_results
from shared.styling import insight_card, page_header, takeaway


def render():
    page_header(
        title="Who might benefit most from advertising?",
        subtitle=(
            "Explore whether a model can identify users whose "
            "purchase behavior is more likely to change under treatment."
        ),
        eyebrow="Uplift modeling · Criteo",
    )

    left, right = st.columns(2)

    with left:
        insight_card(
            "Ordinary purchase prediction",
            "Who is likely to buy?",
            "A likely buyer may purchase with or without advertising. "
            "High purchase probability alone does not tell us "
            "whether an ad changes their behavior.",
        )

    with right:
        insight_card(
            "Uplift prediction",
            "Whose behavior might change?",
            "Estimate purchase probability under treatment and "
            "under control. Their difference is predicted uplift.",
        )

    results = load_experiment_results()
    top = results.loc[
        results["segment"] == "Top 10% predicted uplift"
    ].iloc[0]

    control_rate = float(top["control_conversion_pct"])
    treatment_rate = float(top["treatment_conversion_pct"])
    effect = float(top["lift_pp"])
    lower = float(top["ci_lower_pp"])
    upper = float(top["ci_upper_pp"])
    extra_per_1000 = effect / 100 * 1000

    st.subheader("Results for the highest-ranked 10%")

    col1, col2, col3 = st.columns(3)
    col1.metric("Control conversion", f"{control_rate:.4f}%")
    col2.metric("Treatment conversion", f"{treatment_rate:.4f}%")
    col3.metric("Estimated effect", f"+{effect:.4f} pp")

    st.caption(
        "This group contains 30,000 users from the test set. "
        "pp means percentage points."
    )

    results_tab, method_tab, decision_tab = st.tabs(
        ["Segment results", "How the model works", "What this supports"]
    )

    with results_tab:
        chart_col, insight_col = st.columns([3, 2])

        with chart_col:
            st.subheader("Treatment versus control within this group")

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

        with insight_col:
            insight_card(
                "Illustrative interpretation",
                f"About {extra_per_1000:.1f} extra conversions",
                "Per 1,000 users assigned to treatment in this "
                "selected benchmark group. This rescales the "
                "observed difference; it is not a production forecast.",
            )

            insight_card(
                "95% confidence interval",
                f"+{lower:.4f} to +{upper:.4f} pp",
                "The approximate interval is entirely above zero. "
                "The two-sided z-test gives p ≈ 0.00115.",
            )

        takeaway(
            "The selected group shows a positive treatment–control "
            "difference. This alone does not prove that its effect "
            "is significantly larger than the effect in other groups."
        )

        with st.expander("See the verified segment counts"):
            counts = pd.DataFrame({
                "Group": ["Control", "Treatment"],
                "Users": [4228, 25772],
                "Conversions": [71, 645],
                "Conversion rate": [
                    f"{control_rate:.4f}%",
                    f"{treatment_rate:.4f}%",
                ],
            })
            st.dataframe(counts, hide_index=True)

            st.caption(
                "The confidence interval uses the unpooled normal "
                "standard error. The p-value comes from a two-sided "
                "two-proportion z-test."
            )

    with method_tab:
        st.subheader("Two models estimate two possible outcomes")

        left, right = st.columns(2)

        with left:
            insight_card(
                "Model 1 · Treatment",
                "Estimate purchase probability with treatment",
                "A logistic regression learns from users assigned "
                "to treatment in the training set.",
            )

        with right:
            insight_card(
                "Model 2 · Control",
                "Estimate purchase probability without treatment",
                "A separate logistic regression learns from "
                "control users in the training set.",
            )

        takeaway(
            "Predicted uplift = estimated purchase probability "
            "under treatment − estimated purchase probability "
            "under control."
        )

        st.subheader("How the top 10% was selected")

        st.write(
            "1. Split the 1,000,000-row sample into 700,000 training "
            "rows and 300,000 test rows.\n"
            "2. Fit the two models and their feature scalers using "
            "training data only.\n"
            "3. Predict both purchase probabilities for each test user.\n"
            "4. Rank test users by the difference between those "
            "probabilities.\n"
            "5. Divide the ranking into ten groups of 30,000 users.\n"
            "6. Compare observed treatment and control conversion "
            "within the highest-ranked group."
        )

        st.caption(
            "The top 10% refers to rank by predicted uplift, not "
            "a 10% purchase probability. Test outcomes are used "
            "for evaluation, not as inputs to the fitted models."
        )

        with st.expander("Model specifications"):
            specifications = pd.DataFrame({
                "Component": [
                    "Approach",
                    "Models",
                    "Features",
                    "Preprocessing",
                    "Train/test split",
                    "Split stratification",
                    "Random seed",
                    "Maximum solver iterations",
                    "Evaluation group",
                ],
                "Specification": [
                    "T-learner",
                    "Two logistic regressions",
                    "12 anonymized numeric features: f0–f11",
                    "Separate StandardScaler in each model pipeline",
                    "70% training / 30% test",
                    "Joint treatment assignment and conversion",
                    "42",
                    "1,000",
                    "Highest predicted-uplift decile in the test set",
                ],
            })
            st.dataframe(specifications, hide_index=True)

        st.write(
            "**Why anonymized features matter:** We can evaluate "
            "their predictive usefulness, but cannot identify "
            "business characteristics such as age or shopping "
            "preferences from feature names like f0 or f6."
        )

    with decision_tab:
        left, right = st.columns(2)

        with left:
            insight_card(
                "Supported finding",
                "A promising candidate segment",
                "Users ranked in the highest predicted-uplift decile "
                "show a positive treatment–control difference "
                "in the test sample.",
            )

        with right:
            insight_card(
                "Still unresolved",
                "The best targeting policy",
                "This analysis does not establish whether targeting "
                "10% is optimal, more profitable than broader "
                "deployment, or stable in a new population.",
            )

        st.subheader("Business recommendation")

        st.write(
            "Treat the segment as a candidate for further evaluation. "
            "A deployment decision requires advertising costs, "
            "incremental conversion value, and validation on new data."
        )

        st.write(
            "The 10% cutoff is an interpretable exploratory choice. "
            "If the cutoff or model is revised after examining test "
            "results, the revised policy needs fresh evaluation data."
        )

        takeaway(
            "Group effects are estimated from comparisons between "
            "different users. An individual user's treatment effect "
            "cannot be directly observed because we cannot observe "
            "both outcomes for that person."
        )

    with st.expander("Public benchmark limitations"):
        st.write(
            "Criteo non-uniformly subsampled the public dataset "
            "to conceal original advertising incrementality. "
            "These estimates describe the released benchmark, "
            "not actual advertiser lift or production ROI."
        )

        st.write(
            "Overall results elsewhere in this report use the full "
            "1,000,000-row sample. This page evaluates a selected "
            "30,000-user group within the 300,000-row test set."
        )

        st.markdown(
            "[Source: Criteo public dataset documentation]"
            "(https://huggingface.co/datasets/criteo/criteo-uplift)"
        )

    st.caption(
        "Source: completed Criteo analysis. Displayed values are "
        "rounded. This advertising benchmark is separate from "
        "the proposed GA4 product-page experiment."
    )
