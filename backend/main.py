"""Selçuk AI Asistanı FastAPI backend uygulaması."""
from __future__ import annotations

import asyncio
import logging
import time
import uuid
from typing import Any, Optional

import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from config import Config
from providers.base import CancellationToken, ModelProvider, Usage
from providers.huggingface_provider import HuggingFaceProvider
from providers.ollama_provider import OllamaProvider
from providers.registry import ModelRegistry
from prompts import build_rag_system_prompt, rag_no_source_message
from rag_service import rag_service
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

app = FastAPI(title="Selçuk AI Asistanı Backend")

default_dev_origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5000",
    "http://localhost:5001",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5000",
    "http://127.0.0.1:5001",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080",
]

allowed_origins = [origin.strip() for origin in Config.ALLOWED_ORIGINS if origin.strip()]
if not allowed_origins:
    if Config.ALLOWED_ORIGINS_STRICT:
        logger.warning(
            "ALLOWED_ORIGINS_STRICT etkin, ancak ALLOWED_ORIGINS boş; "
            "CORS tüm origin'leri engelleyecek."
        )
    else:
        allowed_origins = default_dev_origins
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
    logger.info("Appwrite yapılandırılmadı; sohbet kaydı atlandı.")


def _usage_to_schema(usage: Optional[Usage]) -> Optional[UsageInfo]:
    """Giriş: Usage nesnesi.

    Çıkış: UsageInfo ya da None.
    İşleyiş: Usage alanlarını UsageInfo'ya map eder.
    """
    if not usage:
        return None
    return UsageInfo(
        prompt_tokens=usage.prompt_tokens,
        completion_tokens=usage.completion_tokens,
        total_tokens=usage.total_tokens,
    )


def _log_chat_to_appwrite(question: str, answer: str) -> None:
    """Giriş: Soru ve yanıt metni.

    Çıkış: yok.
    İşleyiş: Appwrite aktifse HTTP POST ile sohbet kaydı ekler.
    """
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
        logger.warning("Appwrite kayıt hatası: %s", exc)


@app.get("/")
async def root() -> dict[str, str]:
    """Giriş: yok.

    Çıkış: Durum sözlüğü.
    İşleyiş: Basit sağlık mesajı döndürür.
    """
    return {"status": "ok", "message": "Selçuk AI Asistanı backend çalışıyor"}


@app.get("/health")
async def health() -> dict[str, str]:
    """Giriş: yok.

    Çıkış: Durum sözlüğü.
    İşleyiş: Sağlık kontrolü için kısa mesaj döndürür.
    """
    return {"status": "ok", "message": "Selçuk AI Asistanı backend çalışıyor"}


@app.get("/health/ollama")
async def ollama_health() -> dict[str, Any]:
    """Giriş: yok.

    Çıkış: Ollama sağlık bilgisi.
    İşleyiş: Sağlık sorunlarında 503 döndürür.
    """
    health_status = await ollama_provider.health_check(Config.OLLAMA_MODEL)
    if health_status["status"] == "unhealthy":
        raise HTTPException(status_code=503, detail=health_status)
    return health_status


@app.get("/health/hf")
async def hf_health() -> dict[str, Any]:
    """Giriş: yok.

    Çıkış: HuggingFace bağımlılık ve GPU bilgisi.
    İşleyiş: torch/transformers durumunu raporlar.
    """
    info: dict[str, Any] = {
        "status": "unavailable",
        "torch_version": None,
        "cuda_available": False,
        "cuda_version": None,
        "gpu_name": None,
        "transformers_version": None,
        "bitsandbytes_version": None,
    }

    try:
        import torch
        import transformers

        info["torch_version"] = torch.__version__
        info["cuda_available"] = torch.cuda.is_available()
        info["cuda_version"] = torch.version.cuda
        if info["cuda_available"]:
            try:
                info["gpu_name"] = torch.cuda.get_device_name(0)
            except Exception:
                info["gpu_name"] = None

        info["transformers_version"] = transformers.__version__

        try:
            import bitsandbytes

            info["bitsandbytes_version"] = bitsandbytes.__version__
        except Exception:
            info["bitsandbytes_version"] = None

        info["status"] = "ok"
    except Exception as exc:
        info["error"] = str(exc)

    return info


@app.get("/models")
async def list_models() -> dict[str, Any]:
    """Giriş: yok.

    Çıkış: Model listesi.
    İşleyiş: ModelRegistry üzerinden katalog döndürür.
    """
    models = await model_registry.list_models()
    return {"models": [model.__dict__ for model in models]}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, http_request: Request) -> ChatResponse:
    """Giriş: ChatRequest ve HTTP Request.

    Çıkış: ChatResponse.
    İşleyiş: RAG ve model çağrısını yürütür.
    """
    request_id = uuid.uuid4().hex
    start_time = time.perf_counter()
    language = pick_language(http_request.headers.get("Accept-Language"))
    resolved = model_registry.resolve(request.model)
    provider = providers.get(resolved.provider)
    if not provider:
        raise HTTPException(status_code=400, detail="Bilinmeyen model sağlayıcısı.")

    rag_enabled = request.rag_enabled and Config.RAG_ENABLED
    rag_strict = (
        Config.RAG_STRICT_DEFAULT
        if request.rag_strict is None
        else request.rag_strict
    )
    rag_top_k = request.rag_top_k or Config.RAG_TOP_K

    messages = normalize_messages(request.messages, language)
    citations: list[str] = []

    if rag_enabled:
        question = next((m.content for m in reversed(messages) if m.role == "user"), "")
        try:
            context, citations = rag_service.get_context(question, top_k=rag_top_k)
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        if rag_strict and not context:
            answer = rag_no_source_message(language)
            return ChatResponse(
                answer=answer,
                request_id=request_id,
                provider=resolved.provider,
                model=resolved.model_id,
                usage=None,
                citations=citations,
            )
        if context:
            messages[0].content = build_rag_system_prompt(
                messages[0].content,
                context,
                language,
                rag_strict,
            )
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
        raise HTTPException(
            status_code=504, detail="İstek zaman aşımına uğradı."
        ) from exc
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
        citations=citations or None,
    )


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest, http_request: Request) -> StreamingResponse:
    """Giriş: ChatRequest ve HTTP Request.

    Çıkış: StreamingResponse.
    İşleyiş: SSE tabanlı akış yanıtı üretir.
    """
    request_id = uuid.uuid4().hex
    language = pick_language(http_request.headers.get("Accept-Language"))
    resolved = model_registry.resolve(request.model)
    provider = providers.get(resolved.provider)
    if not provider:
        raise HTTPException(status_code=400, detail="Bilinmeyen model sağlayıcısı.")

    rag_enabled = request.rag_enabled and Config.RAG_ENABLED
    rag_strict = (
        Config.RAG_STRICT_DEFAULT
        if request.rag_strict is None
        else request.rag_strict
    )
    rag_top_k = request.rag_top_k or Config.RAG_TOP_K

    messages = normalize_messages(request.messages, language)
    citations: list[str] = []
    rag_context = ""
    rag_error: Optional[str] = None

    if rag_enabled:
        question = next((m.content for m in reversed(messages) if m.role == "user"), "")
        try:
            rag_context, citations = rag_service.get_context(question, top_k=rag_top_k)
        except RuntimeError as exc:
            rag_error = str(exc)
        if rag_context:
            messages[0].content = build_rag_system_prompt(
                messages[0].content,
                rag_context,
                language,
                rag_strict,
            )
    messages = trim_messages_for_context(messages, Config.MAX_CONTEXT_TOKENS)
    max_tokens = clamp_max_tokens(request.max_tokens, Config.MAX_OUTPUT_TOKENS)
    cancel_token = CancellationToken()

    async def event_generator() -> Any:
        """Giriş: yok.

        Çıkış: SSE veri akışı.
        İşleyiş: Token ve kontrol mesajlarını sırayla üretir.
        """
        if rag_error:
            yield sse_event(
                {
                    "type": "error",
                    "message": rag_error,
                    "request_id": request_id,
                }
            )
            return
        if rag_enabled and rag_strict and not rag_context:
            no_source = rag_no_source_message(language)
            yield sse_event(
                {
                    "type": "token",
                    "token": no_source,
                    "request_id": request_id,
                }
            )
            yield sse_event(
                {
                    "type": "end",
                    "usage": None,
                    "request_id": request_id,
                    "citations": citations,
                }
            )
            return

        cleaner = StreamingResponseCleaner(language=language)
        accumulated_response = ""
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
                            accumulated_response += cleaned
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
                            accumulated_response += final_chunk
                            yield sse_event(
                                {
                                    "type": "token",
                                    "token": final_chunk,
                                    "request_id": request_id,
                                }
                            )
                        
                        # Appwrite'a kaydet
                        question = next((m.content for m in reversed(messages) if m.role == "user"), "")
                        _log_chat_to_appwrite(question=question, answer=accumulated_response)
                        
                        usage_schema = _usage_to_schema(chunk.usage)
                        yield sse_event(
                            {
                                "type": "end",
                                "usage": usage_schema.model_dump()
                                if usage_schema
                                else None,
                                "request_id": request_id,
                                "citations": citations or None,
                            }
                        )
                        break
        except TimeoutError:
            cancel_token.cancel()
            yield sse_event(
                {
                    "type": "error",
                    "message": "İstek zaman aşımına uğradı.",
                    "request_id": request_id,
                }
            )
        except HTTPException as exc:
            cancel_token.cancel()
            message = exc.detail if isinstance(exc.detail, str) else "Beklenmeyen hata."
            yield sse_event(
                {
                    "type": "error",
                    "message": message,
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
