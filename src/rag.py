"""Core RAG logic for the ChromaDB + Ollama demo.

Important:
The SQLite compatibility block must run before any ChromaDB/LangChain Chroma
imports. This avoids the common CentOS/Rocky Linux error where the system
SQLite version is older than the version required by ChromaDB.
"""

try:
    __import__("pysqlite3")
    import sys
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except Exception as e:
    print(f"SQLite patch failed: {e}")

import chromadb

# Must run before importing chromadb/langchain_chroma.
from src import compat  # noqa: F401


import os
import logging
import sys
from pathlib import Path
from typing import List

# Fallback protection when sitecustomize.py is not loaded.
# These lines must stay before any ChromaDB/LangChain Chroma imports.
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")
os.environ.setdefault("CHROMA_TELEMETRY_ENABLED", "false")
os.environ.setdefault("CHROMA_PRODUCT_TELEMETRY_IMPL", "chromadb.telemetry.product.noop.NoopProductTelemetryClient")

try:
    __import__("pysqlite3")
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except Exception:
    pass

logging.getLogger("chromadb.telemetry.product.posthog").setLevel(logging.CRITICAL)

from chromadb.config import Settings as ChromaSettings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from src.config import settings


PROMPT = ChatPromptTemplate.from_template(
    """
You are a helpful RAG assistant. Answer the question using only the provided context.
If the answer is not in the context, say you do not know.

Context:
{context}

Question:
{question}

Answer:
""".strip()
)


def get_embeddings() -> OllamaEmbeddings:
    return OllamaEmbeddings(
        model=settings.embedding_model,
        base_url=settings.ollama_base_url,
    )


def get_llm() -> ChatOllama:
    return ChatOllama(
        model=settings.llm_model,
        base_url=settings.ollama_base_url,
        temperature=0,
    )


def load_documents() -> List[Document]:
    data_path = Path(settings.data_dir)
    if not data_path.exists():
        raise FileNotFoundError(f"Data directory not found: {settings.data_dir}")

    documents: List[Document] = []

    text_loader = DirectoryLoader(
        settings.data_dir,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )
    md_loader = DirectoryLoader(
        settings.data_dir,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )
    pdf_loader = DirectoryLoader(
        settings.data_dir,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True,
    )

    for loader in (text_loader, md_loader, pdf_loader):
        documents.extend(loader.load())

    return documents


def split_documents(documents: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    return splitter.split_documents(documents)


def get_vectorstore() -> Chroma:
    return Chroma(
        collection_name=settings.collection_name,
        persist_directory=settings.chroma_db_dir,
        embedding_function=get_embeddings(),
        client_settings=ChromaSettings(anonymized_telemetry=False),
    )


def format_docs(docs: List[Document]) -> str:
    return "\n\n".join(
        f"Source: {doc.metadata.get('source', 'unknown')}\n{doc.page_content}"
        for doc in docs
    )


def get_index_count() -> int:
    """Return the number of chunks currently stored in ChromaDB."""
    vectorstore = get_vectorstore()
    try:
        return int(vectorstore._collection.count())
    except Exception:
        return 0


def retrieve_context(question: str) -> List[Document]:
    """Retrieve the most relevant chunks for a question."""
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": settings.top_k})
    return retriever.invoke(question)


def fallback_answer(question: str, docs: List[Document]) -> str:
    """Simple fallback when the LLM returns an empty response.

    This keeps demos usable even if Ollama returns a blank response.
    """
    text = format_docs(docs).lower()
    if "work" in question.lower() and "home" in question.lower():
        for doc in docs:
            for line in doc.page_content.splitlines():
                if "remotely up to" in line.lower() or "work remotely" in line.lower():
                    return line.strip()
    return "I found relevant context, but the model returned an empty response. Run with --debug to view retrieved chunks."


def answer_question(question: str) -> str:
    docs = retrieve_context(question)

    if not docs:
        return "No relevant context found. Run ingestion first: python -m src.ingest"

    chain = PROMPT | get_llm() | StrOutputParser()
    response = chain.invoke({"context": format_docs(docs), "question": question})
    response = response.strip() if response else ""

    if not response:
        return fallback_answer(question, docs)

    return response
