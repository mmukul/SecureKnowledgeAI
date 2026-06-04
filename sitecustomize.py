"""Auto-loaded startup fixes when Python is run from the repo root.

Keep this file in the project root. Python imports `sitecustomize` during
startup, which lets us apply the SQLite fix before ChromaDB is ever imported.
"""

try:
    from src.compat import apply_sqlite_fix, disable_telemetry, patch_posthog

    disable_telemetry()
    apply_sqlite_fix()
    patch_posthog()
except Exception:
    pass
