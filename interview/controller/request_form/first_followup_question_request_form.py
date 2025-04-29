from pydantic import BaseModel
from interview.entity.experience_level import ExperienceLevel
from interview.entity.job_category import JobCategory
from interview.service.request.question_generation_request import FirstQuestionGenerationRequest

class FirstFollowupQuestionRequestForm(BaseModel):
    interviewId: int
    topic: int
    experienceLevel: int
    academicBackground: int
    questionId: int
    answerText: str
    userToken: str

    def toQuestionGenerationRequest(self):
        job_name = JobCategory.get_job_name(self.topic)
        experience_level = ExperienceLevel.get_experience_level(self.experienceLevel)

        return FirstQuestionGenerationRequest(
            interviewId=self.interviewId,
            topic=job_name,
            experienceLevel=experience_level,
            userToken=self.userToken,
        )
