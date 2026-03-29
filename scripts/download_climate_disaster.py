from pathlib import Path
import pandas as pd

ONI_URL = "https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php"
SEASON_TO_MONTH = {
    "DJF": 1,
    "JFM": 2,
    "FMA": 3,
    "MAM": 4,
    "AMJ": 5,
    "MJJ": 6,
    "JJA": 7,
    "JAS": 8,
    "ASO": 9,
    "SON": 10,
    "OND": 11,
    "NDJ": 12,
}


def download_oni_monthly() -> pd.DataFrame:
    tables = pd.read_html(ONI_URL)
    oni_raw = tables[0].copy()

    # Keep columns that look like seasons plus year column.
    if "Year" not in oni_raw.columns:
        oni_raw.columns = [str(c).strip() for c in oni_raw.columns]

    year_col = "Year"
    long_df = oni_raw.melt(id_vars=[year_col], var_name="season", value_name="enso_oni")
    long_df["month"] = long_df["season"].map(SEASON_TO_MONTH)
    long_df = long_df.dropna(subset=["month"])
    long_df["date"] = pd.to_datetime(
        dict(year=long_df[year_col].astype(int), month=long_df["month"].astype(int), day=1)
    ) + pd.offsets.MonthEnd(0)
    long_df["enso_oni"] = pd.to_numeric(long_df["enso_oni"], errors="coerce")

    return long_df[["date", "enso_oni"]].sort_values("date").reset_index(drop=True)


def load_optional_feature_csv(path: str, value_column: str, target_name: str) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        print(f"Optional file missing: {path}. Creating empty {target_name} feature.")
        return pd.DataFrame(columns=["date", target_name])

    df = pd.read_csv(p)
    if "date" not in df.columns or value_column not in df.columns:
        raise ValueError(f"{path} must include columns: date and {value_column}")

    out = df[["date", value_column]].copy()
    out["date"] = pd.to_datetime(out["date"]).dt.to_period("M").dt.to_timestamp("M")
    out = out.rename(columns={value_column: target_name})
    return out


if __name__ == "__main__":
    oni = download_oni_monthly()

    # Optional user-provided monthly features. You can replace these with fully automated API pulls later.
    drought = load_optional_feature_csv("data/raw/drought_monthly_input.csv", "drought_index", "drought_index")
    temp = load_optional_feature_csv("data/raw/temp_anomaly_input.csv", "temperature_anomaly", "temperature_anomaly")
    precip = load_optional_feature_csv(
        "data/raw/precip_anomaly_input.csv", "precipitation_anomaly", "precipitation_anomaly"
    )
    heat = load_optional_feature_csv(
        "data/raw/extreme_heat_input.csv", "extreme_heat_events", "extreme_heat_events"
    )

    climate = oni.merge(drought, on="date", how="outer")
    climate = climate.merge(temp, on="date", how="outer")
    climate = climate.merge(precip, on="date", how="outer")
    climate = climate.merge(heat, on="date", how="outer")
    climate = climate.sort_values("date").reset_index(drop=True)

    out = "data/raw/climate_disaster_monthly.csv"
    climate.to_csv(out, index=False)
    print(f"Saved {out} with {len(climate):,} rows.")
