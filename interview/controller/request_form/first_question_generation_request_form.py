from pydantic import BaseModel

from interview.entity.experience_level import ExperienceLevel
from interview.entity.job_category import JobCategory
from interview.service.request.question_generation_request import FirstQuestionGenerationRequest


class FirstQuestionGenerationRequestForm(BaseModel):
    interviewId: int
    topic: int  # 숫자 값으로 받기
    experienceLevel: int  # 숫자 값으로 받기
    userToken: str

    def toFirstQuestionGenerationRequest(self):
        job_name = JobCategory.get_job_name(self.topic)  # 변경된 이름 반영
        experience_level = ExperienceLevel.get_experience_level(self.experienceLevel)  # 변경된 이름 반영

        return FirstQuestionGenerationRequest(
            interviewId=self.interviewId,
            topic=job_name,
            experienceLevel=experience_level,
            userToken=self.userToken,
        )

'''
    # ✅ RAG용 상황 설명 추가
    def toSituationText(self) -> str:
        topic_map = {
            1: "백엔드 개발자",
            2: "프론트엔드 개발자",
            3: "임베디드 개발자",
            4: "AI 엔지니어",
            5: "데브옵스 엔지니어",
            6: "웹, 앱 개발자"
        }

        experience_map = {
            1: "신입",
            2: "3년 이하",
            3: "5년 이하",
            4: "10년 이하",
            5: "10년 이상"
        }

        topic_str = topic_map.get(self.topic, "개발자")
        experience_str = experience_map.get(self.experienceLevel, "")

        return f"{experience_str} {topic_str}입니다."
'''