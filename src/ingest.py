try:
    __import__("pysqlite3")
    import sys
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except Exception as e:
    print(f"SQLite patch failed: {e}")

import chromadb

from src.rag import get_vectorstore, load_documents, split_documents


def main() -> None:
    print("Loading documents...")
    documents = load_documents()

    if not documents:
        print("No documents found. Add .txt, .md, or .pdf files to the data directory.")
        return

    print(f"Loaded {len(documents)} document(s). Splitting into chunks...")
    chunks = split_documents(documents)

    print(f"Created {len(chunks)} chunk(s). Saving to ChromaDB...")
    vectorstore = get_vectorstore()
    vectorstore.add_documents(chunks)

    print("Ingestion complete.")


if __name__ == "__main__":
    main()
