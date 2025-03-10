from abc import ABC, abstractmethod


class PolyglotRepository(ABC):

    @abstractmethod
    def getResult(self, userDefinedReceiverFastAPIChannel):
        pass

    @abstractmethod
    def requestScore(self, userDefinedReceiverFastAPIChannel):
        pass