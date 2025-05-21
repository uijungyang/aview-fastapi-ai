from pydantic import BaseModel

from asynchronous_sample.service.request.async_sample_request import AsyncSampleRequest


class AsyncSampleRequestForm(BaseModel):
    userToken: str
    data: str

    def toRequest(self) -> AsyncSampleRequest:
        return AsyncSampleRequest(userToken=self.userToken, data=self.data)