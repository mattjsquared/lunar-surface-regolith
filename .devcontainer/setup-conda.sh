#!/usr/bin/env bash
set -euxo pipefail

# Speed up solves
conda install -n base -c conda-forge -y mamba

# Create/update the 'regolith' env from environment.yml
if conda env list | awk '{print $1}' | grep -qx regolith; then
  mamba env update -n regolith -f environment.yml
else
  mamba env create -f environment.yml
fi

# Auto-activate in interactive shells
echo 'conda activate regolith' >> ~/.bashrc

# Clean cache to keep image small
conda clean -afy

# Optional: quick smoke test so reviewers see success in the log
bash -lc "python - <<'PY'
import sys, numpy, pandas, matplotlib, shapely, geopandas, cartopy, pyinterp
print('Environment OK:', sys.executable)
PY"

