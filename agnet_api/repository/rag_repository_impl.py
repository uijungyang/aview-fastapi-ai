from agnet_api.entity.embedding import get_embedding
from agnet_api.repository.rag_repository import RagRepository
from chroma.client import get_chroma_collection


class RagRepositoryImpl(RagRepository):
    # RAG가 무슨 기준으로 질문을 가져오나?
    # companyName: 회사이름
    # situation: answerText

    def rag_main(self, companyName: str, situation: str, userToken: str) -> list:
        print(f" AGENT RAG repository - rag_main 실행: {userToken}")

        collection = get_chroma_collection(companyName)
        query_embedding = get_embedding(situation)
        result = collection.query(query_embeddings=[query_embedding], n_results=5)

        documents = result["documents"][0] if result["documents"] else []
        return documents if documents else ["(메인 회사 DB에서 적절한 질문을 찾지 못했습니다.)"]

    def rag_fallback(self, situation: str, userToken: str) -> list:
        print(f" AGENT RAG repository - rag_fallback 실행: {userToken}")

        fallback_collection = get_chroma_collection("fallback")
        #print("fallback_collection 찾음")
        # 이전 답변을 임베딩 -> DB에서 참고해서 질문을 가져올 생각
        query_embedding = get_embedding(situation)
        result = fallback_collection.query(query_embeddings=[query_embedding], n_results=5)
        #print(f"{result}")

        documents = result["documents"][0] if result["documents"] else []
        return documents if documents else ["(Fallback DB에서도 적절한 질문을 찾지 못했습니다.)"]

    def rag_tech(self, techStack:list[str], situation: str, userToken: str) -> list:
        print(f" AGENT RAG repository - rag_tech 실행: {userToken}")

        tech_collection = get_chroma_collection("tech_db1")
        #print("tech_db1 찾음")
        query_embedding = get_embedding(situation)
        result =  tech_collection.query(query_embeddings=[query_embedding], n_results=5)
        #print(f"{result}")

        documents = result["documents"][0] if result["documents"] else []
        return documents if documents else ["(Fallback DB에서도 적절한 질문을 찾지 못했습니다.)"]