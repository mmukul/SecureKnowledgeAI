from src import bootstrap  # noqa: F401 must run before chromadb import

import chromadb
from chromadb.config import Settings
import ollama

from src.config import (
    CHROMA_DIR,
    COLLECTION_NAME,
    EMBED_MODEL,
    LLM_MODEL,
    TOP_K,
)


def get_chroma_client():
    return chromadb.PersistentClient(
        path=str(CHROMA_DIR),
        settings=Settings(anonymized_telemetry=False),
    )


def get_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(name=COLLECTION_NAME)


def embed_text(text: str):
    response = ollama.embeddings(model=EMBED_MODEL, prompt=text)
    return response["embedding"]


def retrieve_context(question: str, top_k: int = TOP_K):
    collection = get_collection()
    query_embedding = embed_text(question)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )
    docs = results.get("documents", [[]])[0]
    return docs


def generate_answer(question: str, context_chunks):
    context = "\n\n".join(context_chunks).strip()
    if not context:
        return "No relevant context found. Please run ingestion first using: python -m src.ingest"

    prompt = f"""
You are an enterprise policy assistant. Answer only from the provided context.
If the answer is not present in the context, say: I could not find this information in the indexed documents.

Context:
{context}

Question:
{question}

Answer:
""".strip()

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"].strip()


def ask(question: str, debug: bool = False) -> str:
    context_chunks = retrieve_context(question)

    if debug:
        print("\nRetrieved Chunks:")
        print("-" * 60)
        for i, chunk in enumerate(context_chunks, start=1):
            print(f"Chunk {i}:\n{chunk}\n")
        print("-" * 60)

    answer = generate_answer(question, context_chunks)
    return answer
