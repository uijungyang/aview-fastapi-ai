from abc import ABC, abstractmethod
from typing import Dict, List
from interview.service.request.question_generate_endInterview_request import EndInterviewRequest


class InterviewService(ABC):
    @abstractmethod
    def generateInterviewQuestions(self, request: dict) -> dict:
        pass

    @abstractmethod
    async def generateFirstFollowupQuestions(self, request: dict) -> dict:
        pass

    @abstractmethod
    def generateProjectQuestion(self, request: dict) -> dict:
        pass

    @abstractmethod
    async def generateProjectFollowupQuestion(self, request: dict) -> dict:
        pass

    @abstractmethod
    async def generateTechFollowupQuestion(self, request: dict) -> dict:
        pass

    @abstractmethod
    async def end_interview_background(self, request: EndInterviewRequest):
        pass

    @abstractmethod
    async def end_interview(self, request: EndInterviewRequest) -> str:
        pass