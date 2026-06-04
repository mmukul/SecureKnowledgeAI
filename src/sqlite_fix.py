"""
Compatibility fix for ChromaDB on Linux distributions that ship an older
SQLite library, such as CentOS, Rocky Linux, and some RHEL-based systems.

ChromaDB requires sqlite3 >= 3.35.0. The pysqlite3-binary package bundles a
newer SQLite build and can be used as a drop-in replacement for Python's
standard sqlite3 module.

This module must be imported before importing chromadb or langchain_chroma.
"""

from __future__ import annotations

import sys


def apply_sqlite_fix() -> None:
    """Use pysqlite3 as sqlite3 when available."""
    try:
        __import__("pysqlite3")
        sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
    except ImportError:
        # If pysqlite3-binary is not installed, Python's default sqlite3 will be used.
        # ChromaDB will raise a clear error if the system SQLite version is too old.
        pass


apply_sqlite_fix()
