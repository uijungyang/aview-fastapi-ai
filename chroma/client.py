
import chromadb

client = chromadb.Client()

def get_chroma_collection(company_name: str):
    collection_name = f"{company_name.lower()}"
    return client.get_or_create_collection(name=collection_name)