"""Compatibility fixes for ChromaDB on CentOS/Rocky/RHEL lab systems.

Import this before importing chromadb or langchain_chroma.

Fixes included:
1. Old system sqlite3 used by Python on CentOS/Rocky/RHEL.
2. ChromaDB/PostHog telemetry warning:
   Failed to send telemetry event ClientStartEvent: capture() takes 1 positional argument but 3 were given

The most reliable fix for the telemetry warning is requirements.txt pinning:
    posthog==2.5.0
This file also disables telemetry and suppresses the warning as a fallback.
"""

from __future__ import annotations

import logging
import os
import sys

# Disable Chroma/PostHog telemetry before ChromaDB is imported.
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"
os.environ["POSTHOG_DISABLED"] = "1"
os.environ["CHROMA_PRODUCT_TELEMETRY_IMPL"] = "chromadb.telemetry.product.noop.NoopProductTelemetryClient"

# Fix old SQLite on CentOS/Rocky/RHEL by forcing pysqlite3-binary.
try:
    __import__("pysqlite3")
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except Exception:
    pass


def _noop(*args, **kwargs):
    return None


# Fallback: hard-disable PostHog functions/classes if present.
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


class _DropTelemetryErrors(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        blocked = (
            "Failed to send telemetry event" in message
            or "capture() takes 1 positional argument" in message
        )
        return not blocked


for logger_name in (
    "chromadb.telemetry.product.posthog",
    "chromadb.telemetry.product",
    "chromadb",
    "posthog",
):
    logger = logging.getLogger(logger_name)
    logger.addFilter(_DropTelemetryErrors())
    logger.setLevel(logging.CRITICAL)
    logger.disabled = True
