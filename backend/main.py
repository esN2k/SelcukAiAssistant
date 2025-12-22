"""FastAPI backend for SelcukAiAssistant with streaming and model routing."""
from __future__ import annotations

import asyncio
import logging
import time
import uuid
from typing import Any, Dict, Optional

import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from config import Config
from providers.base import CancellationToken, ModelProvider, Usage
from providers.huggingface_provider import HuggingFaceProvider
from providers.ollama_provider import OllamaProvider
from providers.registry import ModelRegistry
from response_cleaner import StreamingResponseCleaner, clean_text
from schemas import ChatRequest, ChatResponse, UsageInfo
from utils import (
    clamp_max_tokens,
    normalize_messages,
    pick_language,
    sse_event,
    trim_messages_for_context,
)

logger = logging.getLogger(__name__)

app = FastAPI(title="SelcukAiAssistant Backend")

allowed_origins = [origin.strip() for origin in Config.ALLOWED_ORIGINS if origin.strip()]
if not allowed_origins:
    allowed_origins = ["*"]
allow_all_origins = "*" in allowed_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=not allow_all_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

ollama_provider = OllamaProvider()
huggingface_provider = HuggingFaceProvider()

providers: dict[str, ModelProvider] = {
    "ollama": ollama_provider,
    "huggingface": huggingface_provider,
}
model_registry = ModelRegistry(providers)

appwrite_client: Optional[requests.Session] = None
if Config.APPWRITE_ENDPOINT and Config.APPWRITE_PROJECT_ID and Config.APPWRITE_API_KEY:
    appwrite_client = requests.Session()
    appwrite_client.headers.update(
        {
            "X-Appwrite-Project": Config.APPWRITE_PROJECT_ID,
            "X-Appwrite-Key": Config.APPWRITE_API_KEY,
            "Content-Type": "application/json",
        }
    )
else:
    logger.info("Appwrite not configured; skipping chat logging")


def _usage_to_schema(usage: Optional[Usage]) -> Optional[UsageInfo]:
    if not usage:
        return None
    return UsageInfo(
        prompt_tokens=usage.prompt_tokens,
        completion_tokens=usage.completion_tokens,
        total_tokens=usage.total_tokens,
    )


def _log_chat_to_appwrite(question: str, answer: str) -> None:
    if appwrite_client is None:
        return
    if not Config.APPWRITE_DATABASE_ID or not Config.APPWRITE_COLLECTION_ID:
        return

    import uuid as _uuid
    from datetime import datetime, timezone

    doc_id = f"chat_{_uuid.uuid4().hex[:16]}"
    payload = {
        "documentId": doc_id,
        "data": {
            "question": question[:4000],
            "answer": answer[:4000],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "chatId": doc_id,
            "senderId": "system",
            "receiverId": "user",
            "messageContent": question[:1000],
            "isRead": True,
        },
    }

    client = appwrite_client
    try:
        response = client.post(
            f"{Config.APPWRITE_ENDPOINT}/databases/{Config.APPWRITE_DATABASE_ID}/collections/{Config.APPWRITE_COLLECTION_ID}/documents",
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.warning("Appwrite logging failed: %s", exc)


@app.get("/")
async def root() -> Dict[str, str]:
    return {"status": "ok", "message": "SelcukAiAssistant Backend is running"}


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok", "message": "SelcukAiAssistant Backend is running"}


@app.get("/health/ollama")
async def ollama_health() -> Dict[str, Any]:
    health = await ollama_provider.health_check(Config.OLLAMA_MODEL)
    if health["status"] == "unhealthy":
        raise HTTPException(status_code=503, detail=health)
    return health


@app.get("/models")
async def list_models() -> Dict[str, Any]:
    models = await model_registry.list_models()
    return {"models": [model.__dict__ for model in models]}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, http_request: Request) -> ChatResponse:
    request_id = uuid.uuid4().hex
    start_time = time.perf_counter()
    language = pick_language(http_request.headers.get("Accept-Language"))
    resolved = model_registry.resolve(request.model)
    provider = providers.get(resolved.provider)
    if not provider:
        raise HTTPException(status_code=400, detail="Unknown model provider")

    messages = normalize_messages(request.messages, language)
    messages = trim_messages_for_context(messages, Config.MAX_CONTEXT_TOKENS)
    max_tokens = clamp_max_tokens(request.max_tokens, Config.MAX_OUTPUT_TOKENS)

    try:
        async with asyncio.timeout(Config.REQUEST_TIMEOUT):
            result = await provider.generate(
                messages=[m.model_dump() for m in messages],
                model_id=resolved.model_id,
                temperature=request.temperature,
                top_p=request.top_p,
                max_tokens=max_tokens,
                request_id=request_id,
            )
    except TimeoutError as exc:
        raise HTTPException(status_code=504, detail="Request timeout") from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    answer = clean_text(result.text, language=language)
    _log_chat_to_appwrite(
        question=next((m.content for m in reversed(messages) if m.role == "user"), ""),
        answer=answer,
    )

    logger.info(
        "request_id=%s event=chat_done model=%s provider=%s latency_s=%.3f",
        request_id,
        resolved.model_id,
        resolved.provider,
        time.perf_counter() - start_time,
    )
    return ChatResponse(
        answer=answer,
        request_id=request_id,
        provider=resolved.provider,
        model=resolved.model_id,
        usage=_usage_to_schema(result.usage),
    )


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest, http_request: Request) -> StreamingResponse:
    request_id = uuid.uuid4().hex
    language = pick_language(http_request.headers.get("Accept-Language"))
    resolved = model_registry.resolve(request.model)
    provider = providers.get(resolved.provider)
    if not provider:
        raise HTTPException(status_code=400, detail="Unknown model provider")

    messages = normalize_messages(request.messages, language)
    messages = trim_messages_for_context(messages, Config.MAX_CONTEXT_TOKENS)
    max_tokens = clamp_max_tokens(request.max_tokens, Config.MAX_OUTPUT_TOKENS)
    cancel_token = CancellationToken()

    async def event_generator() -> Any:
        cleaner = StreamingResponseCleaner(language=language)
        try:
            async with asyncio.timeout(Config.REQUEST_TIMEOUT):
                async for chunk in provider.stream(
                    messages=[m.model_dump() for m in messages],
                    model_id=resolved.model_id,
                    temperature=request.temperature,
                    top_p=request.top_p,
                    max_tokens=max_tokens,
                    request_id=request_id,
                    cancel_token=cancel_token,
                ):
                    if await http_request.is_disconnected():
                        cancel_token.cancel()
                        break

                    if chunk.token:
                        cleaned = cleaner.feed(chunk.token)
                        if cleaned:
                            yield sse_event(
                                {
                                    "type": "token",
                                    "token": cleaned,
                                    "request_id": request_id,
                                }
                            )
                    if chunk.done:
                        final_chunk = cleaner.finalize()
                        if final_chunk:
                            yield sse_event(
                                {
                                    "type": "token",
                                    "token": final_chunk,
                                    "request_id": request_id,
                                }
                            )
                        usage_schema = _usage_to_schema(chunk.usage)
                        yield sse_event(
                            {
                                "type": "end",
                                "usage": usage_schema.model_dump()
                                if usage_schema
                                else None,
                                "request_id": request_id,
                            }
                        )
                        break
        except TimeoutError:
            cancel_token.cancel()
            yield sse_event(
                {
                    "type": "error",
                    "message": "Request timeout",
                    "request_id": request_id,
                }
            )
        except Exception as exc:
            cancel_token.cancel()
            yield sse_event(
                {
                    "type": "error",
                    "message": str(exc),
                    "request_id": request_id,
                }
            )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting server on %s:%s", Config.HOST, Config.PORT)
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)
