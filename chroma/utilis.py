import pandas as pd
from chroma.client import get_chroma_collection
from chroma.embedder import get_embedding_from_openai


def import_questions_from_excel(filepath: str, company: str):
    df = pd.read_excel(filepath)
    df = df.dropna(subset=["id", "question"])  # 필수 컬럼만 남김

    collection = get_chroma_collection(company)

    for _, row in df.iterrows():
        question_id = str(row["id"])
        question_text = str(row["question"])

        try:
            embedding = get_embedding_from_openai(question_text)
            print(f"✅ 인덱싱 성공: {question_id} - {question_text[:30]}...")
        except Exception as e:
            print(f"❌ 임베딩 실패: {question_id} - {e}")
            continue

        try:
            collection.add(
                documents=[question_text],
                ids=[question_id],
                embeddings=[embedding],
                metadatas=[{
                    "tech_category": str(row["tech_category"])
                    #"jobCategory": str(row["jobCategory"]),
                    #"questionType": str(row["questionType"]),
                    #"tag": str(row["tag"]),
                    #"company": row["company"].lower(),
                }]
            )
        except Exception as e:
            print(f"❌ Chroma 저장 실패: {question_id} - {e}")


