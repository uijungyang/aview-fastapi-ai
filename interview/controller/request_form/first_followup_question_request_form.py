from pydantic import BaseModel
from interview.entity.experience_level import ExperienceLevel
from interview.entity.job_category import JobCategory
from interview.entity.academic_background import AcademicBackground  # ✅ 이거 추가
from interview.service.request.first_followup_question_generation_request import FirstFollowupQuestionGenerationRequest

class FirstFollowupQuestionRequestForm(BaseModel):
    interviewId: int
    topic: int
    experienceLevel: int
    academicBackground: int
    companyName: str  # 회사명 추가
    questionId: int
    answerText: str
    userToken: str

    def toFirstFollowupQuestionGenerationRequest(self):
        job_name = JobCategory.get_job_name(self.topic)
        experience_level = ExperienceLevel.get_experience_level(self.experienceLevel)
        academic_background = AcademicBackground.get_academic_background(self.academicBackground)

        return FirstFollowupQuestionGenerationRequest(
            interviewId=self.interviewId,
            topic=job_name,
            experienceLevel=experience_level,
            academicBackground=academic_background,
            companyName= self.companyName,
            questionId=self.questionId,
            answerText=self.answerText,
            userToken=self.userToken,
        )
