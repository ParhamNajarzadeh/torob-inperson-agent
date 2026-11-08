"""Self-contained LLM Gateway for deepseek-v4.1-flash via MetisAI Wrapper with 5m Token Caching."""
import os
from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI


def get_deepseek_llm(
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    enable_cache: bool = True
) -> ChatOpenAI:
    """
    Returns a configured ChatOpenAI instance pointing to MetisAI DeepSeek wrapper
    (https://docs.metisai.ir/api/wrapper/deepseek) with 5-minute token caching enabled.
    Zero hardcoded keys: reads strictly from environment variables.
    """
    api_key = os.getenv("METIS_API_KEY", "")
    base_url = os.getenv("METIS_BASE_URL", "https://api.metisai.ir/deepseek/v1")
    model_name = os.getenv("LLM_MODEL_NAME", "deepseek-v4.1-flash")
    temp = temperature if temperature is not None else float(os.getenv("LLM_TEMPERATURE", "0.1"))
    tokens = max_tokens if max_tokens is not None else int(os.getenv("LLM_MAX_TOKENS", "1500"))
    cache_ttl = os.getenv("LLM_CACHE_TTL", "5m")

    extra_body: Dict[str, Any] = {}
    if enable_cache:
        extra_body["cache"] = {"ttl": cache_ttl}

    return ChatOpenAI(
        model=model_name,
        api_key=api_key,
        base_url=base_url,
        temperature=temp,
        max_tokens=tokens,
        extra_body=extra_body
    )
