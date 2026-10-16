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
            "Google Analytics  (GA4) dataset . Shopping behavior",
            "Follow the path to purchase",
            "This dataset contains anonymized activity from visitors "
            "to the Google Merchandise Store, an online shop selling "
            "Google-branded products. It records actions such as viewing "
            "products, adding items to a cart, starting checkout, and "
            "purchasing. We use these records to identify where shoppers "
            "stop progressing toward a purchase. ",
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
        st.markdown("#### Store funnel")

        st.write(
            f"Product-view-to-cart rates: {min_cart_rate:.2f}%–"
            f"{max_cart_rate:.2f}%. The funnel follows product view, "
            "cart, checkout, and purchase in order within one session."
        )

        st.write(
            f"Full-funnel completion: mobile {mobile_rate:.2f}%; "
            f"desktop {desktop_rate:.2f}%."
        )

        st.markdown("#### Proposed product-page experiment")

        st.write(
            "**Design:** User-level random assignment, split 50/50.  \n"
            "**Baseline:** 3.36% purchase conversion.  \n"
            "**Detectable improvement:** 20% relative, "
            "equivalent to 4.032% conversion.  \n"
            "**Statistical assumptions:** 80% power; "
            "5% significance level; two-sided test."
        )

        st.markdown("#### Overall advertising result")

        st.write(
            f"**Control:** {overall['control_conversion_pct']:.4f}%  \n"
            f"**Treatment:** "
            f"{overall['treatment_conversion_pct']:.4f}%  \n"
            f"**Lift:** {overall['lift_pp']:+.4f} percentage points  \n"
            f"**95% confidence interval:** "
            f"{overall['ci_lower_pp']:+.4f} to "
            f"{overall['ci_upper_pp']:+.4f} percentage points"
        )

        st.markdown("#### Highest-ranked 10%")

        st.write(
            f"**Estimated lift:** "
            f"{top['lift_pp']:+.4f} percentage points  \n"
            f"**95% confidence interval:** "
            f"{top['ci_lower_pp']:+.4f} to "
            f"{top['ci_upper_pp']:+.4f} percentage points"
        )

        st.caption(
            "1 million records analyzed; 700,000 used for training "
            "and 300,000 for testing. The top-ranked group contains "
            "30,000 test records."
        )
