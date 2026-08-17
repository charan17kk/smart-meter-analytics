import os
import numpy as np
import pandas as pd


# -----------------------------
# Configuration
# -----------------------------

NUM_METERS = 100
DAYS = 30
FREQUENCY = "15min"

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)


# -----------------------------
# Generate timestamps
# -----------------------------

timestamps = pd.date_range(
    start="2026-01-01",
    periods=(DAYS * 24 * 4),
    freq=FREQUENCY
)


# -----------------------------
# Generate meter data
# -----------------------------

all_data = []

for meter_number in range(1, NUM_METERS + 1):

    meter_id = f"M{meter_number:04d}"

    # Each meter has a different normal consumption level
    base_consumption = np.random.uniform(1.5, 5.0)

    for timestamp in timestamps:

        hour = timestamp.hour
        day_of_week = timestamp.dayofweek

        # -----------------------------
        # Time-of-day pattern
        # -----------------------------

        if 0 <= hour < 6:
            time_factor = 0.5

        elif 6 <= hour < 9:
            time_factor = 0.9

        elif 9 <= hour < 17:
            time_factor = 1.0

        elif 17 <= hour < 22:
            time_factor = 1.5

        else:
            time_factor = 0.7

        # -----------------------------
        # Weekend effect
        # -----------------------------

        if day_of_week >= 5:
            weekend_factor = 1.1
        else:
            weekend_factor = 1.0

        # -----------------------------
        # Random variation
        # -----------------------------

        noise = np.random.normal(0, 0.15)

        energy = (
            base_consumption
            * time_factor
            * weekend_factor
            + noise
        )

        # Energy cannot be negative
        energy = max(0.1, energy)

        # -----------------------------
        # Other meter parameters
        # -----------------------------

        voltage = np.random.normal(230, 3)

        current = max(
            0.1,
            energy * np.random.uniform(1.5, 2.5)
        )

        power_factor = np.random.uniform(0.85, 0.99)

        all_data.append(
            {
                "meter_id": meter_id,
                "timestamp": timestamp,
                "energy_kwh": round(energy, 3),
                "voltage": round(voltage, 2),
                "current": round(current, 2),
                "power_factor": round(power_factor, 3)
            }
        )


# -----------------------------
# Create DataFrame
# -----------------------------

df = pd.DataFrame(all_data)


# -----------------------------
# Save raw data
# -----------------------------

output_path = "data/raw/smart_meter_readings.csv"

os.makedirs("data/raw", exist_ok=True)

df.to_csv(output_path, index=False)


print("Smart meter dataset generated successfully!")
print(f"Rows: {len(df):,}")
print(f"Meters: {df['meter_id'].nunique()}")
print(f"Time range: {df['timestamp'].min()} → {df['timestamp'].max()}")
print(f"Saved to: {output_path}")