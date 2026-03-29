# EAS508 Statistics Project

<<<<<<< HEAD
This repository now includes a starter data pipeline on `main` for building a monthly panel that combines:
=======
This repository now uses **one notebook** for the full monthly pipeline:

- `scripts/monthly_pipeline.ipynb`

It builds a monthly panel containing:
>>>>>>> origin/codex/debug-extractdata.ipynb-vcy2a2

- Futures returns (corn, soybean, wheat)
- ENSO index (ONI)
- Temperature anomaly
- Precipitation anomaly
- Drought index
- Extreme heat events
- U.S. dollar index
- Interest rate
- VIX

<<<<<<< HEAD
## Pipeline layout

- `scripts/download_futures.py` – Yahoo Finance futures prices and monthly log returns.
- `scripts/download_macro_fred.py` – FRED macro series (USD index, interest rate, VIX).
- `scripts/download_climate_disaster.py` – ONI from NOAA CPC + optional monthly CSV inputs for drought/temp/precip/extreme heat.
- `scripts/build_monthly_panel.py` – merge all inputs into one final monthly panel.
- `scripts/run_pipeline.py` – runs all steps in sequence.

=======
>>>>>>> origin/codex/debug-extractdata.ipynb-vcy2a2
## Required setup

1. Install dependencies:

```bash
python -m pip install -e .
```

2. Set your FRED API key:

```bash
export FRED_API_KEY="your_key_here"
```

<<<<<<< HEAD
3. (Optional but recommended) provide monthly CSV files for climate/disaster variables in `data/raw/`:
=======
3. Optional monthly CSV files in `data/raw/` (if available):
>>>>>>> origin/codex/debug-extractdata.ipynb-vcy2a2

- `drought_monthly_input.csv` with columns: `date,drought_index`
- `temp_anomaly_input.csv` with columns: `date,temperature_anomaly`
- `precip_anomaly_input.csv` with columns: `date,precipitation_anomaly`
- `extreme_heat_input.csv` with columns: `date,extreme_heat_events`

<<<<<<< HEAD
If these files are missing, the pipeline still runs and leaves those columns as missing values.

## Run

```bash
python scripts/run_pipeline.py
=======
If optional files are missing, the notebook still runs and keeps those variables as missing values where necessary.

## Run notebook pipeline

```bash
jupyter nbconvert --to notebook --execute scripts/monthly_pipeline.ipynb --inplace
>>>>>>> origin/codex/debug-extractdata.ipynb-vcy2a2
```

Final output:

- `data/processed/monthly_panel.csv`
