from fastapi import APIRouter, Query
from pydantic import BaseModel
from rag_api.service.rag_service_impl import RagServiceImpl

ragRouter = APIRouter()
rag_service = RagServiceImpl()

# 입력 JSON 정의
class RagController(BaseModel):
    situation: str

@ragRouter.post("/generate-question")
async def handle_generate_question(
    body: RagController,
    company: str = Query(...)
):
    return await rag_service.generate_interview_question(company, body.situation)
