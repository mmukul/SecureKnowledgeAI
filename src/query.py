"""Command line query interface for the RAG assistant.

Usage:
    python -m src.query "How many work-from-home days are allowed?"
    python -m src.query --debug "How many work-from-home days are allowed?"
"""

try:
    __import__("pysqlite3")
    import sys
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except Exception as e:
    print(f"SQLite patch failed: {e}")

import chromadb

import argparse
import sys

from src.rag import answer_question, get_index_count, retrieve_context


def interactive_mode(debug: bool = False) -> None:
    print("RAG assistant ready. Type 'exit' to quit.")
    while True:
        question = input("\nQuestion: ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        if not question:
            continue
        run_query(question, debug=debug)


def run_query(question: str, debug: bool = False) -> None:
    try:
        count = get_index_count()
        if count == 0:
            print("No documents found in ChromaDB index.")
            print("Run this first: python -m src.ingest")
            return

        if debug:
            print(f"Indexed chunks: {count}")
            docs = retrieve_context(question)
            print("\nRetrieved chunks:")
            for index, doc in enumerate(docs, start=1):
                source = doc.metadata.get("source", "unknown")
                preview = doc.page_content.replace("\n", " ")[:500]
                print(f"\n--- Chunk {index} | {source} ---")
                print(preview)

        answer = answer_question(question).strip()
        if not answer:
            print("No answer generated. Try running with --debug to verify retrieved chunks.")
            return

        print(answer)

    except Exception as exc:
        print(f"Error while running query: {exc}", file=sys.stderr)
        print("\nChecklist:", file=sys.stderr)
        print("1. Start Ollama: ollama serve", file=sys.stderr)
        print("2. Pull models: ollama pull llama3.2:3b && ollama pull nomic-embed-text", file=sys.stderr)
        print("3. Ingest docs: python -m src.ingest", file=sys.stderr)
        raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask questions against your ChromaDB RAG index.")
    parser.add_argument("question", nargs="*", help="Question to ask")
    parser.add_argument("--debug", action="store_true", help="Show indexed count and retrieved chunks")
    args = parser.parse_args()

    if args.question:
        question = " ".join(args.question).strip()
        run_query(question, debug=args.debug)
    else:
        interactive_mode(debug=args.debug)


if __name__ == "__main__":
    main()
