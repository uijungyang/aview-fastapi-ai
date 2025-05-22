import asyncio
import os
import json

from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from openai import AsyncOpenAI
from interview.entity.evaluation import EvaluationRequest
from interview.controller.request_form.first_followup_question_request_form import FirstFollowupQuestionRequestForm
from interview.controller.request_form.first_question_generation_request_form import FirstQuestionGenerationRequestForm
from interview.controller.request_form.project_followup_question_generation_request_form import ProjectFollowupQuestionGenerationRequestForm
from interview.controller.request_form.project_question_generation_request_form import ProjectQuestionGenerationRequestForm
from interview.controller.request_form.question_generate_endInterview_request_form import QuestionGenerationEndInterviewRequestForm
from interview.controller.request_form.tech_followup_question_generation_request_form import \
    TechFollowupQuestionGenerationRequestForm
from interview.service.interview_service_impl import InterviewServiceImpl
from utility.global_task_queue import task_queue

interviewRouter = APIRouter()

# 의존성 주입
async def injectInterviewService() -> InterviewServiceImpl:
    return InterviewServiceImpl()   # 의존성 주입이 안됐대.


# 첫 질문 생성
@interviewRouter.post("/interview/question/generate")
async def generateInterviewQuestion(
    requestForm: FirstQuestionGenerationRequestForm,
    interviewService: InterviewServiceImpl = Depends(injectInterviewService)
):
    print(f" [controller] Received generateInterviewQuestion() requestForm: {requestForm}")
    try:
        response = interviewService.generateInterviewQuestions(
            requestForm.toFirstQuestionGenerationRequest()
        )

        return JSONResponse(
            content={
                "interviewId": response["interviewId"],
                "question": response["question"],
                "questionId": response["questionId"]  # 여기에 questionId 포함
            },
            status_code=status.HTTP_200_OK,
            headers={"Content-Type": "application/json; charset=UTF-8"}
        )

    except Exception as e:
        print(f"❌ 첫질문 생성 Error in generateInterviewQuestion(): {str(e)}")
        raise HTTPException(status_code=500, detail="서버 내부 오류 발생")

# 첫 질문 꼬리질문
@interviewRouter.post("/interview/question/first-followup-generate")
async def generateFirstFollowupQuestions(
    requestForm: FirstFollowupQuestionRequestForm,
    interviewService: InterviewServiceImpl = Depends(injectInterviewService)
):
    print(f" [controller] Received generateFirstFollowupQuestions() requestForm: {requestForm}")
    try:
        response = await interviewService.generateFirstFollowupQuestions(
            requestForm.toFirstFollowupQuestionGenerationRequest()
        )
        return JSONResponse(
            content=response,
            status_code=status.HTTP_200_OK,
            headers={"Content-Type": "application/json; charset=UTF-8"}
        )

    except Exception as e:
        print(f"❌ 첫질문 심화질문 Error in generateFirstFollowupQuestions(): {str(e)}")
        raise HTTPException(status_code=500, detail="서버 내부 오류 발생")

# 프로젝트 첫 질문 생성
@interviewRouter.post("/interview/question/project-generate")
async def generateProjectQuestion(
    requestForm: ProjectQuestionGenerationRequestForm,
    interviewService: InterviewServiceImpl = Depends(injectInterviewService)
):
    print(f" [controller] Received generateProjectQuestion() requestForm: {requestForm}")
    try:
        response = interviewService.generateProjectQuestion(
            requestForm.toProjectQuestionGenerationRequest()
        )
        return JSONResponse(
            content=response,
            status_code=status.HTTP_200_OK,
            headers={"Content-Type": "application/json; charset=UTF-8"}
        )
    except Exception as e:
        print(f"❌ 프로젝트 고정질문 생성 오류: {str(e)}")
        raise HTTPException(status_code=500, detail="서버 내부 오류 발생")

# 프로젝트 꼬리 질문 생성
@interviewRouter.post("/interview/question/project-followup-generate")
async def generateProjectFollowupQuestion(
    requestForm: ProjectFollowupQuestionGenerationRequestForm,
    interviewService: InterviewServiceImpl = Depends(injectInterviewService)
):
    print(f" [controller] Received generateProjectFollowupQuestion() requestForm: {requestForm}")
    try:
        response = await interviewService.generateProjectFollowupQuestion(
            requestForm.toProjectFollowupQuestionRequest()
        )
        return JSONResponse(
            content=response,
            status_code=status.HTTP_200_OK,
            headers={"Content-Type": "application/json; charset=UTF-8"}
        )
    except Exception as e:
        print(f"❌ 프로젝트 꼬리질문 Error in generateProjectFollowupQuestion(): {str(e)}")
        raise HTTPException(status_code=500, detail="서버 내부 오류 발생")

# 기술 꼬리 질문 생성
@interviewRouter.post("/interview/question/tech-followup-generate")
async def generateTechFollowupQuestion(
    requestForm: TechFollowupQuestionGenerationRequestForm,
    interviewService: InterviewServiceImpl = Depends(injectInterviewService)
):
    print(f" [controller] Received generateTechFollowupQuestion() requestForm: {requestForm}")
    try:
        response = await interviewService.generateTechFollowupQuestion(
            requestForm.toTechFollowupQuestionRequest()
        )
        return JSONResponse(
            content=response,
            status_code=status.HTTP_200_OK,
            headers={"Content-Type": "application/json; charset=UTF-8"}
        )
    except Exception as e:
        print(f"❌ 프로젝트 꼬리질문 Error in generateTechFollowupQuestion(): {str(e)}")
        raise HTTPException(status_code=500, detail="서버 내부 오류 발생")

# 면접 종료 + 평가 결과 반환
@interviewRouter.post("/interview/question/end_interview")
async def getInterviewResult(
    requestForm: QuestionGenerationEndInterviewRequestForm,
    background_tasks: BackgroundTasks,
    interviewService: InterviewServiceImpl = Depends(injectInterviewService)
):
    request = requestForm.toEndInterviewRequest()
    userToken = request.userToken

    task_queue[userToken] = asyncio.Future()
    background_tasks.add_task(interviewService.end_interview_background, request)
    return JSONResponse(
        content={"status": "PROCESSING"},
        status_code=202
    )
    #try:
     #   response = await interviewService.end_interview(requestForm.toEndInterviewRequest())

      #  if isinstance(response, str):
       #     response = json.loads(response)

        #return JSONResponse(
         #   content=response,
          #  status_code=status.HTTP_200_OK,
           # headers={"Content-Type": "application/json; charset=UTF-8"}
        #)

    #except Exception as e:
     #   print(f"❌ Evaluation Error in end_interview: {str(e)}")
        #raise HTTPException(status_code=500, detail="서버 내부 오류 발생")

@interviewRouter.get("/interview/question/check-result/{userToken}")
async def checkInterviewResult(userToken: str):
    from utility.global_task_queue import task_queue
    task = task_queue.get(userToken)

    if task is None:
        return JSONResponse(content={"status": "NOT_FOUND"}, status_code=404)
    elif not task.done():
        return JSONResponse(content={"status": "PROCESSING"}, status_code=200)
    else:
        try:
            result = task.result()
            return JSONResponse(content={"status": "DONE", "result": result}, status_code=200)
        except Exception as e:
            return JSONResponse(content={"status": "FAILED", "error": str(e)}, status_code=500)
