from enum import Enum

class JobCategory(Enum):
    BACKEND = 1
    FRONT = 2
    DEVOPS = 3
    AI = 4
    EMBEDDED = 5
    AppWeb = 6

    @classmethod
    def get_job_name(cls, job_id: int) -> str:
        try:
            return cls(job_id).name
        except ValueError:
            return "알 수 없음"