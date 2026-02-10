# app/services/rag_retriever.py

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import embed_text


def retrieve_similar_chunks(
    db: Session,
    room_id: int,
    query: str,
    top_k: int = 3,
):
    # 1️⃣ Embed query
    query_embedding = embed_text(query)

    # 2️⃣ Cosine similarity search (pgvector)
    stmt = (
        select(DocumentChunk)
        .where(DocumentChunk.room_id == room_id)
        .order_by(
            DocumentChunk.embedding.cosine_distance(query_embedding)
        )
        .limit(top_k)
    )

    return db.execute(stmt).scalars().all()
