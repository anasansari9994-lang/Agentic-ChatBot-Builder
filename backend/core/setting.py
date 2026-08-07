from pydantic_settings import BaseSettings
from typing import Optional, Any

class Settings(BaseSettings):
    APP_NAME: str = "RAG CHATBOT MAKER"
    DEBUG: bool = True

    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    RERANKING_MODEL: str = "BAAI/bge-reranker-base"
    DEVICE: str = "cuda"

    DEFAULT_LLM_PROVIDER : str = "gemini"
    GEMINI_API_KEY : Optional[str] = None
    GROQ_API_KEY : Optional[str] = None
    MISTRAL_API_KEY : Optional[str] = None

    CHUNK_SIZE: int = 1028
    CHUNK_OVERLAP: int = 128
    TOP_K_RETRIVAL: int = 10
    TOP_N_RERANKING: int = 5

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

setting = Settings()
