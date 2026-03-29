import os
import requests
import pandas as pd

FRED_URL = "https://api.stlouisfed.org/fred/series/observations"
SERIES = {
    "usd_index": "DTWEXBGS",
    "interest_rate": "TB3MS",
    "vix": "VIXCLS",
}


def _get_fred_series(series_id: str, start_date: str, api_key: str) -> pd.DataFrame:
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "observation_start": start_date,
    }
    response = requests.get(FRED_URL, params=params, timeout=30)
    response.raise_for_status()
    observations = response.json().get("observations", [])

    df = pd.DataFrame(observations)
    if df.empty:
        return pd.DataFrame(columns=["date", series_id])

    df = df[["date", "value"]].copy()
    df["date"] = pd.to_datetime(df["date"])
    df[series_id] = pd.to_numeric(df["value"], errors="coerce")
    return df[["date", series_id]]


def download_macro_monthly(start_date: str = "2010-01-01") -> pd.DataFrame:
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        raise RuntimeError("FRED_API_KEY is required in your environment.")

    usd = _get_fred_series(SERIES["usd_index"], start_date, api_key)
    rates = _get_fred_series(SERIES["interest_rate"], start_date, api_key)
    vix = _get_fred_series(SERIES["vix"], start_date, api_key)

    usd = usd.set_index("date").resample("ME").mean().rename(columns={SERIES["usd_index"]: "usd_index"}).reset_index()
    vix = vix.set_index("date").resample("ME").mean().rename(columns={SERIES["vix"]: "vix"}).reset_index()
    rates["date"] = pd.to_datetime(rates["date"]).dt.to_period("M").dt.to_timestamp("M")
    rates = rates.rename(columns={SERIES["interest_rate"]: "interest_rate"})

    macro = usd.merge(rates, on="date", how="outer")
    macro = macro.merge(vix, on="date", how="outer")
    return macro.sort_values("date").reset_index(drop=True)


if __name__ == "__main__":
    df = download_macro_monthly()
    out = "data/raw/macro_monthly.csv"
    df.to_csv(out, index=False)
    print(f"Saved {out} with {len(df):,} rows.")
