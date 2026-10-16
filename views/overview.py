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
        title=" 🛒 What Turns a Visit into a Purchase?",
        subtitle=(
            "Understand where shoppers drop off and identify opportunities to improve purchase conversion."
        ),
        eyebrow="An e-commerce case study",
    )

    st.write(
        "This project analyzes the shopping journey from product view to "
        "purchase and proposes an experiment to improve the shopping "
        "experience. It also uses a separate advertising experiment "
        "to assess whether advertising increases purchases."
    )

    st.subheader(" 📊 Two datasets, two questions ")

    left, right = st.columns(2)

    with left:
        insight_card(
            "Google Analytics 4 (GA4) · Shopping behavior",
            "Follow the path to purchase",
            "This dataset contains anonymized activity from the "
            "Google Merchandise Store, an online shop selling "
            "Google-branded products. "
            "It covers 270,154 users and 4.3 million recorded "
            "actions across 92 days. "
            "We follow product views, cart additions, checkout, "
            "and purchases to identify where shoppers stop progressing.",
            height=250,
        )

    with right:
        insight_card(
            "Advertising experiment · Criteo",
            "Does advertising lead to more purchases?",
            "We analyze 1 million records from Criteo’s public "
            "advertising experiment dataset. It includes treatment "
            "and control groups, allowing us to estimate whether "
            "the advertising treatment increased purchases and "
            "explore which users responded more strongly. ",
            height=250,
        )

    st.subheader(" 💡  Highlights from the analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        insight_card(
            "01 · Shopping journey",
            " 🛒 Only about 18 in 100 sessions reach the cart",
            "The biggest drop-off occurs between viewing a product "
            "and adding it to the cart. This pattern appears "
            "across desktop, mobile, and tablet.",
            height=260,
        )

    with col2:
        insight_card(
            "02 · Advertising Results",
            f" 🧾 About About 11 additional purchases per 10,000 users",
            "In the analyzed sample, the advertising group had a "
            "higher purchase rate than the control group. "
            "The difference was statistically significant.",
            height=260,
        )

    with col3:
        insight_card(
            "03 · Targeting opportunity",
            " 👤 Conversion lift differs across user segments",
            "The model ranked users by their predicted response "
            "to advertising. The top 10% showed an estimated "
            "82 additional purchases per 10,000 users, "
            "compared with 11 overall. ",
            height=260,
        )

    st.subheader("⏩ What's next?")

    product_tab, advertising_tab = st.tabs(
        ["Product experience", "Advertising value"]
    )

    with product_tab:
        st.markdown("#### Test clearer product-page information")

        st.write(
             "- Test whether clearer shipping and return information "
             "near *Add to Cart* helps first-time product viewers "
            "complete a purchase."
        )

        left, right = st.columns(2)

        with left:
            insight_card(
                "Proposed test · Not yet run",
                "Compare two page versions",
                "Randomly assign users to the current or revised "
                "page and compare purchase conversion.",
                height=220,
            )

        with right:
            insight_card(
                "Planning estimate",
                "24,696 participants",
                "12,348 users per group. Estimated experiment duration: "
                "about 45 days, plus purchase follow-up, ",
                height=220,
            )

    with advertising_tab:
        st.markdown("#### Compare advertising strategies")

        st.write(
            "- Compare advertising costs and additional purchases "
            "from targeting the model’s top-ranked 10% versus all "
            "users. Determine which approach generates more profit."
        )

    with st.expander("See the numbers and methodology"):
        st.markdown("#### Shopping journey")

        st.markdown(
            f"- **Reach the cart:** {min_cart_rate:.1f}%–"
            f"{max_cart_rate:.1f}% of product-view sessions.\n"
            f"- **Complete the full journey:** "
            f"{mobile_rate:.2f}% on mobile and "
            f"{desktop_rate:.2f}% on desktop."
        )

        st.write(
            "The full journey means viewing a product, adding to cart, "
            "starting checkout, and purchasing—in order within one session."
        )

        st.markdown("#### Proposed product-page experiment")

        st.markdown(
            "- **Comparison:** Randomly assign users equally to "
            "the current or revised page.\n"
            "- **Measure:** The percentage of assigned users who purchase.\n"
            "- **Planning baseline:** 3.36% purchase conversion.\n"
            "- **Improvement to detect:** From 3.36% to 4.03%—"
            "a 20% relative increase.\n"
            "- **Statistical settings:** 80% power, "
            "5% significance level, two-sided test."
        )

        st.markdown("#### Advertising results: all users")

        st.markdown(
            f"- **Control-group purchase rate:** "
            f"{overall['control_conversion_pct']:.3f}%.\n"
            f"- **Advertising-group purchase rate:** "
            f"{overall['treatment_conversion_pct']:.3f}%.\n"
            f"- **Estimated impact:** "
            f"{overall['lift_pp'] * 100:+.0f} purchases "
            "per 10,000 users.\n"
            f"- **95% confidence interval:** "
            f"{overall['ci_lower_pp'] * 100:+.0f} to "
            f"{overall['ci_upper_pp'] * 100:+.0f} purchases "
            "per 10,000 users."
        )

        st.markdown("#### Advertising results: top-ranked 10%")

        st.write(
            "Users ranked highest by their predicted response "
            "to advertising:"
        )

        st.markdown(
            f"- **Estimated impact:** "
            f"{top['lift_pp'] * 100:+.0f} purchases "
            "per 10,000 users.\n"
            f"- **95% confidence interval:** "
            f"{top['ci_lower_pp'] * 100:+.0f} to "
            f"{top['ci_upper_pp'] * 100:+.0f} purchases "
            "per 10,000 users."
        )

        st.caption(
            "1 million records analyzed: 700,000 for model training "
            "and 300,000 for testing. The top-ranked group includes "
            "30,000 test records."
        )
