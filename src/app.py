import streamlit as st
import pandas as pd
from forecast import forecast_load
from capacity import calculate_servers

st.title("Server Load Forecast")

days = st.slider("Days to forecast", 7, 120, 30)

last_data = pd.DataFrame([{
    "lag_1": 200000,
    "lag_7": 180000,
    "rolling_7": 190000,
    "dayofweek": 3,
    "month": 11,
    "is_sale": 0,
    "is_big_sale": 0
}])

if st.button("Run forecast"):
    preds = forecast_load(last_data, days)
    servers, cost = calculate_servers(preds)

    st.line_chart(preds)
    st.subheader(f"Max servers needed: {int(max(servers))}")
    st.subheader(f"Avg infra cost: ${int(cost.mean())}")
