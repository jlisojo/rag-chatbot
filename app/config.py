"""Central configuration for the RAG chatbot, loaded from environment variables."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Chroma's anonymized telemetry has a known compatibility issue with recent
# posthog versions that spams stderr; disable it since it's not needed here.
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

BASE_DIR = Path(__file__).resolve().parent.parent

# Ollama-served models. Both run fully locally, no API keys or cost.
CHAT_MODEL = os.getenv("CHAT_MODEL", "llama3.2:3b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Where source documents live and where the vector index is persisted.
DOCS_DIR = Path(os.getenv("DOCS_DIR", BASE_DIR / "data" / "sample_docs"))
CHROMA_DIR = Path(os.getenv("CHROMA_DIR", BASE_DIR / "data" / "chroma_db"))

# Chunking and retrieval tuning.
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))
RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", "4"))
