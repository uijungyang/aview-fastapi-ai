import openai
from typing import Dict, Optional, List

from openai_api.repository.openai_api_repository import OpenaiApiRepository


class OpenaiApiRepositoryImpl(OpenaiApiRepository):

    async def generate_first_question(self, company: str, position: str, level: Optional[str]) -> str:
        base_prompt = f"""
    너는 {company}의 면접관이야. 지원자는 '{position}' 직무에 지원했고, {'신입' if level == '신입' else '경력' if level == '경력' else '해당 직무'}이야.
    지원자에게 첫 번째 면접 질문을 해줘. 질문은 간단하고, 구체적이며 딱 하나만 제시해야 해.
            """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "너는 실제 기업의 인사담당 면접관이야."},
                {"role": "user", "content": base_prompt.strip()}
            ],
            temperature=0.5
        )

        return response.choices[0].message["content"].strip()

    async def generate_followup_question(self, previous_question: str, user_answer: str, context: Dict[str, str]) -> Dict:
        system_prompt = (
            "너는 면접관이야. 다음은 면접자의 답변과 지금까지의 맥락이야. "
            "이 정보를 바탕으로 더 깊이 있는 꼬리질문을 하나 생성하고, "
            "면접자의 답변에서 유의미한 정보도 JSON 형태로 추출해줘."
        )

        context_summary = "\n".join([f"{k}: {v}" for k, v in context.items()])

        user_prompt = f"""
[이전 질문]
{previous_question}

[면접자 답변]
{user_answer}

[현재까지의 맥락 정보]
{context_summary}

=> 아래 두 가지를 출력해줘:
1. followup_question: 다음 꼬리질문
2. context_update: 새롭게 추출한 정보 (JSON 형식)
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5
        )

        answer = response.choices[0].message["content"]

        result = {
            "followup_question": None,
            "updated_context": context
        }

        if "followup_question:" in answer:
            parts = answer.split("followup_question:")
            q_part = parts[1].split("context_update:")[0].strip()
            c_part = parts[1].split("context_update:")[1].strip() if "context_update:" in parts[1] else "{}"

            result["followup_question"] = q_part
            try:
                result["updated_context"] = eval(c_part)  # 운영 환경에선 json.loads 사용 권장
            except:
                pass

        return result



    async def end_interview(self,
        session_id: str,
        context: Dict[str, str],
        questions: List[str],
        answers: List[str]
    ) -> Dict:
        # GPT를 사용해 면접 요약 생성
        joined_qna = "\n".join(
            [f"Q{i+1}: {q}\nA{i+1}: {a}" for i, (q, a) in enumerate(zip(questions, answers))]
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
