from pydantic import BaseModel

from interview.entity.project_experience import ProjectExperience
from interview.service.request.project_question_generation_request import ProjectQuestionGenerationRequest


class ProjectQuestionGenerationRequestForm(BaseModel):
    userToken: str
    interviewId: int
    projectExperience: int  # 프로젝트 경험
    questionId: int


    def toProjectQuestionGenerationRequest(self):
        project_experience = ProjectExperience.get_project_experience(self.projectExperience)


        return ProjectQuestionGenerationRequest(
            interviewId=self.interviewId,
            projectExperience=project_experience,
            userToken=self.userToken,
            questionId=self.questionId,
        )
