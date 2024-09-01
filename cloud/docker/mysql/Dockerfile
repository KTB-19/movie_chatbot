# 도커 버전 지정
FROM mysql:8.4.2

# 환경 변수 설정
ENV MYSQL_ROOT_PASSWORD=qlalfqjsgh486
ENV TZ=Asia/Seoul

# SQL 스크립트 copy 하기
COPY init.sql /docker-entrypoint-initdb.d/

# Linux 환경을 위한 권한 설정
RUN chmod 755 /docker-entrypoint-initdb.d/init.sql