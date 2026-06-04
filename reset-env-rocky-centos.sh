#!/usr/bin/env bash
set -e

rm -rf .venv chroma_db
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Python version:"
python --version

echo "SQLite version used by Python after patch:"
python -c "from src import bootstrap; import sqlite3; print(sqlite3.sqlite_version)"

echo "Setup completed."
echo "Run: python -m src.ingest"
echo "Run: python -m src.query --debug 'How many work-from-home days are allowed?'"
