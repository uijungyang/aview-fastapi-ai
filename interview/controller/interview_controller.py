from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from interview.controller.request_form.first_followup_question_request_form import FirstFollowupQuestionRequestForm
from interview.controller.request_form.first_question_generation_request_form import FirstQuestionGenerationRequestForm
from interview.controller.request_form.project_followup_question_generation_request_form import \
    ProjectFollowupQuestionGenerationRequestForm
from interview.controller.request_form.project_question_generation_request_form import \
    ProjectQuestionGenerationRequestForm
from interview.controller.request_form.question_generate_endInterview_request_form import \
    QuestionGenerationEndInterviewRequestForm
from interview.service.interview_service_impl import InterviewServiceImpl


interviewRouter = APIRouter()


# 의존성 주입
async def injectInterviewService() -> InterviewServiceImpl:
    return InterviewServiceImpl()


# 첫 질문 생성 1
@interviewRouter.post("/interview/question/generate")
async def generateInterviewQuestion(
    requestForm: FirstQuestionGenerationRequestForm,
    interviewService: InterviewServiceImpl = Depends(injectInterviewService)
):
    print(f"🎯 [controller] Received generateInterviewQuestion() requestForm: {requestForm}")

    try:
        # 여기에 질문 생성 로직 호출
        response = interviewService.generateInterviewQuestions(
            requestForm.toFirstQuestionGenerationRequest() # str로 전부 변경
        )

        return JSONResponse(
            content=response,
            status_code=status.HTTP_200_OK,
            headers={"Content-Type": "application/json; charset=UTF-8"}
        )

    except Exception as e:
        print(f" 첫질문 생성 Error in generateInterviewQuestion(): {str(e)}")
        raise HTTPException(status_code=500, detail="서버 내부 오류 발생")


# 첫 질문 꼬리질문: 2개
@interviewRouter.post("/interview/question/first-followup-generate")
async def generateFirstFollowupQuestions(
    requestForm: FirstFollowupQuestionRequestForm,
    interviewService: InterviewServiceImpl = Depends(injectInterviewService)
):
    print(f"🎯 [controller] Received generateFirstFollowupQuestions() requestForm: {requestForm}")

    try:
        response = interviewService.generateFirstFollowupQuestions(requestForm.toFirstFollowupQuestionGenerationRequest())

        return JSONResponse(
            content=response,
            status_code=status.HTTP_200_OK,
            headers={"Content-Type": "application/json; charset=UTF-8"}
        )

    except Exception as e:
        print(f"첫질문 심화질문 Error in generateFirstFollowupQuestions(): {str(e)}")
        raise HTTPException(status_code=500, detail="서버 내부 오류 발생")


# 프로젝트 첫 질문 생성: 3
@interviewRouter.post("/interview/question/project-generate")
async def generateProjectQuestion(
        requestForm: ProjectQuestionGenerationRequestForm,
        interviewService: InterviewServiceImpl = Depends(injectInterviewService)
):
    print(f"🎯 [controller] Received generateProjectQuestion() requestForm: {requestForm}")

    try:
        # 프로젝트 고정 질문 생성 로직 호출
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
    print(f"🎯 [controller] Received generateFollowupInterviewQuestion() requestForm: {requestForm}")

    try:
        response = interviewService.generateProjectFollowupQuestion(
            requestForm.toProjectFollowupQuestionRequest()
        )

        return JSONResponse(
            content=response,
            status_code=status.HTTP_200_OK,
            headers={"Content-Type": "application/json; charset=UTF-8"}
        )

    except Exception as e:
        print(f"프로젝트 꼬리질문 Error in generateFollowupInterviewQuestion(): {str(e)}")
        raise HTTPException(status_code=500, detail="서버 내부 오류 발생")





# 면접 종료 : 최종적으로 모든 질문 답변 저장
@interviewRouter.post("/interview/question/end_interview")
async def end_interview(
        requestForm: QuestionGenerationEndInterviewRequestForm,
        request: Request,  # ✅ userToken 추출용
        interviewService: InterviewServiceImpl = Depends(injectInterviewService)
):
    try:
        # 1. RequestForm → 내부 VO
        dto: EndInterviewRequest = requestForm.toEndInterviewRequest()

        # 2. 헤더에서 userToken 추출 (예시: 소셜 로그인 후 백에서 만든 식별자)
        user_token = request.headers.get("userToken")
        if not user_token:
            raise HTTPException(status_code=401, detail="userToken 헤더가 필요합니다.")

        # 3. 인터뷰 종료 처리
        answer = interviewService.end_interview(dto)

        # 4. Redis 세션 정리
        await redis_manager.reset_count(user_token, dto.interview_id)
        await redis_manager.mark_session_done(user_token, dto.interview_id)

        # 5. 결과 반환
        return JSONResponse(
            content={"message": "면접 종료", "answer": answer},
            status_code=status.HTTP_200_OK
        )

    except Exception as e:
        print(f"❌ [Controller] end_interview 오류: {str(e)}")
        raise HTTPException(status_code=500, detail="서버 내부 오류 발생")

# 평가 코드 추가 (예정)