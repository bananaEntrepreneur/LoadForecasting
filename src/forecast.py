import joblib
import os

model_path = os.path.join(os.path.dirname(__file__), "..", "models", "xgb_model.pkl")
model = joblib.load(model_path)

def forecast_load(last_data, days=30):

    preds = []
    current = last_data.copy()

    for _ in range(days):

        pred = model.predict(current)[0]
        preds.append(pred)

        current["lag_7"] = current["lag_1"]
        current["lag_1"] = pred
        current["rolling_7"] = (current["rolling_7"]*6 + pred)/7

        if "dayofweek" in current:
            current["dayofweek"] = (current["dayofweek"] + 1) % 7

    return preds
