from openai import BaseModel

from interview.entity.experience_level import ExperienceLevel
from interview.entity.job_category import JobCategory
from interview.entity.project_experience import ProjectExperience
from interview.entity.tech_stack import TechStack
from interview.service.request.question_generation_request import FirstQuestionGenerationRequest


class ProjectFollowupQuestionGenerationRequestForm(BaseModel):
    interviewId: int
    topic: int
    techStack: list[int]
    projectExperience: int
    questionId: int
    answerText: str
    userToken: str

    def toProjectFollowupQuestionRequest(self):
        job_name = JobCategory.get_job_name(self.topic)
        project_experience = ProjectExperience.get_project_experience(self.projectExperience)
        tech_stack = TechStack.get_tech_stack_list(self.techStack)

        return ProjectFollowupGenerationRequest(
            interviewId=self.interviewId,
            topic=job_name,
            techStack=tech_stack,
            projectExperience=project_experience,
            questionId=self.questionId,
            answerText=self.answerText,
            userToken=self.userToken,
        )