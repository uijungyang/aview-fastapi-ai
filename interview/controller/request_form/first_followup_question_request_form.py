from openai import BaseModel

from interview.entity.academic_background import AcademicBackground
from interview.entity.experience_level import ExperienceLevel
from interview.entity.job_category import JobCategory
from interview.service.request.first_followup_question_generation_request import FirstFollowupQuestionGenerationRequest


class FirstFollowupQuestionRequestForm(BaseModel):
    interviewId: int
    topic: int
    experienceLevel: int  # ExperienceLevel에서 변환된 값
    academicBackground: int
    questionId: int    # 질문 저장
    answerText: str   # 걍 통으로 가져옴
    userToken: str  # 사용자 식별


    def toFirstFollowupQuestionGenerationRequest(self):
        job_name = JobCategory.get_job_name(self.topic)  # 변경된 이름 반영
        experience_level = ExperienceLevel.get_experience_level(self.experienceLevel)  # 변경된 이름 반영
        academic_background = AcademicBackground.get_academic_background(self.academicBackground)

        return FirstFollowupQuestionGenerationRequest(
            interviewId=self.interviewId,
            topic=job_name,
            experienceLevel=experience_level,
            academicBackground= academic_background,
            questionId= self.questionId,
            answerText=self.answerText,
            userToken=self.userToken,
        )