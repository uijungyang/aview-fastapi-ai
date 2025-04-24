from enum import Enum

class TechStack(Enum):
    FULLSTACK = 1
    BACKEND_SERVER = 2
    FRONT = 3
    WEB = 4
    FLUTTER =5
    JAVA = 6
    JAVASCRIPT = 7
    PYTHON=8
    VUE = 9
    API=10
    MYSQL=11
    AWS=12
    REACT=13
    ASP=14
    ANGULAR=15
    BOOTSTRAP=16
    NODE_JS=17
    JQUERY=18
    PHP=19
    JSP=20
    GRAPH_QL=21
    HTML5=22

    # 매핑된 사람 친화적인 표현을 반환
    @classmethod
    def get_teck_stack(cls, teckStackId: int) -> str:
        mapping = {
            0: "있음",
            1: "없음",
        }
        return mapping.get(teckStackId, "기술스택 해당사항 없음")

