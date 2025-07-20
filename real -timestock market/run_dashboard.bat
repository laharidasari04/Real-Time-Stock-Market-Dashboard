@echo off
echo 🚀 Starting Real-Time Stock Market Dashboard...
echo ==================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if stock_dashboard.py exists
if not exist "stock_dashboard.py" (
    echo ❌ stock_dashboard.py not found!
    echo Please run this script from the project directory.
    pause
    exit /b 1
)

REM Install requirements if needed
echo 📦 Checking dependencies...
pip install -r requirements.txt >nul 2>&1

REM Start the dashboard
echo 🌐 Starting Streamlit server...
echo 📱 Dashboard will open in your default browser
echo 🔄 To stop the server, press Ctrl+C
echo ==================================================

python -m streamlit run stock_dashboard.py

pause 