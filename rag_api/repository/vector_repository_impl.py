from chroma.client import get_chroma_collection
from rag_api.entity.embedding import get_embedding
from rag_api.repository.vector_repository import RagVectorRepository


class RagVectorRepositoryImpl(RagVectorRepository):

    def get_collection(self, company: str):
        return get_chroma_collection(company)

    def retrieve_similar_document(self, company: str, query: str) -> str:
        collection = get_chroma_collection(company)
        query_embedding = get_embedding(query) # 임베딩 생성 (기존 코드 유지)
        result = collection.query(query_embeddings=[query_embedding], n_results=1)

        if result["documents"]:
            return result["documents"][0][0]
        return ""
