from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
import os

load_dotenv()

app = FastAPI()

@app.get("/")
def first_test():
    return {"message": "First FastAPI Test"}

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv('HOST'), port=int(os.getenv('FASTAPI_PORT')))