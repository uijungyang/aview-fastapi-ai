from abc import ABC, abstractmethod


class TestRepository(ABC):

    @abstractmethod
    def getResult(self, userDefinedReceiverFastAPIChannel):
        pass