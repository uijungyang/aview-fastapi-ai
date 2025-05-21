from abc import ABC, abstractmethod

from asynchronous_sample.service.request.async_sample_request import AsyncSampleRequest


class AsynchronousSampleService(ABC):
    @abstractmethod
    def generateHeavyOperation(self, request: AsyncSampleRequest):
        pass
