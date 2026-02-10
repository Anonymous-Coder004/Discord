# app/services/embedding_service.py

from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import settings
import os

if settings.huggingfacehub_api_token:
    os.environ["HUGGINGFACEHUB_API_TOKEN"]=settings.huggingfacehub_api_token

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
  
def embed_text(text: str) -> list[float]:
    """
    Convert a string into a 384-dim embedding vector.
    Used for query embedding during retrieval.
    """
    print(text)
    return embedding_model.embed_query(text)
