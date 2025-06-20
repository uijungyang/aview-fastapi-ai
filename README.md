![header](https://capsule-render.vercel.app/api?type=speech&color=0:9b59b6,50:fd6e6a,100:f6d365&height=200&section=header&text=JobStick%20%E2%80%93%20AI%20Interview%20Backend&fontSize=50&fontColor=ffffff&animation=twinkling&frontAlign=68&frontAlignY=36)

👤 Author: **양의정** ｜ AI Service Developer ｜ 📧 5012jung@gmail.com ｜ 🔗 [UiJung's GitHub](https://github.com/uijungyang)

<br>

# 1. Project Description
### 💡 JobStick – AI-Powered Mock Interview Platform
JobStick is an AI-driven mock interview service that generates interview questions and evaluates candidate responses using a large language model (LLM).
It supports personalized interview experiences tailored to specific roles and companies.

<br>

### 💡 Why I develop 'JobStick'
---
⬇️ JobStick 파이널 발표 PPT 일부 발췌
<img width="1344" alt="스크린샷 2025-06-16 오후 4 26 11" src="https://github.com/user-attachments/assets/b2d6dcee-384a-48e9-a3a6-efb03fa8e21d" />
<br>
As a new job seeker, it's relatively easy to get help with reviewing your resume or portfolio. But mock interviews? Not so much. Preparing for interviews depends heavily on your speaking proficiency and how much you've practiced. Effective interview preparation is not achieved overnight; it is the result of continuous and deliberate practice. That's why I decided to develop an AI-powered mock interview platform.

<br><br><br>

# 2. Problem & Solution

소셜 로그인 및 AI interview 초기 버전을 만들고 바로 베포를 함

⬇️ 아래 사진은 개발 기간동안 받았던 피드백의 일부입니다.
<br>
<img width="1014" alt="image" src="https://github.com/user-attachments/assets/44605bd0-937d-4a72-b609-77f71a0fa905" />

☑️ 개선점을 크게 3가지로 나누면, 
1. 질문 퀄리티 높이기 (질문 다양화, AI와 자연스러운 커뮤니케이션, 심층 질문, 회사별 질문 차별화)
2. 인터뷰 UI (면접 화면 개선, 면접자 음성 개선)
3. 기타 (메인화면 UI 개선, 로딩 속도 조절, 면접 도중 다른페이지로 이동시 AI 면접관 음성 오류 개션 등등)
   
<br><br>

### 💡 BEFORE & AFTER
---
### 1. 
#### ❌ Before
<img width="1328" alt="스크린샷 2025-06-16 오후 4 29 55" src="https://github.com/user-attachments/assets/ef663e57-d15f-4fbc-8233-097961f03f56" />
질문이 다소 단조롭고, 반복적인 문장이 나옴. 또한 면접자의 답변을 활용하지 못함.
<br><br>


####  ⭕ After
<img width="1298" alt="Readme Before After #1 부분 사진 2" src="https://github.com/user-attachments/assets/6b696b53-b083-4644-9a98-90a9d435a728" />
사용자의 답변과 자연스럽게 이어지는 질문이 생성되었고, 마지막에는 Tech 질문을 추가함
<br><br>

---
### 2.  
#### ❌ Before

![image](https://github.com/user-attachments/assets/03ab5309-20cd-4526-b46a-68c82e258645)

<br><br>

![image](https://github.com/user-attachments/assets/477d28bf-32be-40f9-b1e3-e07b9f5dfd4a)

<br><br>

####  ⭕ After

<img width="1448" alt="image" src="https://github.com/user-attachments/assets/b43c8ab0-1cc7-40fb-8a18-100e116b15d4" />

<br><br>
![IMG_6771](https://github.com/user-attachments/assets/17b2b6e0-0978-4866-8fb0-7848984062b2)

<br><br>
![IMG_6772](https://github.com/user-attachments/assets/19403656-3b19-4368-a816-b7c89cda0326)


---
### 3. 
#### ❌ Before

<img width="1306" alt="스크린샷 2025-06-16 오후 5 06 57" src="https://github.com/user-attachments/assets/7d773074-4ffc-4f91-bbaa-84fcf9397590" />


####  ⭕ After
<img width="1490" alt="스크린샷 2025-06-16 오후 5 06 13" src="https://github.com/user-attachments/assets/7f253e7a-5579-4869-adf6-fe8c1ab10c29" />

<br>

- 메인 화면 UI를 더 깔끔하게 개선하고, 사용자가 JobStick에 대해 쉽게 이해할 수 있도록 주요 정보를 스크롤 구조로 구성함. <br>
- 면접관 음성을 기존보다 자연스러운 모델로 교체해, 기계적인 느낌을 줄임. <br>
- AI 질문 생성 시 로딩 시간이 단축되었으며, '질문 생성 중'이라는 안내 문구를 추가해 사용자 경험을 개선함.

  <br><br><br>


# 3. TECH

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

  
# 4. Project Collaboration Workflow (Git · Notion · Slack)

<img width="358" alt="스크린샷 2025-06-16 오후 7 24 59" src="https://github.com/user-attachments/assets/fa55f39a-7fb7-46f2-ae01-fe54fe9e544d" /> <br>
#### 애자일 보드 주소
- 🛠️ **Backend (Django)**: [github.com/aview-django-backend](https://github.com/uijungyang/aview-django-backend)  
- 🎨 **Frontend (Vue/Nuxt)**: [github.com/aview-nuxt-frontend](https://github.com/uijungyang/aview-nuxt-frontend) 
- 📱 **Mobile App (Android)**: [github.com/aview-flutter-app](https://github.com/uijungyang/aview-flutter-app)

<br>

<img width="1312" alt="스크린샷 2025-06-16 오후 7 35 36" src="https://github.com/user-attachments/assets/696b689f-373a-4ed3-a09e-5e892afdae52" />
<br><br>

<img width="1151" alt="스크린샷 2025-06-16 오후 7 34 50" src="https://github.com/user-attachments/assets/95245a58-3cd1-4d33-aaf0-764cfe21b837" />

