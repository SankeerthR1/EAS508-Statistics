# EAS508 Statistics Project

This repository now uses **one notebook** for the full monthly pipeline:

- `scripts/monthly_pipeline.ipynb`

It builds a monthly panel containing:

- Futures returns (corn, soybean, wheat)
- ENSO index (ONI)
- Temperature anomaly
- Precipitation anomaly
- Drought index
- Extreme heat events
- U.S. dollar index
- Interest rate
- VIX

## Required setup

1. Install dependencies:

```bash
python -m pip install -e .
```

2. Set your FRED API key:

```bash
export FRED_API_KEY="your_key_here"
```

3. Optional monthly CSV files in `data/raw/` (if available):

- `drought_monthly_input.csv` with columns: `date,drought_index`
- `temp_anomaly_input.csv` with columns: `date,temperature_anomaly`
- `precip_anomaly_input.csv` with columns: `date,precipitation_anomaly`
- `extreme_heat_input.csv` with columns: `date,extreme_heat_events`

If optional files are missing, the notebook still runs and keeps those variables as missing values where necessary.

## Run notebook pipeline

```bash
jupyter nbconvert --to notebook --execute scripts/monthly_pipeline.ipynb --inplace
```

Final output:

- `data/processed/monthly_panel.csv`
