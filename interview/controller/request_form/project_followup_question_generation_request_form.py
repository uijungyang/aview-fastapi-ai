from openai import BaseModel

from interview.entity.experience_level import ExperienceLevel
from interview.entity.job_category import JobCategory
from interview.service.request.question_generation_request import FirstQuestionGenerationRequest


class ProjectFollowupQuestionGenerationRequestForm(BaseModel):
    interviewId: int
    jobCategory: int # 숫자 값으로 받기
    experienceLevel: int  # 숫자 값으로 받기
    tech_stack: int
    projectExperience: int   # 이건 꼭 질문으로 넣어야함
    userToken: str

    def toQuestionGenerationRequest(self):
        job_name = JobCategory.get_job_name(self.topic)  # 변경된 이름 반영
        experience_level = ExperienceLevel.get_experience_level(self.experienceLevel)  # 변경된 이름 반영

        return ProjectFollowupQuestionGenerationRequestForm(
            interviewId=self.interviewId,
            topic=job_name,
            experienceLevel=experience_level,
            userToken=self.userToken,
        )