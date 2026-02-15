from fastapi import FastAPI, HTTPException
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(__file__))

from utils import calculate_forecast_and_capacity

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
    """
    Get server load forecast with capacity planning
    
    Args:
        days: Forecast horizon in days (default: 30, min: 1, max: 365)
        base_rps: Current average RPS (default: 150000, min: 1000, max: 1000000)
        growth_rate: Monthly growth percentage (default: 5%, min: 0, max: 50)
    
    Returns:
        Dictionary containing forecasted traffic, required servers, and costs
    """
    if days < 1 or days > 365:
        raise HTTPException(status_code=400, detail="Days must be between 1 and 365")
    
    if base_rps < 1000 or base_rps > 1000000:
        raise HTTPException(status_code=400, detail="Base RPS must be between 1000 and 1000000")
    
    if growth_rate < 0 or growth_rate > 50:
        raise HTTPException(status_code=400, detail="Growth rate must be between 0 and 50")

    growth_preds, servers, cost, p95, peak_servers, peak_cost = calculate_forecast_and_capacity(
        base_rps=base_rps,
        days=days,
        growth_rate=growth_rate
    )
    
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