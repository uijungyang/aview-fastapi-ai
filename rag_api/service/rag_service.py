from abc import ABC, abstractmethod


class RagService(ABC):

    @abstractmethod
    def summarize_metadata_from_collection(self, collection) -> str:
        pass

    @abstractmethod
    async def generate_interview_question(self, company: str, jobCategory: str, situation: str) -> dict:
        pass