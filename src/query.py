import argparse

from src import bootstrap  # noqa: F401 must run before chromadb import
from src.rag import ask


def main():
    parser = argparse.ArgumentParser(description="Ask questions from indexed company policies.")
    parser.add_argument("question", nargs="+", help="Question to ask")
    parser.add_argument("--debug", action="store_true", help="Print retrieved chunks")
    args = parser.parse_args()

    question = " ".join(args.question).strip()
    if not question:
        print("Please provide a question.")
        return

    try:
        answer = ask(question, debug=args.debug)
        print("\nAnswer:")
        print(answer)
    except Exception as exc:
        print(f"Error while running query: {exc}")
        raise


if __name__ == "__main__":
    main()
