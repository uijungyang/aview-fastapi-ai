from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
import os
import sys
import colorama

from config.cors_config import CorsConfig
from convolution_neural_network.controller.cnn_controller import convolutionNeuralNetworkRouter
from dcgan.controller.dcgan_controller import dcganRouter
from ensemble_method.controller.ensemble_method_controller import ensembleMethodRouter
from feature_engineering.controller.feature_engineering_controller import featureEngineeringRouter
from game_data_fine_tuning.controller.gdft_controller import gameDataFineTuningRouter
from game_software_analysis.controller.game_software_analysis_controller import gameSoftwareAnalysisRouter
from gan.controller.gan_controller import ganRouter
from gradient_descent.controller.gradient_descent_controller import gradientDescentRouter
from hyper_parameter.controller.hyper_parameter_controller import hyperParameterRouter
from image_generation.controller.image_generation_controller import imageGenerationRouter
from kmeans.controller.kmeans_controller import kMeansRouter
from mnist.controller.mnist_controller import mnistRouter
from model_regulation.controller.model_regulation_controller import modelRegulationRouter
from openai_basic.controller.openai_basic_controller import openAiBasicRouter
from openai_fine_tuning.openai_fine_tuning_controller import openaiFineTuningRouter
from principal_component_analysis.controller.pca_controller import principalComponentAnalysisRouter

from openai_api.controller.openai_api_controller import openaiApiRouter
from polyglot_temp.controller.polyglot_controller import polyglotRouter
from report_to_db.controller.report_to_db_controller import reportToDbRouter
from test.controller.test_controller import testRouter
from user_defined_initializer.init import UserDefinedInitializer

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'template'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'template', 'include', 'socket_server'))

# from template.deep_learning.controller.deep_learning_controller import deepLearningRouter
# from template.dice.controller.dice_controller import diceResultRouter
# from template.system_initializer.init import SystemInitializer
# from template.task_manager.manager import TaskManager
# from template.include.socket_server.initializer.init_domain import DomainInitializer

# DomainInitializer.initEachDomain()
# SystemInitializer.initSystemDomain()
UserDefinedInitializer.initUserDefinedDomain()

app = FastAPI()

load_dotenv()

CorsConfig.middlewareConfig(app)

origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(deepLearningRouter)
# app.include_router(diceResultRouter)

# APIRouter로 작성한 Router를 실제 main에 매핑
# 결론적으로 다른 도메인에 구성한 라우터를 연결하여 사용할 수 있음.
app.include_router(openaiApiRouter)
app.include_router(testRouter)
app.include_router(polyglotRouter)
app.include_router(reportToDbRouter)
app.include_router(featureEngineeringRouter)
app.include_router(ensembleMethodRouter)
app.include_router(kMeansRouter)
app.include_router(mnistRouter)
app.include_router(modelRegulationRouter)
app.include_router(gradientDescentRouter)
app.include_router(hyperParameterRouter)
app.include_router(principalComponentAnalysisRouter)
app.include_router(convolutionNeuralNetworkRouter)
app.include_router(gameSoftwareAnalysisRouter)
app.include_router(openAiBasicRouter)
app.include_router(gameDataFineTuningRouter)
app.include_router(openaiFineTuningRouter)
app.include_router(ganRouter)
app.include_router(dcganRouter)
app.include_router(imageGenerationRouter)

# HOST는 모두에 열려 있고
# FASTAPI_PORT를 통해서 이 서비스가 구동되는 포트 번호를 지정
if __name__ == "__main__":
    colorama.init(autoreset=True)

    # TaskManager.createSocketServer()
    uvicorn.run(app, host=os.getenv('HOST'), port=int(os.getenv('FASTAPI_PORT')))