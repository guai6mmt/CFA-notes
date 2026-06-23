@echo off
chcp 65001 >nul
cd /d "%~dp0.."

set "PY=python"
if exist ".venv\Scripts\python.exe" set "PY=.venv\Scripts\python.exe"

echo Installing dependencies (first run may take a minute)...
"%PY%" -m pip install -q requests >nul 2>nul
"%PY%" -m pip install -q lameenc >nul 2>nul

"%PY%" scripts\generate_audio.py

echo.
pause
