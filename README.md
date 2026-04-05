# EAS508 Statistics Project

This repository builds a **monthly panel dataset** for analyzing and predicting agricultural futures returns (corn / soybean / wheat) with macro + climate + disaster features.

---

## 1) Repository structure

- `scripts/monthly_pipeline.ipynb`  
  **Main end-to-end pipeline (recommended)**. It downloads/constructs all feature blocks and writes final panel.
- `scripts/extractdata.ipynb`  
  Lightweight extraction notebook for raw futures + ONI + FEMA disaster features.
- `scripts/ml_response_feature_exploration.ipynb`  
  Initial data inspection + baseline ML feasibility test (`futures_return` as response, others as features).
- `scripts/data/raw/*.csv`  
  Example/raw intermediate files.
- `project_submissions/extractdata.ipynb`  
  Submission copy/history notebook.

---

## 2) Variables in the monthly panel

Core variables currently include:

- Futures: `futures_price`, `futures_return`, `commodity`
- Macro (FRED): `usd_index`, `interest_rate`, `vix`
- Climate: `enso_oni`
- Optional local climate inputs (if provided):
  - `temperature_anomaly`
  - `precipitation_anomaly`
  - `drought_index`
  - `extreme_heat_events`
- Disaster (FEMA monthly aggregates):
  - `disaster_event_count`
  - `disaster_storm_count`
  - `disaster_fire_count`
  - `disaster_flood_count`

---

## 3) Environment setup

Install dependencies:

```bash
python -m pip install -e .
```

Set FRED API key (**required** for `monthly_pipeline.ipynb`):

```bash
export FRED_API_KEY="<your_fred_api_key>"
```

> You can get a free FRED key from St. Louis Fed.

---

## 4) Recommended run order (from clean state)

### Step A — Build the full dataset (must run first)
Run:

- `scripts/monthly_pipeline.ipynb`

What it does:
1. Download futures prices and compute monthly log returns
2. Download macro series from FRED
3. Download ONI + FEMA disaster data (and merge optional local climate files if present)
4. Merge into one panel
5. Save outputs

Expected outputs:
- `data/raw/futures_monthly.csv`
- `data/raw/macro_monthly.csv`
- `data/raw/climate_disaster_monthly.csv`
- `data/processed/monthly_panel.csv`  ← main modeling table

### Step B — Inspect and test prediction feasibility
Run:

- `scripts/ml_response_feature_exploration.ipynb`

What it does:
1. Read `data/processed/monthly_panel.csv`
2. Check columns, missingness, date range, commodity coverage
3. Build simple lag features
4. Train/test split by time
5. Fit baseline `Ridge` + `RandomForestRegressor`
6. Report MAE/RMSE/R²

### Optional Step C — Raw extraction notebook only
Run:

- `scripts/extractdata.ipynb`

Use this when you only want quick raw extraction (without full panel merge).

---

## 5) Notes on optional climate input files

`monthly_pipeline.ipynb` will try to read these files if they exist:

- `data/raw/drought_monthly_input.csv` with columns: `date`, `drought_index`
- `data/raw/temp_anomaly_input.csv` with columns: `date`, `temperature_anomaly`
- `data/raw/precip_anomaly_input.csv` with columns: `date`, `precipitation_anomaly`
- `data/raw/extreme_heat_input.csv` with columns: `date`, `extreme_heat_events`

If not found, pipeline continues and those columns are mostly NA.

---

## 6) Common issues / troubleshooting

1. **`FRED_API_KEY` missing**  
   Set env var first, then re-run notebook kernel.

2. **Network/API request failures**  
   Retry later; this pipeline depends on Yahoo Finance / FRED / NOAA / FEMA endpoints.

3. **`data/processed/monthly_panel.csv` missing**  
   You must run `scripts/monthly_pipeline.ipynb` successfully before ML notebook.

4. **Model performance seems weak**  
   This is normal for monthly return prediction; next step is rolling-window validation, stronger lag design, and interaction features.
