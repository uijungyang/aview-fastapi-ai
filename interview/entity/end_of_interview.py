# 면접 종료 후 모든 질문(GPT질문) 답변(사용자 답변) 저장
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class EndOfInterview:
    interview_id: int
    context: str
    questions: List[str]
    answers: List[str]

    def get_question_count(self) -> int:
        return len(self.questions)

    def get_answers_count(self) -> str:
        return f"총 {self.get_question_count()}개의 질문에 답변하셨습니다."
