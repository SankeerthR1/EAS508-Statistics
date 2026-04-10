# EAS508 Statistics Project

This repo builds a monthly commodity panel and evaluates forecasting workflows for next-month agricultural return prediction (`corn`, `soybean`, `wheat`).

## 1) Workflow At A Glance

1. Build the monthly panel from USDA + FRED + NOAA + FEMA + ONI:
   - `scripts/monthly_pipeline.ipynb`
2. Train/evaluate forecasting models and export metrics/explainability:
   - `scripts/ml_response_feature_exploration.ipynb`
3. Optional lightweight extraction notebook (legacy/quick check):
   - `scripts/extractdata.ipynb`

Main modeling table:
- `data/processed/monthly_panel.csv`

## 2) Repository Layout

- `scripts/monthly_pipeline.ipynb`  
  End-to-end data build and merge into final panel.
- `scripts/ml_response_feature_exploration.ipynb`  
  Feature engineering, preprocessing, model training, holdout + rolling validation, SARIMAX baseline, explainability outputs.
- `scripts/extractdata.ipynb`  
  Optional simplified extraction notebook.
- `data/raw/*.csv`  
  Intermediate outputs from extraction/aggregation.
- `data/processed/monthly_panel.csv`  
  Final panel used by modeling notebook.
- `data/performance/**`  
  Saved model metrics and explainability artifacts.

## 3) What Is Input vs Output In Modeling?

### Target (output)

- `target_next_return = futures_return.shift(-1)` by commodity (next-month return).
- `futures_return` is a log return:
  - `log(futures_price_t) - log(futures_price_{t-1})`

### Inputs (features)

Raw panel columns include:
- Price/identity: `futures_price`, `price_proxy`, `commodity`, source metadata columns
- Macro: `usd_index`, `interest_rate`, `vix`
- Climate: `enso_oni`, `temperature_anomaly`, `precipitation_anomaly`, `drought_index`, `extreme_heat_events`
- Disaster: `disaster_event_count`, `disaster_storm_count`, `disaster_fire_count`, `disaster_flood_count`
- Geography metadata: `climate_location_code`

Engineered modeling features include:
- Calendar/time: `month_num`, `month`, `time_idx`
- Lags (1, 2, 3, 6, 12 months) for:
  - `futures_return`, `futures_price`, `usd_index`, `interest_rate`, `vix`, `enso_oni`
  - `disaster_event_count`, `disaster_storm_count`, `disaster_fire_count`, `disaster_flood_count`
- Return momentum/volatility:
  - `ret_mean_3/6/12`, `ret_std_3/6/12`

Notes on scales/transforms:
- `futures_return` and `target_next_return` are log-return values.
- Most other covariates are used as raw levels/counts/anomalies (not logged).

## 4) Data Cleaning And Preprocessing

This section focuses on cleaning/processing (not source acquisition).

### In `monthly_pipeline.ipynb`

- Normalize all dates to month-end.
- USDA series filtering:
  - Keep only `"$ / BU"` rows.
  - Prefer `domain_desc == "TOTAL"` when available.
  - Prefer commodity canonical `short_desc` to avoid subtype mixing.
  - Parse/coerce numeric values and remove invalid rows.
  - De-duplicate by `(commodity, date)`.
- ONI cleanup:
  - Map seasonal labels (`DJF`, `JFM`, ...) to month.
  - Drop rows with invalid mapped month/date.
- FEMA cleanup:
  - Parse declaration dates, drop invalid dates.
  - Fill missing `incidentType` with `"Unknown"`.
  - Aggregate monthly total and type-specific event counts.
  - Fill missing monthly disaster counts with `0.0`.
- NOAA Climate-at-a-Glance cleanup:
  - Parse both JSON/CSV formats robustly.
  - Coerce values to numeric, drop invalid rows, de-duplicate dates.
- Final panel trimming:
  - Compute first non-null availability for required core columns.
  - Trim panel start to max of those dates so the panel is jointly usable.

### In `ml_response_feature_exploration.ipynb`

- Drop rows where target is missing (last month per commodity after shift).
- Drop ultra-sparse columns only if missingness > 90% (if any).
- Numeric preprocessing pipeline:
  - `SimpleImputer(median)` -> winsorize (`1%`, `99%`) -> `RobustScaler`
- Categorical preprocessing pipeline:
  - `SimpleImputer(most_frequent)` -> `OneHotEncoder(handle_unknown="ignore")`
- SARIMAX exogenous preprocessing:
  - forward fill -> backward fill -> fill remaining with `0.0`

## 5) Modeling Process

Implemented in `scripts/ml_response_feature_exploration.ipynb`.

Models:
- Baselines: `seasonal_naive`, `naive_lag1`
- Linear: `Ridge`, `ElasticNet`
- Tree/boosting: `HistGradientBoostingRegressor`
- Optional (if installed): `XGBoost`, `LightGBM`
- Separate baseline family: commodity-wise `SARIMAX` with exogenous regressors

Target variants:
- `raw`
- `deseason_winsor`:
  - subtract commodity-month seasonal mean from target
  - winsorize transformed target at 1%/99%
  - add seasonal component back for raw-scale prediction evaluation

Validation strategy:
- Final holdout: last 24 months
- Rolling-origin validation: repeated 24-month windows
- Also reported commodity-wise rolling summaries

Metrics:
- MAE, RMSE, R², direction accuracy

Explainability exports (LightGBM only, if available):
- Permutation importance (global)
- Mean contribution tables (global)
- Local contribution breakdown for latest holdout sample

## 6) Setup

Install dependencies:

```bash
python -m pip install -e .
```

Set required API keys:

```bash
export FRED_API_KEY="<your_fred_api_key>"
export USDA_NASS_API_KEY="<your_usda_nass_api_key>"
```

If your notebook kernel does not inherit shell environment vars, create `.env` at repo root:

```bash
FRED_API_KEY="<your_fred_api_key>"
USDA_NASS_API_KEY="<your_usda_nass_api_key>"
```

Then restart the notebook kernel.

## 7) How To Run End-To-End

From a clean state:

1. Run all cells in `scripts/monthly_pipeline.ipynb`
2. Confirm output files exist:
   - `data/raw/price_proxy_monthly.csv`
   - `data/raw/macro_monthly.csv`
   - `data/raw/climate_disaster_monthly.csv`
   - `data/processed/monthly_panel.csv`
3. Run all cells in `scripts/ml_response_feature_exploration.ipynb`
4. Check exported evaluation files:
   - `data/performance/metrics/global/model_holdout_results.csv`
   - `data/performance/metrics/global/model_rolling_summary.csv`
   - `data/performance/metrics/commodity/model_commodity_rolling_summary.csv`
   - `data/performance/metrics/sarimax/sarimax_holdout_results.csv`
   - `data/performance/metrics/sarimax/sarimax_rolling_summary.csv`
   - `data/performance/explainability/**` (if LightGBM available)

Optional:
- Run `scripts/extractdata.ipynb` for quick extraction-only checks.

## 8) Troubleshooting

1. `FRED_API_KEY` or `USDA_NASS_API_KEY` missing  
   Set env vars / `.env`, restart kernel, rerun.
2. API/network failures  
   Retry; pipeline depends on external endpoints.
3. `data/processed/monthly_panel.csv` missing  
   Run `scripts/monthly_pipeline.ipynb` first.
4. `xgboost`/`lightgbm` unavailable  
   Notebook continues and skips unavailable model blocks.
5. Weak predictive performance  
   Expected for monthly return forecasting; use rolling and commodity-specific diagnostics to interpret model value.
