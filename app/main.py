"""FastAPI app exposing the RAG chatbot as a small HTTP API."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app import config
from app.rag.chain import answer_question, build_rag_chain
from app.rag.ingest import build_vector_store

app = FastAPI(title="RAG Chatbot", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str


class IngestResponse(BaseModel):
    documents_ingested: int
    chunks_created: int


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "llm_provider": config.LLM_PROVIDER,
        "embedding_provider": config.EMBEDDING_PROVIDER,
        "chat_model": config.GROQ_MODEL if config.LLM_PROVIDER == "groq" else config.CHAT_MODEL,
        "embedding_model": config.HF_EMBEDDING_MODEL if config.EMBEDDING_PROVIDER == "huggingface" else config.EMBEDDING_MODEL,
    }


@app.post("/api/ingest", response_model=IngestResponse)
def ingest():
    """Rebuild the vector store from the documents in data/sample_docs."""
    try:
        _, doc_count, chunk_count = build_vector_store()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    build_rag_chain.cache_clear()
    return IngestResponse(documents_ingested=doc_count, chunks_created=chunk_count)


@app.post("/api/chat")
def chat(request: ChatRequest):
    """Answer a question using retrieval-augmented generation over the ingested documents."""
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="question must not be empty")

    try:
        return answer_question(request.question)
    except Exception as exc:  # noqa: BLE001 - surface ingestion/connection issues to the caller
        raise HTTPException(status_code=503, detail=f"RAG chain unavailable: {exc}") from exc


app.mount("/", StaticFiles(directory=str(config.BASE_DIR / "frontend"), html=True), name="frontend")
