#!/bin/bash

INITSCRIPT_NAME=${1:-add_stocks}

# 모델 변경 사항 감지
python3 manage.py makemigrations

# 데이터베이스에 적용
python3 manage.py migrate

# Django 스크립트 실행
echo "Running Django script..."
python3 manage.py runscript $INITSCRIPT_NAME

# 작업 완료
echo "Finished running script."