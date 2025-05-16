import openai
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_embedding(text: str) -> list[float]:
    #print("여기진입1")
    client = OpenAI()
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    #print("여기진입2")
    return response.data[0].embedding
