from pathlib import Path

import pandas as pd
import streamlit as st


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@st.cache_data
def load_funnel():
    return pd.read_csv(DATA_DIR / "funnel_by_device.csv")


@st.cache_data
def load_experiment_results():
    return pd.read_csv(DATA_DIR / "experiment_results.csv")
