from abc import ABC, abstractmethod


class PolyglotService(ABC):

    @abstractmethod
    def requestNextQuestion(self):
        pass

    @abstractmethod
    def requestScore(self):
        pass