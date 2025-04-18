from pydantic import BaseModel

class QuestionGenerationAfterAnswerRequestForm(BaseModel):
    userToken: str
    interviewId: int
    questionId: int
    answerText: str

    '''
    {
  "userToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "interviewId": 101,
  "questionId": 3,
  "answerText": "저는 백엔드 개발을 주로 해왔고, FastAPI와 Django에 익숙합니다."
}

    '''