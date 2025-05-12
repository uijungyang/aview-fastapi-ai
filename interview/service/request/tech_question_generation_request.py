from pydantic import BaseModel


class TechQuestionGenerationRequest(BaseModel):
    interviewId: int
    techStack : list[str]
    userToken: str
    questionId: int