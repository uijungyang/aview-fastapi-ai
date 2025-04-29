import os
from typing import List, Dict

import openai

from interview.repository.interview_repository import InterviewRepository

class InterviewRepositoryImpl(InterviewRepository):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # 첫 질문 생성: 고장질문 "자기소개 해주세요"
    def generateQuestions(
        self, interviewId: int, topic: str, experienceLevel: str, userToken: str
    ) -> str:
        print(f"[repository] Generating a single question from fine-tuned model for interviewId={interviewId}, userToken={userToken}")

        # 고정질문
        # 자기소개로 개인정보 (이름과 나이, 학교 등등) 얻기 -> 이 정보는 다음 답변에 저장
        return (
            f"{topic}의 {experienceLevel}분야에 지원해주셔서 감사합니다. "
            f"저는 AI 면접관입니다."
            f" 우선 지원자분 자기소개 부탁드립니다."
        )

    def generateFirstFollowup(
            self,
            interviewId: int,
            topic: str,
            experienceLevel: str,
            academicBackground: str,
            questionId: int,
            answerText: str,
            userToken: str
    ) -> list[str]:
        print(f"🧠 [repository] Generating intro follow-up questions for interviewId={interviewId},userToken={userToken}")

        # GPT 프롬프트 구성
        prompt = (
            f"너는 IT 기업의 면접관이야. 아래 면접자의 기본정보(직무, 경력)와 자기소개 답변, 학력 배경을 참고해서, 관련된 꼬리 질문 2개를 만들어줘.\n\n"
            f"- 면접자를 부를 때 '지원자님'이라고 해"
            f"[직무]: {topic}"
            f"[경력]: {experienceLevel}"
            f"[학력 배경]: {academicBackground}\n"
            f"[첫 질문 번호]: {questionId}"
            f"[자기소개 답변]: {answerText}\n\n"
            f"요청사항:\n"
            f"- 질문은 총 2개\n"
            f"- 자기소개 내용과 학력에 기반한 궁금한 점을 명확하게 질문해\n"
            f"- 학력에 대한 질문은 대학교 이름을 물어보지 말고, 어느 학과를 나왔고, 어떤 부분을 공부했냐 이런식으로 질문해줘"
            f"- 질문만 출력하고, 줄바꿈(\\n)으로 구분해줘\n"
            f"- 번호 없이, 설명은 절대 포함하지 마"
        )

        # GPT 호출
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "너는 진짜 면접관처럼 질문을 생성하는 역할이야."},
                {"role": "user", "content": prompt}
            ]
        )

        result_text = response.choices[0].message.content.strip()
        questions = [q.strip() for q in result_text.split("\n") if q.strip()]

        print(f"✅ [repository] Follow-up questions generated: {questions}")
        return questions

    '''''
    # 꼬리질문 생성
    def generateProjectFollowupQuestion(
            self,
            interviewId: int,
            jobCategory: int,
            experienceLevel: int,
            tech_stack: int,
            projectExperience: int,
            userToken: str
    ) -> list[str]:
        print(f"📡 [AI Server] Generating 5 questions for interviewId={interviewId}, userToken={userToken}")


        # 🎯 프롬프트 정의
        prompt = (
            f"너는 기술 면접관이야. 다음 면접자 정보를 기반으로, 맞춤형 면접 질문 5개를 생성해줘.\n\n"
            f"[직무 분야]: {jobCategory}\n"
            f"[경력 수준]: {mapped_experience}\n"
            f"[학력 배경]: {mapped_academic}\n"
            f"[사용 기술 스택]: {mapped_tech}\n"
            
            f"- '프로젝트 경험'이 과 관련된 질문이 반드시 1개 포함되어야 해\n"
            f"[프로젝트 경험]: {'있음' if projectExperience else '없음'}\n\n"
            f"요청사항:\n"
            f"- 질문은 총 5개\n"
            f"- 질문은 짧고 명확하게\n"
            f"- 질문만 출력하고 설명은 생략\n"
            f"- 줄바꿈(\n)으로 질문을 구분해줘\n"
        )

        # 📡 GPT-4 호출
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "너는 IT 기업의 실제 면접관이야."},
                {"role": "user", "content": prompt}
            ]
        )

        questions_text = response.choices[0].message["content"].strip()
        questions = [q.strip() for q in questions_text.split("\n") if q.strip()]

        return questions
'''''
    # 면접 종료
    def end_interview(self,
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

            response = openai.ChatCompletion.create(
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
                "message": "면접이 성공적으로 종료되었습니다."
            }
