from abc import ABC, abstractmethod


class AgentService(ABC):
    @abstractmethod
    async def get_context_with_agent_fallback(self, target_company: str, situation: str):
        pass