# 간단한 NLP app을 위한 도커 파일

# 최신 Ubuntu image로 시작하자
FROM ubuntu:latest

# 최신 업데이트 설치
RUN apt-get update -y

# 파이썬 설치 및 라이브러리 구축
RUN apt-get install -y python-pip python-dev build-essential

# 현재 폴더(.)에서 컨테이너 폴더(.)로 모든 파일을 복사
COPY . .

# 워킹 디렉터리를 컨테이너 기본 폴더(.)로 설정
WORKDIR .

# requirements 파일에 명시된 모든 의존성 설치
RUN pip install -r requirements.txt

# 컨테이너가 시작할 때 실행할 프로그램 지정
ENTRYPOINT [ "python" ]

# 앱을 실행하기 위해 입력 명령에 파일을 매개변수로 전달
CMD [ "app.py" ]