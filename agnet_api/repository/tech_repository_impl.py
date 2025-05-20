import os
from dotenv import load_dotenv
from langchain_community.utils.math import cosine_similarity
from openai import AsyncOpenAI
from agnet_api.entity.embedding import get_embedding
from agnet_api.repository.tech_repository import TechRepository

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class TechRepositoryImpl(TechRepository):
    # 선별한 tech 질문들 유사도 계산
    def embeddingForTech(self, tech_db_questions:list[str], answerText: str, userToken: str):
        print(f"[Tech repository] Generating intro embedding Tech questions for userToken={userToken}")
        answer_embedding = get_embedding(answerText)

        # 2. Tech DB에서 유사 질문 추출 (예: 3개)
        tech_result = []
        for q in tech_db_questions:  # 미리 저장된 기술 질문 리스트
            q_embedding = get_embedding(q)
            score = cosine_similarity([answer_embedding], [q_embedding])[0][0]
            if score > 0.8:  # 기준점
                tech_result.append((q, score))

        # 유사도 순으로 상위 3개만 선택
        tech_result.sort(key=lambda x: x[1], reverse=True)
        top_questions = [q for q, _ in tech_result[:3]]
        return top_questions
