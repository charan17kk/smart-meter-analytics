from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# --------------------------------
# Project paths
# --------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "dashboard_results.csv"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "energy_forecasting_model.pkl"
)

THRESHOLD_PATH = (
    PROJECT_ROOT
    / "models"
    / "anomaly_threshold.pkl"
)


# --------------------------------
# Load models and data
# --------------------------------

model = joblib.load(MODEL_PATH)

anomaly_threshold = joblib.load(
    THRESHOLD_PATH
)

dashboard_df = pd.read_csv(DATA_PATH)

dashboard_df["timestamp"] = pd.to_datetime(
    dashboard_df["timestamp"]
)


# --------------------------------
# FastAPI application
# --------------------------------

app = FastAPI(
    title="Smart Meter Analytics API",
    description="API for smart-meter forecasting and anomaly monitoring",
    version="1.0.0"
)


# --------------------------------
# Request models
# --------------------------------

class ForecastRequest(BaseModel):
    hour: int
    day_of_week: int
    lag_1: float
    lag_4: float
    lag_96: float
    rolling_mean_4: float
    rolling_mean_96: float


class AnomalyRequest(BaseModel):
    actual_energy_kwh: float
    expected_energy_kwh: float


# --------------------------------
# Home
# --------------------------------

@app.get("/")
def home():
    return {
        "message": "Smart Meter Analytics API is running"
    }


# --------------------------------
# Model information
# --------------------------------

@app.get("/model-info")
def model_info():
    return {
        "model_type": type(model).__name__,
        "features": list(model.feature_names_in_)
    }


# --------------------------------
# Energy forecasting
# --------------------------------

@app.post("/forecast")
def forecast(request: ForecastRequest):

    input_data = pd.DataFrame([{
        "hour": request.hour,
        "day_of_week": request.day_of_week,
        "lag_1": request.lag_1,
        "lag_4": request.lag_4,
        "lag_96": request.lag_96,
        "rolling_mean_4": request.rolling_mean_4,
        "rolling_mean_96": request.rolling_mean_96
    }])

    prediction = model.predict(input_data)[0]

    return {
        "predicted_energy_kwh": round(
            float(prediction),
            4
        )
    }


# --------------------------------
# Anomaly detection
# --------------------------------

@app.post("/anomaly")
def detect_anomaly(request: AnomalyRequest):

    residual = (
        request.actual_energy_kwh
        - request.expected_energy_kwh
    )

    absolute_residual = abs(residual)

    is_anomaly = (
        absolute_residual > anomaly_threshold
    )

    return {
        "actual_energy_kwh": request.actual_energy_kwh,
        "expected_energy_kwh": request.expected_energy_kwh,
        "residual": round(residual, 4),
        "absolute_residual": round(
            absolute_residual,
            4
        ),
        "threshold": round(
            float(anomaly_threshold),
            4
        ),
        "is_anomaly": bool(is_anomaly),
        "status": (
            "Anomaly"
            if is_anomaly
            else "Normal"
        )
    }


# --------------------------------
# Latest meter reading
# --------------------------------

@app.get("/meter/{meter_id}/latest")
def get_latest_meter_reading(
    meter_id: str
):

    meter_data = dashboard_df[
        dashboard_df["meter_id"] == meter_id
    ]

    if meter_data.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Meter {meter_id} not found"
        )

    latest = meter_data.sort_values(
        "timestamp"
    ).iloc[-1]

    actual = float(
        latest["actual_energy"]
    )

    expected = float(
        latest["expected_energy"]
    )

    error = abs(
        actual - expected
    )

    is_anomaly = (
        error > anomaly_threshold
    )

    return {
        "meter_id": meter_id,
        "timestamp": str(
            latest["timestamp"]
        ),
        "actual_energy_kwh": round(
            actual,
            4
        ),
        "expected_energy_kwh": round(
            expected,
            4
        ),
        "prediction_error": round(
            error,
            4
        ),
        "threshold": round(
            float(anomaly_threshold),
            4
        ),
        "is_anomaly": bool(
            is_anomaly
        ),
        "status": (
            "Anomaly"
            if is_anomaly
            else "Normal"
        )
    }

@app.get("/meter/{meter_id}/history")
def get_meter_history(meter_id: str):

    meter_data = dashboard_df[
        dashboard_df["meter_id"] == meter_id
    ].copy()

    if meter_data.empty:
        return {
            "error": f"Meter {meter_id} not found"
        }

    meter_data = meter_data.sort_values("timestamp")

    return meter_data[
        [
            "timestamp",
            "actual_energy",
            "expected_energy",
            "prediction_error",
            "is_anomaly"
        ]
    ].to_dict(orient="records")