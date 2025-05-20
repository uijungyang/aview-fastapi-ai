from typing import List, Dict

from pydantic import BaseModel

from interview.service.request.question_generate_endInterview_request import EndInterviewRequest


class QuestionGenerationEndInterviewRequestForm(BaseModel):
    userToken: str #
    interviewId: int #
    questionId: List[int]  # 질문id를 리스트로 받아 저장[1~8]
    #answerText: str  # 백엔드에서 마지막 답변 받는 용도
    #topic: int
    #experienceLevel: int
    #projectExperience: int
    #academicBackground: int
    #interviewTechStack: List[int]
    context: Dict[str, str]  #
    questions: List[str]  #
    answers: List[str]   #

    def toEndInterviewRequest(self):
        return EndInterviewRequest(
            userToken=self.userToken,
            interviewId=self.interviewId,
            questionId=self.questionId,
            #answerText=self.answerText,
            #topic=self.topic,
            #experienceLevel=self.experienceLevel,
            #projectExperience=self.projectExperience,
            #academicBackground=self.academicBackground,
            #interviewTechStack=self.interviewTechStack,
            context=self.context,
            questions=self.questions,
            answers=self.answers
        )
