from abc import ABC, abstractmethod
from typing import Dict, List


class EvaluateRepository(ABC):
    @abstractmethod
    async def interview_feedback(self,
                                 interview: str,
                                 questions: List[str],
                                 answers: List[str],
                                 userToken: str
                            ) -> Dict:
        pass

    @abstractmethod
    async def evaluate_session(self, interview_id: int, qa_items: list[dict]) -> dict:
        pass