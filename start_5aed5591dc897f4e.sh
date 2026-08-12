#!/usr/bin/env bash
set -e
export PORT=39693
export PYTHONUNBUFFERED=1
if [ -f "./start.sh" ]; then
  bash ./start.sh
else
  python3 -m venv .venv 2>/dev/null || true
  source .venv/bin/activate
  if [ -f "./requirements.txt" ]; then
    pip install -r requirements.txt -q
  fi
  uvicorn app.main:app --host 0.0.0.0 --port 39693
fi
