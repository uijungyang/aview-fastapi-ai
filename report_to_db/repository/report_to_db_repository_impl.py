import json
import queue

from report_to_db.repository.report_to_db_repository import ReportToDbRepository


class ReportToDbRepositoryImpl(ReportToDbRepository):

    def requestAiResult(self, userDefinedReceiverFastAPIChannel):
        print(f"TestRepositoryImpl getResult()")

        try:
            receivedResponseFromSocketClient = userDefinedReceiverFastAPIChannel.get(False)
            return json.loads(receivedResponseFromSocketClient)

        except queue.Empty:
            return "아직 데이터를 처리 중이거나 요청한 데이터가 없습니다."