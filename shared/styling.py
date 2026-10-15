from html import escape

import streamlit as st


def apply_style():
    """Apply consistent typography, spacing, and colors across pages."""
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #F5F7FB;
            color: #172B4D;
        }

        [data-testid="stMainBlockContainer"] {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        h1 {
            font-size: 2rem !important;
            font-weight: 750 !important;
            letter-spacing: -0.04em;
            line-height: 1.2 !important;
        }

        h2 {
            font-size: 1.35rem !important;
            letter-spacing: -0.02em;
        }

        h3 {
            font-size: 1.05rem !important;
        }

        p, li {
            line-height: 1.65;
        }

        [data-testid="stSidebar"] {
            background-color: #EAF0F7;
        }

        [data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 1px solid #DFE6EF;
            border-radius: 14px;
            padding: 18px;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.8rem;
        }

        .report-header {
            margin-bottom: 1.5rem;
        }

        .report-eyebrow {
            color: #087F8C;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.6rem;
        }

        .report-title {
            color: #172B4D;
            margin: 0 0 0.65rem 0;
        }

        .report-subtitle {
            color: #52627A;
            max-width: 780px;
            font-size: 1rem;
        }

        .report-card {
            background-color: #FFFFFF;
            border: 1px solid #DFE6EF;
            border-top: 3px solid #087F8C;
            border-radius: 14px;
            padding: 22px;
            margin-bottom: 16px;
        }

        .report-card-label {
            color: #52627A;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.07em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }

        .report-card-title {
            color: #172B4D;
            font-size: 1.15rem;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .report-card-body {
            color: #52627A;
            font-size: 0.95rem;
            line-height: 1.65;
        }

        .report-takeaway {
            background-color: #E8F5F3;
            border-left: 4px solid #087F8C;
            border-radius: 8px;
            padding: 16px 20px;
            color: #174A4B;
            line-height: 1.6;
            margin: 16px 0;
        }

        @media (max-width: 640px) {
            h1 {
                font-size: 1.6rem !important;
            }

            [data-testid="stMainBlockContainer"] {
                padding-top: 1rem;
            }

            .report-card {
                padding: 16px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title, subtitle, eyebrow="Product analytics case study"):
    """Show a compact page introduction."""
    st.markdown(
        f"""
        <div class="report-header">
            <div class="report-eyebrow">{escape(eyebrow)}</div>
            <h1 class="report-title">{escape(title)}</h1>
            <div class="report-subtitle">{escape(subtitle)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight_card(label, title, body):
    """Show a reusable card with a short explanation."""
    st.markdown(
        f"""
        <div class="report-card">
            <div class="report-card-label">{escape(label)}</div>
            <div class="report-card-title">{escape(title)}</div>
            <div class="report-card-body">{escape(body)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def takeaway(text):
    """Highlight the main message beneath a chart or comparison."""
    st.markdown(
        f'<div class="report-takeaway">{escape(text)}</div>',
        unsafe_allow_html=True,
    )
