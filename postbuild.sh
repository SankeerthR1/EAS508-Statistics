#!/bin/bash
set -e

homework_folder=$(find . -maxdepth 1 -type d -name 'homework*' | head -n 1)

cp $homework_folder/pyproject.toml .

# Sync python packages
uv sync

# Activate the environment
source ./.venv/bin/activate

# Install modflow
#mkdir -p ./modflow
#python -c "from flopy.utils import get_modflow; get_modflow('./modflow')"
#python -m ipykernel install --user --name ert574
