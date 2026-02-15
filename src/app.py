import streamlit as st
import pandas as pd
import numpy as np
from forecast import forecast_load
from capacity import calculate_servers

st.set_page_config(page_title="Server Capacity Forecast", layout="wide")

st.title("Server Load Forecast")
st.write("ML-прогноз нагрузки и расчёт инфраструктуры")

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

    preds = forecast_load(last_data, days)

    growth_preds = []
    val = preds[0]

    for p in preds:
        val = p * (1 + growth_rate/30)
        growth_preds.append(val)

    servers, cost = calculate_servers(growth_preds)

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

    p95 = np.percentile(growth_preds, 95)
    peak_servers = int(np.ceil(p95 / 20000))
    peak_cost = peak_servers * 300

    st.metric("Servers for peak load", peak_servers)
    st.metric("Peak monthly cost ($)", peak_cost)
