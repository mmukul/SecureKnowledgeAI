"""Early runtime patches for Rocky/CentOS + ChromaDB.

This module must be imported before importing chromadb anywhere.
"""
import logging
import os

# Disable/suppress telemetry before ChromaDB/PostHog are imported.
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")
os.environ.setdefault("CHROMA_TELEMETRY_ENABLED", "false")
os.environ.setdefault("POSTHOG_DISABLED", "1")

logging.getLogger("chromadb.telemetry").setLevel(logging.CRITICAL)
logging.getLogger("posthog").setLevel(logging.CRITICAL)

# ChromaDB requires sqlite >= 3.35. Rocky/CentOS Python may link older sqlite.
# pysqlite3-binary provides a modern sqlite build.
try:
    __import__("pysqlite3")
    import sys
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except Exception:
    # If pysqlite3 is not available, normal sqlite3 import will be used.
    # ChromaDB will raise a clear error if the version is still too old.
    pass
