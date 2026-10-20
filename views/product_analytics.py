import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from shared.data import load_funnel
from shared.styling import page_header, takeaway


def render():
    page_header(
        title="Where do shoppers drop off?",
        subtitle="Analyzing the shopping funnel from product view to purchase to identify key drop-off points.",
        eyebrow="Product analytics · GA4",
    )

    st.write(
        "The analysis tracks how many shopping sessions reach each "
        "stage of the funnel. Each session represents a store visit,"
        "and a user may have multiple sessions."
    )

    funnel = load_funnel()

    device = st.selectbox(
        "Choose a device",
        funnel["device_category"].tolist(),
        format_func=str.title,
        key="product_device",
    )

    row = funnel.loc[
        funnel["device_category"] == device
    ].iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Sessions with a product view",
        f"{int(row['view_sessions']):,}",
    )
    col2.metric(
        "Sessions completing the journey",
        f"{int(row['purchase_sessions']):,}",
    )
    col3.metric(
        "Journey completion rate",
        f"{row['overall_conversion_rate']:.2f}%",
    )

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
    ax.set_xlabel("Sessions")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    takeaway(
        f"About {cart_rate:.0f}% of {device} product-view sessions "
        f"reach the cart, and {row['overall_conversion_rate']:.1f}% "
        "complete the full purchase journey."
    )


    st.subheader("👥 New vs Returning Visitors")

    new_col, returning_col = st.columns(2)

    new_col.metric(
        "New visitors · Journey completion",
        "2.11%",
    )

    returning_col.metric(
        "Returning visitors · Journey completion",
        "6.53%",
    )

    st.write(
        "New-visitor sessions are less likely to complete the "
        "purchase journey. This supports investigating the "
        "experience for first-time visitors."
    )
    
    st.subheader("💡 What Could We Test?")

    st.write(
        "Test whether clearer shipping and return information "
        "near *Add to Cart* increases purchases."
    )

    with st.expander("Compare devices"):
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
        ax.set_ylabel("Journey completion (%)")
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

        st.write(
            f"Mobile: **{mobile_rate:.2f}%** · "
            f"Desktop: **{desktop_rate:.2f}%**."
        )

    with st.expander("See the numbers"):
        rates = pd.DataFrame({
            "Transition": [
                "Product view → Add to cart",
                "Add to cart → Checkout",
                "Checkout → Purchase",
            ],
            "Progress": [
                f"{cart_rate:.2f}%",
                f"{checkout_rate:.2f}%",
                f"{purchase_rate:.2f}%",
            ],
            "Do not progress": [
                f"{100 - cart_rate:.2f}%",
                f"{100 - checkout_rate:.2f}%",
                f"{100 - purchase_rate:.2f}%",
            ],
        })

        st.dataframe(rates, hide_index=True)

    with st.expander("Definitions and assumptions"):
        st.markdown(
            "- **Source:** GA4 BigQuery analysis.\n"
            "- **Unit:** Sessions; one person may have multiple sessions.\n"
            "- **Sequence:** Product view → Add to cart → Checkout → "
            "Purchase, strictly in order within the same user/session.\n"
            "- **Purchases:** Only sessions completing the entire "
            "sequence are counted.\n"
            "- **Product matching:** Steps may involve different products.\n"
            "- **Completion rate:** Full-funnel purchase sessions "
            "divided by product-view sessions.\n"
            "- **Step conversion:** Step conversion measures the percentage of "
            "shopping sessions that move from one funnel stage to the next."
            "Sessions reaching the next step divided by sessions reaching "
            "the current step."
        )

        st.write(
            "Shoppers may purchase later or follow a different path. "
            "The funnel does not establish why they stop progressing "
            "or whether device differences cause conversion differences."
        )

        st.write(
            "The proposed test targets first-time product viewers, "
            "a narrower population than this funnel. Shipping and "
            "return uncertainty remain hypotheses."
        )

    with st.expander("View the exported data"):
        st.dataframe(funnel, hide_index=True)
