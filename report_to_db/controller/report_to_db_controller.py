import os
import sys

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from report_to_db.service.report_to_db_service_impl import ReportToDbServiceImpl
from user_defined_queue.repository.user_defined_queue_repository_impl import UserDefinedQueueRepositoryImpl

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'template'))

# from template.include.socket_server.utility.color_print import ColorPrinter

reportToDbRouter = APIRouter()

async def injectReportToDbService() -> ReportToDbServiceImpl:
    return ReportToDbServiceImpl(UserDefinedQueueRepositoryImpl.getInstance())

@reportToDbRouter.post('/update')
async def requestReportToDb(reportToDbService: ReportToDbServiceImpl = Depends(injectReportToDbService)):

    # ColorPrinter.print_important_message("requestReportToDbPoint()")

    success = await reportToDbService.requestReportToAi()

    return JSONResponse(content=success, status_code=status.HTTP_200_OK)