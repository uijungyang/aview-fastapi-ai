import os
import json

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from openai import AsyncOpenAI

from interview.controller.request_form.first_followup_question_request_form import FirstFollowupQuestionRequestForm
from interview.controller.request_form.first_question_generation_request_form import FirstQuestionGenerationRequestForm
from interview.controller.request_form.project_followup_question_generation_request_form import ProjectFollowupQuestionGenerationRequestForm
from interview.controller.request_form.project_question_generation_request_form import ProjectQuestionGenerationRequestForm
from interview.controller.request_form.question_generate_endInterview_request_form import QuestionGenerationEndInterviewRequestForm
from interview.controller.request_form.tech_followup_question_generation_request_form import \
    TechFollowupQuestionGenerationRequestForm
from interview.service.interview_service_impl import InterviewServiceImpl

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

# 면접 종료
@interviewRouter.post("/interview/question/end_interview")
async def endInterview(
    requestForm: QuestionGenerationEndInterviewRequestForm,
    request: Request,
    interviewService: InterviewServiceImpl = Depends(injectInterviewService)
):
    try:
        dto = requestForm.toEndInterviewRequest()
        user_token = requestForm.userToken
        answer = await interviewService.end_interview(dto)
        if isinstance(answer, str):
            try:
                answer = json.loads(answer)
            except Exception as e:
                print(f"❌ FastAPI 응답 파싱 오류: {e}")
                raise HTTPException(status_code=500, detail="AI 서버 응답 파싱 실패")

        return JSONResponse(
            content={
                "message": "면접 종료",
                "summary": answer.get("summary","요약 없음"),
                "qa_scores": answer.get("qa_scores",[]),
                "success": answer.get("success",True)
            },
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        print(f"❌ [Controller] end_interview 오류: {str(e)}")
        raise HTTPException(status_code=500, detail="서버 내부 오류 발생")
