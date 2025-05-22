from pydantic import BaseModel

class AsyncSampleCheckRequest(BaseModel):
    userToken: str
