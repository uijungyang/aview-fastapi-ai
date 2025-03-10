from abc import ABC, abstractmethod


class ReportToDbRepository(ABC):

    @abstractmethod
    def requestAiResult(self, userDefinedReceiverFastAPIChannel):
        pass