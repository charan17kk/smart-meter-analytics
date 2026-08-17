import pandas as pd


def validate_meter_data(df):

    report = {}

    # -----------------------------
    # Basic information
    # -----------------------------

    report["total_rows"] = len(df)

    report["total_meters"] = df["meter_id"].nunique()

    # -----------------------------
    # Missing values
    # -----------------------------

    report["missing_values"] = df.isnull().sum().to_dict()

    # -----------------------------
    # Duplicate records
    # -----------------------------

    report["duplicate_rows"] = int(df.duplicated().sum())

    # -----------------------------
    # Invalid energy values
    # -----------------------------

    report["negative_energy"] = int(
        (df["energy_kwh"] < 0).sum()
    )

    # -----------------------------
    # Unrealistic voltage
    # -----------------------------

    report["invalid_voltage"] = int(
        ((df["voltage"] < 180) | (df["voltage"] > 260)).sum()
    )

    # -----------------------------
    # Extreme energy consumption
    # -----------------------------

    report["extreme_energy"] = int(
        (df["energy_kwh"] > 20).sum()
    )

    return report