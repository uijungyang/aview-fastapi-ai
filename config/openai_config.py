import os
from dotenv import load_dotenv


class OpenAIConfig:

    @classmethod
    def loadConfig(cls):
        """환경 변수 로드 및 검증"""
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("API Key가 준비되어 있지 않습니다!")

        os.environ["OPENAI_API_KEY"] = api_key

    @classmethod
    def get_api_key(cls):
        """API Key 가져오기"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API Key가 설정되지 않았습니다. loadConfig()를 먼저 호출하세요.")
        return api_key