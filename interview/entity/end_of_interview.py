from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class EndOfInterview:
    interview_id: int
    user_token: str
    question_id: int
    answer_text: str
    topic: int
    experience_level: int
    project_experience: int
    academic_background: int
    tech_stack: List[int]