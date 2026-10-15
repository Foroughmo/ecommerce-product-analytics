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
    st.subheader("Can clearer product information help visitors buy?")

    st.info(
        "Proposed test — this experiment has not been run. "
        "This page explains what we would change and how we would "
        "evaluate whether it helps."
    )

    st.subheader("Why consider this change?")

    st.write(
        "Our shopping-funnel analysis found that the largest drop-off "
        "happens between viewing a product and adding it to the cart. "
        "Across devices, only about 18–19 out of every 100 product-view "
        "sessions reach Add to Cart."
    )

    st.write(
        "One possible explanation is uncertainty about shipping or "
        "returns. The data does not tell us whether this is the cause. "
        "An experiment would help us test that explanation."
    )

    st.subheader("What would visitors experience?")

    control_col, treatment_col = st.columns(2)

    with control_col:
        st.markdown("### A · Current experience")
        st.write("Visitors see the existing product page.")

    with treatment_col:
        st.markdown("### B · Proposed experience")
        st.write(
            "Visitors see the product page with:\n"
            "- Clearer shipping estimates\n"
            "- More visible return information\n"
            "- Purchase reassurance near Add to Cart"
        )

    st.write(
        "**Hypothesis:** Giving first-time product viewers clearer "
        "information will reduce uncertainty and increase the share "
        "who make a purchase."
    )

    st.subheader("How would we run the test?")

    st.write(
        "First-time visitors who view a product would be randomly "
        "assigned to one of the two experiences, with half in each "
        "group. Assignment would be at the user level, so a returning "
        "participant would continue to see the same version."
    )

    st.write(
        "**Main outcome:** The percentage of eligible users in each "
        "group who make a purchase. We would compare this percentage "
        "between the two groups."
    )

    st.subheader("What improvement are we planning to detect?")

    col1, col2, col3 = st.columns(3)

    col1.metric("Planning baseline", "3.36%")
    col2.metric("Detectable target", "4.032%")
    col3.metric("Absolute improvement", "+0.672 pp")

    st.write(
        "For every 1,000 eligible users, this means moving from about "
        "**34 purchasers to 40 purchasers**—roughly **7 additional "
        "purchasers**."
    )

    st.caption(
        "pp means percentage points. A 20% relative improvement on "
        "a 3.36% baseline equals a 0.672-percentage-point increase. "
        "This is a planning target, not a forecast or an observed result."
    )

    st.subheader("How many participants and how long?")

    col1, col2 = st.columns(2)
    col1.metric("Total participants needed", "24,696")
    col2.metric("Estimated recruitment", "About 45 days")

    st.write(
        "We need **12,348 users in each group**. At the notebook's "
        "planning estimate of **553.6 eligible users per day**, "
        "recruitment would take about **44.6 days, or 6.4 weeks**."
    )

    st.write(
        "Smaller improvements need more participants to distinguish "
        "them from random variation. The notebook compared several "
        "targets before selecting 20% as a practical planning compromise."
    )

    with st.expander("See the sample-size trade-off"):
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
            "These are alternative planning scenarios, not four "
            "separate experiments or predicted outcomes."
        )

    st.subheader("What else should we monitor?")

    st.write(
        "A higher purchase rate would not be enough if the change "
        "creates other problems. Proposed guardrails are:\n"
        "- **Bounce and engagement:** Are visitors leaving more quickly "
        "or engaging less?\n"
        "- **Page performance:** Does the revised page load more slowly?\n"
        "- **Refunds and returns:** Do these increase, if the data "
        "is available?"
    )

    st.subheader("How would we make a decision?")

    st.write(
        "After reaching the planned sample and allowing the purchase "
        "measurement window to finish, we would compare conversion "
        "rates, the uncertainty around the difference, and the "
        "guardrails. A rollout decision would consider both the "
        "strength of the evidence and the business value of the change."
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
                "44.6 days, approximately 6.4 weeks",
            ],
        })

        st.dataframe(design, hide_index=True)

        st.write(
            "**Minimum detectable effect (MDE):** The improvement "
            "used to plan the sample size. Smaller effects may exist "
            "even if this test cannot reliably detect them."
        )

        st.write(
            "**80% power:** If the true improvement equals the planned "
            "MDE and the assumptions hold, the test has about an 80% "
            "chance of detecting it."
        )

        st.write(
            "**5% significance level:** Under the test assumptions, "
            "when there is truly no effect, this procedure has a 5% "
            "false-positive rate."
        )

        st.write(
            "**Two-sided test:** The analysis allows for either an "
            "increase or a decrease in conversion."
        )

        st.caption(
            "Sample sizes were calculated with statsmodels "
            "NormalIndPower and proportion_effectsize, with equal "
            "allocation between groups."
        )

    with st.expander("Planning assumptions to confirm before launch"):
        st.write(
            "- Confirm the source and eligibility definitions behind "
            "the 3.36% baseline and 553.6 daily-user estimate.\n"
            "- Specify how long each assigned user has to purchase "
            "and align the baseline with that measurement window.\n"
            "- Define acceptable guardrail changes before the test.\n"
            "- Allow for outcome follow-up after recruitment; "
            "45 days is a recruitment estimate, not necessarily "
            "the total time until a final decision."
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


# Temporary preview of the redesigned pages
st.divider()

with st.expander("Preview the new design", expanded=False):
    preview_page = st.selectbox(
        "Choose a redesigned page",
        ["Overview", "Product Analytics", "Experiment Design"],
        key="design_preview_page",
    )

    show_preview = st.checkbox(
        "Show redesigned page",
        key="show_design_preview",
    )

    if show_preview:
        from shared.styling import apply_style

        apply_style()

        if preview_page == "Overview":
            from views.overview import render
        elif preview_page == "Product Analytics":
            from views.product_analytics import render
        else:
            from views.experiment_design import render

        render()
