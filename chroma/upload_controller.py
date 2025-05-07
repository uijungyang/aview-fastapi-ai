import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Query

from chroma.client import get_chroma_collection
from chroma.embedder import get_embedding_from_openai
from chroma.utilis import import_questions_from_excel

uploadRouter = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@uploadRouter.post("/upload-excel")
async def upload_excel_file(company: str = Query(...), file: UploadFile = File(...)):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="엑셀 파일(.xlsx)만 허용됩니다.")

    file_location = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        import_questions_from_excel(file_location, company)
        return {"message": f"{file.filename} 업로드 및 DB 저장 완료!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 처리 중 오류 발생: {str(e)}")


@uploadRouter.get("/questions")
def get_questions(company: str):
    collection = get_chroma_collection(company)
    results = collection.get()

    questions = []
    for doc, id, metadata in zip(results["documents"], results["ids"], results["metadatas"]):
        questions.append({
            "id": id,
            "question": doc,
            "jobCategory": metadata.get("jobCategory"),
            "questionType": metadata.get("questionType"),
            "tag": metadata.get("tag"),
        })

    return {
        "count": len(questions),
        "questions": questions
    }