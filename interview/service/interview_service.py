from abc import ABC, abstractmethod
from typing import Dict, List


class InterviewService(ABC):
    @abstractmethod
    def generateInterviewQuestions(self, request: dict) -> dict:
        pass

    @abstractmethod
    def generateFirstFollowupQuestions(self, request: dict) -> dict:
        pass

    #@abstractmethod
    #def generateProjectFollowupQuestion(self, interviewId: int, questionId: int, answerText: str, userToken: str) -> dict:
    #    pass

    @abstractmethod
    def end_interview(self, sessionId: str, context: Dict[str, str], questions: List[str], answers: List[str]) -> Dict:
        pass