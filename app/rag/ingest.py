"""Load documents, split them into chunks, and persist embeddings in a local Chroma index."""

import os
from pathlib import Path

# Must be set before chromadb is imported anywhere; disables a noisy telemetry
# call that errors out against recent posthog versions.
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app import config

LOADERS_BY_EXTENSION = {
    ".pdf": PyPDFLoader,
    ".txt": TextLoader,
    ".md": TextLoader,
}


def load_documents(docs_dir: Path):
    """Load every supported file in docs_dir into LangChain Document objects."""
    documents = []
    for path in sorted(docs_dir.rglob("*")):
        if not path.is_file():
            continue
        loader_cls = LOADERS_BY_EXTENSION.get(path.suffix.lower())
        if not loader_cls:
            continue
        documents.extend(loader_cls(str(path)).load())
    return documents


def build_vector_store(docs_dir: Path = config.DOCS_DIR, persist_dir: Path = config.CHROMA_DIR):
    """Ingest documents and (re)build the persisted Chroma vector store."""
    documents = load_documents(docs_dir)
    if not documents:
        raise ValueError(f"No supported documents found in {docs_dir}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)

    embeddings = OllamaEmbeddings(model=config.EMBEDDING_MODEL, base_url=config.OLLAMA_BASE_URL)

    persist_dir.mkdir(parents=True, exist_ok=True)
    store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(persist_dir),
    )
    return store, len(documents), len(chunks)


def load_vector_store(persist_dir: Path = config.CHROMA_DIR):
    """Load an already-built Chroma vector store without re-ingesting documents."""
    embeddings = OllamaEmbeddings(model=config.EMBEDDING_MODEL, base_url=config.OLLAMA_BASE_URL)
    return Chroma(persist_directory=str(persist_dir), embedding_function=embeddings)


if __name__ == "__main__":
    vector_store, doc_count, chunk_count = build_vector_store()
    print(f"Ingested {doc_count} document(s) into {chunk_count} chunk(s).")
    print(f"Vector store persisted at: {config.CHROMA_DIR}")
