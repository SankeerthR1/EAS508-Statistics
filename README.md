# EAS508 Statistics Project

Main notebook:
- `scripts/monthly_pipeline.ipynb`

## Quick start

```bash
python -m pip install -e .
export FRED_API_KEY="your_key"
jupyter nbconvert --to notebook --execute scripts/monthly_pipeline.ipynb --inplace
```

Output file:
- `data/processed/monthly_panel.csv`

Optional local input files (if you have them):
- `data/raw/oni_monthly_input.csv` (`date`, `enso_oni`)
- `data/raw/drought_monthly_input.csv` (`date`, `drought_index`)
- `data/raw/temp_anomaly_input.csv` (`date`, `temperature_anomaly`)
- `data/raw/precip_anomaly_input.csv` (`date`, `precipitation_anomaly`)
- `data/raw/extreme_heat_input.csv` (`date`, `extreme_heat_events`)
