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
    async def interview_feedback(self,
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

            # 요약 프롬프트
            summary_prompt = f"""
    너는 면접관이야. 아래는 한 사용자의 전체 면접 흐름과 그에 대한 답변이야.

    [면접자 정보]
    {context_summary}

    [면접 내용]
    {joined_qna}

    면접자의 강점과 개선점을 간단히 3문장 이내로 요약해줘.
    """
            summary_task = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "너는 면접 요약을 해주는 AI 면접관이야."},
                    {"role": "user", "content": summary_prompt.strip()}
                ],
                temperature=0.4,
                max_tokens=150
            )
            # 평가 프롬프트
            async def evaluate_qna(q,a):
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
"""
                try:
                    response = await client.chat.completions.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": prompt.strip()}],
                        temperature=0.3,
                        max_tokens=300
                    )
                    content = response.choices[0].message.content.strip()
                    return json.loads(content)
                except Exception as e:
                    print(f"평가 실패(질문:{q}):{e}")
                return {
                    "question": q,
                    "answer": a,
                    "intent": "알수 없음",
                    "feedback":"평가 실패"
                }
            #모든 질문에 대한 병렬평가 요청
            eval_tasks = [evaluate_qna(q,a) for q, a in zip(questions,answers)]

            try:
                summary_response, qa_scores = await asyncio.gather(
                    summary_task,
                    asyncio.gather(*eval_tasks)
                )
            except asyncio.TimeoutError:
                return {
                    "session_id": session_id,
                    "summary":"GPT 응답 지연",
                    "qa_scores":[],
                    "success":False
                }

            summary = summary_response.choices[0].message.content.strip()
            return {
                "session_id": session_id,
                "summary": summary,
                "qa_scores": qa_scores,
                "success": True
            }



    # 육각형 차트 생성을 위한 계산
    async def evaluate_session(self, interview_id: int, qa_items: list[dict]) -> dict:
        answer_summary = "\n\n".join(
            f"[질문] {item['question']}\n[답변] {item['answer']}" for item in qa_items
        )

        if interview_id == 1:
            prompt = """
    너는 IT 면접관이야. 아래 면접자의 인성 관련 질문과 답변을 보고 '커뮤니케이션 능력'을 100점 만점 기준으로 평가해. 점수(score)와 이유(reason)를 JSON 형식으로 출력해.
    """
        elif interview_id == 2:
            prompt = """
    너는 IT 면접관이야. 아래 면접자의 프로젝트 관련 답변을 보고 다음 4개 항목을 각각 100점 만점 기준으로 평가해.
    - 생산성
    - 문서작성능력
    - 유연성 (운영/서비스 경험 언급 없으면 0점)
    - 문제해결능력

    각 항목에 대해 점수(score)와 이유(reason)를 JSON 형식으로 출력해.
    """
        elif interview_id == 3:
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