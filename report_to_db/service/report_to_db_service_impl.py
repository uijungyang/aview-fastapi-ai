import os
import sys

from report_to_db.repository.report_to_db_repository_impl import ReportToDbRepositoryImpl
from report_to_db.service.report_to_db_service import ReportToDbService

from api.django_http_client import DjangoHttpClient

from user_defined_queue.repository.repository.user_defined_queue_repository_impl import UserDefinedQueueRepositoryImpl

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'template'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'template', 'include', 'socket_server'))

# from template.include.socket_server.utility.color_print import ColorPrinter


class RepositoryToDbServiceImpl(ReportToDbService):

    def __init__(self, userDefinedQueueRepository: userDefinedQueueRepositoryImpl):
        self.__reportToDbRepository = ReportToDbRepositoryImpl()
        self.__userDefinedQueueRepository = userDefinedQueueRepository

    def requestReportToAi(self):
        userDefinedReceiverFastAPIChannel = self.__userDefinedQueueRepository.getUserDefinedSocketReceiverFastAPIChannel()

        # ColorPrinter.print_important_message("requestToCheckMultipleUserTestPoint()")

        aiResponse = self.__reportToDbRepository.requestAiResult(userDefinedReceiverFastAPIChannel)

        success = DjangoHttpClient.post("/company_report/update", aiResponse)
        print(f"success => {success}")
        return success