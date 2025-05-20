import importlib
import json
import asyncio
import os
import sys
from openai import AsyncOpenAI
from dotenv import load_dotenv

from interview.repository.interview_repository import InterviewRepository

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class InterviewRepositoryImpl(InterviewRepository):

    # 첫 질문 생성: 고장질문 "자기소개 해주세요"
    def generateQuestions(
        self, interviewId: int, topic: str, experienceLevel: str, userToken: str
    ) -> str:
        print(f"[repository] Generating a single question from fine-tuned model for interviewId={interviewId}, userToken={userToken}")

        # 고정질문
        # 자기소개로 개인정보 (이름과 나이, 학교 등등) 얻기 -> 이 정보는 다음 답변에 저장
        return {
            "question": (
                f"{topic}의 {experienceLevel} 분야에 지원해주셔서 감사합니다."
                f" 저는 AI 면접관입니다. "
                f"우선 지원자분 자기소개 부탁드립니다."),
            "questionId": 1  # 실제 DB 저장 시 ID로 교체
        }


    async def generateFirstFollowup(
            self,
            interviewId: int,
            topic: str,
            experienceLevel: str,
            academicBackground: str,
            companyName: str,
            questionId: int,
            answerText: str,
            userToken: str,
    ) -> list[str]:
        print(f" [repository] Generating intro follow-up questions for interviewId={interviewId},userToken={userToken}")

        # prompt 도메인 위치 찾기
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        try:
            # prompt에 있는 기업별 직무 요구사항 프롬프트 가져오기
            module_path = f"prompt.{companyName}.{topic.lower()}"
            #print(f"프롬프트 경로: {module_path}")
            module = importlib.import_module(module_path)
            requirements = getattr(module, "REQUIREMENTS", "해당 직무의 요구사항이 없습니다.")
        except ModuleNotFoundError:
            requirements = "REQUIREMENTS 프롬프트 파일을 찾을 수 없습니다."
        except AttributeError:
            requirements = "REQUIREMENTS가 등록되어 있지 않습니다."

        system_prompt = """
        너는 IT 기업의 실제 면접관이야. 지원자의 경력·학력·답변을 참고하여, 인성·적성·학교생활 중심의 꼬리 질문을 한 문장으로 만들어야 해.

        질문 작성 시 다음 요청사항을 반드시 지켜야 한다:

        1. 기술, 프로젝트, 프레임워크, API, 라이브러리 관련 질문은 금지  
        2. 복합 질문 금지: 하나의 주제만 물어볼 것  
        3. 설명, 인삿말, 줄바꿈, 기타 문장 포함 금지  
        4. 대학 이름은 묻지 말고 전공이나 공부한 내용을 기준으로 작성  
        5. 질문은 반드시 짧고 명확한 한 문장으로 작성하고 아무 설명도 붙이지 말 것

        예시 (출력은 아래처럼 하나의 문장만):
        - 대학교에서 가장 흥미있었던 과목은 무엇인가요? 
        - 통계학 전공에서 AI 분야로 전환하게 된 계기가 무엇인가요?
        - 사용자에게 의미 있는 AI 서비스를 만들기 위해 가장 중요하다고 생각하는 역량은 무엇인가요?
        """.strip()

        user_message = (
            f"면접자의 경력은 {experienceLevel}, 학력은 {academicBackground}입니다. "
            f"이전 답변은 다음과 같습니다: {answerText}\n"
            f"해당 직무의 요구사항은 다음과 같습니다: {requirements}\n"
            f"이 정보를 바탕으로 한 문장의 꼬리 질문을 생성하세요."
        )

        # GPT 호출
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        if not response.choices:
            raise ValueError("GPT 응답이 비어 있음 (choices 없음)")

        question = response.choices[0].message.content.strip()

        #print(f" [repository] Follow-up questions generated: {question}")
        #print(f" returning questions: {question}")
        return question

    # 프로젝트 질문: 3
    def generateProjectQuestion(
            self,
            interviewId: int,
            projectExperience: str,
            userToken: str
    ) -> list[str]:
        print(f" [AI Server] Generating fixed project question for interviewId={interviewId}, userToken={userToken}")

        if projectExperience == "프로젝트 경험 있음":
            return ["다음 질문은 프로젝트에 관한 질문입니다.\n 어떤 프로젝트를 진행하셨나요? \n 직무에 가장 잘 어필할 수 있는 프로젝트로 말씀해주세요."]
        else:
            return ["다음 질문은 프로젝트 혹은 직무 관련 활동에 관한 질문입니다.\n 직무와 관련된 활동을 해보신 경험이 있으신가요?"]


    # 프로젝트 꼬리질문 생성: 4
    async def generateProjectFollowupQuestion(
            self,
            interviewId: int,
            topic: str,
            techStack: list[str],
            projectExperience: str,
            companyName : str,
            questionId: int,
            answerText: str,
            userToken: str,
    ) -> list[str]:
# interviewId, topic, techStack, projectExperience, companyName, questionId, answerText, userToken
        print(f"[AI Server] Generating 5 questions for interviewId={interviewId}, userToken={userToken}")

        try:
            module_path = f"entity.{companyName}.{topic}"
            module = importlib.import_module(module_path)
            requirements = getattr(module, "REQUIREMENTS", "해당 직무의 요구사항이 없습니다.")
        except ModuleNotFoundError:
            requirements = "REQUIREMENTS 프롬프트 파일을 찾을 수 없습니다."
        except AttributeError:
            requirements = "REQUIREMENTS가 등록되어 있지 않습니다."


            # 프롬프트 정의
        if projectExperience == "프로젝트 경험 있음":
            user_message = f"""
                [질문 ID]: {questionId}
                [면접자 답변]: {answerText}
                [직무 요구사항]: {requirements}\n
                """

            system_prompt = f"""
            너는 IT 기업의 실제 면접관이야.
            면접자의 이전 답변과 회사에서 자주 사용하는 면접 스타일을 바탕으로,
            답변 흐름에 자연스럽게 이어지는 후속 질문을 만들어줘.

            규칙:
            - 질문은 반드시 **직전 답변에 논리적으로 이어지는 한 문장**이어야 함
            - **"~한 적 있나요?", "~한 이유는 무엇인가요?"**처럼 부드럽고 구체적인 질문 형태 권장
            - **"프로젝트 경험이 있다면..."**처럼 조건식으로 시작하는 문장은 금지
            - 질문은 **짧고 명확하게**, 설명 없이 출력
            - 사용한 기술(스택)의 활용 방식, 선택 이유, 문제 해결 경험 등으로 연결되면 좋음

            예시:
            - 기술적 제약이 있었을 때, 어떻게 우선순위를 정하고 문제를 해결했나요?  
            - 처음 계획했던 구조와 실제 구현된 구조 사이에 차이가 있었다면, 그 이유는 무엇인가요?  
            - 팀원과의 기술적 의견 충돌을 조율할 때 어떤 기준을 가지고 설득했나요?  
            - 문제를 해결하는 과정에서 다른 접근 방안은 고려해봤나요? 그때 왜 지금의 방식을 택했는지 설명해 주세요.
            """.strip()


        else:
            user_message = f"""
                [질문 ID]: {questionId}
                [면접자 답변]: {answerText}
                [직무 요구사항]: {requirements}\n
                """

            system_prompt = f"""
            너는 IT 기업의 실제 면접관이야.
            면접자의 답변과 기업 면접 스타일에 맞춰, 직무나 기술 학습 경험에 기반한
            자연스럽고 구체적인 꼬리질문을 한 문장으로 생성해줘.

            규칙:
            - 직무 관련 학습 경험, 협업 경험, 기술 습득 노력에 기반한 질문을 생성할 것
            - "경험이 없다면...", "프로젝트를 해보지 않았다면..."처럼 가정형 조건문으로 시작하는 문장은 사용하지 말 것
            - 반드시 한 문장의 **실제 질문**만 출력 (설명, 줄바꿈, 따옴표 금지)
            - 사용한 기술(스택)의 활용 방식, 선택 이유, 문제 해결 경험 등으로 자연스럽게 이어지면 좋음

            예시:
            - 처음 해당 기술을 공부하게 된 계기는 무엇이었나요?  
            - 이론적으로 배운 개념을 실제에 적용한다면 어떤 부분이 가장 어려울 것 같나요?  
            - 학습 중 가장 어려웠던 기술 개념은 무엇이었고, 어떻게 이해하려고 노력했나요?
            """.strip()

        # GPT-4 호출
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        question = response.choices[0].message.content.strip()
        #questions = [q.strip() for q in result_text.split("\n") if q.strip()]

        return question


    async def generateTechFollowupQuestion(
            self,
            interviewId: int,
            techStack: list[str],
            selected_tech_questions: list[str],
            questionId: int,
            answerText: str,
            userToken: str,
    ) -> list[str]:
        print(f"[AI Server] Generating tech follow-up questions for interviewId={interviewId}, userToken={userToken}")

        # 프롬프트 정의
        tech_stack_str = ", ".join(techStack)
        reference_text = "\n".join(f"- {q}" for q in selected_tech_questions)

        # GPT가 참고할 text
        user_message = f"""
                면접자 답변: {answerText}
                기술 스택: {tech_stack_str}
                참고 질문 예시: {reference_text}
                """

        system_prompt = """
        너는 IT 기업의 실제 면접관이야. 
        면접자의 개발 지식을 평가할 수 있는 질문을 생성해야 해.

        목표:
        - 컴퓨터 공학, 프로그래밍 언어, 디자인 패턴, 웹/서버 구조, 데이터베이스 등 기술 개념에 대한 이해도를 확인할 수 있는 질문을 만들어야 해.

        요구사항:
        - 질문은 반드시 짧고 명확한 한 문장으로 작성하세요.
        - 질문 ID, 설명, 예시 등은 절대 포함하지 마세요.
        - 출력은 질문 문장 하나만 출력하세요.
        - "설명해주세요", "차이점을 말해주세요"처럼 끝나는 실제 질문 형태로 작성하세요.

        예시:
        - 파이썬의 데코레이터에 대해 설명해주세요  
        - 싱글톤 패턴이란 무엇이며 언제 사용하는지 설명해주세요  
        - REST API와 RESTful의 차이를 설명해주세요  
        - JOIN과 SUBQUERY의 차이점을 설명해주세요  
        - HTTP와 HTTPS의 차이를 설명해주세요
        """.strip()

        # GPT-4 호출
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        tech_question = response.choices[0].message.content.strip()
        # question = response.choices[0].message.content.strip()
        print(f"{tech_question}")

        return tech_question

