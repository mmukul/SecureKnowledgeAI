"""Early runtime compatibility fixes for ChromaDB.

This module MUST be imported before importing `chromadb`, `langchain_chroma`,
or any code that imports ChromaDB.

Fixes:
- CentOS/Rocky/RHEL old sqlite3 issue by replacing stdlib sqlite3 with
  pysqlite3-binary's newer SQLite build.
- Chroma/PostHog telemetry warning suppression.
"""

from __future__ import annotations

import logging
import os
import sys


def disable_telemetry() -> None:
    """Disable ChromaDB/PostHog telemetry as early as possible."""
    os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")
    os.environ.setdefault("CHROMA_TELEMETRY_ENABLED", "false")
    os.environ.setdefault("POSTHOG_DISABLED", "1")
    os.environ.setdefault(
        "CHROMA_PRODUCT_TELEMETRY_IMPL",
        "chromadb.telemetry.product.noop.NoopProductTelemetryClient",
    )

    class _DropTelemetryErrors(logging.Filter):
        def filter(self, record: logging.LogRecord) -> bool:
            msg = record.getMessage()
            return not (
                "Failed to send telemetry event" in msg
                or "capture() takes 1 positional argument" in msg
            )

    for name in (
        "chromadb.telemetry.product.posthog",
        "chromadb.telemetry.product",
        "chromadb",
        "posthog",
    ):
        logger = logging.getLogger(name)
        logger.addFilter(_DropTelemetryErrors())
        logger.setLevel(logging.CRITICAL)


def apply_sqlite_fix() -> None:
    """Force Python to use pysqlite3-binary for ChromaDB.

    This is stronger than `sys.modules.pop('pysqlite3')` because it maps the
    DB-API module directly to `sqlite3` and `sqlite3.dbapi2`.
    """
    try:
        import pysqlite3.dbapi2 as pysqlite_dbapi2  # type: ignore

        sys.modules["sqlite3"] = pysqlite_dbapi2
        sys.modules["sqlite3.dbapi2"] = pysqlite_dbapi2
    except Exception:
        # ChromaDB will raise its standard SQLite error if the package is absent.
        pass


def patch_posthog() -> None:
    """Best-effort no-op PostHog patch for noisy telemetry versions."""
    def _noop(*args, **kwargs):
        return None

    try:
        import posthog  # type: ignore

        posthog.capture = _noop
        posthog.identify = _noop
        posthog.alias = _noop
        posthog.flush = _noop

        if hasattr(posthog, "Client"):
            posthog.Client.capture = _noop
            posthog.Client.identify = _noop
            posthog.Client.alias = _noop
            posthog.Client.flush = _noop
    except Exception:
        pass


disable_telemetry()
apply_sqlite_fix()
patch_posthog()
