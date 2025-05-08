from openai import BaseModel

from interview.entity.job_category import JobCategory
from interview.entity.project_experience import ProjectExperience
from interview.entity.interview_tech_stack import InterviewTechStack
from interview.service.request.project_followup_generation_request import ProjectFollowupGenerationRequest



class ProjectFollowupQuestionGenerationRequestForm(BaseModel):
    interviewId: int
    topic: int
    techStack: list[int]
    projectExperience: int
    companyName : str
    questionId: int
    answerText: str
    userToken: str

    def toProjectFollowupQuestionRequest(self):
        job_name = JobCategory.get_job_name(self.topic)
        project_experience = ProjectExperience.get_project_experience(self.projectExperience)
        tech_stack = InterviewTechStack.get_tech_stack_list(self.techStack)

        return ProjectFollowupGenerationRequest(
            interviewId=self.interviewId,
            topic=job_name,
            techStack=tech_stack,
            projectExperience=project_experience,
            companyName=self.companyName,
            questionId=self.questionId,
            answerText=self.answerText,
            userToken=self.userToken,
        )