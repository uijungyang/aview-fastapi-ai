import multiprocessing

from fastapi import APIRouter, Depends

from user_defined_queue.repository.user_defined_queue_repository_impl import UserDefinedQueueRepositoryImpl

#fastAPI 라우터 생성
userDefinedQueueRouter = APIRouter()

# 요청이 여러번이어서 대기열 쌓아놓는거임
# 1. 의존성 주입 함수 (싱글톤 인스턴스 주입)
async def injectUserDefinedQueueRepository() -> UserDefinedQueueRepositoryImpl:
    return UserDefinedQueueRepositoryImpl.getInstance()

# 2. 큐 생성 요청 (초기화)
@userDefinedQueueRouter.post("/queue/create")
async def create_queues(
    queueRepo: UserDefinedQueueRepositoryImpl = Depends(injectUserDefinedQueueRepository)
):
    queueRepo.create()
    return {"message": "큐가 성공적으로 생성되었습니다."}

# 3. Receiver Queue 확인
@userDefinedQueueRouter.get("/queue/receiver")
async def get_receiver_queue(
    queueRepo: UserDefinedQueueRepositoryImpl = Depends(injectUserDefinedQueueRepository)
):
    queue = queueRepo.getUserDefinedSocketReceiverFastAPIChannel()
    if isinstance(queue, multiprocessing.queues.Queue):
        return {"receiverQueue": "존재함"}
    return {"receiverQueue": "없음"}

# 4. Transmitter Queue 확인
@userDefinedQueueRouter.get("/queue/transmitter")
async def get_transmitter_queue(
    queueRepo: UserDefinedQueueRepositoryImpl = Depends(injectUserDefinedQueueRepository)
):
    queue = queueRepo.getUserDefinedFastAPISocketTransmitterChannel()
    if isinstance(queue, multiprocessing.queues.Queue):
        return {"transmitterQueue": "존재함"}
    return {"transmitterQueue": "없음"}