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

        # 2. 질문별 평가 함수 정의
        async def evaluate_qna(q, a):
            eval_prompt = f"""
                    너는 면접 평가 담당 AI야.
                    다음 질문과 답변을 보고 3문장 이상으로 intent와 feedback을 아래 JSON 형식으로 작성해.

                    Example:
                    {{
                        "question": "...",
                        "answer": "...",
                        "intent": "지원동기",
                        "feedback": "답변은 핵심 내용을 잘 담고 있으며, 논리적인 흐름도 적절합니다. 특히 회사와의 연결고리를 잘 설명한 점이 좋습니다. 다만, 본인의 구체적 경험을 더 추가하면 설득력이 높아질 것입니다."
        }}
                    }}

                    질문: {q}
                    답변: {a}
                    """.strip()

            correction_prompt = f"""
                    너는 면접 첨삭 전문가야.

                    1. 아래 답변에서 **문맥상 어색하거나 부족한 부분**이 있다면 구체적으로 어떤 문장이나 단어를 추가하면 좋은지 추천해줘.  
                       (예: 사례 보강, 숫자 제시, 논리적 연결어 사용 등)

                    2. 문법 오류나 표현이 어색한 문장은 수정해줘. 틀린 문장은 ❌, 고친 문장은 ⭕로 표시해.  
                       단순히 틀린 단어만 고치는 게 아니라, **문맥 흐름에 맞게 자연스럽게** 다듬어줘.

                    예시:
                    - 추가 추천: "답변이 전체적으로 명확하지만, '협업 과정에서의 역할'에 대한 구체적인 예시가 들어가면 더 설득력 있습니다."  
                    - 첨삭 예시:  
                      ❌ 저는 프로젝트를 하면서 팀원과 의사소통이 어려웠지만 열심히 노력했습니다.  
                      ⭕ 프로젝트 초반에는 팀원과의 의사소통에 어려움이 있었지만, 회의 주기를 정하고 피드백 루틴을 만들어 해결했습니다.

                    답변: {a}
                    """.strip()

            try:
                eval_task = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": eval_prompt}],
                    temperature=0.3,
                    max_tokens=700
                )
                correction_task = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": correction_prompt}],
                    temperature=0.3,
                    max_tokens=300
                )

                eval_res, correction_res = await asyncio.gather(eval_task, correction_task)

                eval_data = json.loads(eval_res.choices[0].message.content.strip())
                correction_text = correction_res.choices[0].message.content.strip()

                return {
                    **eval_data,
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

        # 3. 질문별 평가 + 첨삭 병렬 처리
        qa_scores = await asyncio.gather(
            *[evaluate_qna(q, a) for q, a in zip(questions, answers)]
        )

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

        tasks = []
        prompts = []

        # 1. 커뮤니케이션 평가
        if any(qid in [1, 2] for qid in question_ids):
            comm_prompt = """
            너는 IT 면접관이야. 아래 면접자의 인성 관련 질문과 답변을 보고 '커뮤니케이션 능력'을 10점 만점 기준으로 평가해.

            출력 형식은 반드시 아래와 같은 JSON 객체 형태로 해줘:
            { "communication": 7 }

            숫자는 정수(int)로만 작성하고, 다른 설명은 절대 포함하지 마.
            """
            tasks.append(
                client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": comm_prompt},
                        {"role": "user", "content": answer_summary}
                    ]
                )
            )
            prompts.append("communication")

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
            tasks.append(
                client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": proj_prompt},
                        {"role": "user", "content": answer_summary}
                    ]
                )
            )
            prompts.append("project")

        # 3. 개발 역량 평가
        if any(qid in [5, 6] for qid in question_ids):
            tech_prompt = """
            너는 IT 면접관이야. 아래 면접자의 기술 면접 답변을 보고 '개발 역량'을 10점 만점 기준으로 평가해.

            평가 기준: 얼마나 기본 개념과 유사하게 답을 했는지

            출력 예시:
            { "technical_skills": 8 }
            """
            tasks.append(
                client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": tech_prompt},
                        {"role": "user", "content": answer_summary}
                    ]
                )
            )
            prompts.append("technical")

        # 비동기 병렬 실행
        if tasks:
            responses = await asyncio.gather(*tasks)
            for res in responses:
                try:
                    content = res.choices[0].message.content.strip()
                    evaluation_result.update(json.loads(content))
                except Exception as e:
                    print(f"❌ GPT 응답 파싱 실패: {e}")

        if not evaluation_result:
            return {"error": "Invalid or empty session"}

        return evaluation_result