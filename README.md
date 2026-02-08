# TECH

### 💡 Domain Structure

각 도메인은 DDD(Domain-Driven Design) 원칙에 따라 `controller`, `entity`, `repository`, `service` 레이어로 구성됨.  
또한 책임 단위로 분리되어 있으며, 유지보수성과 역할 분리가 명확하게 설계되어 있음. 
<br>

```
├──  app/ 
|      └── main.py
|
├── interview/                  질문 생성 및 면접 평가 도메인
|      ├── controller.py/       요청 처리 및 API 라우팅
|               ├── request_form/ Server(Django) DB에 저장된 사용자의 정보를 받음
|               └── interview_controller.py 
|      ├── entity.py/
|               ├── academic_background.py    사용자의 학력
|               ├──experience_level.py        신입/경력
|               ├──interview_tech_stack.py    사용가능한 기술스택
|               ├──job_category.py            직무 선택
|               ├──project_experience.py      프로젝트 경험 유/무
|               ├──end_of_interview.py        면접 평가를 위한 정보 저장
|               └── evaluation.py             평가 결과 저장
│      ├── repository.py/
|               ├─ interview_repository(_impl).py  면접 질문 생성 및 심화질문 생성 코드      
|               └── evaluate_repository(_impl).py  면접 평가 코드
│      └── service.py/
|               ├── request/
|               └── interview_service(_impl).py   질문 생성 및 평가 로직 컨트롤
|
├──  agent_api/   RAG 및 AGENT 도메인
|      ├── controller.py/
|               └── agent_controller.py          요청 처리 및 API 라우팅
|      ├── entity.py/
|               ├── embeddings.py
|               └── rag_schema.py
│      ├── repository.py/
|               ├── agent_repository(_impl).py        Fallback 판단 및 질문 생성 경로 전환 로직
|               ├── rag_repository(_impl).py          RAG 기반 면접질문 데이터베이스 검색
|               ├── tech_repository(_impl).py         기술 면접 질문 전용 생성 로직 담당
|               └── simiarity_repository(_impl).py    생성된 질문과 답변 간 유사도 비교 로직 구현
│      └── service.py/
|               └── agent_service(_impl).py           RAG, AGENT 로직 컨트롤
│      
├──  prompt/           기업 맞춤형 질문 생성 프롬프트 
|      ├── danggeun/   당근마켓
|      ├── toss/       토스
|      ├── sk_encore/  SK 엔코아
|      └── kt_mobile/  KT 모바일

```
<br>

### Tech Stack
<table>
  <tr>
     <td>Backend</td>
     <td><img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=white"/></td>
     <td><img src="https://img.shields.io/badge/Django-092E20?style=flat&logo=Django&logoColor=white"/></td>
     <td><img src="https://img.shields.io/badge/FastAPI-009688?style=flat&logo=FastAPI&logoColor=white"/></td>
     <td><img src="https://img.shields.io/badge/Redis-FF4438?style=flat&logo=FastAPI&logoColor=white"/></td>
  </tr>
  <tr>
     <td>AI/LLM</td>
     <td><img src="https://img.shields.io/badge/OpenAI-412991?style=flat&logo=OpenAI&logoColor=white"/></td>
     <td><img src="https://img.shields.io/badge/LangChain-1C3C3C?style=flat&logo=LangChain&logoColor=white"/></td>
     <td><img src="https://img.shields.io/badge/RAG-%231E90FF.svg?style=for-the-badge&logoColor=white"/></td>
     <td><img src="https://img.shields.io/badge/AGENT-%23FF69B4.svg?style=for-the-badge&logoColor=white"/></td>
  </tr>
  <tr>
     <td>Frontend</td>
     <td><img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=JavaScript&logoColor=white"/></td>
     <td><img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=TypeScript&logoColor=white"/></td>
     <td><img src="https://img.shields.io/badge/Vue.js-4FC08D?style=flat&logo=Vue.js&logoColor=white"/></td>
     <td><img src="https://img.shields.io/badge/Nuxt-00DC82?style=flat&logo=Nuxt&logoColor=white"/></td>
  </tr>
  <tr>
     <td>Database</td>
     <td><img src="https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=MySQL&logoColor=white"/></td>
     <td><img src="https://img.shields.io/badge/ChromaDB-%231E90FF.svg?style=for-the-badge&logoColor=white"/></td>
  </tr>
   <tr>
     <td> Infra / DevOps</td>
      <td><img src="https://img.shields.io/badge/AWS-%231E90FF.svg?style=for-the-badge&logoColor=white"/></td>
      <td><img src="https://img.shields.io/badge/Docker-2496ED?style=flat&logo=Docker&logoColor=white"/></td>
      <td><img src="https://img.shields.io/badge/GitHubActions-2088FF?style=flat&logo=GitHubActions&logoColor=white"/></td>
      <td><img src="https://img.shields.io/badge/Linux-FCC624?style=flat&logo=Linux&logoColor=white"/></td> 
      <td><img src="https://img.shields.io/badge/Ubuntu-E95420?style=flat&logo=Linux&logoColor=white"/></td>
      <td><img src="https://img.shields.io/badge/WSL-%23FF69B4.svg?style=for-the-badge&logoColor=white"/></td>
      <td><img src="https://img.shields.io/badge/Go-00ADD8?style=flat&logo=Dart&logoColor=white"/></td>
  </tr>
  <tr>
     <td>Collaboration</td>
     <td><img src="https://img.shields.io/badge/Git-F05032?style=flat&logo=Git&logoColor=white"/></td>
     <td><img src="https://img.shields.io/badge/GitHub-181717?style=flat&logo=GitHub&logoColor=white"/></td>
     <td><img src="https://img.shields.io/badge/Notion-000000?style=flat&logo=Notion&logoColor=white"/></td>
     <td><img src="https://img.shields.io/badge/Slack-4A154B?style=flat&logo=Slack&logoColor=white"/></td>
  </tr>
    <tr>
     <td>Application</td>
     <td><img src="https://img.shields.io/badge/Dart-0175C2?style=flat&logo=Dart&logoColor=white"/></td>
  </tr>
</table>



### 💡 JobStick's AI Tech Pipline
---
![Readme 기술파이프라인](https://github.com/user-attachments/assets/9c62a228-8052-4940-873a-d9a73ebf39ab)

<br>

<!--  ### 💡 Explanation for codes regarding AI

RAG (Retrieval Augmented Generation): '필요한 정보를 검색해서 답변할 때 활용하도록 돕는 기술' 이다. 학원 수강생들의 면접 후기 데이터 (회사 질문 데이터)를 사용자의 답변과 유사한 질문을 2개의 데이터베이스 (Main 기업 데이터, fallback 타기업 데이터)에서 1개를 뽑는다. 
외부 문서나 데이터베이스에서 관련 정보를 찾고 그 내용을 토대로 답변을 생성하게 만듬 -->

### 💡 Prompt Engineering
---

<img width="1318" alt="스크린샷 2025-06-16 오후 9 44 37" src="https://github.com/user-attachments/assets/0fe0d69b-ce47-49d4-8141-02c875bed8b7" />

<img width="1300" alt="스크린샷 2025-06-16 오후 9 44 51" src="https://github.com/user-attachments/assets/3da27682-8f17-4106-983d-d8885b0fbaa9" />
- 기업 맞춤형 질문 생성을 위해, 각 기업의 채용 정보를 requirement 항목으로 정의하여 활용함


  <br><br><br>

  
# Project Collaboration Workflow (Git · Notion · Slack)

<img width="358" alt="스크린샷 2025-06-16 오후 7 24 59" src="https://github.com/user-attachments/assets/fa55f39a-7fb7-46f2-ae01-fe54fe9e544d" /> <br>
#### 애자일 보드 주소
- 🛠️ **Backend (Django)**: [github.com/aview-django-backend](https://github.com/uijungyang/aview-django-backend)  
- 🎨 **Frontend (Vue/Nuxt)**: [github.com/aview-nuxt-frontend](https://github.com/uijungyang/aview-nuxt-frontend) 
- 📱 **Mobile App (Android)**: [github.com/aview-flutter-app](https://github.com/uijungyang/aview-flutter-app)

<br>

<img width="1312" alt="스크린샷 2025-06-16 오후 7 35 36" src="https://github.com/user-attachments/assets/696b689f-373a-4ed3-a09e-5e892afdae52" />
<br><br>

<img width="1151" alt="스크린샷 2025-06-16 오후 7 34 50" src="https://github.com/user-attachments/assets/95245a58-3cd1-4d33-aaf0-764cfe21b837" />

