from pydantic import BaseModel


class OpenaiApiRequestForm(BaseModel):
    userSendMessage: str