from enum import Enum


class ProjectExperience(Enum):
    NO_PROJECT = 1
    HAS_PROJECT = 2


    @classmethod
    def get_project_experience(cls, projectExperience: int) -> str:
        mapping = {
            1: "프로젝트 경험 없음",
            2: "프로젝트 경험 있음",
        }
        return mapping.get(projectExperience, "프로젝트 해당사항 없음")