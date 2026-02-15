import pandas as pd
import numpy as np
from .forecast import forecast_load
from .capacity import calculate_servers


def calculate_forecast_and_capacity(
    base_rps: float = 150000.0,
    days: int = 30,
    growth_rate: float = 5.0
):
    """
    Calculate forecast and capacity requirements
    
    Args:
        base_rps: Current average RPS (default: 150000)
        days: Forecast horizon in days (default: 30)
        growth_rate: Monthly growth percentage (default: 5%)
    
    Returns:
        Tuple of (growth_preds, servers, cost, p95, peak_servers, peak_cost)
    """
    growth_rate_decimal = growth_rate / 100

    last_data = pd.DataFrame([{
        "lag_1": base_rps,
        "lag_7": base_rps * 0.9,
        "rolling_7": base_rps * 0.95,
        "dayofweek": 2,
        "month": 11
    }])

    preds = forecast_load(last_data, days)

    growth_preds = []
    val = preds[0]
    for p in preds:
        val = p * (1 + growth_rate_decimal/30)
        growth_preds.append(val)

    servers, cost = calculate_servers(growth_preds)

    p95 = np.percentile(growth_preds, 95)
    peak_servers = int(np.ceil(p95 / 20000))
    peak_cost = peak_servers * 300
    
    return growth_preds, servers, cost, p95, peak_servers, peak_cost