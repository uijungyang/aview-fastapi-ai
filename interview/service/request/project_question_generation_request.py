from pydantic import BaseModel


class ProjectQuestionGenerationRequest(BaseModel):
    interviewId: int
    projectExperience: str
    userToken: str
    questionId: int