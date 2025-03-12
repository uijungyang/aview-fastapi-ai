import os
import sys

from polyglot_temp.repository.polyglot_repository_impl import PolyglotRepositoryImpl
from polyglot_temp.service.polyglot_service import PolyglotService
from user_defined_queue.repository.user_defined_queue_repository_impl import UserDefinedQueueRepositoryImpl

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'template'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'template', 'include', 'socket_server'))

# from template.include.socket_server.utility.color_print import ColorPrinter

class PolyglotServiceImpl(PolyglotService):
    def __init__(self, userDefinedQueueRepository: UserDefinedQueueRepositoryImpl):
        self.__polyglotRepository = PolyglotRepositoryImpl()
        self.__userDefinedQueueRepository = userDefinedQueueRepository

    def requestNextQuestion(self):
        userDefinedReceiverFastAPIChannel = self.__userDefinedQueueRepository.getUserDefinedSocketReceiverFastAPIChannel()
        # ColorPrinter.print_important_data("userDefinedReceiverFastAPIChannel", userDefinedReceiverFastAPIChannel)
        return self.__polyglotRepository.getResult(userDefinedReceiverFastAPIChannel)

    def requestScore(self):
        userDefinedReceiverFastAPIChannel = self.__userDefinedQueueRepository.getUserDefinedSocketReceiverFastAPIChannel()
        # ColorPrinter.print_important_data("userDefinedReceiverFastAPIChannel", userDefinedReceiverFastAPIChannel)
        return self.__polyglotRepository.requestScore(userDefinedReceiverFastAPIChannel)