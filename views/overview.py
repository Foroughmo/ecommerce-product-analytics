import streamlit as st

from shared.data import load_experiment_results, load_funnel
from shared.styling import insight_card, page_header, takeaway


def render():
    funnel = load_funnel()
    results = load_experiment_results()

    overall = results.loc[
        results["segment"] == "Overall"
    ].iloc[0]

    top = results.loc[
        results["segment"] == "Top 10% predicted uplift"
    ].iloc[0]

    min_cart_rate = funnel["view_to_cart_rate"].min()
    max_cart_rate = funnel["view_to_cart_rate"].max()

    desktop_rate = funnel.loc[
        funnel["device_category"] == "desktop",
        "overall_conversion_rate",
    ].iloc[0]

    mobile_rate = funnel.loc[
        funnel["device_category"] == "mobile",
        "overall_conversion_rate",
    ].iloc[0]

    extra_purchases = overall["lift_pp"] * 100

    page_header(
        title="From Browsing to Buying",
        subtitle=(
            "Where do shoppers leave and what could help "
            "more of them become customers?"
        ),
        eyebrow="An e-commerce case study",
    )

    st.write(
        "Getting people to visit a store is only part of the challenge. "
        "They still need to find something they want, add it to their "
        "cart, and complete a purchase. This project follows that "
        "journey, identifies an opportunity to improve it, and "
        "outlines how to test whether a change makes a difference."
    )

    st.subheader("A first look at the data")

    left, right = st.columns(2)

    with left:
        insight_card(
            "Shopping behavior · Google Analytics",
            "Follow the path to purchase",
            "Public sample data from the Google Merchandise Store "
            "captures product views, cart additions, checkout, and "
            "purchases. The analysis follows these steps within a "
            "shopping session and compares results across devices.",
            height=300,
        )

    with right:
        insight_card(
            "Advertising experiment · Criteo",
            "Measure what advertising changes",
            "A sample of 1 million records from a public advertising "
            "experiment lets us compare purchase rates between "
            "people assigned to an advertising treatment and "
            "a control group.",
            height=300,
        )

    st.caption(
        "These datasets come from different businesses. "
        "The store data helps identify a product opportunity; "
        "the advertising data provides a separate experiment "
        "to analyze."
        height=300,
    )

    st.subheader("What stood out")

    col1, col2, col3 = st.columns(3)

    with col1:
        insight_card(
            "01 · The shopping journey",
            "Most product views stop before the cart",
            f"Across devices, only {min_cart_rate:.1f}–"
            f"{max_cart_rate:.1f}% of sessions with a product view "
            "continue to Add to Cart. This is the largest drop-off "
            "in the measured journey.",
        )

    with col2:
        insight_card(
            "02 · The advertising experiment",
            f"About {extra_purchases:.0f} extra purchases per 10,000",
            "The advertising treatment increased conversion "
            "compared with control in the analyzed sample. "
            "The estimated difference is statistically significant.",
        )

    with col3:
        insight_card(
            "03 · Differences between shoppers",
            "Some shoppers may respond more strongly",
            "The 10% ranked highest by the model had an estimated "
            f"conversion increase of {top['lift_pp']:.2f} percentage "
            "points on held-out data. This is a reason to "
            "investigate targeting further.",
        )

    st.subheader("What should the team do next?")

    product_tab, advertising_tab = st.tabs(
        ["Improve the product experience", "Evaluate advertising value"]
    )

    with product_tab:
        st.markdown("#### Give shoppers more clarity before they add to cart")

        st.write(
            "Test whether clearer shipping estimates, return "
            "information, and purchase reassurance near Add to Cart "
            "help first-time product viewers complete a purchase."
        )

        st.write(
            "The drop-off tells us where to investigate. It does "
            "not tell us why people leave. This proposed test would "
            "check whether clearer information helps them decide."
        )

        left, right = st.columns(2)

        with left:
            insight_card(
                "Proposed test · Not yet run",
                "Compare two product-page experiences",
                "Keep the current page for one group and show "
                "clearer purchase information to the other. "
                "Compare the share of users who purchase.",
            )

        with right:
            insight_card(
                "Initial planning estimate",
                "24,696 participants",
                "12,348 users per group. Recruitment is estimated "
                "at about 45 days, subject to confirming eligible "
                "traffic and the purchase measurement window.",
            )

        takeaway(
            f"Mobile full-funnel completion is {mobile_rate:.2f}%, "
            f"compared with {desktop_rate:.2f}% on desktop. "
            "This difference also deserves investigation."
        )

    with advertising_tab:
        st.markdown("#### Check whether the extra purchases justify the cost")

        st.write(
            "The advertising treatment increased purchases in "
            "this benchmark. A business decision would also need "
            "to account for the cost of advertising and the "
            "value of each additional purchase."
        )

        st.write(
            "The model also identifies a group with a larger "
            "estimated response. Before using that group for "
            "targeting, compare alternative strategies and "
            "check whether the results hold on new data."
        )

        takeaway(
            "The results support further evaluation. They do not "
            "yet show that advertising is profitable or that "
            "targeting the highest-ranked 10% is the best strategy."
        )

        st.caption(
            "Criteo altered the public sample through non-uniform "
            "subsampling to conceal the original advertising "
            "effect. These estimates describe the benchmark, "
            "not the advertiser's original business results."
        )

    with st.expander("See the numbers and how they were calculated"):
        st.markdown("#### Store funnel")

        st.write(
            f"Product-view-to-cart rates range from "
            f"{min_cart_rate:.2f}% to {max_cart_rate:.2f}%. "
            "The funnel counts sessions, not unique people. "
            "Full-funnel completion requires a product view, "
            "cart addition, checkout, and purchase, in that "
            "order within the same session."
        )

        st.markdown("#### Proposed product-page experiment")

        st.write(
            "Users would be randomly assigned equally between "
            "the two versions. Planning assumptions: 3.36% baseline "
            "purchase conversion; 20% relative minimum detectable "
            "improvement, equivalent to a target rate of 4.032%; "
            "80% power; and a two-sided 5% significance level."
        )

        st.caption(
            "The baseline source, eligible traffic, and purchase "
            "measurement window still need confirmation. "
            "The target improvement is a planning assumption, "
            "not a forecast."
        )

        st.markdown("#### Overall advertising result")

        st.write(
            f"Control conversion: "
            f"{overall['control_conversion_pct']:.4f}%. "
            f"Treatment conversion: "
            f"{overall['treatment_conversion_pct']:.4f}%. "
            f"Difference: {overall['lift_pp']:+.4f} percentage points. "
            f"95% confidence interval: "
            f"{overall['ci_lower_pp']:+.4f} to "
            f"{overall['ci_upper_pp']:+.4f} percentage points."
        )

        st.markdown("#### Highest-ranked 10%")

        st.write(
            f"Estimated conversion difference: "
            f"{top['lift_pp']:+.4f} percentage points. "
            f"95% confidence interval: "
            f"{top['ci_lower_pp']:+.4f} to "
            f"{top['ci_upper_pp']:+.4f} percentage points."
        )

        st.caption(
            "Overall analysis: 1,000,000 sampled records. "
            "Model training: 700,000 records. "
            "Held-out evaluation: 300,000 records. "
            "Highest-ranked group: 30,000 held-out records."
        )

    with st.expander("Where to explore next"):
        st.markdown(
            "- **Product Analytics:** Follow the shopping journey "
            "and compare devices.\n"
            "- **Experiment Design:** Review the proposed "
            "product-page test.\n"
            "- **Experiment Results:** See how advertising "
            "affected purchases.\n"
            "- **Uplift Modeling:** Explore who may respond "
            "most to advertising."
        )
