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

## Providers

By default everything runs locally through Ollama. Two environment variables
switch to hosted/CPU-only alternatives, used for the public demo deployment
where Ollama isn't available:

| Variable | `ollama` (default) | Alternative |
|---|---|---|
| `LLM_PROVIDER` | `ChatOllama` (`llama3.2:3b`) | `groq` → `ChatGroq`, a free hosted API serving open-weight models (requires `GROQ_API_KEY`) |
| `EMBEDDING_PROVIDER` | `OllamaEmbeddings` (`nomic-embed-text`) | `huggingface` → `HuggingFaceEmbeddings` (`all-MiniLM-L6-v2`), runs on CPU, no API key |

See `.env.example` for the full list of provider-related variables.

## Deploying a public demo (Hugging Face Spaces)

Ollama can't run in a visitor's browser, so the public demo instead runs the
same codebase in a small Docker container with Groq (LLM) and a local
CPU embedding model, both free.

1. Create a free account at [huggingface.co](https://huggingface.co) and a
   new **Space** → SDK: **Docker** → visibility: **Public**.
2. In the Space's **Settings → Repository secrets**, add `GROQ_API_KEY` with
   your key from [console.groq.com](https://console.groq.com). Never commit
   this key to git.
3. Add the Space as a second git remote and push this repo to it:
   ```bash
   git remote add space https://huggingface.co/spaces/<your-username>/rag-chatbot
   git push space main
   ```
4. The included `Dockerfile` installs dependencies, builds the vector index
   at build time using CPU embeddings, and serves the FastAPI app (chat UI
   included) on port `7860`, which is what Spaces expects.
5. Once built, the Space URL is a real public chat demo that can be linked or
   embedded via iframe.

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
- **Provider factory (`app/rag/providers.py`)**: isolates the Ollama vs.
  Groq/HuggingFace choice behind two functions, so the ingestion and chain
  code never need to know which provider is active.

## License

MIT
