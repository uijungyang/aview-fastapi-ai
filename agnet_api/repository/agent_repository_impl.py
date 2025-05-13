# agent_repository.py
import importlib

class AgentRepositoryImpl:
    def build_decision_prompt(self, companyName: str, topic: str, gpt_question: str, rag_main_result: list,
                              rag_fallback_result: list = None) -> str:

        #GPT 질문, RAG 검색 결과를 바탕으로 AGENT가 최종 판단할 수 있도록 Prompt를 구성합니다.

        # 1. 직무 요구사항 로드
        try:
            module_path = f"prompt.{companyName}.{topic}"
            module = importlib.import_module(module_path)
            requirements = getattr(module, "REQUIREMENTS", "요구사항이 등록되어 있지 않습니다.")
        except ModuleNotFoundError:
            requirements = "REQUIREMENTS 프롬프트 파일을 찾을 수 없습니다."
        except AttributeError:
            requirements = "REQUIREMENTS가 등록되어 있지 않습니다."

        # 2. RAG 검색 결과 정리
        rag_main_text = "\n".join(rag_main_result) if rag_main_result else "메인 회사 DB에서 유사 질문 없음"
        rag_fallback_text = "\n".join(rag_fallback_result) if rag_fallback_result else "Fallback DB에서 유사 질문 없음"

        # 3. AGENT용 최종 Prompt 생성
        prompt = f"""
        당신은 {companyName} 기업의 면접관입니다.
        면접자는 '{topic}' 직무에 지원했습니다.

        [직무 요구사항]
        {requirements}

        [후보 질문 목록]
        1. GPT가 생성한 질문: {gpt_question}
        2. 메인 회사 DB 질문들: {rag_main_text}
        3. 타기업 DB 질문들: {rag_fallback_text}

        위 질문 중에서 면접자의 답변(상황)에 가장 적합한 질문을 선택하고 이유를 설명하세요.
        단, 유사도가 높다고 무조건 고르지 말고, 질문의 맥락과 현실성까지 고려해 주세요.
        최종 결과는 "최종 선택된 질문: XXX" 형식으로 말해 주세요.

        결과는 아래와 같은 형식으로 출력하세요.
        >> 최종 질문: [선택한 질문]
        >> 선택 이유: [간단한 이유 설명]
        """

        return prompt

