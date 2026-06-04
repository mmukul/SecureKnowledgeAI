from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Data
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "company_policies.txt"

# ChromaDB
CHROMA_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "company_policies"

# Models
MODEL_NAME = "llama3.2:3b"
EMBED_MODEL = "nomic-embed-text"

# RAG Settings
TOP_K = 4
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
