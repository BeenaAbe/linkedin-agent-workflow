@echo off
REM LinkedIn Content Engine - Setup Script

echo ============================================================
echo LinkedIn Content Engine - Setup
echo ============================================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    echo Make sure Python 3.10+ is installed
    pause
    exit /b 1
)
echo [OK] Virtual environment created
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Activated
echo.

echo Step 3: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] All packages installed
echo.

echo Step 4: Setting up environment file...
if exist ".env" (
    echo [SKIP] .env already exists
) else (
    copy .env.example .env
    echo [OK] Created .env file
    echo.
    echo ============================================================
    echo IMPORTANT: Edit .env file with your API keys!
    echo ============================================================
    echo.
    echo Required keys:
    echo   - NOTION_TOKEN
    echo   - NOTION_DATABASE_ID
    echo   - TAVILY_API_KEY
    echo   - OPENROUTER_API_KEY  ^(same as your n8n workflow^)
    echo   - SLACK_WEBHOOK_URL
    echo.
)

echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo   1. Edit .env file with your API keys
echo   2. Run test: run.bat single
echo   3. Run continuous: run.bat continuous
echo.
pause
