# app/services/embedding_service.py

from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import settings
import os

_embedding_model = None  # private variable


def get_embedding_model():
    global _embedding_model

    if _embedding_model is None:
        if settings.huggingfacehub_api_token:
            os.environ["HUGGINGFACEHUB_API_TOKEN"] = settings.huggingfacehub_api_token

        _embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    return _embedding_model


def embed_text(text: str) -> list[float]:
    model = get_embedding_model()
    return model.embed_query(text)
