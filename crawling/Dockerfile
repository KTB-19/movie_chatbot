FROM python:3.12

# 작업 디렉토리 설정
WORKDIR /app

# 루트 디렉토리의 모든 파일을 컨테이너의 /app 디렉토리로 복사
COPY . /app

# 가상환경 구축
RUN python venv -m crawlenv
RUN source crawlenv/bin/activate

# 필요 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 크롬 브라우저 설치
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
RUN sudo yum install ./google-chrome-stable_current_x86_64.rpm

RUN ["python", "main.py"]