"""Environment diagnostic checks for the RAG repo.

Usage:
    python -m src.doctor
"""

from src import compat  # noqa: F401 - must run before sqlite/chromadb imports

import sqlite3
import sys


def main() -> None:
    print("Python:", sys.version.split()[0])
    print("SQLite used by Python:", sqlite3.sqlite_version)

    try:
        import pysqlite3.dbapi2 as pysqlite_dbapi2  # type: ignore
        print("pysqlite3-binary:", pysqlite_dbapi2.sqlite_version)
    except Exception as exc:
        print("pysqlite3-binary: NOT AVAILABLE", exc)

    try:
        import chromadb
        print("ChromaDB:", chromadb.__version__)
    except Exception as exc:
        print("ChromaDB import failed:", exc)

    try:
        import posthog
        print("PostHog:", getattr(posthog, "__version__", "unknown"))
    except Exception as exc:
        print("PostHog: NOT AVAILABLE", exc)

    if tuple(int(part) for part in sqlite3.sqlite_version.split(".")[:3]) < (3, 35, 0):
        print("\nERROR: SQLite is still below 3.35.0.")
        print("Run: pip install --force-reinstall pysqlite3-binary")
    else:
        print("\nSQLite check passed for ChromaDB.")


if __name__ == "__main__":
    main()
