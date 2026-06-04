# SecureKnowledgeAI

Enterprise AI knowledge assistant using Ollama, ChromaDB, and Retrieval-Augmented Generation (RAG).

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Install/pull Ollama models:

```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

## Run

```bash
python -m src.ingest
python -m src.query --debug "How many work-from-home days are allowed?"
```

Expected answer:

```text
Employees may work remotely up to 3 days per week with manager approval.
```

## Rocky Linux / CentOS

Use:

```bash
chmod +x reset-env-rocky-centos.sh
./reset-env-rocky-centos.sh
```

## Fixes Included

- SQLite fix using `pysqlite3-binary`
- ChromaDB telemetry suppression
- `posthog==3.7.0`
- Clean `config.py` with all required variables
- Fixed `NameError: answer is not defined`
- Sample policy data and sample queries

## Sample Queries

See `samples/queries.txt`.
