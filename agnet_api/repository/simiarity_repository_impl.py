#from langchain_community.utils.math import cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity
from agnet_api.entity.embedding import get_embedding
from agnet_api.repository.simiarity_repository import SimilarityRepository


class SimilarityRepositoryImpl(SimilarityRepository):

    def embeddingForGPT(self, situation: str, gpt_question: str, userToken:str):
        print(f" AGENT Similarity repository - embeddingForGPT 실행: {userToken}")

        # 이전 답변 임베딩, gpt로 생성한 질문 임베딩 -> 메인 DB와 gpt 질문 유사도 비교를 위해
        try:
            answer_embedding = get_embedding(situation)
            gpt_embedding = get_embedding(gpt_question)
        except Exception as e:
            print("get_embedding 호출 중 에러 발생:", e)
        # 이 둘의 유사도를 계산함
        #print(" answer_embedding:", type(answer_embedding), len(answer_embedding) if answer_embedding else "None")
        #print(" gpt_embedding:", type(gpt_embedding), len(gpt_embedding) if gpt_embedding else "None")
        similarity_score = cosine_similarity([answer_embedding], [gpt_embedding])[0][0]
        return similarity_score


    def embeddingForMainRAG(self, situation: str, rag_main_result: list[str], userToken: str):
        print(f" AGENT repository - embeddingForMainRAG 실행: {userToken}")
        answer_embedding = get_embedding(situation)
        #print("답변 situation 임베딩 끝")

        # RAG 1차 (메인 회사 DB 조회) VS 이전 답변 유시도 판단 : cosine_similarity 사용
        main_rag_score = 0
        main_rag_question = None

        for i in rag_main_result:
            i_embedding = get_embedding(i)
            score = cosine_similarity([answer_embedding], [i_embedding])[0][0]
            print(f"질문: {i} | 유사도: {score:.4f}")
            if score > main_rag_score:
                main_rag_score= score  # 유사도 최고점수
                main_rag_question = i  # 이건 유사도가 제일 높은 문장인거같고

        return main_rag_score, main_rag_question


    def embeddingForFallbackRAG(self, situation: str, rag_fallback_result: list[str], userToken: str):
        print(f" AGENT repository - embeddingForFallbackRAG 실행: {userToken}")
        answer_embedding = get_embedding(situation)

        fallback_rag_score = 0
        fallback_rag_question = None

        for j in rag_fallback_result:
            j_embedding = get_embedding(j)
            score = cosine_similarity([answer_embedding], [j_embedding])[0][0]
            print(f" 질문: {i} | 유사도: {score:.4f}")
            if score > fallback_rag_score:
                fallback_rag_score = score  # 유사도 최고점수
                fallback_rag_question = j  # 이건 유사도가 제일 높은 문장인거같고

        return fallback_rag_score, fallback_rag_question
