from pydantic import BaseModel
from typing import List

class EndInterviewRequest(BaseModel):
    userToken: str
    interviewId: int
    questionId: int
    answerText: str
    topic: int
    experienceLevel: int
    projectExperience: int
    academicBackground: int
    interviewTechStack: List[int]
