@echo off
REM ============================================================
REM  Courier & Parcel Tracking System - one-command setup
REM  Creates a venv, installs deps, and starts the app.
REM  The database is auto-created and auto-seeded on first run.
REM ============================================================
setlocal

cd /d "%~dp0"

echo.
echo === Courier ^& Parcel Tracking System - Setup ===
echo.

REM --- 1. Find Python ---
where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python was not found on your PATH.
  echo         Please install Python 3.9+ from https://www.python.org/downloads/
  echo         and be sure to check "Add Python to PATH" during install.
  pause
  exit /b 1
)

REM --- 2. Create virtual environment (if missing) ---
if not exist "venv\" (
  echo [1/4] Creating virtual environment...
  python -m venv venv
  if errorlevel 1 (
    echo [ERROR] Failed to create the virtual environment.
    pause
    exit /b 1
  )
) else (
  echo [1/4] Virtual environment already exists - skipping.
)

REM --- 3. Install dependencies ---
echo [2/4] Installing dependencies...
call "venv\Scripts\python.exe" -m pip install --upgrade pip >nul
call "venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
  echo [ERROR] Failed to install dependencies.
  pause
  exit /b 1
)

REM --- 4. Start the app (DB is auto-created + auto-seeded on first run) ---
echo [3/4] Starting the app...
echo [4/4] Open your browser at:  http://127.0.0.1:5000
echo.
echo      Staff login:  admin / admin123
echo      Press CTRL+C in this window to stop the server.
echo.
call "venv\Scripts\python.exe" app.py

endlocal
