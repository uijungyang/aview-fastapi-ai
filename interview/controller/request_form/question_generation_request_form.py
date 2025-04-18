from pydantic import BaseModel

from interview.entity.experience_level import ExperienceLevel
from interview.entity.job_category import JobCategory
from interview.service.request.question_generation_request import QuestionGenerationRequest


class QuestionGenerationRequestForm(BaseModel):
    interviewId: int
    topic: int  # 숫자 값으로 받기
    experienceLevel: int  # 숫자 값으로 받기
    userToken: str

    def toQuestionGenerationRequest(self):
        job_name = JobCategory.get_job_name(self.topic)  # 변경된 이름 반영
        experience_level = ExperienceLevel.get_experience_level(self.experienceLevel)  # 변경된 이름 반영

        return QuestionGenerationRequest(
            interviewId=self.interviewId,
            topic=job_name,
            experienceLevel=experience_level,
            userToken=self.userToken,
        )