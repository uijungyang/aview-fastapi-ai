from abc import ABC, abstractmethod


class AgentService(ABC):
    @abstractmethod
    async def get_best_followup_question(self, companyName, topic, situation, questions, userToken):
        pass
