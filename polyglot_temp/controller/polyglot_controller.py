import os
import sys

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from polyglot_temp.service.polyglot_service_impl import PolyglotServiceImpl
from user_defined_queue.repository.user_defined_queue_repository_impl import UserDefinedQueueRepositoryImpl
# from template.include.socket_server.utility.color_print import ColorPrinter

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'template'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'template', 'include', 'socket_server'))


polyglotRouter = APIRouter()

def injectPolyglotService() -> PolyglotServiceImpl:
    return PolyglotServiceImpl(UserDefinedQueueRepositoryImpl.getInstance())

@polyglotRouter.get('/polyglot-result')
def requestNextQuestion(polyglotService: PolyglotServiceImpl =
                                 Depends(injectPolyglotService)):

    # ColorPrinter.print_important_message("requestNextQuestion()")

    nextQuestion = polyglotService.requestNextQuestion()

    return JSONResponse(content=nextQuestion, status_code=status.HTTP_200_OK)

@polyglotRouter.get('/polyglot-score-result')
def requestScore(polyglotService: PolyglotServiceImpl = Depends(injectPolyglotService)):
    # ColorPrinter.print_important_message("requestScore()")
    scoreResult = polyglotService.requestScore()
    return JSONResponse(content=scoreResult, status_code=status.HTTP_200_OK)