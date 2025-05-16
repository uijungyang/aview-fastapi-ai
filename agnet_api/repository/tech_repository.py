from abc import ABC, abstractmethod


class TechRepository(ABC):

    @abstractmethod
    def embeddingForTech(self, answerText: str, question_from_tech:list[str], userToken: str):
        pass
