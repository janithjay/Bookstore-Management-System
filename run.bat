@echo off
REM Bookstore Simulation Launcher with Java Path
REM This script ensures Java is in PATH before running Streamlit

echo Starting Bookstore Management System...
echo.

REM Add Java to PATH
set PATH=C:\Program Files\Eclipse Adoptium\jre-17.0.16.8-hotspot\bin;%PATH%

REM Activate virtual environment
call venv\Scripts\activate

REM Run Streamlit dashboard
echo Launching Streamlit dashboard...
streamlit run ui/streamlit_app.py

pause
