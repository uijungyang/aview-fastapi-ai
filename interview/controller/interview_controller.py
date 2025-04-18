from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from interview.controller.request_form.question_generate_endInterview_request_form import \
    QuestionGenerationEndInterviewRequestForm
from interview.controller.request_form.question_generation_after_answer_request_form import \
    QuestionGenerationAfterAnswerRequestForm
from interview.service.interview_service_impl import InterviewServiceImpl

from interview.controller.request_form.question_generation_request_form import QuestionGenerationRequestForm

interviewRouter = APIRouter()


# 의존성 주입
async def injectInterviewService() -> InterviewServiceImpl:
    return InterviewServiceImpl()


# 첫 질문 생성
@interviewRouter.post("/interview/question/generate")
async def generateInterviewQuestion(
    requestForm: QuestionGenerationRequestForm,
    interviewService: InterviewServiceImpl = Depends(injectInterviewService)
):
    print(f"🎯 [controller] Received generateInterviewQuestion() requestForm: {requestForm}")

    try:
        # 여기에 질문 생성 로직 호출
        response = interviewService.generateInterviewQuestions(
            requestForm.toQuestionGenerationRequest()
        )

        return JSONResponse(
            content=response,
            status_code=status.HTTP_200_OK,
            headers={"Content-Type": "application/json; charset=UTF-8"}
        )

    except Exception as e:
        print(f"❌ Error in generateInterviewQuestion(): {str(e)}")
        raise HTTPException(status_code=500, detail="서버 내부 오류 발생")


# 꼬리 질문 생성
@interviewRouter.post("/interview/question/generate-after-answer")
async def generateFollowupInterviewQuestion(
    requestForm: QuestionGenerationAfterAnswerRequestForm,
    interviewService: InterviewServiceImpl = Depends(injectInterviewService)
):
    print(f"🎯 [controller] Received generateFollowupInterviewQuestion() requestForm: {requestForm}")

    try:
        response = interviewService.generateFollowupQuestion(
            interview_id=requestForm.interviewId,
            question_id=requestForm.questionId,
            answer_text=requestForm.answerText,
            user_token=requestForm.userToken
        )

        return JSONResponse(
            content=response,
            status_code=status.HTTP_200_OK,
            headers={"Content-Type": "application/json; charset=UTF-8"}
        )

    except Exception as e:
        print(f"❌ Error in generateFollowupInterviewQuestion(): {str(e)}")
        raise HTTPException(status_code=500, detail="서버 내부 오류 발생")

# 면접 종료
@interviewRouter.post("/interview/question/end_interview")
async def end_interview(
        requestForm: QuestionGenerationEndInterviewRequestForm,
        interviewService: InterviewServiceImpl = Depends(injectInterviewService)
):
    try:
        summary = interviewService.end_interview(
            session_id=requestForm.sessionId,
            context=requestForm.context,
            questions=requestForm.questions,
            answers=requestForm.answers
        )
        return JSONResponse(content={"message": "면접 종료", "summary": summary}, status_code=status.HTTP_200_OK)

    except Exception as e:
        print(f"❌ Error in generateInterviewQuestion(): {str(e)}")
        raise HTTPException(status_code=500, detail="서버 내부 오류 발생")