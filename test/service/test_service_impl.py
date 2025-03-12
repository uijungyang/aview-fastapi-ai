import os
import sys

from test.repository.test_repository_impl import TestRepositoryImpl
from test.service.test_service import TestService
from user_defined_queue.repository.user_defined_queue_repository_impl import UserDefinedQueueRepositoryImpl

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'template'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'template', 'include', 'socket_server'))

# from template.include.socket_server.utility.color_print import ColorPrinter

class TestServiceImpl(TestService):
    def __init__(self, userDefinedQueueRepository: UserDefinedQueueRepositoryImpl):
        self.__testRepository = TestRepositoryImpl()
        self.__userDefinedQueueRepository = userDefinedQueueRepository

    def requestTestResult(self):
        userDefinedReceiverFastAPIChannel = self.__userDefinedQueueRepository.getUserDefinedSocketReceiverFastAPIChannel()
        # ColorPrinter.print_important_data("userDefinedReceiverFastAPIChannel", userDefinedReceiverFastAPIChannel)
        return self.__testRepository.getResult(userDefinedReceiverFastAPIChannel)