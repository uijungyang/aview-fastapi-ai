from typing import Dict, List
from interview.repository.evaluate_repository import EvaluateRepository
import importlib
import json
import asyncio
import os
import sys
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class EvaluateRepositoryImpl(EvaluateRepository):

    # 면접 답변 피드백 (기존: end_interview)
    async def interview_feedback(
            self,
            interview_id: str,
            questions: List[str],
            answers: List[str],
            userToken: str
    ) -> Dict:

        # 1. 질문 + 답변 합치기
        joined_qna = "\n".join(
            [f"Q{i + 1}: {q}\nA{i + 1}: {a}" for i, (q, a) in enumerate(zip(questions, answers))]
        )

        # 2. 요약 프롬프트
        summary_prompt = f"""
        너는 면접관이야. 아래는 한 사용자의 전체 면접 흐름과 그에 대한 답변이야.

        [면접 내용]
        {joined_qna}

        면접자의 강점과 개선점을 간단히 3문장 이내로 요약해줘.
        """.strip()

        # 3. GPT 요약 요청 함수 정의
        async def get_summary():
            try:
                response = await client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "너는 면접 요약을 해주는 AI 면접관이야."},
                        {"role": "user", "content": summary_prompt}
                    ],
                    temperature=0.4,
                    max_tokens=150
                )
                return response
            except Exception as e:
                print(f"❌ 요약 실패: {e}")
                return None

        # 4. 질문별 평가 함수
        async def evaluate_qna(q, a):
            prompt = f"""
        너는 면접 평가 담당 AI야.

        다음 질문과 답변을 보고 intent와 feedback을 아래 JSON 형식으로 작성해.

        형식:
        {{
          "question": "...",
          "answer": "...",
          "intent": "지원동기",
          "feedback": "답변이 구체적이고 명확함"
        }}

        질문: {q}
        답변: {a}
        """.strip()

            try:
                response = await client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=300
                )
                content = response.choices[0].message.content.strip()
                return json.loads(content)
            except Exception as e:
                print(f"❌ 평가 실패(질문:{q}): {e}")
                return {
                    "question": q,
                    "answer": a,
                    "intent": "알 수 없음",
                    "feedback": "평가 실패"
                }

        # 5. 모든 질문에 대해 병렬 평가 태스크 생성
        eval_tasks = [evaluate_qna(q, a) for q, a in zip(questions, answers)]

        try:
            # 6. 요약 + 병렬 평가 동시에 실행
            summary_response, qa_scores = await asyncio.gather(
                get_summary(),
                asyncio.gather(*eval_tasks)
            )
        except asyncio.TimeoutError:
            return {
                "interview_id": interview_id,
                "summary": "GPT 응답 지연",
                "qa_scores": [],
                "success": False
            }

        # 7. 요약 결과 파싱
        summary = (
            summary_response.choices[0].message.content.strip()
            if summary_response and summary_response.choices
            else "면접 요약 실패"
        )

        # 8. 최종 결과 리턴
        return {
            "interview_id": interview_id,
            "summary": summary,
            "qa_scores": qa_scores,
            "success": True
        }



    # 육각형 차트 생성을 위한 계산
    async def evaluate_session(self, interview_id: int, qa_items: list[dict]) -> dict:
        # qa_items가 뭔데???
        answer_summary = "\n\n".join(
            f"[질문] {item['question']}\n[답변] {item['answer']}" for item in qa_items
        )

        if interview_id in [1, 2, 3]:
            prompt = """
    너는 IT 면접관이야. 아래 면접자의 인성 관련 질문과 답변을 보고 '커뮤니케이션 능력'을 100점 만점 기준으로 평가해. 점수(score)와 이유(reason)를 JSON 형식으로 출력해.
    """

        elif interview_id in [4, 5, 6]:
            prompt = """
    너는 IT 면접관이야. 아래 면접자의 프로젝트 관련 답변을 보고 다음 4개 항목을 각각 100점 만점 기준으로 평가해.
    - 생산성
    - 문서작성능력
    - 유연성 (운영/서비스 경험 언급 없으면 0점)
    - 문제해결능력

    각 항목에 대해 점수(score)와 이유(reason)를 JSON 형식으로 출력해.
    """


        elif interview_id in [7, 8]:
            prompt = """
    너는 IT 면접관이야. 아래 면접자의 기술 면접 답변을 보고 '개발 역량'을 100점 만점 기준으로 평가해. 점수(score)와 이유(reason)를 JSON 형식으로 출력해.
    """
        else:
            return {"error": "Invalid session type"}

        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": answer_summary}
            ]
        )
        content = response.choices[0].message.content
        return eval(content)  # 주의: eval은 신뢰 가능한 GPT 출력일 때만 사용