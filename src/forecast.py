import joblib
import numpy as np
import pandas as pd

model = joblib.load("models/xgb_model.pkl")


def forecast_load(last_data, days=30):
    preds = []
    current = last_data.copy()

    for _ in range(days):
        pred = model.predict(current)[0]
        preds.append(pred)

        current["lag_7"] = current["lag_1"]
        current["lag_1"] = pred
        current["rolling_7"] = (current["rolling_7"] * 6 + pred) / 7

        current["is_sale"] = np.random.choice([0, 1], p=[0.9, 0.1])
        current["is_big_sale"] = 1 if np.random.rand() < 0.05 else 0

    return preds
