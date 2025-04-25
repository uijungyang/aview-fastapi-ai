from fastapi import APIRouter, Depends, HTTPException, status
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


# 첫 질문 생성
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
    print(f"🎯 [controller] Received generateIntroFollowupQuestions() requestForm: {requestForm}")

    try:
        # 여기에 질문 생성 로직 호출
        response = interviewService.generateFirstFollowupQuestions(
            requestForm.toQuestionGenerationRequest()
        )

        return JSONResponse(
            content=response,
            status_code=status.HTTP_200_OK,
            headers={"Content-Type": "application/json; charset=UTF-8"}
        )

    except Exception as e:
        print(f"첫질문 심화질문 Error in generateIntroFollowupQuestions(): {str(e)}")
        raise HTTPException(status_code=500, detail="서버 내부 오류 발생")


# 프로젝트 첫 질문 생성
@interviewRouter.post("/interview/question/project-generate")
async def generateProjectQuestion(
        requestForm: ProjectQuestionGenerationRequestForm,
        interviewService: InterviewServiceImpl = Depends(injectInterviewService)
):
    print(f"🎯 [controller] Received generateProjectFixedQuestion() requestForm: {requestForm}")

    try:
        # 프로젝트 고정 질문 생성 로직 호출
        response = interviewService.generateProjectQuestion(
            interviewId=requestForm.interviewId,
            userToken=requestForm.userToken
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
            interviewId=requestForm.interviewId,
            questionId=requestForm.questionId,
            answerText=requestForm.answerText,
            userToken=requestForm.userToken
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
        interviewService: InterviewServiceImpl = Depends(injectInterviewService)
):
    try:
        summary = interviewService.end_interview(
            sessionId=requestForm.sessionId,
            context=requestForm.context,
            questions=requestForm.questions,
            answers=requestForm.answers
        )
        return JSONResponse(content={"message": "면접 종료", "summary": summary}, status_code=status.HTTP_200_OK)

    except Exception as e:
        print(f"❌ Error in generateInterviewQuestion(): {str(e)}")
        raise HTTPException(status_code=500, detail="서버 내부 오류 발생")



# 평가 코드 추가 (예정)