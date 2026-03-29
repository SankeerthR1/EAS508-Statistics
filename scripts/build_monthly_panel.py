from pathlib import Path
import pandas as pd


def read_csv_required(path: str) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Required file not found: {path}")
    return pd.read_csv(p, parse_dates=["date"])


if __name__ == "__main__":
    futures_df = read_csv_required("data/raw/futures_monthly.csv")
    macro_df = read_csv_required("data/raw/macro_monthly.csv")
    climate_df = read_csv_required("data/raw/climate_disaster_monthly.csv")

    panel = futures_df.merge(macro_df, on="date", how="left")
    panel = panel.merge(climate_df, on="date", how="left")

    # Ensure all requested proposal variables exist in final panel.
    required_columns = [
        "futures_return",
        "enso_oni",
        "temperature_anomaly",
        "precipitation_anomaly",
        "drought_index",
        "extreme_heat_events",
        "usd_index",
        "interest_rate",
        "vix",
    ]
    for col in required_columns:
        if col not in panel.columns:
            panel[col] = pd.NA

    panel = panel.sort_values(["commodity", "date"]).reset_index(drop=True)

    out = "data/processed/monthly_panel.csv"
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    panel.to_csv(out, index=False)

    print(panel.head())
    print("\nMissing values by column:")
    print(panel[required_columns].isna().sum())
    print(f"\nSaved {out} with {len(panel):,} rows.")
