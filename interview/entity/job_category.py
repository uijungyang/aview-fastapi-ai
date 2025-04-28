from enum import Enum

class JobCategory(Enum):
    BACKEND = 1
    FRONTEND = 2
    EMBEDDED = 3
    AI = 4
    DEVOPS = 5
    WEBAPP = 6

    @classmethod
    def get_job_name(cls, job_id: int) -> str:
        try:
            return cls(job_id).name
        except ValueError:
            return "알 수 없음"