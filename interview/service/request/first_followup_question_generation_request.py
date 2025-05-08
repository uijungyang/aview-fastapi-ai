from pydantic import BaseModel


class FirstFollowupQuestionGenerationRequest(BaseModel):
    interviewId: int
    topic: str
    experienceLevel: str
    academicBackground: str
    companyName : str
    questionId: int
    answerText: str
    userToken: str