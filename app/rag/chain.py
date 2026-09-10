"""Build the retrieval-augmented generation chain: retriever + local LLM."""

from functools import lru_cache

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama

from app import config
from app.rag.ingest import load_vector_store

SYSTEM_PROMPT = """You are a helpful assistant answering questions using only the provided context.
If the answer isn't in the context, say you don't know instead of guessing.
Keep answers concise and cite which part of the context you used when relevant.

Context:
{context}
"""

PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{question}"),
    ]
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


@lru_cache(maxsize=1)
def build_rag_chain():
    """Assemble a retriever -> prompt -> local LLM -> string output chain, cached for reuse."""
    store = load_vector_store()
    retriever = store.as_retriever(search_kwargs={"k": config.RETRIEVAL_K})

    llm = ChatOllama(model=config.CHAT_MODEL, base_url=config.OLLAMA_BASE_URL, temperature=0.2)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | PROMPT
        | llm
        | StrOutputParser()
    )
    return chain, retriever


def answer_question(question: str):
    """Run a single question through the RAG chain and return the answer with sources."""
    chain, retriever = build_rag_chain()
    sources = retriever.invoke(question)
    answer = chain.invoke(question)
    return {
        "answer": answer,
        "sources": [
            {
                "source": doc.metadata.get("source", "unknown"),
                "excerpt": doc.page_content[:200],
            }
            for doc in sources
        ],
    }
