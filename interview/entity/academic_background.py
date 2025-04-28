from enum import Enum


class AcademicBackground(Enum):
    NON_MAJOR = 1
    MAJOR = 2

    # 매핑된 사람 친화적인 표현을 반환
    @classmethod
    def get_academic_background(cls, academicBackground: int) -> str:
        mapping = {
            1: "비전공자",
            2: "전공자",
        }
        return mapping.get(academicBackground, "전공 해당사항 없음")