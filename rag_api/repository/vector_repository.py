from abc import ABC, abstractmethod


class RagVectorRepository(ABC):
    @abstractmethod
    def get_collection(self, company: str):
        pass

    @abstractmethod
    def retrieve_similar_document(self, company: str, query: str) -> str:
        pass

