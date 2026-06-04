#!/usr/bin/env bash
set -euo pipefail

sudo dnf update -y
sudo dnf install -y python3 python3-pip python3-devel gcc gcc-c++ make sqlite sqlite-devel

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

python - <<'PY'
import os
print("ANONYMIZED_TELEMETRY=", os.getenv("ANONYMIZED_TELEMETRY"))
print("sitecustomize loaded successfully if no import error occurred")
PY

python - <<'PY'
import sqlite3
print(f"Python SQLite version: {sqlite3.sqlite_version}")
PY

echo "Setup complete. Start Ollama and run: python -m src.ingest"
