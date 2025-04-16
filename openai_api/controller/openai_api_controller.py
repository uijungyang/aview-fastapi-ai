import os
import sys

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, FileResponse

from openai_api.controller.request_form.openAI_endInterview_request_form import EndInterviewRequest
from openai_api.controller.request_form.openAI_firstQuestion_request_form import FirstQuestionRequest
from openai_api.controller.request_form.openAI_followupQuestion_request_form import FollowupQuestionRequest
from openai_api.service.openai_api_service import OpenaiApiService
from openai_api.service.openai_api_service_impl import OpenaiApiServiceImpl

# 소켓 통신
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'template'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'template', 'include', 'socket_server'))


openaiApiRouter = APIRouter()

async def injectOpenaiApiService() -> OpenaiApiServiceImpl:
    return OpenaiApiServiceImpl()


#면접 시작: 첫 질문 생성
@openaiApiRouter.post("/openai/introductionAndFirstQuestion")
async def introduction_and_first_question(
    request: FirstQuestionRequest,
    service: OpenaiApiService = Depends(injectOpenaiApiService)
):
    question = await service.generate_first_question(
        company=request.company,
        position=request.position,
        level=request.level
    )
    return JSONResponse(content={"question": question}, status_code=status.HTTP_200_OK)


# 꼬리질문 생성
@openaiApiRouter.post("/openai/generate_followup")
async def generate_followup(
    request: FollowupQuestionRequest,
    service: OpenaiApiService = Depends(injectOpenaiApiService)
):
    result = await service.generate_followup_question(
        previous_question=request.previousQuestion,
        user_answer=request.userAnswer,
        context=request.context
    )
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)


# 면접 종료
@openaiApiRouter.post("/openai/end_interview")
async def end_interview(
    request: EndInterviewRequest,
    service: OpenaiApiService = Depends(injectOpenaiApiService)
):
    summary = await service.end_interview(
        session_id=request.sessionId,
        context=request.context,
        questions=request.questions,
        answers=request.answers
    )
    return JSONResponse(content={"message": "면접 종료", "summary": summary}, status_code=status.HTTP_200_OK)