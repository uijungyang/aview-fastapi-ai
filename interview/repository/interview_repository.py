from abc import ABC, abstractmethod
from typing import List, Dict


class InterviewRepository(ABC):
    @abstractmethod
    def generateQuestions(self,
            interviewId: int,
            jobCategory: str,
            experienceLevel: str,
            userToken: str
    ) -> str:
        pass

    @abstractmethod
    def generateFirstFollowup(
            self,
            interviewId: int,
            topic: str,
            experienceLevel: str,
            academicBackground: str,
            questionId: int,
            answerText: str,
            userToken: str
    ) -> list[str]:
        pass




    @abstractmethod
    def generateFollowupQuestion(self,
            interviewId: int,
            jobCategory: int,
            experienceLevel: int,
            tech_stack: int,
            projectExperience: int,
            userToken: str
    ) -> list[str]:
        pass


    @abstractmethod
    async def end_interview(self,
        sessionId: str,
        context: Dict[str, str],
        questions: List[str],
        answers: List[str]
    ) -> Dict:
        pass
