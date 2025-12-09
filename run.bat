@echo off
REM LinkedIn Content Engine - Quick Run Script

echo ============================================================
echo LinkedIn Content Engine - LangGraph Version
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Please run setup first:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
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

echo [OK] Virtual environment activated
echo [OK] .env file found
echo.

REM Parse command line argument
if "%1"=="continuous" (
    echo Starting in CONTINUOUS mode...
    echo Press Ctrl+C to stop
    echo.
    python main.py continuous %2
) else if "%1"=="single" (
    echo Running SINGLE execution...
    echo.
    python main.py single
) else (
    echo Usage:
    echo   run.bat single           - Run once for testing
    echo   run.bat continuous       - Run continuously every 2 minutes
    echo   run.bat continuous 300   - Run continuously every 5 minutes
    echo.
    echo Example:
    echo   run.bat single
    echo.
    pause
)
