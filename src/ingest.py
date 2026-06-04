from src import bootstrap  # noqa: F401 - must run before chromadb import

import sqlite3
from src.config import DATA_FILE, CHUNK_SIZE, CHUNK_OVERLAP
from src.rag import get_collection, embed_text


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def main():
    print(f"SQLite version used by Python: {sqlite3.sqlite_version}")

    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Data file not found: {DATA_FILE}")

    text = DATA_FILE.read_text(encoding="utf-8")
    chunks = chunk_text(text)

    collection = get_collection()

    existing = collection.get()
    if existing.get("ids"):
        collection.delete(ids=existing["ids"])

    ids = []
    embeddings = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        ids.append(f"policy_chunk_{i}")
        embeddings.append(embed_text(chunk))
        documents.append(chunk)
        metadatas.append({"source": str(DATA_FILE.name), "chunk": i})

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )

    print(f"Indexed {len(chunks)} chunks into ChromaDB.")


if __name__ == "__main__":
    main()
