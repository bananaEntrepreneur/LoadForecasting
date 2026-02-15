import streamlit as st
import pandas as pd
import numpy as np
from utils import calculate_forecast_and_capacity

st.set_page_config(page_title="Server Capacity Forecast", layout="wide")

st.title("Server Load Forecast")
st.write("ML-forecast infrastructure")

st.divider()

days = st.slider("Forecast horizon (days)", 7, 180, 30)

st.subheader("Base traffic level (RPS)")
base = st.slider("Current average RPS", 50000, 500000, 150000, step=10000)

st.subheader("Growth scenario")
growth = st.slider("Monthly growth %", 0, 20, 5)

growth_rate = growth / 100

st.divider()

last_data = pd.DataFrame([{
    "lag_1": base,
    "lag_7": base * 0.9,
    "rolling_7": base * 0.95,
    "dayofweek": 2,
    "month": 11
}])

if st.button("Run forecast"):

    growth_preds, servers, cost, p95, peak_servers, peak_cost = calculate_forecast_and_capacity(
        base_rps=base,
        days=days,
        growth_rate=growth
    )

    st.subheader("Traffic forecast (RPS)")
    st.line_chart(growth_preds)

    st.subheader("Servers required")
    st.line_chart(servers)

    col1, col2, col3 = st.columns(3)

    col1.metric("Max servers", int(max(servers)))
    col2.metric("Avg servers", int(np.mean(servers)))
    col3.metric("Monthly cost ($)", int(np.mean(cost)))

    st.divider()
    st.subheader("Peak capacity planning (p95)")

    st.metric("Servers for peak load", peak_servers)
    st.metric("Peak monthly cost ($)", peak_cost)
