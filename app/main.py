from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
import os
import sys

from starlette.middleware.cors import CORSMiddleware

from config.cors_config import CorsConfig
from openai_api.controller.openai_api_controller import openaiApiRouter
from polyglot_temp.controller.polyglot_controller import polyglotRouter
from report_to_db.controller.report_to_db_controller import reportToDbRouter
from test.controller.test_controller import testRouter
from user_defined_initializer.init import UserDefinedInitializer

# sys.path에 경로 추가해서 외부 모듈을 import 가능하게 함
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'template'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'template', 'include', 'socket_server'))
# 소켓 관련 초기화 실행
UserDefinedInitializer.initUserDefinedDomain()

# 기본 구조
app = FastAPI()
load_dotenv()
CorsConfig.middlewareConfig(app)


# APIRouter로 작성한 Router를 실제 main에 매핑
# 결론적으로 다른 도메인에 구성한 라우터를 연결하여 사용할 수 있음.
app.include_router(openaiApiRouter)
app.include_router(testRouter)
app.include_router(polyglotRouter)
app.include_router(reportToDbRouter)


# HOST는 모두에 열려 있고
# FASTAPI_PORT를 통해서 이 서비스가 구동되는 포트 번호를 지정
if __name__ == "__main__":
    #colorama.init(autoreset=True)

    # TaskManager.createSocketServer()
    uvicorn.run(app, host=os.getenv('HOST'), port=int(os.getenv('FASTAPI_PORT')))