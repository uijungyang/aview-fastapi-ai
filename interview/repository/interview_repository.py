from abc import ABC, abstractmethod
from typing import List, Dict


class InterviewRepository(ABC):
    @abstractmethod
    def generateQuestions(self,
            interviewId: int,
            topic: str,
            experienceLevel: str,
            userToken: str
    ) -> str:
        pass

    @abstractmethod
    async def generateFirstFollowup(
            self,
            interviewId: int,
            topic: str,
            experienceLevel: str,
            academicBackground: str,
            companyName: str,
            questionId: int,
            answerText: str,
            userToken: str,
    ) -> list[str]:
        pass

    @abstractmethod
    def generateProjectQuestion(
            self,
            interviewId: int,
            projectExperience: str,
            userToken: str
    ) -> list[str]:
        pass

    @abstractmethod
    async def generateProjectFollowupQuestion(
            self,
            interviewId: int,
            topic: str,
            techStack: list[str],
            projectExperience: str,
            companyName: str,
            answerText: str,
            questionId: int,
            userToken: str,
    ) -> list[str]:
        pass

    @abstractmethod
    async def generateTechFollowupQuestion(
            self,
            interviewId: int,
            techStack: list[str],
            selected_tech_questions: list[str],
            questionId: int,
            answerText: str,
            userToken: str,
    ) -> list[str]:
        pass
