# app/agents/llm_connection.py

from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings

def get_llm_model():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=settings.google_api_key
    )
