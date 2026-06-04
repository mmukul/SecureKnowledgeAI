#!/usr/bin/env bash
set -euo pipefail

echo "Removing old virtual environment and Chroma database..."
rm -rf .venv chroma_db

echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip setuptools wheel

pip uninstall -y posthog chromadb langchain langchain-community langchain-chroma langchain-ollama pysqlite3-binary || true
pip install --no-cache-dir -r requirements.txt

echo "Running environment doctor..."
python -m src.doctor

echo ""
echo "Setup complete. Now run:"
echo "source .venv/bin/activate"
echo "python -m src.ingest"
echo "python -m src.query --debug \"How many work-from-home days are allowed?\""
