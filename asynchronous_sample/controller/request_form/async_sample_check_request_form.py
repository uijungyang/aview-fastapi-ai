from pydantic import BaseModel

from asynchronous_sample.service.request.async_sample_check_request import AsyncSampleCheckRequest


class AsyncSampleCheckRequestForm(BaseModel):
    userToken: str

    def toRequest(self) -> AsyncSampleCheckRequest:
        return AsyncSampleCheckRequest(userToken=self.userToken)