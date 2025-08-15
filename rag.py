from typing import List
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def jobs_to_documents(jobs) -> List[Document]:
    docs: List[Document] = []
    for j in jobs:
        meta = {
            "title": j.get("title", ""),
            "company": j.get("company", ""),
            "link": j.get("link", ""),
            "location": j.get("location", ""),
            "type": j.get("type", ""),
            "salary": j.get("salary", ""),
        }
        content_parts = [
            j.get("title", ""),
            j.get("company", ""),
            j.get("description", ""),
            f"Location: {j.get('location', '')}",
            f"Type: {j.get('type', '')}",
            f"Skills: {j.get('skills', '')}",
            f"Experience: {j.get('experience', '')}",
            f"Salary: {j.get('salary', '')}",
            f"Apply: {j.get('link', '')}",
        ]
        page = " | ".join([p for p in content_parts if p])
        docs.append(Document(page_content=page, metadata=meta))
    return docs


def build_vectorstore(jobs) -> FAISS:
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    docs = jobs_to_documents(jobs)
    return FAISS.from_documents(docs, embeddings)


def retrieve(vectorstore: FAISS, query: str, k: int = 10) -> List[Document]:
    return vectorstore.similarity_search(query, k=k)