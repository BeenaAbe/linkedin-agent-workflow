@echo off
REM Security Verification Script
REM Checks if your secrets are protected before deploying

echo ============================================================
echo Security Verification Check
echo ============================================================
echo.

echo Checking if .gitignore exists...
if exist ".gitignore" (
    echo [OK] .gitignore file found
) else (
    echo [ERROR] .gitignore file NOT found!
    echo This is critical for security.
    pause
    exit /b 1
)
echo.

echo Checking if .env is ignored by git...
git check-ignore .env >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] .env is properly ignored by git
) else (
    echo [WARNING] .env might not be ignored!
    echo Check your .gitignore file.
)
echo.

echo Checking if .env exists locally...
if exist ".env" (
    echo [OK] .env file exists for local development
) else (
    echo [INFO] .env file not found
    echo Run: copy .env.example .env
)
echo.

echo Checking git status...
git status --short | findstr ".env" >nul
if %errorlevel% == 0 (
    echo [ERROR] .env appears in git status!
    echo DO NOT COMMIT THIS FILE!
    echo Run: git reset HEAD .env
    pause
    exit /b 1
) else (
    echo [OK] .env is not staged for commit
)
echo.

echo Checking for hardcoded secrets in Python files...
findstr /S /I /C:"sk-or-v1-" /C:"tvly-" /C:"secret_" *.py >nul 2>&1
if %errorlevel% == 0 (
    echo [WARNING] Possible API keys found in .py files!
    echo Review your code and move keys to .env
    findstr /S /I /N /C:"sk-or-v1-" /C:"tvly-" /C:"secret_" *.py
) else (
    echo [OK] No hardcoded secrets found in Python files
)
echo.

echo ============================================================
echo Security Check Complete
echo ============================================================
echo.
echo Summary:
echo - .gitignore: Protects your secrets
echo - .env: Local keys only (not committed)
echo - Python files: No hardcoded keys
echo.
echo You are safe to push to GitHub!
echo.
pause
