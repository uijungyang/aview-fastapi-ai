import os
import sys

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from test.service.test_service_impl import TestServiceImpl
from user_defined_queue.repository.user_defined_queue_repository_impl import UserDefinedQueueRepositoryImpl
# from template.include.socket_server.utility.color_print import ColorPrinter

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'template'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'template', 'include', 'socket_server'))

testRouter = APIRouter()

def injectTestService() -> TestServiceImpl:
    return TestServiceImpl(UserDefinedQueueRepositoryImpl.getInstance())

@testRouter.get('/test-result')
def requestOpenaiApiResult(testService: TestServiceImpl = Depends(injectTestService)):

    # ColorPrinter.print_import_message("requestTestResult()")

    testResult = testService.requestTestResult()

    return JSONResponse(content=testResult, status_code=status.HTTP_200_OK)