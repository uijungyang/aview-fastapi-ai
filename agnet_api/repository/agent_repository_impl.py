# agent_repository.py
from agnet_api.entity.company_description import CompanyDescription
from agnet_api.repository.agent_repository import AgentRepository


class AgentRepositoryImpl(AgentRepository):
    def get_company_description(self, company_name: str) -> str:
        return CompanyDescription.get(company_name)

