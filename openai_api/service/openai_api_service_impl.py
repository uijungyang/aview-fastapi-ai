import openai
import os
from typing import Dict, Optional, List

from openai_api.repository.openai_api_repository_impl import OpenaiApiRepositoryImpl
from openai_api.service.openai_api_service import OpenaiApiService


class OpenaiApiServiceImpl(OpenaiApiService):

    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.OpenaiApiRepository = OpenaiApiRepositoryImpl()

    async def generate_first_question(self, company: str, position: str, level: Optional[str]) -> str:
        return await self.OpenaiApiRepository.generate_first_question(company, position, level)

    async def generate_followup_question(self, previous_question: str, user_answer: str, context: Dict[str, str]) -> Dict:
        return await self.OpenaiApiRepository.generate_followup_question(previous_question, user_answer, context)

    async def end_interview(self,
        session_id: str,
        context: Dict[str, str],
        questions: List[str],
        answers: List[str]
    ) -> Dict:
        return await self.OpenaiApiRepository.end_interview(session_id, context, questions, answers)
