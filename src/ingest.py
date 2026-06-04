from src import bootstrap  # noqa: F401 must run before chromadb import

from src.config import DATA_FILE, CHUNK_SIZE, CHUNK_OVERLAP
from src.rag import get_collection, embed_text


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def ingest():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Data file not found: {DATA_FILE}")

    text = DATA_FILE.read_text(encoding="utf-8")
    chunks = chunk_text(text)
    collection = get_collection()

    if not chunks:
        print("No text chunks found for ingestion.")
        return

    ids = [f"policy-{i}" for i in range(len(chunks))]
    embeddings = [embed_text(chunk) for chunk in chunks]

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
    )

    print(f"Ingestion completed. Indexed {len(chunks)} chunks from {DATA_FILE}.")


if __name__ == "__main__":
    try:
        ingest()
    except Exception as exc:
        print(f"Error while running ingestion: {exc}")
        raise
