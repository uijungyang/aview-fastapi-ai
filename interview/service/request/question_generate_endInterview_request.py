from pydantic import BaseModel
from typing import List, Dict

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
    # 요약 생성을 위한
    context: Dict[str, str]
    questions: List[str]
    answers: List[str]
