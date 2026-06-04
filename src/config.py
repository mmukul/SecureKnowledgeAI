from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "company_policies.txt"
CHROMA_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "company_policies"

LLM_MODEL = "llama3.2:3b"
MODEL_NAME = LLM_MODEL
EMBED_MODEL = "nomic-embed-text"
EMBEDDING_MODEL = EMBED_MODEL
OLLAMA_HOST = "http://localhost:11434"

TOP_K = 4
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
