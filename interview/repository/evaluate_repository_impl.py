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

            # 평가 프롬프트
            eval_prompt = f"""
            너는 면접 평가 담당 AI야.
            다음 질문과 답변을 보고 3문장 이상으로 intent와 feedback을 아래 JSON 형식으로 작성해.

            Example:
            {{
                "question": "...",
                "answer": "...",
                "intent": "지원동기",
                "feedback": "답변이 구체적이고 논리적입니다."
            }}

            질문: {q}
            답변: {a}
            """.strip()

            # 첨삭 프롬프트
            correction_prompt = f"""
            너는 면접 첨삭 전문가야.
            1. 답변에 추가했으면 하는 문장이나, 단어 추천해줘 - 내용 보강 목적
            2. 다음 답변에서 잘못된 문장을 고쳐줘. 틀린 문장은 ❌, 고친 문장은 ⭕로 표시해.

            답변: {a}
            """.strip()

            try:
                # 평가
                eval_res = await client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": eval_prompt}],
                    temperature=0.3,
                    max_tokens=300
                )
                eval_data = json.loads(eval_res.choices[0].message.content.strip())

                # 첨삭
                correction_res = await client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": correction_prompt}],
                    temperature=0.3,
                    max_tokens=300
                )
                correction_text = correction_res.choices[0].message.content.strip()

                # 병합
                return {
                    **eval_data,  # question, answer, intent, feedback
                    "correction": correction_text
                }

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
        if any(qid in [1, 2, 3] for qid in question_ids):
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
        if any(qid in [4, 5, 6] for qid in question_ids):
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
        if any(qid in [7, 8] for qid in question_ids):
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