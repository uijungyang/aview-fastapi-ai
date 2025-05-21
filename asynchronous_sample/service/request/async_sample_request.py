from pydantic import BaseModel

class AsyncSampleRequest(BaseModel):
    userToken: str
    data: str