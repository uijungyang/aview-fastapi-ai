from pydantic import BaseModel
from typing import List, Dict

class EndInterviewRequest(BaseModel):
    userToken: str
    interviewId: int
    questionId: List[int] #질문ID를 리스트 형식으로 받음
    #answerText: str
    #topic: int
    #experienceLevel: int
    #projectExperience: int
    #academicBackground: int
    #interviewTechStack: List[int]
    # 요약 생성을 위한
    context: Dict[str, str]
    questions: List[str]
    answers: List[str]