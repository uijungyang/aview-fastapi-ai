from openai import BaseModel


from interview.entity.interview_tech_stack import InterviewTechStack
from interview.service.request.tech_followup_generation_request import TechFollowupGenerationRequest



class TechFollowupQuestionGenerationRequestForm(BaseModel):
    interviewId: int
    techStack: list[int]
    questionId: int
    answerText: str
    userToken: str

    def toTechFollowupQuestionRequest(self):
        tech_stack = InterviewTechStack.get_tech_stack_list(self.techStack)

        return TechFollowupGenerationRequest(
            interviewId=self.interviewId,
            techStack=tech_stack,
            questionId=self.questionId,
            answerText=self.answerText,
            userToken=self.userToken,
        )
