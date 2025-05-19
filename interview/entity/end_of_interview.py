from dataclasses import dataclass

@dataclass(frozen=True)
class EndOfInterview:
    interview_id: int
    user_token: str
    question_id: int
    answer_text: str
