import os
from typing import List
from sqlalchemy.orm import Session
from pgvector.sqlalchemy import Vector
from sqlalchemy import select
import numpy as np

from .models import Document

try:
    import google.generativeai as genai
except Exception:  # pragma: no cover
    genai = None


def embed_text(text: str) -> List[float]:
    if os.getenv("MOCK_LLM", "false").lower() == "true" or genai is None:
        return [0.0] * 3072
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    result = genai.embed_content(model="models/embedding-001", content=text)
    return result["embedding"]


def add_document(db: Session, title: str, source: str, content: str):
    emb = embed_text(content)
    doc = Document(title=title, source=source, content=content, embedding=emb)
    db.add(doc)
    db.commit()


def search(db: Session, query: str, top_k: int = 3) -> List[Document]:
    q_emb = embed_text(query)
    if db.bind.dialect.name == 'postgresql':
        stmt = select(Document).order_by(Document.embedding.l2_distance(q_emb)).limit(top_k)
        return list(db.execute(stmt).scalars())
    else:
        return db.query(Document).limit(top_k).all()
