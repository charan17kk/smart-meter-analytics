import pandas as pd
import numpy as np


# -----------------------------
# Load clean dataset
# -----------------------------

input_path = "data/raw/smart_meter_readings.csv"

df = pd.read_csv(input_path)

np.random.seed(42)


# -----------------------------
# 1. Missing readings
# -----------------------------

missing_indices = np.random.choice(
    df.index,
    size=int(len(df) * 0.01),
    replace=False
)

df.loc[missing_indices, "energy_kwh"] = np.nan


# -----------------------------
# 2. Duplicate records
# -----------------------------

duplicate_rows = df.sample(
    n=int(len(df) * 0.005),
    random_state=42
)

df = pd.concat(
    [df, duplicate_rows],
    ignore_index=True
)


# -----------------------------
# 3. Negative energy values
# -----------------------------

negative_indices = np.random.choice(
    df.index,
    size=100,
    replace=False
)

df.loc[negative_indices, "energy_kwh"] = -5


# -----------------------------
# 4. Unrealistic voltage values
# -----------------------------

voltage_indices = np.random.choice(
    df.index,
    size=100,
    replace=False
)

df.loc[voltage_indices, "voltage"] = 500


# -----------------------------
# 5. Extreme consumption values
# -----------------------------

extreme_indices = np.random.choice(
    df.index,
    size=100,
    replace=False
)

df.loc[extreme_indices, "energy_kwh"] = 100


# -----------------------------
# Save corrupted dataset
# -----------------------------

output_path = "data/raw/smart_meter_readings_messy.csv"

df.to_csv(
    output_path,
    index=False
)

print("Messy smart-meter dataset created!")
print(f"Rows: {len(df):,}")
print(f"Saved to: {output_path}")