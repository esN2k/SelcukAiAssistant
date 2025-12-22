"""Ollama provider implementation."""
from __future__ import annotations

import logging
from typing import AsyncIterator, Dict, List

from config import Config
from ollama_service import OllamaService
from providers.base import CancellationToken, ChatResult, ModelProvider, StreamChunk, Usage
from utils import ReasoningFilter

logger = logging.getLogger(__name__)


class OllamaProvider(ModelProvider):
    name = "ollama"

    def __init__(self) -> None:
        self._client = OllamaService(
            base_url=Config.OLLAMA_BASE_URL,
            timeout=Config.OLLAMA_TIMEOUT,
            max_retries=Config.OLLAMA_MAX_RETRIES,
            retry_delay=Config.OLLAMA_RETRY_DELAY,
        )

    async def generate(
        self,
        messages: List[Dict[str, str]],
        model_id: str,
        temperature: float,
        top_p: float,
        max_tokens: int,
        request_id: str,
    ) -> ChatResult:
        logger.info("request_id=%s provider=ollama generate model=%s", request_id, model_id)
        result = await self._client.generate(
            messages=messages,
            model=model_id,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
        )
        usage_raw = result.get("usage") or {}
        usage = Usage(
            prompt_tokens=usage_raw.get("prompt_tokens"),
            completion_tokens=usage_raw.get("completion_tokens"),
        )
        if usage.prompt_tokens is not None and usage.completion_tokens is not None:
            usage.total_tokens = usage.prompt_tokens + usage.completion_tokens
        return ChatResult(text=result["text"], usage=usage)

    async def stream(
        self,
        messages: List[Dict[str, str]],
        model_id: str,
        temperature: float,
        top_p: float,
        max_tokens: int,
        request_id: str,
        cancel_token: CancellationToken,
    ) -> AsyncIterator[StreamChunk]:
        logger.info("request_id=%s provider=ollama stream model=%s", request_id, model_id)
        reasoning_filter = ReasoningFilter()
        async for chunk in self._client.generate_stream(
            messages=messages,
            model=model_id,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
        ):
            if cancel_token.is_cancelled():
                logger.info("request_id=%s stream cancelled", request_id)
                break

            token = chunk.get("token") or ""
            if token:
                token = reasoning_filter.feed(token)
                if token:
                    yield StreamChunk(token=token)

            if chunk.get("done"):
                usage_raw = chunk.get("usage") or {}
                usage = Usage(
                    prompt_tokens=usage_raw.get("prompt_tokens"),
                    completion_tokens=usage_raw.get("completion_tokens"),
                )
                if usage.prompt_tokens is not None and usage.completion_tokens is not None:
                    usage.total_tokens = usage.prompt_tokens + usage.completion_tokens
                yield StreamChunk(token="", done=True, usage=usage)
                break

    def list_models(self) -> list:
        return []

    async def list_model_names(self) -> List[str]:
        return await self._client.list_model_names()

    async def health_check(self, model_id: str) -> Dict[str, object]:
        return await self._client.health_check(model_id)
