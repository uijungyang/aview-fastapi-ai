from agnet_api.repository.agent_repository_impl import AgentRepositoryImpl
from agnet_api.service.agent_service import AgentService
from rag_api.repository.vector_repository_impl import RagVectorRepositoryImpl
from rag_api.entity.embedding import get_embedding

from sklearn.metrics.pairwise import cosine_similarity

class AgentServiceImpl(AgentService):

    def __init__(self):
        self.ragVectorRepository = RagVectorRepositoryImpl()
        self.agentRepository = AgentRepositoryImpl()


    async def get_context_with_agent_fallback(self, target_company: str, situation: str):
        print(f"\U0001F525 [AGENT] fallback initiated from {target_company}")

        # 1. 공통 DB에서 유사 질문 검색
        supplemental_collection = self.ragVectorRepository.get_collection("supplemental")
        query_embedding = get_embedding(situation)
        result = supplemental_collection.query(query_embeddings=[query_embedding], n_results=10)

        if not result["documents"]:
            return []

        matched_docs = result["documents"][0]
        matched_metas = result["metadatas"][0]

        # 2. target 회사 설명과 각 회사 설명 비교
        target_desc = self.agentRepository.get_company_description(target_company)
        target_desc_emb = get_embedding(target_desc)

        company_scores = {}
        for meta in matched_metas:
            comp = meta.get("company")
            comp_desc = self.agentRepository.get_company_description(comp)
            comp_desc_emb = get_embedding(comp_desc)

            sim = cosine_similarity([target_desc_emb], [comp_desc_emb])[0][0]
            company_scores[comp] = sim

        # 3. 상위 유사 회사들 필터링
        top_companies = sorted(company_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        top_names = {c[0] for c in top_companies}

        final_contexts = [doc for doc, meta in zip(matched_docs, matched_metas) if meta["company"] in top_names]

        return final_contexts