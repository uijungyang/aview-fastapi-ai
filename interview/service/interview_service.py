from abc import ABC, abstractmethod
from typing import Dict, List


class InterviewService(ABC):
    @abstractmethod
    def generateInterviewQuestions(self, request: dict) -> dict:
        pass

    @abstractmethod
    def generateFollowupQuestion(self, interviewId: int, questionId: int, answerText: str, userToken: str) -> dict:
        pass

    @abstractmethod
    def end_interview(self, session_id: str, context: Dict[str, str], questions: List[str], answers: List[str]) -> Dict:
        pass