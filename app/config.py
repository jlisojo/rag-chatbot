"""Central configuration for the RAG chatbot, loaded from environment variables."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Chroma's anonymized telemetry has a known compatibility issue with recent
# posthog versions that spams stderr; disable it since it's not needed here.
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

# Provider switches: "ollama" (default, fully local) or a hosted alternative
# used for the public web demo where Ollama isn't available.
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "ollama")

# Ollama-served models. Both run fully locally, no API keys or cost.
CHAT_MODEL = os.getenv("CHAT_MODEL", "llama3.2:3b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Groq-hosted open-source model, used when LLM_PROVIDER=groq (e.g. the public
# demo deployment, where a local Ollama instance isn't available).
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "qwen/qwen3.6-27b")

# CPU-friendly local embedding model, used when EMBEDDING_PROVIDER=huggingface.
# No API key required; runs anywhere via sentence-transformers.
HF_EMBEDDING_MODEL = os.getenv("HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# Where source documents live and where the vector index is persisted.
DOCS_DIR = Path(os.getenv("DOCS_DIR", BASE_DIR / "data" / "sample_docs"))
CHROMA_DIR = Path(os.getenv("CHROMA_DIR", BASE_DIR / "data" / "chroma_db"))

# Chunking and retrieval tuning.
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))
RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", "2"))
