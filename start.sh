#!/usr/bin/env bash
set -euo pipefail
PORT="${PORT:-20468}"
export PORT
export PYTHONUNBUFFERED=1

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
if [ -f ".venv/bin/activate" ]; then
  . .venv/bin/activate
fi
python3 -m pip install --upgrade pip -q
python -m pip install -r requirements.txt -q
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT" --reload
