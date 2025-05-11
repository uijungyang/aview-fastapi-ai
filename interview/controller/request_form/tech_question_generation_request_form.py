from pydantic import BaseModel

from interview.entity.project_experience import ProjectExperience
from interview.service.request.project_question_generation_request import ProjectQuestionGenerationRequest


class TechQuestionGenerationRequestForm(BaseModel):
    userToken: str
    interviewId: int
    techStack: int
    questionId: int


    def toProjectQuestionGenerationRequest(self):
        tech_stack = ProjectExperience.get_project_experience(self.projectExperience)


        return TechQuestionGenerationRequest(
            interviewId=self.interviewId,
            techStack=tech_stack,
            userToken=self.userToken,
            questionId=self.questionId,
        )
