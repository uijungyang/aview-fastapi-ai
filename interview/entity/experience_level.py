from enum import Enum

class ExperienceLevel(Enum):
    NEWBIE = 1
    THREE_YEARS_OR_LESS = 2
    FIVE_YEARS_OR_LESS = 3
    TEN_YEARS_OR_LESS = 4
    TEN_YEARS_OR_MORE = 5

    # 매핑된 사람 친화적인 표현을 반환
    @classmethod
    def get_experience_level(cls, experience_id: int) -> str:
        mapping = {
            1: "신입",
            2: "3년 이하",
            3: "5년 이하",
            4: "10년 이하",
            5: "10년 이상"
        }
        return mapping.get(experience_id, "알 수 없음")