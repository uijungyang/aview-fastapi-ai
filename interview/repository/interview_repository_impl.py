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
            print(f"프롬프트 경로: {module_path}")
            module = importlib.import_module(module_path)
            requirements = getattr(module, "REQUIREMENTS", "해당 직무의 요구사항이 없습니다.")
        except ModuleNotFoundError:
            requirements = "REQUIREMENTS 프롬프트 파일을 찾을 수 없습니다."
        except AttributeError:
            requirements = "REQUIREMENTS가 등록되어 있지 않습니다."


        prompt = (
            f"너는 IT 기업의 {topic}직무의 면접관이야. 아래 면접자의 **경력인 {experienceLevel}**와 **학력 배경인 {academicBackground}**을 고려하고, "
            f"**이전 질문 답변인 {answerText}**를 토대로 맥락에 맞는 최종 답변을 생성하는거야."
            f"직무·경력·학력 배경과 관련된 **인성, 적성, 학교생활 중심의 꼬리 질문**을 만드는거야.\n"
            f" 또한 **직무 요구사항: {requirements}**도 질문을 생성할때 필수적으로 고려해봐야해"

        f"요청사항:\n"
            f" 1. **기술, 프로젝트, 프레임워크, API, 라이브러리 관련 질문은 금지**\n"
            f" 2. **복합 질문 금지**: 하나의 주제만 물어볼 것\n"
            f" 3. **설명, 인삿말, 줄바꿈, 기타 문장 포함 금지**\n"
            f" 4. 대학 이름은 묻지 말고 전공이나 공부한 내용을 기준으로 작성\n"
            f" 5. 질문은 반드시 **짧고 명확한 한 문장**으로 작성하고 아무 설명도 붙이지 말고 출력할 것\n"
        )

        # GPT 호출
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "너는 진짜 면접관처럼 질문을 생성하는 역할이야."},
                {"role": "user", "content": prompt}
            ]
        )
        if not response.choices:
            raise ValueError("❌ GPT 응답이 비어 있음 (choices 없음)")

        question = response.choices[0].message.content.strip()

        print(f" [repository] Follow-up questions generated: {question}")
        print(f" returning questions: {question}")
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
            tech_stack_str = ", ".join(techStack)
            prompt = f"""
        너는 IT 기업의 실제 면접관이야.
        면접자의 이전 답변과 회사에서 자주 사용하는 면접 스타일을 바탕으로,
        답변 흐름에 자연스럽게 이어지는 후속 질문을 만들어줘.

        [질문 ID]: {questionId}
        [면접자 답변]: {answerText}
        [사용 기술 스택]: {tech_stack_str}
        [직무 요구사항]: {requirements}\n

        규칙:
        - 질문은 **반드시 직전 답변에 논리적으로 이어지는 한 문장**이어야 함
        - **"~한 적 있나요?", "~한 이유는 무엇인가요?"**처럼 부드럽고 구체적인 질문 형태 권장
        - **"프로젝트 경험이 있다면..."**처럼 조건식으로 시작하는 문장은 금지
        - 질문은 **짧고 명확하게**, 설명 없이 출력
        - 사용한 기술(스택)의 활용 방식, 선택 이유, 문제 해결 경험 등으로 연결되면 좋음
        """

        else:
            tech_stack_str = ", ".join(techStack)
            prompt = f"""
        너는 IT 기업의 실제 면접관이야.
        면접자의 답변과 기업 면접 스타일에 맞춰, 직무나 기술 학습 경험에 기반한
        자연스럽고 구체적인 꼬리질문을 한 문장으로 생성해줘.

        [질문 ID]: {questionId}
        [면접자 답변]: {answerText}
        [사용 기술 스택]: {tech_stack_str}
        [직무 요구사항]: {requirements}\n

        규칙:
        - 직무 관련 학습 경험, 협업 경험, 기술 습득 노력에 기반한 질문을 생성할 것
        - **"경험이 없다면..."** 또는 가정형 조건문으로 시작하는 문장은 사용하지 말 것
        - 반드시 **한 문장의 실제 질문**만 출력 (설명, 줄바꿈 금지)
        - 사용한 기술(스택)의 활용 방식, 선택 이유, 문제 해결 경험 등으로 연결되면 좋음
        
        출력 결과:
        1. ** 반드시 1문장으로 출력해**
        """

        # GPT-4 호출
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "너는 진짜 면접관처럼 질문을 생성하는 역할이야."},
                {"role": "user", "content": prompt}
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

        prompt = f"""
    **면접자 답변 {answerText}**, **기술 스택: {tech_stack_str}**, **기술 질문 예시:{reference_text}**을 참고해서 기술을 얼마나 잘 아는지 설명하라는 형태의 질문을 만들어. 
        
        출력 형식 지시사항:
        1. 질문 한 문장만 출력하세요.
        2. 질문 ID", "질문 예시", 설명, 줄바꿈 등의 부가 정보는 출력하지 마세요.
        3. 반드시 하나의 질문 문장으로만 구성하세요.

        """
        print(f"TECH Prompt: {prompt}")

        # GPT-4 호출
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "너는 IT 기업의 면접관이야."},
                {"role": "user", "content": prompt}
            ]
        )
        tech_question = response.choices[0].message.content.strip()
        # question = response.choices[0].message.content.strip()
        print(f"{tech_question}")

        return tech_question

