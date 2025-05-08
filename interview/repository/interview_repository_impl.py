import os
from typing import List, Dict
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
            context: str,
            summary: str,
    ) -> list[str]:
        print(f" [repository] Generating intro follow-up questions for interviewId={interviewId},userToken={userToken}")

        prompt = (
            f"너는 IT 기업의 면접관이야. 아래 면접자의 기본 정보와 자기소개 답변을 참고해, 직무·경력·학력 배경과 관련된 꼬리 질문을 하나 생성해줘.\n\n"
            f"[직무]: {topic}\n"
            f"[경력]: {experienceLevel}\n"
            f"[학력 배경]: {academicBackground}\n"
            f"[첫 질문 번호]: {questionId}\n"
            f"[자기소개 답변]: {answerText}\n\n"
            f"[이 회사의 질문 스타일 요약]: {summary}\n"
            f"[과거 유사 질문 예시]: {context}\n\n"
            f"요청사항:\n"
            f"- 질문은 반드시 **짧고 명확한 한 문장**으로 작성할 것\n"
            f"- **복합 질문 금지**: 하나의 주제만 물어볼 것\n"
            f"- **설명, 인삿말, 줄바꿈, 기타 문장 포함 금지**\n"
            f"- 학력 관련 질문 시, 대학 이름은 묻지 말고 전공이나 공부한 내용을 기준으로 작성\n"
            f"- **[프로젝트] 관련 질문은 하지 말 것**\n"
            f"- 출력은 질문 한 문장만, 아무 설명도 붙이지 말고 출력할 것"
        )

        # GPT 호출
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "너는 진짜 면접관처럼 질문을 생성하는 역할이야."},
                {"role": "user", "content": prompt}
            ]
        )
        print(f" response type: {type(response)}")

        result_text = response.choices[0].message.content.strip()
        questions = [q.strip() for q in result_text.split("\n") if q.strip()]

        print(f" [repository] Follow-up questions generated: {questions}")
        print(f" returning questions: {questions}")
        return questions

    # 프로젝트 질문: 3
    def generateProjectQuestion(
            self,
            interviewId: int,
            projectExperience: str,
            userToken: str
    ) -> list[str]:
        print(f"📡 [AI Server] Generating fixed project question for interviewId={interviewId}, userToken={userToken}")

        if projectExperience == "프로젝트 경험 있음":
            return ["다음 질문은 프로젝트에 관한 질문입니다.\n 어떤 프로젝트를 진행하셨나요?"]
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
            context: str,
            summary: str,
    ) -> list[str]:

        print(f"[AI Server] Generating 5 questions for interviewId={interviewId}, userToken={userToken}")

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
        [이 회사의 질문 스타일 요약]: {summary}
        [과거 유사 질문 예시]: {context}

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
        [이 회사의 질문 스타일 요약]: {summary}
        [과거 유사 질문 예시]: {context}

        규칙:
        - 직무 관련 학습 경험, 협업 경험, 기술 습득 노력에 기반한 질문을 생성할 것
        - **"경험이 없다면..."** 또는 가정형 조건문으로 시작하는 문장은 사용하지 말 것
        - 반드시 **한 문장의 실제 질문**만 출력 (설명, 줄바꿈 금지)
        - 사용한 기술(스택)의 활용 방식, 선택 이유, 문제 해결 경험 등으로 연결되면 좋음
        """

        # GPT-4 호출
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "너는 진짜 면접관처럼 질문을 생성하는 역할이야."},
                {"role": "user", "content": prompt}
            ]
        )

        result_text = response.choices[0].message.content.strip()
        questions = [q.strip() for q in result_text.split("\n") if q.strip()]

        return questions

    # 면접 종료
    async def end_interview(self,
                                session_id: str,
                                context: Dict[str, str],
                                questions: List[str],
                                answers: List[str]
                                ) -> Dict:
            # GPT를 사용해 면접 요약 생성
            joined_qna = "\n".join(
                [f"Q{i + 1}: {q}\nA{i + 1}: {a}" for i, (q, a) in enumerate(zip(questions, answers))]
            )

            context_summary = "\n".join([f"{k}: {v}" for k, v in context.items()])

            prompt = f"""
    너는 면접관이야. 아래는 한 사용자의 전체 면접 흐름과 그에 대한 답변이야.

    [면접자 정보]
    {context_summary}

    [면접 내용]
    {joined_qna}

    면접자의 전체적인 태도, 경험, 강점을 기반으로 간단한 요약 및 피드백을 생성해줘.
    """

            response = await client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "너는 면접 결과를 정리해주는 AI 인사담당자야."},
                    {"role": "user", "content": prompt.strip()}
                ],
                temperature=0.5
            )

            summary = response.choices[0].message["content"].strip()

            return {
                "session_id": session_id,
                "summary": summary,
                "message": "면접이 성공적으로 종료되었습니다.",
                "success": True
            }