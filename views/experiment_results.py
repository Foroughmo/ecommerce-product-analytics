
import streamlit as st

from shared.data import load_experiment_results
from shared.styling import insight_card, page_header, takeaway


def render():
    page_header(
        title="Does Advertising Actually Increase Conversions?",
        subtitle=(
            "Analyzing a real randomized experiment to measure "
            "whether advertising targeting leads to more conversions."
        ),
        eyebrow="Experiment results · Criteo",
    )

    # Load experiment results
    results = load_experiment_results()
    overall = results.loc[results["segment"] == "Overall"].iloc[0]

    control_rate = float(overall["control_conversion_pct"])
    treatment_rate = float(overall["treatment_conversion_pct"])
    lift = float(overall["lift_pp"])
    lower = float(overall["ci_lower_pp"])
    upper = float(overall["ci_upper_pp"])

    relative_lift = lift / control_rate * 100 if control_rate else 0

    # Section 1: Experiment setup
    st.subheader("⚒️ How was the experiment conducted?")

    st.write(
        "We analyzed 1 million users from Criteo's randomized "
        "advertising experiments, comparing two groups:"
    )

    left, right = st.columns(2)

    with left:
        insight_card(
            "Control Group · 149,825 Users",
            "No advertising targeting",
            "These users were excluded from advertising "
            "targeting, providing a baseline for comparison.",
            height=170,
        )

    with right:
        insight_card(
            "Treatment Group · 850,175 Users",
            "Eligible for advertising",
            "These users were eligible to receive ads, "
            "allowing us to measure whether advertising "
            "increased conversions.",
            height=170,
        )

    with st.expander("Why are the group sizes different?"):
        st.write(
            "The Criteo dataset contains approximately 85% treatment "
            "users and 15% control users. We preserved this distribution "
            "in our sample. A/B tests do not require equal group sizes, "
            "and the statistical analysis accounts for the difference."
        )

    
    # Section 2: Results
    st.subheader("🔎 Did advertising make a difference?")

    left, right = st.columns(2)

    with left:
        st.metric(
            "Control conversion rate",
            f"{control_rate:.3f}%"
        )

    with right:
        st.metric(
            "Treatment conversion rate",
            f"{treatment_rate:.3f}%"
        )

    st.markdown(
        f"**{relative_lift:+.1f}% higher conversion rate** "
        "for users eligible for advertising — approximately "
        f"**{lift * 100:.0f} additional conversions per 10,000 users**."
    )

    
    
    # Section 3: Statistical and business significance
    st.subheader("📊 Statistical and Practical Significance")

    left, right = st.columns(2)

    with left:
        insight_card(
            "Statistical Significance",
            "Strong evidence of a positive effect",
            (
                "P-value < 0.001. The 95% confidence interval "
                f"ranges from +{lower:.4f} to +{upper:.4f} "
                "percentage points, excluding zero."
            ),
            height=190,
        )

    with right:
        insight_card(
            "Business Significance",
            f"+{lift * 1000:.0f} conversions per 100K users",
            (
                "Advertising generates additional conversions "
                "at scale. Profitability depends on whether "
                "their value exceeds advertising costs."
            ),
            height=190,
        )

    
    # Section 4: Business recommendation
    st.subheader("💡 Business takeaway")

    takeaway(
            "Recommendation: Consider scaling advertising, "
            "subject to confirming that incremental conversion value "
            "exceeds advertising costs and key guardrails remain stable."
        )

    # Section 5: Technical details
    with st.expander("Statistical methodology"):
        st.markdown(
            "- **Dataset:** Criteo advertising experiment, "
            "1 million sampled users.\n"
            "- **Treatment effect:** Difference in conversion rates "
            "between users assigned to treatment and control, "
            "regardless of actual ad exposure.\n"
            "- **Absolute lift:** "
            f"{lift:+.4f} percentage points.\n"
            "- **Relative lift:** "
            f"{relative_lift:+.1f}%.\n"
            "- **95% confidence interval:** "
            f"{lower:+.4f} to {upper:+.4f} percentage points.\n"
            "- **Hypothesis test:** Two-sided two-proportion z-test "
            "(α = 0.05; p ≈ 7.24 × 10⁻¹⁴).\n"
            "- **Confidence interval method:** Normal approximation.\n"
            "- **Group sizes:** The analysis accounts for unequal "
            "numbers of users in the two groups."
        )

    st.markdown(
        "[Criteo dataset documentation]"
        "(https://huggingface.co/datasets/criteo/criteo-uplift)"
    )
