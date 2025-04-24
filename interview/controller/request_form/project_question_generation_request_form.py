from pydantic import BaseModel

class ProjectQuestionGenerationRequestForm(BaseModel):
    userToken: str
    interviewId: int
    questionId: int   # 이전 질문 id
    answerText: str   # 사용자 답변

