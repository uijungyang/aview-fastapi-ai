from pydantic import BaseModel


class ReportToDbResponse(BaseModel):
    aiResult: str

    @classmethod
    def fromValues(cls, aiResult: str):
        return cls(aiResult=aiResult)