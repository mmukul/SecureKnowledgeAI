
## Important: Fix ChromaDB Telemetry Warning

If you still see this warning:

```text
Failed to send telemetry event ClientStartEvent: capture() takes 1 positional argument but 3 were given
```

It usually means your existing virtual environment still has a conflicting `posthog` package. Recreate the environment fully:

```bash
chmod +x reset-env-rocky-centos.sh
./reset-env-rocky-centos.sh
```

Then run:

```bash
source .venv/bin/activate
python -m src.ingest
python -m src.query "What is the AI usage policy?"
```

This repo also hard-disables Chroma/PostHog telemetry in `sitecustomize.py` and `src/compat.py`.

# RAG with ChromaDB + Ollama

A simple local Retrieval-Augmented Generation demo using:

- **Ollama** for local LLM and embeddings
- **ChromaDB** as the vector database
- **LangChain** for document loading, chunking, retrieval, and RAG orchestration

## Architecture

```text
Documents → Chunking → Ollama Embeddings → ChromaDB
                                            ↓
User Question → Retriever → Relevant Chunks → Ollama LLM → Answer
```

## Prerequisites

Install Ollama and pull the required models:

```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

Start Ollama:

```bash
ollama serve
```


## CentOS / Rocky Linux Setup

CentOS, Rocky Linux, and some RHEL-based systems may ship an older SQLite version. ChromaDB requires SQLite `3.35.0` or higher. This repo includes a compatibility fix using `pysqlite3-binary`.

Install system dependencies:

```bash
sudo dnf update -y
sudo dnf install -y python3 python3-pip python3-devel gcc gcc-c++ make sqlite sqlite-devel
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Verify the SQLite version used by Python:

```bash
python -c "import sqlite3; print(sqlite3.sqlite_version)"
```

If your system SQLite is old, the project automatically applies this fix before ChromaDB loads:

```python
from src import sqlite_fix  # must run before ChromaDB imports
```

The fix is implemented in `src/sqlite_fix.py` and requires:

```bash
pip install pysqlite3-binary
```

## ChromaDB SQLite Troubleshooting

If you see this error:

```text
Your system has an unsupported version of sqlite3. Chroma requires sqlite3 >= 3.35.0
```

Make sure `pysqlite3-binary` is installed:

```bash
pip install pysqlite3-binary
```

Then confirm `src/rag.py` imports the SQLite fix before importing ChromaDB:

```python
from src import sqlite_fix  # noqa: F401 - must run before ChromaDB imports
```

After that, run ingestion again:

```bash
python -m src.ingest
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## Add documents

Put your `.txt`, `.md`, or `.pdf` files inside the `data/` folder.

A sample document is already included.

## Ingest documents into ChromaDB

```bash
python -m src.ingest
```

## Ask questions

```bash
python -m src.query "What is this project about?"
```

Interactive mode:

```bash
python -m src.query
```

## Configuration

Edit `.env` to change model names, paths, chunk size, and retrieval settings.

Default values:

```env
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=llama3.2:3b
EMBEDDING_MODEL=nomic-embed-text
CHROMA_DB_DIR=./chroma_db
DATA_DIR=./data
COLLECTION_NAME=rag_demo
CHUNK_SIZE=800
CHUNK_OVERLAP=120
TOP_K=4
```

## Repository structure

```text
rag-chromadb-ollama/
├── data/
│   └── sample.txt
├── sitecustomize.py
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── ingest.py
│   ├── query.py
│   ├── rag.py
│   └── sqlite_fix.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Notes

- This project runs fully locally after models are downloaded.
- ChromaDB data is stored in `./chroma_db` and ignored by Git.
- For production, add authentication, logging, evaluation, document deduplication, and access controls.

## Sample Policy Questions

After ingesting `data/sample.txt`, try asking:

```bash
python src/query.py "How many work-from-home days are allowed?"
python src/query.py "What is the leave carry-forward policy?"
python src/query.py "When must security incidents be reported?"
python src/query.py "Can employees upload customer PII to public AI systems?"
python src/query.py "What are the DevSecOps requirements before deployment?"
python src/query.py "How quickly must High vulnerabilities be fixed?"
python src/query.py "What training is required for new employees?"
python src/query.py "What is the cloud security policy for public storage buckets?"
python src/query.py "What checks are required in the secure SDLC?"
python src/query.py "What is the policy for source code repository branch protection?"
```

## Fix: ChromaDB Telemetry Warning

If you see this warning:

```text
Failed to send telemetry event ClientStartEvent: capture() takes 1 positional argument but 3 were given
```

It is usually caused by a telemetry dependency conflict, commonly with `posthog` or OpenTelemetry packages. The application disables ChromaDB telemetry by default using:

```python
from chromadb.config import Settings as ChromaSettings

client_settings=ChromaSettings(anonymized_telemetry=False)
```

The repo also sets these environment variables in `.env.example`:

```bash
ANONYMIZED_TELEMETRY=False
CHROMA_TELEMETRY_ENABLED=false
```

If the warning still appears, it is normally due to a `posthog` API mismatch. This repo applies a stronger fix in `sitecustomize.py`, which Python loads automatically from the project root before ChromaDB starts. It disables telemetry early and suppresses the known non-fatal PostHog telemetry error.

Recreate the virtual environment so the pinned dependency is applied:

```bash
rm -rf .venv venv chroma_db
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m src.ingest
```

Confirm the pinned PostHog version:

```bash
pip show posthog
```

The repo pins:

```txt
posthog<4.0.0
```

Do not run the scripts from inside the `src/` directory. Run them from the project root so `sitecustomize.py` loads automatically.

---

## Latest Fix: ChromaDB Telemetry Warning

If you still see this warning:

```text
Failed to send telemetry event ClientStartEvent: capture() takes 1 positional argument but 3 were given
```

Use the included reset script. It pins `posthog==2.5.0`, disables telemetry before ChromaDB imports, and rebuilds the virtual environment cleanly.

```bash
chmod +x reset-env-rocky-centos.sh
./reset-env-rocky-centos.sh
```

Then run:

```bash
source .venv/bin/activate
python -m src.ingest
python -m src.query "How many work-from-home days are allowed?"
```

Expected response:

```text
Employees may work remotely up to 3 days per week with manager approval.
```

### Why this fix works

Some ChromaDB and PostHog version combinations cause a telemetry method signature mismatch. This repo fixes it by:

- Pinning `posthog==2.5.0`
- Disabling telemetry with environment variables before ChromaDB imports
- Adding `sitecustomize.py` for early startup configuration
- Adding `src/compat.py` as a fallback compatibility layer
- Passing `Settings(anonymized_telemetry=False)` to ChromaDB

## Sample Query File

Sample demo questions are available here:

```text
samples/queries.txt
```

Example:

```bash
python -m src.query "How many work-from-home days are allowed?"
```

## Fix: Query Command Generates No Output

If this command prints nothing:

```bash
python -m src.query "How many work-from-home days are allowed?"
```

Use the debug mode:

```bash
python -m src.query --debug "How many work-from-home days are allowed?"
```

Expected answer:

```text
Employees may work remotely up to 3 days per week with manager approval.
```

If ChromaDB is empty, run:

```bash
python -m src.ingest
```

If Ollama is not running, start it and pull the required models:

```bash
ollama serve
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```
