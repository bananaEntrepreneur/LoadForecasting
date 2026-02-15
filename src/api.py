from fastapi import FastAPI, HTTPException
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(__file__))

from forecast import forecast_load
from capacity import calculate_servers

app = FastAPI(title="Server Load Forecast API", description="API for forecasting server load and calculating capacity needs")

@app.get("/")
async def root():
    return {"message": "Server Load Forecast API"}

@app.get("/forecast/")
async def get_forecast(
    days: int = 30,
    base_rps: float = 150000.0,
    growth_rate: float = 5.0
):
    if days < 1 or days > 365:
        raise HTTPException(status_code=400, detail="Days must be between 1 and 365")
    
    if base_rps < 1000 or base_rps > 1000000:
        raise HTTPException(status_code=400, detail="Base RPS must be between 1000 and 1000000")
    
    if growth_rate < 0 or growth_rate > 50:
        raise HTTPException(status_code=400, detail="Growth rate must be between 0 and 50")

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
    
    return {
        "forecast_days": days,
        "base_rps": float(base_rps),
        "growth_rate_percent": float(growth_rate),
        "traffic_forecast": [float(x) for x in growth_preds],
        "required_servers": [int(s) for s in servers],
        "monthly_costs": [int(c) for c in cost],
        "max_servers": int(max(servers)),
        "avg_servers": float(np.mean(servers)),
        "avg_monthly_cost": float(np.mean(cost)),
        "peak_capacity": {
            "p95_load": float(p95),
            "peak_servers": int(peak_servers),
            "peak_monthly_cost": int(peak_cost)
        }
    }