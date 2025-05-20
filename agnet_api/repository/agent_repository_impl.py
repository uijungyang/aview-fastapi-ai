# agent_repository.py
import importlib
import sys
import os

class AgentRepositoryImpl:
# companyName: str, topic: str, situation: str, gpt_question: str, rag_main_result: list,
#                               rag_fallback_result: list = None) -> str
    def build_decision_prompt(self,
        score_of_gpt: float,
        questions: str,
        main_rag_score: float,
        main_rag_question: str,
        fallback_rag_score: float,
        fallback_rag_question: str,
        userToken: str) -> str:

        print(f" AGENT repository - build_decision_promp 실행: {userToken}")

        # 최종 선택 (기본적으로 GPT 질문 선택)
        final_question = questions
        final_score = score_of_gpt
        source = "GPT"

        if main_rag_score > 0.99:
            final_question = main_rag_question
            final_score = main_rag_score
            source = "MAIN"

        if fallback_rag_score > 0.90:
            final_question = fallback_rag_question
            final_score = fallback_rag_score
            source = "FALLBACK"

        print(f"최종 선택: {source} 질문 (유사도: {final_score:.4f})")

        return final_question

