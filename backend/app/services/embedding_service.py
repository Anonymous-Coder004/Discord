
# app/services/embedding_service.py
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from app.core.config import settings

_embedding_model = None  # private variable


def get_embedding_model():
    global _embedding_model

    if _embedding_model is None:
        _embedding_model = HuggingFaceEndpointEmbeddings(
            huggingfacehub_api_token=settings.huggingfacehub_api_token,
            model="sentence-transformers/all-MiniLM-L6-v2",
        )

    return _embedding_model


def embed_text(text: str) -> list[float]:
    model = get_embedding_model()
    return model.embed_query(text)