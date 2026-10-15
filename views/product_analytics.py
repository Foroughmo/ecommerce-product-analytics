import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from shared.data import load_funnel
from shared.styling import insight_card, page_header, takeaway


def render():
    page_header(
        title="Where do shoppers leave?",
        subtitle=(
            "Follow the journey from viewing a product to completing "
            "a purchase. Select a device to explore its funnel."
        ),
        eyebrow="Product analytics · GA4",
    )

    funnel = load_funnel()

    st.write(
        "A shopping funnel counts how many sessions progress through "
        "each step. Here, every step must happen after the previous "
        "one within the same session."
    )

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
        "Full-funnel completion is the share of product-view sessions "
        "that complete all four steps in order."
    )

    journey_tab, comparison_tab = st.tabs(
        ["Selected device", "Compare devices"]
    )

    with journey_tab:
        chart_col, insight_col = st.columns([3, 2])

        with chart_col:
            st.subheader(f"{device.title()}: the shopping journey")

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

            fig, ax = plt.subplots(figsize=(7, 3.8))
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

        with insight_col:
            cart_rate = float(row["view_to_cart_rate"])
            checkout_rate = float(row["cart_to_checkout_rate"])
            purchase_rate = float(row["checkout_to_purchase_rate"])

            insight_card(
                "First transition",
                f"{cart_rate:.2f}% reach Add to Cart",
                f"About {100 - cart_rate:.1f} out of every 100 "
                "product-view sessions do not progress to the cart "
                "stage in this measured session funnel.",
            )

            insight_card(
                "Final transition",
                f"{purchase_rate:.2f}% complete purchase",
                "Among sessions reaching checkout through the earlier "
                "funnel steps, this share goes on to purchase.",
            )

        st.subheader("Conversion between steps")

        rates = pd.DataFrame({
            "Transition": [
                "Product view → Add to cart",
                "Add to cart → Checkout",
                "Checkout → Purchase",
            ],
            "Progress to next step": [
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

        takeaway(
            "The largest drop-off for this device occurs before "
            "Add to Cart. This identifies a place to investigate, "
            "not the reason visitors leave."
        )

    with comparison_tab:
        st.subheader("Full-funnel completion by device")

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
            f"Mobile completion is {mobile_rate:.2f}% versus "
            f"{desktop_rate:.2f}% on desktop. This funnel does not "
            "support a claim that mobile underperforms desktop."
        )

        st.caption(
            "These are descriptive comparisons. They do not establish "
            "that device type causes the difference, and no statistical "
            "significance test is shown here."
        )

    st.subheader("From observation to a testable idea")

    left, right = st.columns(2)

    with left:
        insight_card(
            "What the data shows",
            "The biggest gap is before the cart",
            "Across devices, only 17.88%–18.93% of product-view "
            "sessions reach Add to Cart. This pattern is shared "
            "across desktop, mobile, and tablet.",
        )

    with right:
        insight_card(
            "What we propose to test",
            "Make purchase information clearer",
            "Test shipping estimates, return-policy visibility, "
            "and reassurance near Add to Cart for first-time "
            "product viewers.",
        )

    st.caption(
        "These findings summarize all three device groups and remain "
        "the same when the device selector changes. The proposed "
        "first-time-visitor experiment targets a narrower population "
        "than this device-level funnel. Shipping or return uncertainty "
        "is a hypothesis, not an established cause of drop-off."
    )

    with st.expander("How this funnel is defined"):
        st.write(
            "- **Source:** GA4 BigQuery analysis, "
            "`05_funnel_by_device`.\n"
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
