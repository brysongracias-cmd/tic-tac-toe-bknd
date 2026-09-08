@echo off
set PORT=20468
set PYTHONUNBUFFERED=1
if not exist .venv (
  python -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip -q
python -m pip install -r requirements.txt -q
uvicorn app.main:app --host 0.0.0.0 --port 20468 --reload
