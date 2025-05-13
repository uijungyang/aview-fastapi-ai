import os
from dotenv import load_dotenv
#from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from agnet_api.repository.agent_repository_impl import AgentRepositoryImpl
from agnet_api.repository.rag_repository_impl import RagRepositoryImpl

load_dotenv()

class AgentServiceImpl:
    def __init__(self):
        self.agentRepository = AgentRepositoryImpl()
        self.ragRepository = RagRepositoryImpl()
        self.openAPI = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), temperature=0)

    async def get_best_followup_question(self, companyName: str, topic: str, situation: str, gpt_question: str):
        # situation : answerText (이전 질문에 대한 면접자의 답변)
        print(f"🔥 AGENT started: company={companyName}, topic={topic}")

        # 1. RAG 1차 (메인 회사 DB)
        rag_main_result = self.ragRepository.rag_main(companyName, situation)
        print(f"🟢 RAG Main 결과: {rag_main_result}")

        # 2. RAG 2차 (Fallback DB) 조건부 호출
        rag_fallback_result = []
        if not rag_main_result:
            print(f"🔄 RAG Main 실패 → Fallback DB 조회 진행")
            rag_fallback_result = self.ragRepository.rag_fallback(situation)
            print(f"🟢 RAG Fallback 결과: {rag_fallback_result}")

        # 3. AGENT에게 최종 선택 요청
        decision_prompt = self.agentRepository.build_decision_prompt(
            companyName, topic, gpt_question, rag_main_result, rag_fallback_result
        )

        print(f"📝 AGENT Prompt:\n{decision_prompt}")

        response = self.openAPI .predict(decision_prompt)
        print(f"🎯 AGENT 최종 선택: {response}")

        # 4. used_context / summary 리턴 포맷
        used_context = "\n".join(rag_main_result or rag_fallback_result)
        summary = f"{companyName} DB 검색 + Fallback 여부 포함"

        return response, used_context, summary
