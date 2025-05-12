from pydantic import BaseModel

from interview.entity.interview_tech_stack import InterviewTechStack
from interview.service.request.tech_question_generation_request import TechQuestionGenerationRequest


class TechQuestionGenerationRequestForm(BaseModel):
    userToken: str
    techStack: list[int]
    techStack: int
    questionId: int


    def toTechQuestionGenerationRequest(self):
        tech_stack = InterviewTechStack.get_tech_stack_list(self.techStack)


        return TechQuestionGenerationRequest(
            interviewId=self.interviewId,
            techStack=tech_stack,
            userToken=self.userToken,
            questionId=self.questionId,
        )
