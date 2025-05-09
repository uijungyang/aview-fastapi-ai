from fastapi import APIRouter, Query
import chromadb

deleteRouter = APIRouter()
#client = chromadb.Client()
client = chromadb.PersistentClient(path="./chroma_db")

@deleteRouter.get("/collections")
def list_collections():
    try:
        collections = client.list_collections()
        return {"collections": [col.name for col in collections]}
    except Exception as e:
        return {"error": str(e)}


@deleteRouter.delete("/delete-collection")
def delete_collection(company: str = Query(...)):
    try:
        client.delete_collection(name=company)
        return {"message": f"{company} 컬렉션 삭제 완료"}
    except Exception as e:
        return {"error": str(e)}