#!/usr/bin/env bash
set -euo pipefail

echo "Removing old virtual environment and Chroma database..."
rm -rf .venv chroma_db

echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip setuptools wheel

# Clean incompatible telemetry packages from previous installs.
pip uninstall -y posthog chromadb langchain langchain-community langchain-chroma langchain-ollama || true

pip install -r requirements.txt

echo "Verifying versions..."
python - <<'PY'
import sqlite3
import chromadb
import posthog
print("SQLite:", sqlite3.sqlite_version)
print("ChromaDB:", chromadb.__version__)
print("PostHog:", getattr(posthog, "__version__", "unknown"))
PY

echo "Setup complete. Now run:"
echo "source .venv/bin/activate"
echo "python -m src.ingest"
echo "python -m src.query \"How many work-from-home days are allowed?\""
