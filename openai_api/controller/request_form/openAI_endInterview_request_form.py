from typing import List, Dict
from pydantic import BaseModel

class EndInterviewRequest(BaseModel):          # 종료용
    sessionId: str
    context: Dict[str, str]
    questions: List[str]
    answers: List[str]