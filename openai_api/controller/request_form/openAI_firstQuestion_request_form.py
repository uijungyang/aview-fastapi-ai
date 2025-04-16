from typing import Optional
from pydantic import BaseModel

class FirstQuestionRequest(BaseModel): # 첫 질문용
    company: str
    position: str
    level: Optional[str] = None