"""Provider factories: swap between local Ollama and hosted alternatives via config."""

from app import config


def get_embeddings():
    """Return an embeddings client based on EMBEDDING_PROVIDER."""
    if config.EMBEDDING_PROVIDER == "huggingface":
        from langchain_huggingface import HuggingFaceEmbeddings

        return HuggingFaceEmbeddings(model_name=config.HF_EMBEDDING_MODEL)

    from langchain_ollama import OllamaEmbeddings

    return OllamaEmbeddings(model=config.EMBEDDING_MODEL, base_url=config.OLLAMA_BASE_URL)


def get_llm():
    """Return a chat model based on LLM_PROVIDER."""
    if config.LLM_PROVIDER == "groq":
        from langchain_groq import ChatGroq

        if not config.GROQ_API_KEY:
            raise RuntimeError("LLM_PROVIDER=groq requires GROQ_API_KEY to be set")
        return ChatGroq(
            model=config.GROQ_MODEL,
            api_key=config.GROQ_API_KEY,
            temperature=0.2,
            max_tokens=950,
            model_kwargs={"reasoning_format": "hidden", "reasoning_effort": "none"},
        )

    from langchain_ollama import ChatOllama

    return ChatOllama(model=config.CHAT_MODEL, base_url=config.OLLAMA_BASE_URL, temperature=0.2)
