from abc import ABC, abstractmethod
from typing import Dict, List


class EvaluateRepository(ABC):
    @abstractmethod
    async def interview_feedback(self,
                            session_id: str,
                            context: Dict[str, str],
                            questions: List[str],
                            answers: List[str]
                            ) -> Dict:
        pass

    @abstractmethod
    async def evaluate_session(self, interview_id: int, qa_items: list[dict]) -> dict:
        pass