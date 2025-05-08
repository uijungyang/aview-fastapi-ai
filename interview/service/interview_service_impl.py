import json
from typing import List, Dict

from interview.entity.end_of_interview import EndOfInterview
from interview.repository.interview_repository_impl import InterviewRepositoryImpl
from interview.service.interview_service import InterviewService
from interview.service.request.question_generate_endInterview_request import EndInterviewRequest
from interview.service.request.first_followup_question_generation_request import FirstFollowupQuestionGenerationRequest
from interview.service.request.project_question_generation_request import ProjectQuestionGenerationRequest
from interview.service.request.question_generation_request import FirstQuestionGenerationRequest
from interview.service.request.project_followup_generation_request import ProjectFollowupGenerationRequest
from rag_api.service.rag_service_impl import RagServiceImpl


class InterviewServiceImpl(InterviewService):

    def __init__(self):
        self.interviewRepository = InterviewRepositoryImpl()
        self.ragService = RagServiceImpl()

    # 인터뷰 첫질문 생성 + 첫질문의 꼬리질문
    def generateInterviewQuestions(self, request: FirstQuestionGenerationRequest) -> dict:
        interviewId = request.interviewId
        topic = request.topic
        experienceLevel = request.experienceLevel
        userToken = request.userToken

        print(f" [service] Requesting question generation for interviewId={interviewId}")

        questionData = self.interviewRepository.generateQuestions(
            interviewId, topic, experienceLevel, userToken
        )
        if isinstance(questionData, str):
            questionData = json.loads(questionData)

        return {
            "interviewId": interviewId,
            "question": questionData["question"],
            "questionId": 1
        }

    async def generateFirstFollowupQuestions(self, request: FirstFollowupQuestionGenerationRequest) -> dict:
        interviewId = request.interviewId
        topic = request.topic
        experienceLevel = request.experienceLevel
        academicBackground = request.academicBackground
        companyName = request.companyName
        questionId = request.questionId
        answerText = request.answerText
        userToken = request.userToken

        print(f" [service] Requesting first follow-up questions for interviewId={interviewId}")

        # 2. RAG로 질문 생성 (answerText 기반으로 하나만 생성)
        print(f"🟢 [Service] Calling RAG now..., companyName: {companyName}, answerText :{answerText}")
        rag_response = await self.ragService.generate_interview_question(companyName, answerText)

        # GPT에 질문 생성 요청
        questions = await self.interviewRepository.generateFirstFollowup(
            interviewId, topic, experienceLevel, academicBackground, companyName, questionId, answerText, userToken, rag_response["used_context"], rag_response["summary"]
        )
        question_ids = [questionId + i + 1 for i in range(len(questions))]

        return {
            "interviewId": interviewId,
            "questions": questions,
            "questionIds": question_ids,
            "usedContext": rag_response["used_context"],
            "summary": rag_response["summary"]
        }

    # 프로젝트 첫질문 생성
    def generateProjectQuestion(self, request: ProjectQuestionGenerationRequest) -> dict:
        interviewId = request.interviewId
        projectExperience = request.projectExperience
        userToken = request.userToken
        questionId = request.questionId

        print(f" [service] Requesting question generation for interviewId={interviewId}")

        questions = self.interviewRepository.generateProjectQuestion(
            interviewId, projectExperience, userToken
        )

        return {
            "interviewId": interviewId,
            "question": questions,
            "questionId": questionId + 1
        }

    async def generateProjectFollowupQuestion(self, request: ProjectFollowupGenerationRequest) -> dict:
        interviewId = request.interviewId
        topic = request.topic
        techStack = request.techStack
        projectExperience = request.projectExperience
        companyName = request.companyName
        questionId = request.questionId
        answerText = request.answerText
        userToken = request.userToken
        print(f" [service] Requesting follow-up question for interviewId={interviewId}, questionId={questionId}")

        # 2. RAG 기반 질문 생성 (답변 기반)
        rag_response = await self.ragService.generate_interview_question(companyName, answerText)

        followup_question = await self.interviewRepository.generateProjectFollowupQuestion(
            interviewId, topic, techStack, projectExperience, companyName, questionId, answerText, userToken, rag_response["used_context"], rag_response["summary"]
        )
        question_ids = [questionId + i + 1 for i in range(len(followup_question))]

        return {
            "interviewId": interviewId,
            "questions": followup_question,
            "questionIds": question_ids,
            "usedContext": rag_response["used_context"],
            "summary": rag_response["summary"]
        }

    async def end_interview(self, request: EndInterviewRequest) -> str:
        print(f" [Service] end_interview() 호출 - interviewId={request.interviewId}")

        # 1. 종료 정보 저장
        interview = EndOfInterview(
            interview_id=request.interviewId,
            user_token=request.userToken,
            question_id=request.questionId,
            answer_text=request.answerText,
            topic=request.topic,
            experience_level=request.experienceLevel,
            project_experience=request.projectExperience,
            academic_background=request.academicBackground,
            tech_stack=request.interviewTechStack
        )

        context = {
            "userToken": request.userToken,
            "topic": request.topic,
            "experienceLevel": request.experienceLevel,
            "projectExperience": request.projectExperience,
            "acdemicBackground": request.academicBackground,
            "techStack": request.interviewTechStack,
        }
        interviewResult = await self.interviewRepository.end_interview(
            interview,
            context,
            request.questions,
            request.answers
        )
        print(f"{interviewResult}")
        return interviewResult
