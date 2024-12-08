@echo off

set PORT=%1
if "%PORT%"=="" set PORT=8000

python3 manage.py runserver localhost:%PORT%

pause
