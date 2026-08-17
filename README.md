# ⚡ Smart Meter Analytics Platform

A machine learning platform for energy consumption forecasting and anomaly detection using smart-meter time-series data.

## 📌 Project Overview

Smart meters generate energy consumption readings at regular time intervals. This project uses historical smart-meter data to:

- Forecast expected energy consumption
- Identify unusual consumption patterns
- Visualize actual vs expected consumption
- Provide ML predictions through an API

## 🧠 Machine Learning Approach

The project uses time-series features such as:

- Hour
- Day of week
- Lag 1
- Lag 4
- Lag 96
- Rolling mean 4
- Rolling mean 96

Since the meter records data every 15 minutes, 96 readings represent approximately 24 hours of previous consumption.

An XGBoost Regressor is used to predict expected energy consumption.

### Anomaly Detection

The difference between actual and predicted consumption is calculated as a residual.

If the absolute residual crosses a threshold calculated from the training residual distribution, the reading is flagged as a potential anomaly.

## 📊 Dashboard

The Streamlit dashboard provides:

- Total readings
- Average energy consumption
- Potential anomalies
- Anomaly rate
- Actual vs expected energy consumption
- Potential anomaly records

## 🚀 API

FastAPI is used to expose the machine learning functionality through REST endpoints.

Available endpoints include:

- `GET /`
- `GET /model-info`
- `POST /forecast`
- `POST /anomaly`
- `GET /meter/{meter_id}/latest`
- `GET /meter/{meter_id}/history`

Swagger documentation is automatically available through FastAPI.

## 🛠️ Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- Joblib
- Streamlit
- FastAPI
- Uvicorn
- Jupyter Notebook

## 📁 Project Structure

```text
smartmeter-ai/
│
├── api/
├── data/
├── models/
├── notebooks/
├── src/
├── app.py
├── requirements.txt
└── README.md