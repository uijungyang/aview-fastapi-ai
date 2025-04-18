from typing import List, Dict

from interview.service.interview_service import InterviewService
from interview.repository.interview_repository_impl import InterviewRepositoryImpl
from interview.service.request.question_generation_request import QuestionGenerationRequest


class InterviewServiceImpl(InterviewService):
    def __init__(self):
        self.interviewRepository = InterviewRepositoryImpl()

    # 인터뷰 질문 생성
    def generateInterviewQuestions(self, request: QuestionGenerationRequest) -> dict:
        interviewId = request.interviewId
        topic = request.topic
        experienceLevel = request.experienceLevel
        userToken = request.userToken

        print(f"💡 [service] Requesting question generation for interviewId={interviewId}")

        questions = self.interviewRepository.generateQuestions(
            interviewId, topic, experienceLevel, userToken
        )

        return {
            "interviewId": interviewId,
            "questions": questions
        }

    def generateFollowupQuestion(
            self, interview_id: int, question_id: int, answer_text: str, user_token: str
    ) -> dict:
        print(f"💡 [service] Requesting follow-up question for interviewId={interview_id}, questionId={question_id}")

        followup_question = self.interviewRepository.generateFollowupQuestion(
            interview_id, question_id, answer_text, user_token
        )

        return {
            "interviewId": interview_id,
            "questions": followup_question
        }


    def end_interview(self,
        session_id: str,
        context: Dict[str, str],
        questions: List[str],
        answers: List[str]
    ) -> Dict:
        return self.OpenaiApiRepository.end_interview(session_id, context, questions, answers)