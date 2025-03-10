import json
import queue

from test.repository.test_repository import TestRepository


class TestRepositoryImpl(TestRepository):

    def getResult(self, userDefinedReceiverFastAPIChannel):
        print(f"TestRepositoryImpl getResult()")

        try:
            receivedResponseFromSocketClient = userDefinedReceiverFastAPIChannel.get(False)
            return json.loads(receivedResponseFromSocketClient)

        except queue.Empty:
            return "아직 데이터를 처리 중이거나 요청한 데이터가 없습니다."