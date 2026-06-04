from src import bootstrap  # noqa: F401 - must run before chromadb import

import ollama
import chromadb
from chromadb.config import Settings

from src.config import CHROMA_DIR, COLLECTION_NAME, EMBED_MODEL, LLM_MODEL, TOP_K


def get_chroma_client():
    # Do not use chromadb.telemetry.product.noop.
    # That import path is invalid in several ChromaDB versions.
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
    documents = results.get("documents", [[]])[0]
    return documents


def answer_question(question: str, debug: bool = False):
    documents = retrieve_context(question)
    context = "\n\n---\n\n".join(documents)

    if debug:
        print("\nRetrieved Chunks:")
        print("-" * 60)
        for index, doc in enumerate(documents, start=1):
            print(f"Chunk {index}:\n{doc}\n")
        print("-" * 60)

    if not context.strip():
        return "No relevant context found. Please run ingestion first with: python -m src.ingest"

    prompt = f"""
You are a helpful enterprise policy assistant.
Answer the question only using the provided context.
If the answer is not present in the context, say: "I could not find this in the provided policy documents."

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
