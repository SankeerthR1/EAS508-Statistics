# EAS508 Statistics Project

This repository now includes a starter data pipeline on `main` for building a monthly panel that combines:

- Futures returns (corn, soybean, wheat)
- ENSO index (ONI)
- Temperature anomaly
- Precipitation anomaly
- Drought index
- Extreme heat events
- U.S. dollar index
- Interest rate
- VIX

## Pipeline layout

- `scripts/download_futures.py` – Yahoo Finance futures prices and monthly log returns.
- `scripts/download_macro_fred.py` – FRED macro series (USD index, interest rate, VIX).
- `scripts/download_climate_disaster.py` – ONI from NOAA CPC + optional monthly CSV inputs for drought/temp/precip/extreme heat.
- `scripts/build_monthly_panel.py` – merge all inputs into one final monthly panel.
- `scripts/run_pipeline.py` – runs all steps in sequence.

## Required setup

1. Install dependencies:

```bash
python -m pip install -e .
```

2. Set your FRED API key:

```bash
export FRED_API_KEY="your_key_here"
```

3. (Optional but recommended) provide monthly CSV files for climate/disaster variables in `data/raw/`:

- `drought_monthly_input.csv` with columns: `date,drought_index`
- `temp_anomaly_input.csv` with columns: `date,temperature_anomaly`
- `precip_anomaly_input.csv` with columns: `date,precipitation_anomaly`
- `extreme_heat_input.csv` with columns: `date,extreme_heat_events`

If these files are missing, the pipeline still runs and leaves those columns as missing values.

## Run

```bash
python scripts/run_pipeline.py
```

Final output:

- `data/processed/monthly_panel.csv`
