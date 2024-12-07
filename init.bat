@echo off

:: ex) init.bat venv study add_stocks
set ENV_NAME=%1
if "%ENV_NAME%"=="" set ENV_NAME=venv

set PROJECT_NAME=%2
if "%PROJECT_NAME%"=="" set PROJECT_NAME=study

set INITSCRIPT_NAME=%3
if "%INITSCRIPT_NAME%"=="" set INITSCRIPT_NAME=add_stocks

set SCRIPT_PATH=scripts\add_stocks.py

:: 가상환경 생성
echo Creating virtual environment...
python -m venv %ENV_NAME%

:: 가상환경 활성화
echo Activating virtual environment...
call %ENV_NAME%\Scripts\activate

:: 필요한 패키지 설치
echo Installing dependencies...
pip install -r requirements.txt

:: 모델 변경 사항 감지
echo Making migrations...
python %PROJECT_NAME%\manage.py makemigrations

:: 데이터베이스에 적용
echo Applying migrations...
python %PROJECT_NAME%\manage.py migrate

:: Django 스크립트 실행
echo Running Django script...
python %PROJECT_NAME%\manage.py runscript %INITSCRIPT_NAME%

:: 작업 완료
echo Finished running script.
pause
