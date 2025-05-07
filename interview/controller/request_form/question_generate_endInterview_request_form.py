from pydantic import BaseModel
from typing import List, Dict

from interview.service.request.question_generate_endInterview_request import EndInterviewRequest


class QuestionGenerationEndInterviewRequestForm(BaseModel):
    userToken: str
    interviewId: int
    questionId: int
    answerText: str
    topic: int
    experienceLevel: int
    projectExperience: int
    academicBackground: int
    interviewTechStack: List[int]
    context: Dict[str, str]
    questions: List[str]
    answers: List[str]

    def toEndInterviewRequest(self) -> EndInterviewRequest:
        return EndInterviewRequest(
            userToken=self.userToken,
            interviewId=self.interviewId,
            questionId=self.questionId,
            answerText=self.answerText,
            topic=self.topic,
            experienceLevel=self.experienceLevel,
            projectExperience=self.projectExperience,
            academicBackground=self.academicBackground,
            interviewTechStack=self.interviewTechStack,
            context=self.context,
            questions=self.questions,
            answers=self.answers
        )



    ''''
    데이터 예시
    {
  "sessionId": "session_20250416_abc123",
  "context": {
    "company": "삼성전자",
    "position": "소프트웨어 개발",
    "level": "신입",
    "project": "안드로이드 앱 개발",
    "tech": "Flutter, Spring"
  },
  "questions": [
    "자기소개 해주세요.",
    "소프트웨어 개발자로서 가장 자신 있는 기술은 무엇인가요?",
    "안드로이드 앱 개발 프로젝트에서 어떤 역할을 맡았나요?"
  ],
  "answers": [
    "저는 삼성전자 소프트웨어 개발 직무에 지원한 신입 김지원입니다.",
    "Flutter 개발에 가장 자신 있습니다.",
    "백엔드 API 설계와 데이터베이스 연동을 맡았습니다."
  ]
}

    '''