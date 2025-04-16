from typing import Optional, Dict
from pydantic import BaseModel

class FollowupQuestionRequest(BaseModel):      # 꼬리 질문용
    previousQuestion: str
    userAnswer: str
    context: Optional[Dict[str, str]] = {}