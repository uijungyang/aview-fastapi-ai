from enum import Enum

class InterviewTechStack(Enum):
    FULLSTACK: 1
    BACKEND_SERVER: 2
    FRONTEND: 3
    WEB: 4
    FLUTTER: 5
    JAVA: 6
    JAVASCRIPT: 7
    PYTHON: 8
    VUE_JS: 9
    API: 10
    MYSQL: 11
    AWS: 12
    REACTJS: 13
    ASP: 14
    ANGULAR: 15
    BOOTSTRAP: 16
    NODE_JS: 17
    JQUERY: 18
    PHP: 19
    JSP: 20
    GRAPHQL: 21
    HTML5: 22

    @classmethod
    def get_tech_stack_list(cls, tech_stack_id: list[int]) -> list[str]:
        mapping = {
            1: "FULLSTACK",
            2: "BACKEND_SERVER",
            3: "FRONTEND",
            4: "WEB",
            5: "FLUTTER",
            6: "JAVA",
            7: "JAVASCRIPT",
            8: "PYTHON",
            9: "VUE_JS",
            10: "API",
            11: "MYSQL",
            12: "AWS",
            13: "REACTJS",
            14: "ASP",
            15: "ANGULAR",
            16: "BOOTSTRAP",
            17: "NODE_JS",
            18: "JQUERY",
            19: "PHP",
            20: "JSP",
            21: "GRAPHQL",
            22: "HTML5"
        }
        return [mapping.get(tid, "기술스택 해당사항 없음") for tid in tech_stack_id]

