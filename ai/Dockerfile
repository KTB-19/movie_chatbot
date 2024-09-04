# 공식 Python 3.12 런타임을 부모 이미지로 사용
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치 (git 추가)
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# 프로젝트 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 파일 복사
COPY . .

# 데이터 저장을 위한 디렉토리 생성
RUN mkdir -p /app/data

# 환경 변수 설정
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# 포트 8000 노출
EXPOSE 8000

# FastAPI 애플리케이션 실행
CMD ["python", "app/main.py"]
