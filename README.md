# 🌱 무비빔밥
사용자 선호 및 위치 기반 영화관을 추천해주는 **지능형 고객 지원 챗봇**

<img src="https://github.com/user-attachments/assets/342ac0ff-9b80-4e05-8504-551a7830d80e" width="400" height="400" />


- 🔗 서비스 링크 : ~~http://d14hn9nv9zhgf7.cloudfront.net/~~
- 📅 개발 기간 : 2024.07.17 ~ 2024.09.03 (7주)

<br>

## 👫 팀 구성 및 역할

<details>
<summary> 🎞️ Alyssa - 인공지능 담당</summary>
<div markdown="1">

- Git : https://github.com/Yeeun-Jeong
- ChatGPT API를 활용한 응답 생성
    - 사용자 질문 데이터 전처리
    - 프롬프트 엔지니어링을 통한 영화관 추천 생성
- 프로젝트 협업 관리

</div>
</details>



<details>
<summary> 🎾 Ryan - 인공지능 담당</summary>
<div markdown="1">

- Git : https://github.com/KHyunJoong
- LLM ChatGPT api를 활용한 응답 생성
    - 사용자 질문에서 NER을 이용하여 Entity 추출
    - koBERT,kiwi를 이용한 RAG구축 후
    - FAISS를 이용한 Semantic Search, 및 Levenshtein distance 기반 검색 기능 개발
    - LLM 응답 정형화

</div>
</details>

<details>
<summary> 🧩 Yohan - 풀스택 담당</summary>
<div markdown="1">

- Git : https://github.com/yohanii
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
<summary> 🍭 Mir - 풀스택 담당</summary>
<div markdown="1">

- Git : https://github.com/mirlee0304
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
<summary> 🎸 Bryan - 클라우드 담당</summary>
<div markdown="1">

- Git : https://github.com/dogyungkim
- AWS 인프라 설계
- Terraform을 활용해 AWS 구현
- Ansible을 활용한 EC2 인스턴스 개발 환경 구축
- Prometheus 및 Grafana를 활용한 인스턴스 모니터링 환경 구축

</div>
</details>

<details>
<summary> 🚀 Eddy - 클라우드 담당</summary>
<div markdown="1">

- Git : https://github.com/KimMinWoooo
- CI/CD 파이프라인 구축
- Docker를 이용한 애플리케이션 이미지 만들기 및 배포
- 전체적인 배포 환경에서의 애플리케이션 실행 테스트

</div>
</details>

<br>

## 🔧 주요 기능
- 채팅, 버튼을 통한, 의사소통 기능
- 영화 이름, 지역, 날짜, 시간 정보를 통해 조건에 맞는 영화관의 상영 정보 제공 기능

<br>

## 📚 Stack
- Frontend   
   <img src="https://img.shields.io/badge/react-61DAFB?style=for-the-badge&logo=react&logoColor=black">
- Backend   
   <img src="https://img.shields.io/badge/java-007396?style=for-the-badge&logo=java&logoColor=white">  <img src="https://img.shields.io/badge/spring-6DB33F?style=for-the-badge&logo=spring&logoColor=white"> <img src="https://img.shields.io/badge/springboot-6DB33F?style=for-the-badge&logo=springboot&logoColor=white"> <img src="https://img.shields.io/badge/JPA-6DB33F?style=for-the-badge&logoColor=white"> <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white"> 
- Cloud  
    <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white"> <img src="https://img.shields.io/badge/Terraform-844FBA?style=for-the-badge&logo=Terraform&logoColor=white"> <img src="https://img.shields.io/badge/Ansible-EE0000?style=for-the-badge&logo=Ansible&logoColor=white"> <img src="https://img.shields.io/badge/Github Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white"> <img src="https://img.shields.io/badge/prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white"> <img src="https://img.shields.io/badge/grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white"> <img src="https://img.shields.io/badge/AWS-FF9900?style=for-the-badge&logoColor=white">
- AI  
    <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/chatgpt-000000?style=for-the-badge"> <img src="https://img.shields.io/badge/kobert-512BD4?style=for-the-badge"> <img src="https://img.shields.io/badge/faiss-DB6A26?style=for-the-badge"> <img src="https://img.shields.io/badge/langchain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white"> 

<br>

## 🗺️ 아키텍처
![Movie-chatbot1](https://github.com/user-attachments/assets/1e5d10f9-a22c-4588-90c4-65a51d475259)


<br>

## 💎 프로젝트 수행 결과

- 프론트엔드 [자세히](https://github.com/KTB-19/movie_chatbot/blob/main/docs/%EA%B2%B0%EA%B3%BC_%ED%94%84%EB%A1%A0%ED%8A%B8%EC%97%94%EB%93%9C.md)
  - React를 사용한 사용자 인터페이스 구축
  - 상태 관리 및 전역 상태 관리
  - 백엔드 API와의 통신
- 백엔드 [자세히](https://github.com/KTB-19/movie_chatbot/blob/main/docs/%EA%B2%B0%EA%B3%BC_%EB%B0%B1%EC%97%94%EB%93%9C.md)
    - RESTful API 설계에 대한 이해 및 적용
    - BDDMockito, JUnit5를 사용한 단위 테스트 작성
    - ExceptionHandler을 통한 공통 예외 처리
    - Validation 과정을 통해 데이터 유효성 검증
    - Swagger를 사용한 API 명세서 작성
    - AI 워드 임베딩 과정 스케줄링
- 크롤링 [자세히](https://github.com/KTB-19/movie_chatbot/blob/main/docs/%EA%B2%B0%EA%B3%BC_%ED%81%AC%EB%A1%A4%EB%A7%81.md)
  - Kobis에서 제공하는 지역별 및 날짜별 상영 스케줄 정보를 크롤링
  - DB 설계 및 데이터 저장
  - 크롤링 속도 개선을 위해 멀티프로세싱 적용
- 클라우드 [자세히](https://github.com/KTB-19/movie_chatbot/blob/main/docs/%EA%B2%B0%EA%B3%BC_%ED%81%B4%EB%9D%BC%EC%9A%B0%EB%93%9C.md)
  - Terraform을 활용한 인프라 구성
  - Ansible을 활용하여 Docker, Docker-compose, Node_exporter를 세팅
  - Github Actions를 이용한 CI/CD
  - Prometheus, Grafana를 통해 모니터링
  - 컨테이너 배포 후 연결 및 배포환경 api 연결
- 인공지능 [자세히](https://github.com/KTB-19/movie_chatbot/blob/main/docs/%EA%B2%B0%EA%B3%BC_%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5.md)
  - RAG 활용한 영화관 추천 전문 고객지원 챗봇 커스텀
  - ChatGPT API 프롬프트 엔지니어링을 통해 응답 생성

<br>

## ⚠️ 트러블 슈팅

- 프론트엔드 [자세히](https://github.com/KTB-19/movie_chatbot/blob/main/docs/%ED%8A%B8%EB%9F%AC%EB%B8%94%EC%8A%88%ED%8C%85_%ED%94%84%EB%A1%A0%ED%8A%B8%EC%97%94%EB%93%9C.md)
  - useRef를 사용한 상태 반영
- 백엔드 [자세히](https://github.com/KTB-19/movie_chatbot/blob/main/docs/%ED%8A%B8%EB%9F%AC%EB%B8%94%EC%8A%88%ED%8C%85_%EB%B0%B1%EC%97%94%EB%93%9C.md)
  - AI 코드 구동을 위한 효율적인 아키텍처
  - stream을 활용한 복잡한 로직 단순화
- 크롤링 [자세히](https://github.com/KTB-19/movie_chatbot/blob/main/docs/%ED%8A%B8%EB%9F%AC%EB%B8%94%EC%8A%88%ED%8C%85_%ED%81%AC%EB%A1%A4%EB%A7%81.md)
  - 멀티 프로세싱을 사용한 크롤링 시간 단축
- 클라우드 [자세히](https://github.com/KTB-19/movie_chatbot/blob/main/docs/%ED%8A%B8%EB%9F%AC%EB%B8%94%EC%8A%88%ED%8C%85_%ED%81%B4%EB%9D%BC%EC%9A%B0%EB%93%9C.md)
  - Mysql 도커 이미지로 EC2에서 Endtrypoint 에러
  - Python Crawling 이미지 생성 중 chrome browser 설치 문제
  - 크롤링 인스턴스의 적절한 type 설정
  - 크롤링 이외의 시간에 사용되지 않는 인스턴스
  - 인스턴스와 서브넷 등의 네트워크 관계에 대한 공부의 필요성
  - CI/CD는 모든 상황에서 필요한 것인가?
  - Docker container 배포시 각 컨테이너의 연결 방법에 대한 고민
- 인공지능 [자세히](https://github.com/KTB-19/movie_chatbot/blob/main/docs/%ED%8A%B8%EB%9F%AC%EB%B8%94%EC%8A%88%ED%8C%85_%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5.md)
  - chatgpt api를 활용한 최적의 응답 생성 방법
  - 가공을 위한 정형화된 아웃풋
  - chatgpt api를 활용한 엔티티 추출 방식

<br>

## 🥳 회고

- 종합 회고
  - 성과
    - 👍 초기 계획한 최소 기능 구현 완료
    - 👎 처음부터 기획 기능을 명확히 설계했다면, 시간 절약했을 듯
    - 👎 실 서비스 사용 테스트를 통해 예외 처리 개선 필요
  - 배움
    - 👍 서로 다른 직무 간 협업 방식을 익힘
    - 👍 실무에 필요한 기술 습득
  - 협업
    - 👍 매일 스크럼을 통해 진행상황과 문제점 공유
    - 👍 애자일 방식 도입을 통해 즉각적으로 논의 및 수정
    - 👎 일정 딜레이와 스프린트 진행 방식 변경이 아쉬움
    - 👎 태스크 관리 및 문서화 할 수 있는 환경 필요
- [개인별 회고](https://github.com/KTB-19/movie_chatbot/blob/main/docs/%ED%9A%8C%EA%B3%A0.md)


<br>

## 📌 시연

- 메인 화면
<img src="https://github.com/user-attachments/assets/54a43b61-b472-4d52-9544-8ebd5c2d2163" width=600>
<img src="https://github.com/user-attachments/assets/8bda2c90-fe6b-4f97-8991-441c6fb80440" width=600>

