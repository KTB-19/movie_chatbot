# 무비빔밥
사용자 선호 및 위치 기반 영화관을 추천해주는 **지능형 고객 지원 챗봇**

<img src="https://github.com/user-attachments/assets/342ac0ff-9b80-4e05-8504-551a7830d80e" width="400" height="400" />


- 🔗 서비스 링크 : http://d14hn9nv9zhgf7.cloudfront.net/
- 📅 개발 기간 : 2024.07.17 ~ 2024.09.03 (7주)

<br>

## 팀 구성 및 역할

<details>
<summary>Alyssa - 인공지능 담당</summary>
<div markdown="1">

- ChatGPT API를 활용한 응답 생성
    - 사용자 질문 데이터 전처리
    - 프롬프트 엔지니어링을 통한 영화관 추천 생성
- 프로젝트 협업 관리

</div>
</details>

<details>
<summary>Ryan - 인공지능 담당</summary>
<div markdown="1">

- LLM ChatGPT api를 활용한 응답 생성
    - 사용자 질문에서 NER을 이용하여 Entity 추출
    - koBERT,kiwi를 이용한 RAG구축 후
    - FAISS를 이용한 Semantic Search, 및 Levenshtein distance 기반 검색 기능 개발
    - LLM 응답 정형화

</div>
</details>

<details>
<summary>Yohan - 풀스택 담당</summary>
<div markdown="1">

- 백엔드
    - Spring 애플리케이션 서버 개발
    - AI 모델 구동을 위한 FastAPI 서버 개발
    - OpenFeign을 사용해 서버 간 통신 구현
    - MySQL DB 조회 기능 개발
- 프론트엔드
    - 날짜 선택, 지역 선택 화면 구현

</div>
</details>

<details>
<summary>Mir - 풀스택 담당</summary>
<div markdown="1">

- 영화 상영정보 크롤링 및 DB에 저장
- 프론트엔드
    - 채팅 화면 구현
        - 질문-답변 채팅형태 구현 및 엔티티 관리
        - 매뉴얼/응답대기 메시지 및 재확인 버튼/체크박스 구현
        - 스타일 적용
    - 백엔드 연결

</div>
</details>

<details>
<summary>Bryan - 클라우드 담당</summary>
<div markdown="1">

- AWS 인프라 설계
- Terraform을 활용해 AWS 구현
- Ansible을 활용한 EC2 인스턴스 개발 환경 구축
- Prometheus 및 Grafana를 활용한 인스턴스 모니터링 환경 구축

</div>
</details>

<details>
<summary>Eddy - 클라우드 담당</summary>
<div markdown="1">

- CI/CD 파이프라인 구축
- Docker를 이용한 애플리케이션 이미지 만들기 및 배포
- 전체적인 배포 환경에서의 애플리케이션 실행 테스트

</div>
</details>

<br>

## 주요 기능
- 채팅, 버튼을 통한, 의사소통 기능
- 영화 이름, 지역, 날짜, 시간 정보를 통해 조건에 맞는 영화관의 상영 정보 제공 기능

<br>

## Stack
- Frontend : <img src="https://img.shields.io/badge/react-61DAFB?style=for-the-badge&logo=react&logoColor=black">
- Backend : <img src="https://img.shields.io/badge/java-007396?style=for-the-badge&logo=java&logoColor=white">  <img src="https://img.shields.io/badge/spring-6DB33F?style=for-the-badge&logo=spring&logoColor=white"> <img src="https://img.shields.io/badge/springboot-6DB33F?style=for-the-badge&logo=springboot&logoColor=white"> <img src="https://img.shields.io/badge/JPA-6DB33F?style=for-the-badge&logoColor=white"> <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white"> 
- Cloud : <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white"> <img src="https://img.shields.io/badge/Terraform-844FBA?style=for-the-badge&logo=Terraform&logoColor=white"> <img src="https://img.shields.io/badge/Ansible-EE0000?style=for-the-badge&logo=Ansible&logoColor=white"> <img src="https://img.shields.io/badge/Github Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white"> <img src="https://img.shields.io/badge/prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white"> <img src="https://img.shields.io/badge/grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white"> <img src="https://img.shields.io/badge/AWS-FF9900?style=for-the-badge&logoColor=white">
- AI : <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/chatgpt-000000?style=for-the-badge"> <img src="https://img.shields.io/badge/kobert-512BD4?style=for-the-badge"> <img src="https://img.shields.io/badge/faiss-DB6A26?style=for-the-badge"> <img src="https://img.shields.io/badge/langchain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white"> 

<br>

## 아키텍처

<br>

## 프로젝트 수행 결과

- 풀스택
- 클라우드
- 인공지능

<br>

## 트러블 슈팅

- 풀스택
- 클라우드
- 인공지능

<br>

## 회고

- 회고

<br>
