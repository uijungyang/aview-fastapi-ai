from fastapi import FastAPI
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import uvicorn
import os
import sys

from starlette.middleware.cors import CORSMiddleware

from agnet_api.controller.agent_controller import agentRouter
from asynchronous_sample.controller.asynchronous_sample_controller import asynchronousSampleRouter
from chroma.delete_controller import deleteRouter
from interview.controller.interview_controller import interviewRouter
from config.cors_config import CorsConfig
from openai_api.controller.openai_api_controller import openaiApiRouter
from polyglot_temp.controller.polyglot_controller import polyglotRouter
from test.controller.test_controller import testRouter
from chroma.upload_controller import uploadRouter

from api import rss
from api import sitemap

# sys.path에 경로 추가해서 외부 모듈을 import 가능하게 함
#sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'template'))
#sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'template', 'include', 'socket_server'))
# 소켓 관련 초기화 실행
#UserDefinedInitializer.initUserDefinedDomain()

# 기본 구조
app = FastAPI()
load_dotenv()
CorsConfig.middlewareConfig(app)


# APIRouter로 작성한 Router를 실제 main에 매핑
# 결론적으로 다른 도메인에 구성한 라우터를 연결하여 사용할 수 있음.
app.include_router(openaiApiRouter)
app.include_router(interviewRouter)
app.include_router(testRouter)
app.include_router(uploadRouter, prefix="/chroma")
app.include_router(polyglotRouter)
app.include_router(rss.router)
app.include_router(sitemap.router)
app.include_router(deleteRouter, prefix="/chroma")
app.include_router(agentRouter, prefix="/agent")
app.include_router(asynchronousSampleRouter)


@app.get("/robots.txt", include_in_schema=False)
async def robots():
    return FileResponse("robots.txt", media_type="text/plain")


# FASTAPI_PORT를 통해서 이 서비스가 구동되는 포트 번호를 지정
if __name__ == "__main__":
    #colorama.init(autoreset=True)

    # TaskManager.createSocketServer()
    uvicorn.run(app, host=os.getenv('HOST'), port=int(os.getenv('FASTAPI_PORT')))