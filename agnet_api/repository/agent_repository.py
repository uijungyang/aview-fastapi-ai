from abc import ABC, abstractmethod


class AgentRepository(ABC):
    @abstractmethod
    def build_decision_prompt(self, companyName: str, topic: str, gpt_question: str, rag_main_result: list,
                              rag_fallback_result: list = None) -> str:
        pass
