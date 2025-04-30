from pydantic import BaseModel
from typing import List

class EndInterviewRequest(BaseModel):
    interview_id: int
    context: str
    questions: List[str]
    answers: List[str]
