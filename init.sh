#!/bin/bash

# ex) sh init.sh venv study
PROJECT_NAME=${1:-study}
INITSCRIPT_NAME=${2:-add_stocks}
SCRIPT_PATH="scripts/add_stocks.py"

# 모델 변경 사항 감지
python $PROJECT_NAME/manage.py makemigrations

# 데이터베이스에 적용
python $PROJECT_NAME/manage.py migrate

# Django 스크립트 실행
echo "Running Django script..."
python $PROJECT_NAME/manage.py runscript $INITSCRIPT_NAME

# 작업 완료
echo "Finished running script."