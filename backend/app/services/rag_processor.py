import os
import tempfile
from sqlalchemy.orm import Session
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from app.models.room_document import RoomDocument
from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import embedding_model

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)


async def process_pdf(
    db: Session,
    room_id: int,
    user_id: int,
    file,
):

    # 🔥 1️⃣ Delete existing document (1 room = 1 pdf)
    existing = (
        db.query(RoomDocument)
        .filter(RoomDocument.room_id == room_id)
        .first()
    )

    if existing:
        db.delete(existing)
        db.commit()

    # 🔥 2️⃣ Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        temp_path = tmp.name
    # 🔥 3️⃣ Load PDF
    loader = PyPDFLoader(temp_path)
    docs = loader.load()
    # 🔥 4️⃣ Split
    chunks = splitter.split_documents(docs)
    # 🔥 5️⃣ Create metadata entry
    document = RoomDocument(
        room_id=room_id,
        uploaded_by=user_id,
        file_name=file.filename,
        storage_path=temp_path,
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    # 🔥 6️⃣ Generate embeddings
    texts = [chunk.page_content for chunk in chunks]
    embeddings = embedding_model.embed_documents(texts)
    # 🔥 7️⃣ Insert chunks
    total = len(chunks)

    for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
        db.add(
            DocumentChunk(
                document_id=document.id,
                room_id=room_id,
                chunk_index=i,
                total_chunks=total,
                content=chunk.page_content,
                embedding=vector,
            )
        )

    db.commit()
    # 🔥 8️⃣ Remove temp file
    os.remove(temp_path)
