from typing import List

import openai

from interview.repository.interview_repository import InterviewRepository

class InterviewRepositoryImpl(InterviewRepository):

    # 첫 질문 생성
    def generateQuestions(
        self, interview_id: int, topic: str, experience_level: str, user_token: str
    ) -> str:
        print(f"📡 [repository] Generating a single question from fine-tuned model for interviewId={interview_id}, userToken={user_token}")

        # TODO: OpenAI 연동 or 파인튜닝 모델로 대체
        return (
            f"{topic} 분야에서 최근 관심 있게 본 트렌드는 무엇이며, "
            f"그에 관련한 본인의 경험을 말씀해주시고, "
            f"{experience_level} 수준에서 마주치는 대표적인 문제는 무엇이라 생각하시나요?"
        )

    # 꼬리질문 생성
    def generateFollowupQuestion(
            self, interview_id: int, question_id: int, answer_text: str, user_token: str
    ) -> str:
        print(f"📡 [repository] Generating follow-up question for interviewId={interview_id}, questionId={question_id}")

        # TODO: OpenAI 연동 or 파인튜닝 모델로 대체
        return (
            "이전에 말씀하신 경험 중 가장 어려웠던 상황은 무엇이었고, "
            "그 상황을 어떻게 극복하셨는지 자세히 말씀해 주세요."
        )

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
