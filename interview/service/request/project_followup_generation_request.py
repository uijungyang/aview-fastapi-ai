from pydantic import BaseModel


class ProjectFollowupGenerationRequest(BaseModel):
    interviewId: int
    topic : str
    techStack : list[str]
    projectExperience: str
    companyName: str
    questionId : int
    answerText : str
    userToken: str





