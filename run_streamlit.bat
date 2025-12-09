@echo off
REM LinkedIn Content Engine - Streamlit Launch Script

echo ============================================================
echo LinkedIn Content Engine - Streamlit Web Interface
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Please run setup first:
    echo   setup.bat
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist ".env" (
    echo [ERROR] .env file not found!
    echo.
    echo Please copy .env.example to .env and fill in your API keys:
    echo   copy .env.example .env
    echo.
    pause
    exit /b 1
)

REM Check if Streamlit is installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo [INFO] Streamlit not found. Installing...
    pip install streamlit
)

echo [OK] Environment ready
echo.
echo Starting Streamlit app...
echo.
echo The app will open in your browser at: http://localhost:8501
echo Press Ctrl+C to stop the server
echo.
echo ============================================================
echo.

streamlit run streamlit_app.py
