"""Basic tests for the document loading and chunking pipeline (no LLM calls)."""

from pathlib import Path

from app.rag.ingest import load_documents

SAMPLE_DOCS_DIR = Path(__file__).resolve().parent.parent / "data" / "sample_docs"


def test_load_documents_finds_sample_file():
    documents = load_documents(SAMPLE_DOCS_DIR)
    assert len(documents) > 0


def test_loaded_documents_have_content():
    documents = load_documents(SAMPLE_DOCS_DIR)
    assert any("Simple Events" in doc.page_content for doc in documents)
