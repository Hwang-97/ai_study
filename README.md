## python 설치

### venv 이름의 파일에 가상환경 생성
python3 -m venv ./venv

#### 가상환경 적용
source venv/bin/activate

#### 필수 패키지 설치
pip3 install -r requirements.txt

#### db setting
init.sh or init.bat 실행

#### api 서버 실행
run.sh run.bat 실행

#### url
http://localhost:3006/api/v1/test/?str=실행확인!!

#### 사용모델
chat : Bllossom/llama-3.2-Korean-Bllossom-3B

news 분석 : ProsusAI/finbert

거래 판단 : google/flan-t5-base
