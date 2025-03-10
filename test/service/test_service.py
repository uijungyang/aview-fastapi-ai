from abc import ABC, abstractmethod


class TestService(ABC):

    @abstractmethod
    def requestTestResult(self):
        pass