from abc import ABC, abstractmethod


class AgentRepository(ABC):
    @abstractmethod
    def build_decision_prompt(self,
        score_of_gpt: float,
        gpt_question: str,
        main_rag_score: float,
        main_rag_question: str,
        fallback_rag_score: float,
        fallback_rag_question: str,
        userToken: str)-> str:
        pass
