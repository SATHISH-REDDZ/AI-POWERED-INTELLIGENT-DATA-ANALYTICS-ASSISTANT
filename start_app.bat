@echo off
title AI-Powered Intelligent Data Analytics Assistant Launcher
echo ============================================================
echo   Starting AI-Powered Intelligent Data Analytics Assistant...
echo ============================================================
echo.

cd /d "%~dp0"

echo Launching Flask Web Server...
start http://127.0.0.1:5000

python run.py

pause
