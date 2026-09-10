# Lightweight container for deploying the RAG chatbot to Hugging Face Spaces.
FROM python:3.11-slim

WORKDIR /app

# System deps for sentence-transformers / pypdf
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY frontend ./frontend
COPY data/sample_docs ./data/sample_docs

# Build the vector index at image build time using CPU-only embeddings.
ENV EMBEDDING_PROVIDER=huggingface
ENV LLM_PROVIDER=groq
RUN python3 -m app.rag.ingest

# Hugging Face Spaces expects the app to listen on port 7860.
EXPOSE 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
