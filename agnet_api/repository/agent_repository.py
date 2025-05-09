from abc import ABC, abstractmethod


class AgentRepository(ABC):
    @abstractmethod
    def get_company_description(self, company_name: str) -> str:
        pass