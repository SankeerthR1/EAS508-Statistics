# EAS508 Statistics Project

This repository contains the data pipeline for our EAS508 group project. The goal is to build a monthly dataset for statistical analysis of agricultural futures returns and their relationships with climate and macroeconomic variables.

## Project contents

The pipeline builds a monthly panel with the following variables:

- Futures returns for corn, soybean, and wheat
- ENSO index using ONI
- Temperature anomaly
- Precipitation anomaly
- Drought index
- Extreme heat events
- U.S. dollar index
- Interest rate
- VIX

## Main workflow

This project currently uses one notebook for the full pipeline:

- `scripts/monthly_pipeline.ipynb`

The notebook does the following:

1. Downloads and processes futures price data
2. Downloads macroeconomic series from FRED
3. Reads climate and disaster-related inputs
4. Merges all variables into one monthly panel
5. Saves the final dataset

## Output

The final output file is:

- `data/processed/monthly_panel.csv`

## Setup

Install the package and dependencies:

```bash
python -m pip install -e .
