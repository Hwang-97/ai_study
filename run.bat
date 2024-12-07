@echo off

:: Usage: run.bat <project_name> <port>
:: Default values
set PROJECT_NAME=%1
if "%PROJECT_NAME%"=="" set PROJECT_NAME=study

set PORT=%2
if "%PORT%"=="" set PORT=8000

:: Navigate to the project directory
cd /d %~dp0%PROJECT_NAME%
if %errorlevel% neq 0 (
    echo Project directory not found!
    exit /b 1
)

:: Activate virtual environment (if any)
if exist "..\venv\Scripts\activate.bat" (
    call ..\venv\Scripts\activate.bat
)

:: Run the Django server on the specified port
python manage.py runserver localhost:%PORT%

pause
