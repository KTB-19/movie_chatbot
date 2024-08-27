# 빌드 스테이지
FROM openjdk:21-oracle AS build

# 필요한 유틸리티 설치
RUN microdnf install findutils

WORKDIR /workspace/app

# Gradle Wrapper와 빌드 스크립트 복사
COPY gradlew .
COPY gradle gradle
COPY build.gradle .
COPY settings.gradle .

# 소스 코드 복사
COPY src src

# Gradle Wrapper에 실행 권한 부여
RUN chmod +x ./gradlew

# Gradle을 사용하여 애플리케이션 빌드
RUN ./gradlew build -x test

# 실행 스테이지
FROM openjdk:21-oracle

WORKDIR /app

# 빌드 스테이지에서 생성된 JAR 파일 복사
COPY --from=build /workspace/app/build/libs/*.jar app.jar

# 설정 파일 복사
COPY src/main/resources/application.yml /app

# 애플리케이션 실행
ENTRYPOINT ["java", "-jar", "app.jar"]