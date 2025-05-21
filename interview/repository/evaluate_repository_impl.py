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
    # 면접 답변 피드백 (기존: end_interview)
    async def interview_feedback(
            self,
            interview_id: str,
            questions: List[str],
            answers: List[str],
            userToken: str
    ) -> Dict:
        # 1. 질문 + 답변 합치기 (면접 결과용)
        joined_qna = "\n".join(
            [f"Q{i + 1}: {q}\nA{i + 1}: {a}" for i, (q, a) in enumerate(zip(questions, answers))]
        )

        # 2. 질문별 평가 (intent, feedback + 첨삭)
        async def evaluate_qna(q, a):
            prompt = f"""
            너는 면접관이야. 아래 질문과 지원자의 답변을 보고 다음 3가지를 JSON으로 작성해줘:

            1. intent (이 질문이 무엇을 평가하는 질문인지, 예: 자기소개, 협업 경험, 기술지식 등)
            2. feedback (답변에 대한 3문장 이상의 피드백)
            3. correction (문법 오류나 어색한 표현 수정, 예: ❌, ⭕로 표시)

            출력 예시:
            {{
                "question": "...",
                "answer": "...",
                "intent": "...",
                "feedback": "...",
                "correction": "..."
            }}

            질문: {q}
            답변: {a}
            """

            try:
                res = await client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=700  # 필요 시 600으로도 가능
                )
                return json.loads(res.choices[0].message.content.strip())

            except Exception as e:
                print(f" 평가 실패(질문:{q}): {e}")
                return {
                    "question": q,
                    "answer": a,
                    "intent": "알 수 없음",
                    "feedback": "평가 실패",
                    "correction": "평가 실패로 첨삭 불가"
                }

        # 3. 병렬 실행
        qa_scores = await asyncio.gather(*[evaluate_qna(q, a) for q, a in zip(questions, answers)])

        # 4. 최종 결과 리턴
        return {
            "interview_id": interview_id,
            "qna": joined_qna,
            "qa_scores": qa_scores,
            "success": True
        }


    # 육각형 차트 생성을 위한 계산
    async def evaluate_session(self, qa_items: list[dict]) -> dict:
        evaluation_result = {}
        question_ids = [item["questionId"] for item in qa_items]
        answer_summary = "\n\n".join(
            f"[질문] {item['question']}\n[답변] {item['answer']}" for item in qa_items
        )

        # 1. 커뮤니케이션 평가
        if any(qid in [1, 2] for qid in question_ids):
            comm_prompt = """
            너는 IT 면접관이야. 아래 면접자의 인성 관련 질문과 답변을 보고 '커뮤니케이션 능력'을 10점 만점 기준으로 평가해.

            출력 형식은 반드시 아래와 같은 JSON 객체 형태로 해줘:
            { "communication": 7 }

            숫자는 정수(int)로만 작성하고, 다른 설명은 절대 포함하지 마.
            """
            comm_response = await client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": comm_prompt},
                    {"role": "user", "content": answer_summary}
                ]
            )
            evaluation_result.update(json.loads(comm_response.choices[0].message.content))

        # 2. 프로젝트 평가
        if any(qid in [3, 4] for qid in question_ids):
            proj_prompt = """
            너는 IT 면접관이야. 아래 면접자의 프로젝트 관련 답변을 보고 다음 4개 항목을 각각 10점 만점 기준으로 평가해.
            - 생산성
            - 문서작성능력
            - 유연성 (운영/서비스 경험 언급 없으면 0점)
            - 문제해결능력

            각 항목에 대해 점수(score)를 다음과 같은 JSON 형식으로 출력해:
            {"productivity": 7, "documentation_skills": 6, "flexibility": 0, "problem_solving": 8}
            """
            proj_response = await client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": proj_prompt},
                    {"role": "user", "content": answer_summary}
                ]
            )
            evaluation_result.update(json.loads(proj_response.choices[0].message.content))

        # 3. 개발 역량 평가
        if any(qid in [5, 6] for qid in question_ids):
            tech_prompt = """
            너는 IT 면접관이야. 아래 면접자의 기술 면접 답변을 보고 '개발 역량'을 10점 만점 기준으로 평가해.
            
            평가 기준: 얼마나 기본 개념과 유사하게 답을 했는지

            출력 예시:
            { "technical_skills": 8 }
            """
            tech_response = await client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": tech_prompt},
                    {"role": "user", "content": answer_summary}
                ]
            )
            evaluation_result.update(json.loads(tech_response.choices[0].message.content))

        if not evaluation_result:
            return {"error": "Invalid or empty session"}

        return evaluation_result