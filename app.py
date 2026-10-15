from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="E-commerce Product Analytics",
    page_icon="📊",
    layout="wide",
)

DATA_DIR = Path(__file__).parent / "data"

st.title("E-commerce Product Analytics & Experimentation")
st.write(
    "Exploring shopping behavior with GA4 data and "
    "advertising treatment effects with Criteo data."
)

section = st.sidebar.radio(
    "Report sections",
    [
        "Overview",
        "Product Analytics",
        "Experiment Design",
        "Experiment Results",
        "Uplift Modeling",
    ],
)

st.header(section)


if section == "Overview":
    st.subheader("Executive summary")

    st.write(
        "This project investigates where shoppers leave an e-commerce "
        "purchase funnel, proposes a product experiment, and separately "
        "evaluates advertising effectiveness using randomized data."
    )

    st.subheader("1. Product opportunity — GA4")

    st.write(
        "The largest funnel drop-off occurs between product view and "
        "Add to Cart: only 17.88%–18.93% of product-view sessions reach "
        "the cart stage across device groups. Mobile full-funnel "
        "completion is 3.77%, compared with 3.50% on desktop."
    )

    st.write(
        "**Recommendation:** Test clearer shipping estimates, return "
        "information, and reassurance near Add to Cart for first-time "
        "product viewers. These are hypotheses to test; the funnel "
        "does not establish the cause of drop-off."
    )

    st.subheader("2. Proposed experiment")

    st.write(
        "Randomize eligible users 50/50 between the existing product "
        "page and the revised page. The design uses a 3.36% baseline "
        "purchase conversion rate and a 20% relative minimum detectable "
        "effect, with 80% power and a 5% significance level."
    )

    st.write(
        "**Planned sample:** 24,696 users total "
        "(12,348 per group), requiring approximately 45 days of "
        "recruitment under the earlier traffic estimate. "
        "This experiment has not been run."
    )

    st.subheader("3. Advertising effectiveness — Criteo")

    st.write(
        "In the separate randomized advertising analysis, conversion "
        "increased from 0.1876% in control to 0.2988% in treatment: "
        "an absolute lift of 0.1112 percentage points "
        "(95% CI: 0.0864–0.1360 percentage points)."
    )

    st.write(
        "For the top 10% of test-set users ranked by predicted uplift, "
        "the estimated treatment effect was 0.8234 percentage points "
        "(95% CI: 0.3917–1.2552 percentage points)."
    )

    st.write(
        "**Recommendation:** Evaluate the selected group's advertising "
        "costs and incremental conversion value before deployment. "
        "A positive conversion effect alone does not establish "
        "profitability or an optimal targeting strategy."
    )

    st.subheader("Explore the report")

    st.write(
        "- **Product Analytics:** Filter the session funnel by device.\n"
        "- **Experiment Design:** Review the proposed test and sample size.\n"
        "- **Experiment Results:** Inspect the overall advertising effect.\n"
        "- **Uplift Modeling:** Review the selected high-uplift group."
    )


elif section == "Product Analytics":
    funnel = pd.read_csv(DATA_DIR / "funnel_by_device.csv")

    st.subheader("Shopping funnel by device")

    device = st.selectbox(
        "Choose a device",
        funnel["device_category"].tolist(),
        format_func=str.title,
    )

    row = funnel.loc[funnel["device_category"] == device].iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Product-view sessions",
        f"{int(row['view_sessions']):,}",
    )
    col2.metric(
        "Full-funnel purchase sessions",
        f"{int(row['purchase_sessions']):,}",
    )
    col3.metric(
        "View-to-purchase rate",
        f"{row['overall_conversion_rate']:.2f}%",
    )

    stages = ["Product view", "Add to cart", "Checkout", "Purchase"]
    counts = [
        int(row["view_sessions"]),
        int(row["cart_sessions"]),
        int(row["checkout_sessions"]),
        int(row["purchase_sessions"]),
    ]

    fig, ax = plt.subplots(figsize=(8, 4))

    bars = ax.barh(stages, counts, color="#2563EB")
    ax.invert_yaxis()
    ax.bar_label(
        bars,
        labels=[f"{count:,}" for count in counts],
        padding=5,
    )
    ax.set_xlim(0, max(counts) * 1.2)
    ax.set_xlabel("Sessions")
    ax.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Step conversion rates")

    rates = pd.DataFrame({
        "Transition": [
            "Product view → Add to cart",
            "Add to cart → Checkout",
            "Checkout → Purchase",
        ],
        "Conversion rate": [
            f"{row['view_to_cart_rate']:.2f}%",
            f"{row['cart_to_checkout_rate']:.2f}%",
            f"{row['checkout_to_purchase_rate']:.2f}%",
        ],
    })
    st.dataframe(rates, hide_index=True)

    st.subheader("Key findings across devices")

    st.write(
        "**The largest drop-off occurs between product view and "
        "Add to Cart.** Only 17.88%–18.93% of product-view sessions "
        "reach the cart stage across the three device groups."
    )

    st.write(
        "**Mobile does not underperform desktop in this funnel.** "
        "Full-funnel completion is 3.77% on mobile versus 3.50% "
        "on desktop. These are descriptive comparisons; they do "
        "not establish that device type causes the difference."
    )

    st.write(
        "**Proposed next action:** Test clearer shipping estimates "
        "and return information near Add to Cart for first-time "
        "product viewers. The funnel identifies where to investigate; "
        "it does not establish why visitors leave."
    )

    st.caption(
        "These findings summarize all three device groups and remain "
        "the same when the device selector changes. The proposed "
        "first-time-visitor experiment targets a narrower population "
        "than this device-level funnel."
    )

    st.caption(
        "Source: GA4 BigQuery analysis, 05_funnel_by_device. "
        "Ordered, same-session funnel: product view → add to cart → "
        "checkout → purchase. Each step must occur strictly after the "
        "previous step within the same user/session. "
        "Counts represent sessions, not unique users. "
        "Conversion is the share of product-view sessions completing "
        "all four steps. Steps are not matched by product."
    )


elif section == "Experiment Design":
    st.subheader("Proposed test: product-page reassurance")

    st.info(
        "This is a proposed experiment informed by GA4 analysis. "
        "It has not been run."
    )

    st.write(
        "**Hypothesis:** Clearer shipping estimates, visible return "
        "information, and reassurance near Add to Cart will increase "
        "purchase conversion among first-time visitors viewing a product."
    )

    st.write("**Control:** Existing product page.")

    st.write(
        "**Treatment:** Product page with shipping estimates, "
        "return-policy visibility, and purchase reassurance."
    )

    st.write(
        "**Assignment:** Randomize eligible users 50/50 between groups."
    )

    st.write("**Primary metric:** User-level purchase conversion.")

    design = pd.DataFrame({
        "Planning parameter": [
            "Baseline conversion",
            "Minimum detectable effect (relative)",
            "Corresponding treatment conversion",
            "Absolute effect",
            "Significance level",
            "Statistical power",
            "Required users per group",
            "Required users total",
            "Estimated recruitment duration",
        ],
        "Value": [
            "3.36%",
            "20%",
            "4.032%",
            "+0.672 percentage points",
            "5%",
            "80%",
            "12,348",
            "24,696",
            "Approximately 45 days (6.4 weeks)",
        ],
    })
    st.dataframe(design, hide_index=True)

    st.caption(
        "The MDE is a planning choice, not a predicted result. "
        "Duration is the earlier traffic-based planning estimate; "
        "actual recruitment time depends on eligible traffic."
    )

    st.subheader("Proposed guardrails")

    st.write(
        "- Bounce and engagement\n"
        "- Page performance\n"
        "- Refunds and returns, if available"
    )

    st.caption(
        "This design uses a user-level metric. The Product Analytics "
        "funnel separately reports ordered, same-session completion. "
        "Criteo advertising results do not evaluate this proposed change."
    )


elif section == "Experiment Results":
    results = pd.read_csv(DATA_DIR / "experiment_results.csv")
    overall = results.loc[results["segment"] == "Overall"].iloc[0]

    st.subheader("Did advertising increase conversion?")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Control conversion",
        f"{overall['control_conversion_pct']:.4f}%",
    )
    col2.metric(
        "Treatment conversion",
        f"{overall['treatment_conversion_pct']:.4f}%",
    )
    col3.metric(
        "Absolute lift",
        f"{overall['lift_pp']:+.4f} percentage points",
    )

    st.write(
        f"**95% confidence interval:** "
        f"{overall['ci_lower_pp']:+.4f} to "
        f"{overall['ci_upper_pp']:+.4f} percentage points."
    )

    st.write(
        "The estimated overall effect is positive, and the confidence "
        "interval excludes zero. A rollout decision also requires "
        "advertising costs and the value of incremental conversions."
    )

    st.caption(
        "Source: completed Criteo analysis. Displayed values are rounded. "
        "Segment results will be covered under Uplift Modeling."
    )

    st.subheader("Conversion by experiment group")

    rates = [
        overall["control_conversion_pct"],
        overall["treatment_conversion_pct"],
    ]

    fig, ax = plt.subplots(figsize=(7, 3.5))

    bars = ax.bar(
        ["Control", "Treatment"],
        rates,
        color=["#94A3B8", "#2563EB"],
        width=0.5,
    )
    ax.bar_label(
        bars,
        labels=[f"{rate:.4f}%" for rate in rates],
        padding=5,
    )
    ax.set_ylabel("Conversion rate (%)")
    ax.set_ylim(0, max(rates) * 1.25)
    ax.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


elif section == "Uplift Modeling":
    results = pd.read_csv(DATA_DIR / "experiment_results.csv")
    top = results.loc[
        results["segment"] == "Top 10% predicted uplift"
    ].iloc[0]

    st.subheader("Who benefits most from treatment?")

    st.write(
        "A T-learner estimates conversion probability under treatment "
        "and under control. The difference is the predicted uplift. "
        "Users in the test set were ranked by this score, and the "
        "highest-scoring 10% were evaluated as a group."
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Top 10%: control conversion",
        f"{top['control_conversion_pct']:.4f}%",
    )
    col2.metric(
        "Top 10%: treatment conversion",
        f"{top['treatment_conversion_pct']:.4f}%",
    )

    st.metric(
        "Estimated treatment effect in this group",
        f"{top['lift_pp']:+.4f} percentage points",
    )

    st.write(
        f"**95% confidence interval:** "
        f"{top['ci_lower_pp']:+.4f} to "
        f"{top['ci_upper_pp']:+.4f} percentage points."
    )

    st.write(
        "**Interpretation:** The estimated effect corresponds to about "
        "8.2 additional conversions per 1,000 treated users in this "
        "selected group."
    )

    st.write(
        "**Business implication:** This group is a candidate for "
        "targeted advertising. Profitability and whether targeting "
        "outperforms broader deployment still require evaluation."
    )

    st.caption(
        "The top 10% refers to predicted uplift rank, not a 10% "
        "conversion probability. Effects are estimated for the group; "
        "individual treatment effects are not directly observed."
    )


st.caption(
    "GA4 and Criteo are separate datasets. "
    "The Criteo experiment does not test changes to the GA4 store."
)

if section in ["Overview", "Experiment Results", "Uplift Modeling"]:
    st.info(
        "Dataset limitation: Criteo non-uniformly subsampled the public "
        "dataset to conceal original advertising incrementality. "
        "These results describe the public benchmark and should not "
        "be interpreted as actual advertiser lift or production ROI."
    )

    st.caption(
        "Overall results use the 1,000,000-row sample. "
        "Uplift evaluation uses the 300,000-row test set; "
        "the top decile contains 30,000 users. "
        "A positive effect in that group alone does not prove that "
        "targeting it outperforms other targeting policies."
    )
