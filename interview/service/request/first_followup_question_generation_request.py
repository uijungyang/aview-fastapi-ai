from pydantic import BaseModel


class FirstFollowupQuestionGenerationRequest(BaseModel):
    interviewId: int
    topic: str
    experienceLevel: str
    academicBackground: str
    questionId: int
    answerText: str
    userToken: str