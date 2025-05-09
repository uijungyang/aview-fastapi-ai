from fastapi import APIRouter, Query

from agnet_api.service.agent_service_impl import AgentService, AgentServiceImpl

agentRouter = APIRouter()
agent_service = AgentServiceImpl()

# 의존성 주입
async def injectAgentService() -> AgentServiceImpl:
    return AgentServiceImpl()

@agentRouter.get("/agent/fallback-context")
async def get_fallback_context(company: str = Query(...), situation: str = Query(...)):
    result = await agent_service.get_context_with_agent_fallback(company, situation)
    return {"context": result}

