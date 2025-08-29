#!/usr/bin/env bash
set -euo pipefail

# Requires: Python 3.6.x, pipenv ~= 11.x (2018-era)
# Example setup:
#   pyenv local 3.6.9
#   pip install "pipenv==11.10.1"

export PIPENV_IGNORE_VIRTUALENVS=1
success=0
runs=10

for i in $(seq 1 $runs); do
  echo "=== Rebuild attempt $i/$runs ==="
  rm -rf .venv Pipfile.lock || true
  if pipenv lock --clear && pipenv install --deploy --ignore-pipfile; then
    echo "OK"
    success=$((success+1))
  else
    echo "FAIL"
  fi
done

echo "Successful rebuilds: $success/$runs"
