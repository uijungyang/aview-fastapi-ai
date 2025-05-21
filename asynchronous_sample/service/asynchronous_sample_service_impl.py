import asyncio

from asynchronous_sample.repository.asynchronous_sample_repository_impl import AsynchronousSampleRepositoryImpl
from asynchronous_sample.service.asynchronous_sample_service import AsynchronousSampleService
from asynchronous_sample.service.request.async_sample_check_request import AsyncSampleCheckRequest
from asynchronous_sample.service.request.async_sample_request import AsyncSampleRequest
from utility.global_task_queue import task_queue


class AsynchronousSampleServiceImpl(AsynchronousSampleService):

    def __init__(self):
        self.asynchronousSampleRepository = AsynchronousSampleRepositoryImpl()

    async def generateHeavyOperation(self, request: AsyncSampleRequest):
        userToken = request.userToken
        data = request.data

        task_queue[userToken] = asyncio.Future()

        try:
            result = await self.asynchronousSampleRepository.heavyOperation(userToken, data)
            task_queue[userToken].set_result(result)

        except Exception as e:
            task_queue[userToken].set_exception(e)

    async def checkAsyncSampleResult(self, request: AsyncSampleCheckRequest) -> tuple[str, str | None]:
        return await self.asynchronousSampleRepository.checkTaskResult(request.userToken)
