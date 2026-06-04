from src import bootstrap  # noqa: F401 - must run before chromadb import

import argparse
from src.rag import answer_question


def main():
    parser = argparse.ArgumentParser(description="Ask questions over company policies using RAG.")
    parser.add_argument("question", nargs="+", help="Question to ask")
    parser.add_argument("--debug", action="store_true", help="Show retrieved chunks")
    args = parser.parse_args()

    question = " ".join(args.question)
    try:
        answer = answer_question(question, debug=args.debug)
        print("\nAnswer:")
        print(answer)
    except Exception as exc:
        print(f"Error while running query: {exc}")
        raise


if __name__ == "__main__":
    main()
