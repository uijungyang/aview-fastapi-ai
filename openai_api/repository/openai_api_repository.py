from abc import ABC, abstractmethod
from typing import Dict, Optional, List


class OpenaiApiRepository(ABC):

    @abstractmethod
    async def generate_first_question(self, company: str, position: str, level: Optional[str]) -> str:
        pass

    @abstractmethod
    async def generate_followup_question(self, previous_question: str, user_answer: str, context: Dict[str, str]) -> Dict:
        pass

    @abstractmethod
    async def end_interview(self,
        session_id: str,
        context: Dict[str, str],
        questions: List[str],
        answers: List[str]
    ) -> Dict:
        pass
