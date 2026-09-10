# RAG Chatbot (Local, Open-Source LLMs)

A retrieval-augmented generation (RAG) chatbot that answers questions about a
document set using **fully open-source, locally-run models** via
[Ollama](https://ollama.com/) — no API keys, no per-request cost, no data
leaving your machine.

## Why this project

Most RAG demos rely on a paid hosted API (OpenAI, Anthropic, etc.). This one
runs the entire pipeline — embeddings, vector search, and generation — on
open-source models on a local machine, which matters for privacy-sensitive
use cases (internal docs, legal, healthcare) and for cost control at scale.

## Stack

- **LLM & embeddings**: [Ollama](https://ollama.com/) serving `llama3.2:3b` (chat) and `nomic-embed-text` (embeddings)
- **Orchestration**: [LangChain](https://python.langchain.com/) (retriever → prompt → LLM chain)
- **Vector store**: [Chroma](https://www.trychroma.com/) (local, persisted to disk, no external service)
- **API**: [FastAPI](https://fastapi.tiangolo.com/)
- **Frontend**: a single dependency-free HTML/CSS/JS chat page served by FastAPI

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for a diagram and design
notes on chunking, retrieval, and prompt design.

## Requirements

- Python 3.11+
- [Ollama](https://ollama.com/download) installed and running locally

## Setup

```bash
# 1. Install Ollama models (one-time)
ollama pull llama3.2:3b
ollama pull nomic-embed-text

# 2. Create a virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Add your documents (PDF, .md, or .txt) to data/sample_docs/,
#    or use the included sample document.

# 4. Build the vector index
python3 -m app.rag.ingest

# 5. Run the API + chat UI
uvicorn app.main:app --reload
```

Then open **http://localhost:8000** in your browser to chat with your
documents.

## API

| Endpoint | Method | Description |
|---|---|---|
| `/api/health` | GET | Reports status and which models are configured |
| `/api/ingest` | POST | Rebuilds the vector index from `data/sample_docs/` |
| `/api/chat` | POST | `{ "question": "..." }` → `{ "answer": "...", "sources": [...] }` |

## Project layout

```
app/
  main.py          FastAPI app and routes
  config.py        Environment-driven configuration
  rag/
    ingest.py      Document loading, chunking, and vector store creation
    chain.py       Retriever + prompt + LLM chain
frontend/
  index.html       Minimal chat UI (no framework, no build step)
data/
  sample_docs/     Documents to ingest
tests/
  test_ingest.py   Ingestion pipeline tests (no LLM calls, fast/CI-friendly)
```

## Notes on design decisions

- **Chroma over a hosted vector DB**: keeps the whole stack local and free,
  appropriate for a demo and for small-to-medium document sets.
- **`lru_cache` on the chain builder**: avoids reconnecting to Ollama and
  reloading the vector store on every request.
- **Explicit "I don't know" instruction in the system prompt**: reduces
  hallucination when the retrieved context doesn't contain the answer.

## License

MIT
