#!/usr/bin/env bash
set -euo pipefail
PORT=46999
export PORT
export PYTHONUNBUFFERED=1

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
. .venv/bin/activate
python -m pip install --upgrade pip -q
python -m pip install -r requirements.txt -q
exec uvicorn app.main:app --host 0.0.0.0 --port 46999 --reload
