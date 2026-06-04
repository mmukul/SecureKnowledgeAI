# SecureKnowledgeAI

Enterprise AI knowledge assistant built with ChromaDB, Ollama, and Retrieval-Augmented Generation (RAG) to provide secure, context-aware answers from organizational policies, security standards, and technical documentation.

## Models

Recommended local models:

```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

## Setup on Rocky Linux / CentOS

```bash
chmod +x reset-env-rocky-centos.sh
./reset-env-rocky-centos.sh
```

## Ingest Documents

```bash
source .venv/bin/activate
python -m src.ingest
```

## Ask a Question

```bash
python -m src.query --debug "How many work-from-home days are allowed?"
```

Expected answer:

```text
Employees may work remotely up to 3 days per week with manager approval.
```

## Sample Queries

See:

```text
samples/queries.txt
```

## SQLite Fix

ChromaDB requires SQLite 3.35.0 or higher. Rocky Linux and CentOS may ship older SQLite versions.

This repo uses `pysqlite3-binary` and patches SQLite before importing ChromaDB in `src/bootstrap.py`.

Verify:

```bash
python -c "from src import bootstrap; import sqlite3; print(sqlite3.sqlite_version)"
```

## Telemetry Fix

This repo avoids the invalid setting:

```text
chromadb.telemetry.product.noop
```

Do not use it. It can cause:

```text
No module named 'chromadb.telemetry.product.noop'
```

Telemetry is disabled using supported environment variables and Chroma settings:

```python
Settings(anonymized_telemetry=False)
```

Environment variables:

```bash
ANONYMIZED_TELEMETRY=False
CHROMA_TELEMETRY_ENABLED=false
POSTHOG_DISABLED=1
```

## Repository Description

Enterprise AI knowledge assistant powered by Retrieval-Augmented Generation (RAG), ChromaDB, and Ollama. Enables secure semantic search and context-aware question answering across organizational policies, security standards, and technical documentation.
