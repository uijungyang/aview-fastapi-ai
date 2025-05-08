import os
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI
from chroma.client import client
from rag_api.entity.embedding import get_embedding
from rag_api.repository.vector_repository_impl import RagVectorRepositoryImpl

# load_dotenv()
#client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class RagServiceImpl:

    def __init__(self):
        self.ragVectorRepository = RagVectorRepositoryImpl()
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def summarize_metadata_from_collection(self, collection) -> str:
        result = collection.get()

        job_categories = []
        question_types = []
        tags = []

        for metadata in result["metadatas"]:
            job_categories.append(metadata.get("jobCategory", ""))
            question_types.append(metadata.get("questionType", ""))
            tags.append(metadata.get("tag", ""))

        def most_common(lst):
            return max(set(lst), key=lst.count) if lst else "정보 없음"

        return (
            f"- 자주 나오는 직무 분야: {most_common(job_categories)}\n"
            f"- 질문 유형: {most_common(question_types)}\n"
            f"- 태그 키워드: {most_common(tags)}"
        )

    async def generate_interview_question(self, company: str, situation: str) -> dict:
        print("🔥🔥🔥 RAG 진입 확인!")
        print(f"[RAG] Generating question using RAG... (company={company})")

        # 1. 기업 컬렉션 및 메타데이터 요약
        collection = self.ragVectorRepository.get_collection(company)
        metadata_summary = self.summarize_metadata_from_collection(collection)

        # 2. 상황 설명 임베딩 후 가장 유사한 기존 질문 추출
        embedding = get_embedding(situation)
        result = collection.query(query_embeddings=[embedding], n_results=3)
        documents = result["documents"][0] if result["documents"] else []
        context = "\n".join(documents) if documents else (
            "유사 질문은 없지만, 사용자의 답변과 기업의 스타일을 고려해 자연스러운 면접 질문을 생성해 주세요."
        )

        # 3. GPT 프롬프트 구성
        prompt = f"""
        당신은 {company}의 AI 면접관이야.
        이 회사는 일반적으로 다음과 같은 스타일의 질문을 해: {metadata_summary}
        
        후보자의 배경 또는 인터뷰 상황:{situation}
        
        과거에 실제로 물어본 유사 질문 예시: {context}
        
        이 회사의 스타일과 상황에 맞는 새로운 현실적인 면접 질문을 하나 생성해줘.
        결과는 반드시 질문 한 문장만 출력해.
        """


        # 4. GPT 호출
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "generated_question": response.choices[0].message.content.strip(),
            "used_context": context,
            "summary": metadata_summary
        }