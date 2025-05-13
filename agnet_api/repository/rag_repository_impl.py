from agnet_api.entity.embedding import get_embedding
from agnet_api.repository.rag_repository import RagRepository
from chroma.client import get_chroma_collection


class RagRepositoryImpl(RagRepository):
    # RAG가 무슨 기준으로 질문을 가져오나?
    # companyName: 회사이름
    # situation: answerText

    def rag_main(self, companyName: str, situation: str) -> list:
        collection = get_chroma_collection(companyName)
        query_embedding = get_embedding(situation)
        result = collection.query(query_embeddings=[query_embedding], n_results=5)

        documents = result["documents"][0] if result["documents"] else []
        return documents if documents else ["(메인 회사 DB에서 적절한 질문을 찾지 못했습니다.)"]

    def rag_fallback(self, situation: str) -> list:
        fallback_collection = get_chroma_collection("fallback")
        query_embedding = get_embedding(situation)
        result = fallback_collection.query(query_embeddings=[query_embedding], n_results=5)

        documents = result["documents"][0] if result["documents"] else []
        return documents if documents else ["(Fallback DB에서도 적절한 질문을 찾지 못했습니다.)"]