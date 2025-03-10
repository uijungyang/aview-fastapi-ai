from abc import ABC, abstractmethod


class ReportToDbService(ABC):

    @abstractmethod
    def requestReportToAi(self):
        pass