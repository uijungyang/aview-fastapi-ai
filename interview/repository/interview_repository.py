from abc import ABC, abstractmethod
from typing import List, Dict


class InterviewRepository(ABC):
    @abstractmethod
    def generateQuestions(
        self, interview_id: int, topic: str, experience_level: str, user_token: str
    ) -> str:
        pass

    @abstractmethod
    def generateFollowupQuestion(
        self, interview_id: int, question_id: int, answer_text: str, user_token: str
    ) -> str:
        pass

    @abstractmethod
    async def end_interview(self,
        session_id: str,
        context: Dict[str, str],
        questions: List[str],
        answers: List[str]
    ) -> Dict:
        pass
