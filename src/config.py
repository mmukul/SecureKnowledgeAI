from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    llm_model: str = os.getenv("LLM_MODEL", "llama3.2:3b")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    chroma_db_dir: str = os.getenv("CHROMA_DB_DIR", "./chroma_db")
    data_dir: str = os.getenv("DATA_DIR", "./data")
    collection_name: str = os.getenv("COLLECTION_NAME", "rag_demo")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "800"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "120"))
    top_k: int = int(os.getenv("TOP_K", "4"))


settings = Settings()
