FROM python:3.12

# 작업 디렉토리 설정
WORKDIR /app

# 루트 디렉토리의 모든 파일을 컨테이너의 /app 디렉토리로 복사
COPY . /app

RUN apt-get update
RUN pip install -r requirements.txt
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

ENTRYPOINT [ "python", "main.py" ]