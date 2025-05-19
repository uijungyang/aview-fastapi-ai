# models/evaluation.py
from pydantic import BaseModel
from typing import List, Literal

class EvaluationItem(BaseModel):
    question: str
    answer: str

class EvaluationRequest(BaseModel):
    session: Literal["personality", "project", "technical"]
    items: List[EvaluationItem]
