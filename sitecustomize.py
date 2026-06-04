"""Startup fixes loaded automatically when running Python from repo root.

This file is intentionally duplicated with src/compat.py so the fixes run as
early as possible, before ChromaDB imports.
"""
from __future__ import annotations

import logging
import os
import sys

os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"
os.environ["POSTHOG_DISABLED"] = "1"
os.environ["CHROMA_PRODUCT_TELEMETRY_IMPL"] = "chromadb.telemetry.product.noop.NoopProductTelemetryClient"

try:
    __import__("pysqlite3")
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except Exception:
    pass


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


class _DropTelemetryErrors(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        return not (
            "Failed to send telemetry event" in msg
            or "capture() takes 1 positional argument" in msg
        )


for name in ("chromadb.telemetry.product.posthog", "chromadb.telemetry.product", "chromadb", "posthog"):
    lg = logging.getLogger(name)
    lg.addFilter(_DropTelemetryErrors())
    lg.setLevel(logging.CRITICAL)
    lg.disabled = True
