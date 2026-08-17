import pandas as pd


def clean_meter_data(df):

    df = df.copy()

    # -----------------------------
    # 1. Remove exact duplicates
    # -----------------------------

    df = df.drop_duplicates()

    # -----------------------------
    # 2. Remove invalid negative
    #    energy readings
    # -----------------------------

    df.loc[df["energy_kwh"] < 0, "energy_kwh"] = pd.NA

    # -----------------------------
    # 3. Handle unrealistic voltage
    # -----------------------------

    invalid_voltage = (
        (df["voltage"] < 180) |
        (df["voltage"] > 260)
    )

    df.loc[invalid_voltage, "voltage"] = pd.NA

    # -----------------------------
    # 4. Handle extreme energy
    # -----------------------------

    # We don't immediately delete these.
    # We mark them for anomaly analysis.

    df["potential_anomaly"] = (
        df["energy_kwh"] > 20
    )

    # -----------------------------
    # 5. Interpolate missing energy
    #    within each meter
    # -----------------------------

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df = df.sort_values(
        ["meter_id", "timestamp"]
    )

    df["energy_kwh"] = (
        df.groupby("meter_id")["energy_kwh"]
        .transform(
            lambda x: x.interpolate(
                method="linear",
                limit_direction="both"
            )
        )
    )

    return df