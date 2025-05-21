from abc import ABC, abstractmethod


class AsynchronousSampleRepository(ABC):
    @abstractmethod
    def heavyOperation(self, userToken: str, data: str) -> str:
        pass