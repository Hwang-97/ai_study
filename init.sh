#!/bin/bash

# ex) sh init.sh venv study
ENV_NAME=${1:-venv}
PROJECT_NAME=${2:-study}
INITSCRIPT_NAME=${3:-add_stocks}
SCRIPT_PATH="scripts/add_stocks.py"

python3 -m venv ./$ENV_NAME

# Activate virtual environment (if any)
if [ -f "../$ENV_NAME/bin/activate" ]; then
    source ../$ENV_NAME/bin/activate
fi

pip install -r requirements.txt

# 모델 변경 사항 감지
python $PROJECT_NAME/manage.py makemigrations

# 데이터베이스에 적용
python $PROJECT_NAME/manage.py migrate

# Django 스크립트 실행
echo "Running Django script..."
python $PROJECT_NAME/manage.py runscript $INITSCRIPT_NAME

# 작업 완료
echo "Finished running script."