from pydantic import BaseModel


class TechFollowupGenerationRequest(BaseModel):
    interviewId: int
    techStack : list[str]
    questionId : int
    answerText : str
    userToken: str
