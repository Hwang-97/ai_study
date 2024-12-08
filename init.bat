@echo off

set INITSCRIPT_NAME=%1
if "%INITSCRIPT_NAME%"=="" set INITSCRIPT_NAME=add_stocks

:: 모델 변경 사항 감지
echo Making migrations...
python3 manage.py makemigrations

:: 데이터베이스에 적용
echo Applying migrations...
python3 manage.py migrate

:: Django 스크립트 실행
echo Running Django script...
python3 manage.py runscript %INITSCRIPT_NAME%

:: 작업 완료
echo Finished running script.
pause
