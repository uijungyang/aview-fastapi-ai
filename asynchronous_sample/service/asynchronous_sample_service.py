from abc import ABC, abstractmethod

from asynchronous_sample.service.request.async_sample_check_request import AsyncSampleCheckRequest
from asynchronous_sample.service.request.async_sample_request import AsyncSampleRequest


class AsynchronousSampleService(ABC):
    @abstractmethod
    def generateHeavyOperation(self, request: AsyncSampleRequest):
        pass

    @abstractmethod
    def checkAsyncSampleResult(self, request: AsyncSampleCheckRequest) -> tuple[str, str | None]:
        pass