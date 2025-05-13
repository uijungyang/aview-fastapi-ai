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

    async def generate_interview_question(self, company: str, jobCategory: str, situation: str) -> dict:
        print("🔥🔥🔥 RAG 진입 확인!")
        print(f"[RAG] Generating question using RAG... (company={company})")


        # 1. 기업 컬렉션 및 메타데이터 요약
        collection = self.ragVectorRepository.get_collection(company)
        metadata_summary = self.summarize_metadata_from_collection(collection)
        # 지금 이 메타데이터 summary를 가져와도 프롬프트에서 활용을 못하는 상황


        # 2. 상황 설명 임베딩 후 가장 유사한 기존 질문 추출
        embedding = get_embedding(situation)
        result = collection.query(query_embeddings=[embedding], n_results=3)
        documents = result["documents"][0] if result["documents"] else []
        context = "\n".join(documents) if documents else (
            "유사 질문은 없지만, 사용자의 답변과 기업의 스타일을 고려해 자연스러운 면접 질문을 생성해 주세요."
        )

        requirements = self.ragVectorRepository.get_requirements(company, jobCategory)

        # 3. GPT 프롬프트 구성
        # question -> situation: 면접자가 이전에 한 답변(또는 답변 요약)을 한 줄로 변경해서 이쪽 코드로 보낸것임
        # 이후 그걸 기반으로 GPT가 "그럼 이런 상황이면 이런 질문이 적절하겠다" 하고 새 질문을 만들어내는 용도

        prompt = f"""
        당신은 {company}의 {jobCategory} 기술 면접관이야.
        다음은 회사의 요구사항이야: {requirements}

        상황: "{situation}"
        과거 유사 질문 예시:{context}

        위 내용을 참고해 적절한 기술 면접 질문을 생성해줘.
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

