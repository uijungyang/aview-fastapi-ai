import json
import asyncio
from typing import List, Dict

from agnet_api.repository.rag_repository_impl import RagRepositoryImpl
from agnet_api.service.agent_service_impl import AgentServiceImpl
from interview.entity.end_of_interview import EndOfInterview
from interview.repository.evaluate_repository_impl import EvaluateRepositoryImpl
from interview.repository.interview_repository_impl import InterviewRepositoryImpl
from interview.service.interview_service import InterviewService
from interview.service.request.question_generate_endInterview_request import EndInterviewRequest
from interview.service.request.first_followup_question_generation_request import FirstFollowupQuestionGenerationRequest
from interview.service.request.project_question_generation_request import ProjectQuestionGenerationRequest
from interview.service.request.question_generation_request import FirstQuestionGenerationRequest
from interview.service.request.project_followup_generation_request import ProjectFollowupGenerationRequest
from interview.service.request.tech_followup_generation_request import TechFollowupGenerationRequest
from utility.global_task_queue import task_queue

class InterviewServiceImpl(InterviewService):

    def __init__(self):
        self.interviewRepository = InterviewRepositoryImpl()
        self.evaluateRepository = EvaluateRepositoryImpl()
        #self.end_entity = EndOfInterview
        self.agentService = AgentServiceImpl()
        self.ragRepository = RagRepositoryImpl()

    # 인터뷰 첫질문 생성 + 첫질문의 꼬리질문
    def generateInterviewQuestions(self, request: FirstQuestionGenerationRequest) -> dict:
        interviewId = request.interviewId
        topic = request.topic
        experienceLevel = request.experienceLevel
        userToken = request.userToken

        #print(f" [service] Requesting question generation for interviewId={interviewId}")

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

        #print(f" [service] Requesting first follow-up questions for interviewId={interviewId}")

        # 1. GPT에 먼저 질문 생성 요청
        gpt_question = await self.interviewRepository.generateFirstFollowup(
            interviewId, topic, experienceLevel, academicBackground, companyName, questionId, answerText, userToken)


         # 2. AGENT에게 최종 질문 선택 요청 (RAG + Fallback 포함)
        #print(f" [Interview Service] Calling AGENT now..., companyName: {companyName}, GPT's question :{gpt_question}")
        final_question = await self.agentService.get_best_followup_question(
            companyName, topic, answerText, gpt_question, userToken
        )
        question_ids = [questionId + 1]

        return {
            "interviewId": interviewId,
            "questions": [final_question],
            "questionIds": question_ids
        }

    # 프로젝트 첫질문 생성
    def generateProjectQuestion(self, request: ProjectQuestionGenerationRequest) -> dict:
        interviewId = request.interviewId
        projectExperience = request.projectExperience
        userToken = request.userToken
        questionId = request.questionId

        #print(f" [service] Requesting question generation for interviewId={interviewId}")

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

        # GPT가 먼저 질문 생성
        gpt_question = await self.interviewRepository.generateProjectFollowupQuestion(
            interviewId, topic, techStack, projectExperience, companyName, questionId, answerText, userToken)

        # AGENT 에서 최종 질문 (final_question) 반환
        #print(f" [Interview Service] Calling AGENT now..., companyName: {companyName}, GPT's question :{gpt_question}")
        final_question = await self.agentService.get_best_followup_question(
            companyName, topic, answerText, gpt_question, userToken
        )
        # question_ids = [questionId + i + 1 for i in range(len(questions))] 기존 코드
        question_ids = [questionId + 1]

        return {
            "interviewId": interviewId,
            "questions": [final_question],
            "questionIds": question_ids
        }

    async def generateTechFollowupQuestion(self, request: TechFollowupGenerationRequest) -> dict:
        interviewId = request.interviewId
        techStack = request.techStack
        questionId = request.questionId
        answerText = request.answerText
        userToken = request.userToken
        #print(f" [service] Requesting follow-up question for interviewId={interviewId}, questionId={questionId}")

        # Tech DB에서 찾은 질문리스트 : 질문을 뽑아서 유사도 검사까지 함. 최종 top 3 질문 출력
        selected_tech_questions = await self.agentService.get_best_tech_question(techStack, answerText, userToken)

        # Tech 질문 유사도 비교 후 가장 연관성 높은 3개의 질문만 추리기


        # GPT로 질문 나중에 생성
        followup_tech_question = await self.interviewRepository.generateTechFollowupQuestion(
            interviewId, techStack, selected_tech_questions, questionId, answerText, userToken
        )

        #question_ids = [questionId + i + 1 for i in range(len(followup_tech_question))]
        question_ids = [questionId + 1]

        # AGENT를 도입해야하나? 아무튼 기술 DB 등록해서 연결시켜야하긴함.

        return {
            "interviewId": interviewId,
            "questions": [followup_tech_question],
            "questionIds": question_ids,
        }

    async def end_interview_background(self, request: EndInterviewRequest):
        userToken = request.userToken
        task_queue[userToken] = asyncio.Future()

        try:
            result = await self.end_interview(request)
            task_queue[userToken].set_result(result)
        except Exception as e:
            task_queue[userToken].set_exception(e)

    async def end_interview(self, request: EndInterviewRequest) -> str:
        #print(f" [Service] end_interview() 호출 - interviewId={request.interviewId}")

        interview_id = request.interviewId
        userToken = request.userToken
        question_id = request.questionId
        #answer_text = request.answerText
        questions = request.questions
        answers = request.answers

        # 1. 종료 정보 저장 (반환값 안 쓰면 그냥 호출만 하면 됨)
        EndOfInterview(
            interview_id,
            userToken,
            question_id,
            #answer_text,
        )

        # 2. GPT 기반 답변 첨삭 및 요약
        # 면접자 답변 요약할 필요 없음 -> 전체 첨삭이기 때문
        interviewResult = self.evaluateRepository.interview_feedback(
            str(interview_id),
            questions,
            answers,
            userToken
        )

        # 3. 질문 + 답변 → 평가용 구조로 변환
        # 이 부분은 면접자 답변 요약해서 넘겨야함
        #question_id도 받아서 저장
        qa_scores = [{"questionId":qid,"question": q, "answer": a} for qid, q, a in zip(question_id, questions, answers)]

        # 4. 육각형 점수 평가
        radarChart = self.evaluateRepository.evaluate_session(
            qa_scores
        )
        interviewResult, radarChart = await asyncio.gather(
            interviewResult,
            radarChart
        )

        # 5. 결과에 점수 붙이기
        interviewResult["evaluation_result"] = radarChart

        print(f"{interviewResult}")
        return interviewResult
