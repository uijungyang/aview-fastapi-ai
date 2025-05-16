from abc import ABC, abstractmethod


class SimilarityRepository(ABC):
    @abstractmethod
    def embeddingForGPT(self, situation: str, gpt_question: str, userToken:str):
        pass

    @abstractmethod
    def embeddingForMainRAG(self, situation: str, rag_main_result: list[str], userToken: str):
        pass

    @abstractmethod
    def embeddingForFallbackRAG(selfs,situation: str, rag_fallback_result: list[str], userToken: str):
        pass