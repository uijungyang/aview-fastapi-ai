from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class EndOfInterview:
    interview_id: int
    user_token: str
    question_id: List[int]
    #answer_text: str
