from abc import ABC, abstractmethod


class RagRepository(ABC):
    @abstractmethod
    def rag_main(self, company: str, situation: str, userToken: str) -> list:
        pass

    @abstractmethod
    def rag_fallback(self, situation: str, userToken: str) -> list:
        pass

    @abstractmethod
    def rag_tech(self, techStack:list[str], situation:str, userToken: str) -> list:
        pass