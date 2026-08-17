import streamlit as st
import pandas as pd
import requests


# Page configuration
st.set_page_config(
    page_title="Smart Meter Analytics",
    page_icon="⚡",
    layout="wide"
)


# FastAPI URL
import os

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)

# Title
st.title("⚡ Smart Meter Analytics Platform")

st.write(
    "Energy consumption forecasting and anomaly monitoring"
)


# Meter selection
meter_id = st.selectbox(
    "Select Meter",
    ["M0001"]
)

st.write(f"Monitoring Meter: **{meter_id}**")


# Get meter history from FastAPI
response = requests.get(
    f"{API_URL}/meter/{meter_id}/history"
)

if response.status_code != 200:
    st.error("Unable to fetch meter data from API.")
    st.stop()


history = response.json()

df = pd.DataFrame(history)

df["timestamp"] = pd.to_datetime(
    df["timestamp"]
)


# -----------------------------
# Dashboard Metrics
# -----------------------------

total_readings = len(df)

anomaly_count = int(
    df["is_anomaly"].sum()
)

anomaly_percentage = (
    anomaly_count / total_readings
) * 100

avg_consumption = (
    df["actual_energy"].mean()
)


# Get latest reading from API
latest_response = requests.get(
    f"{API_URL}/meter/{meter_id}/latest"
)

if latest_response.status_code == 200:

    latest_data = latest_response.json()

    latest_consumption = (
        latest_data["actual_energy_kwh"]
    )

else:

    latest_consumption = (
        df["actual_energy"].iloc[-1]
    )


# -----------------------------
# Metrics
# -----------------------------

col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Total Readings",
    f"{total_readings:,}"
)


col2.metric(
    "Avg Consumption",
    f"{avg_consumption:.2f} kWh"
)


col3.metric(
    "Potential Anomalies",
    anomaly_count
)


col4.metric(
    "Anomaly Rate",
    f"{anomaly_percentage:.2f}%"
)


# -----------------------------
# Actual vs Expected
# -----------------------------

st.subheader(
    "📈 Actual vs Expected Energy Consumption"
)


chart_df = df[
    [
        "timestamp",
        "actual_energy",
        "expected_energy"
    ]
].set_index("timestamp")


st.line_chart(chart_df)


# -----------------------------
# Anomalies
# -----------------------------

st.subheader("🚨 Potential Anomalies")


anomalies = df[
    df["is_anomaly"] == True
]


st.dataframe(
    anomalies[
        [
            "timestamp",
            "actual_energy",
            "expected_energy",
            "prediction_error",
            "is_anomaly"
        ]
    ],
    use_container_width=True
)