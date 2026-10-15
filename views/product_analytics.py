import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from shared.data import load_funnel
from shared.styling import page_header, takeaway


def render():
    page_header(
        title="Where does the shopping journey slow down?",
        subtitle=(
            "Follow shoppers from their first product view "
            "to a completed purchase."
        ),
        eyebrow="Product analytics · GA4",
    )

    funnel = load_funnel()

    st.write(
        "A shopper views a product, adds it to their cart, starts "
        "checkout, and purchases. How many shopping sessions make "
        "it from one step to the next?"
    )

    st.caption(
        "We follow these steps in order within the same session. "
        "One person can have multiple sessions."
    )

    st.subheader("📊 Follow the shopping journey")

    device = st.selectbox(
        "Choose a device",
        funnel["device_category"].tolist(),
        format_func=str.title,
        key="product_device",
    )

    row = funnel.loc[
        funnel["device_category"] == device
    ].iloc[0]

    stages = [
        "Product view",
        "Add to cart",
        "Checkout",
        "Purchase",
    ]

    counts = [
        int(row["view_sessions"]),
        int(row["cart_sessions"]),
        int(row["checkout_sessions"]),
        int(row["purchase_sessions"]),
    ]

    cart_rate = float(row["view_to_cart_rate"])
    checkout_rate = float(row["cart_to_checkout_rate"])
    purchase_rate = float(row["checkout_to_purchase_rate"])

    st.markdown(f"#### {device.title()}: from product view to purchase")

    fig, ax = plt.subplots(figsize=(9, 3.8))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    bars = ax.barh(
        stages,
        counts,
        color=["#172B4D", "#2563EB", "#087F8C", "#38B2AC"],
        height=0.6,
    )

    ax.invert_yaxis()
    ax.bar_label(
        bars,
        labels=[f"{count:,}" for count in counts],
        padding=6,
        fontsize=10,
    )
    ax.set_xlim(0, max(counts) * 1.23)
    ax.set_xlabel("Sessions", color="#52627A")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    st.caption(
        "Each bar includes only sessions that completed all earlier "
        "steps in order. Purchase counts therefore exclude purchases "
        "that followed a different path."
    )

    # Identify the largest proportional drop-off for the selected device.
    transitions = [
        {
            "name": "Product view → Add to cart",
            "rate": cart_rate,
            "location": "between viewing a product and adding it to the cart",
        },
        {
            "name": "Add to cart → Checkout",
            "rate": checkout_rate,
            "location": "between adding to the cart and starting checkout",
        },
        {
            "name": "Checkout → Purchase",
            "rate": purchase_rate,
            "location": "between starting checkout and completing a purchase",
        },
    ]

    largest_drop = min(
        transitions,
        key=lambda transition: transition["rate"],
    )

    st.subheader("What stands out?")

    takeaway(
        f"For every 100 {device} sessions with a product view, "
        f"about {cart_rate:.0f} reach Add to Cart. "
        f"About {row['overall_conversion_rate']:.1f} complete "
        "the full journey to purchase."
    )

    st.write(
        f"The largest proportional drop-off is "
        f"{largest_drop['location']}: "
        f"{100 - largest_drop['rate']:.1f}% of sessions reaching "
        "that stage do not progress to the next step."
    )

    st.caption(
        "This shows where sessions stop progressing, but does not "
        "explain why. Shoppers may continue browsing, return later, "
        "or purchase through a different path."
    )

    with st.expander("Does this pattern differ by device?"):
        st.write(
            "Compare the share of product-view sessions that "
            "complete all four steps on each device."
        )

        fig, ax = plt.subplots(figsize=(7, 3.5))
        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FFFFFF")

        device_rates = funnel["overall_conversion_rate"].tolist()

        bars = ax.bar(
            funnel["device_category"].str.title(),
            device_rates,
            color="#087F8C",
            width=0.5,
        )

        ax.bar_label(
            bars,
            labels=[f"{rate:.2f}%" for rate in device_rates],
            padding=6,
        )
        ax.set_ylim(0, max(device_rates) * 1.25)
        ax.set_ylabel("Full-funnel completion (%)")
        ax.spines[["top", "right"]].set_visible(False)
        fig.tight_layout()

        st.pyplot(fig)
        plt.close(fig)

        desktop_rate = funnel.loc[
            funnel["device_category"] == "desktop",
            "overall_conversion_rate",
        ].iloc[0]

        mobile_rate = funnel.loc[
            funnel["device_category"] == "mobile",
            "overall_conversion_rate",
        ].iloc[0]

        takeaway(
            f"Mobile completion is {mobile_rate:.2f}%, compared "
            f"with {desktop_rate:.2f}% on desktop."
        )

        st.caption(
            "These are observed differences. They do not establish "
            "that the device itself causes the difference."
        )

    st.subheader("💡 What could we test?")

    min_cart_rate = funnel["view_to_cart_rate"].min()
    max_cart_rate = funnel["view_to_cart_rate"].max()

    st.write(
        f"Across devices, {min_cart_rate:.2f}%–"
        f"{max_cart_rate:.2f}% of product-view sessions reach "
        "Add to Cart. This makes the product page a useful "
        "place to investigate."
    )

    st.write(
        "One idea is to make shipping estimates, return information, "
        "and purchase reassurance easier to find near Add to Cart. "
        "The proposed experiment would test whether this helps "
        "first-time product viewers complete a purchase."
    )

    st.caption(
        "Shipping or return uncertainty is a hypothesis, not an "
        "established cause of drop-off. The proposed experiment "
        "focuses on a narrower group than the session funnel shown "
        "here. This recommendation remains the same when you "
        "change the device selector."
    )

    st.markdown(
        "**Next: Experiment Design** — See how the proposed change "
        "would be tested and how success would be measured."
    )

    with st.expander("See the selected device's numbers"):
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
            "Full-funnel completion",
            f"{row['overall_conversion_rate']:.2f}%",
        )

        st.caption(
            "Full-funnel completion is the share of product-view "
            "sessions that complete all four steps in order."
        )

        st.markdown("#### Conversion between steps")

        rates = pd.DataFrame({
            "Transition": [
                transition["name"]
                for transition in transitions
            ],
            "Progress to next step": [
                f"{transition['rate']:.2f}%"
                for transition in transitions
            ],
            "Do not progress": [
                f"{100 - transition['rate']:.2f}%"
                for transition in transitions
            ],
        })

        st.dataframe(rates, hide_index=True)

        st.caption(
            "Each transition uses sessions reaching its starting "
            "stage as the denominator. For example, checkout-to-"
            "purchase conversion counts only sessions that reached "
            "checkout through the earlier funnel steps."
        )

    with st.expander("How this funnel is defined"):
        st.markdown(
            "- **Source:** GA4 BigQuery analysis.\n"
            "- **Unit:** Sessions, not unique users. A user may "
            "contribute more than one session.\n"
            "- **Order:** Product view → Add to cart → Checkout → "
            "Purchase. Each event must occur strictly after the "
            "previous step.\n"
            "- **Session boundary:** All four steps must occur "
            "within the same user/session combination.\n"
            "- **Purchase count:** Only purchases completing the "
            "entire funnel are included—not all store purchases.\n"
            "- **Product matching:** Steps are not matched by product.\n"
            "- **Overall conversion:** Full-funnel purchase sessions "
            "divided by product-view sessions."
        )

        st.write(
            "Not progressing in this funnel does not necessarily "
            "mean a visitor never purchases. They could purchase "
            "in a later session or follow a different path."
        )

    with st.expander("View the exported data"):
        st.dataframe(funnel, hide_index=True)
