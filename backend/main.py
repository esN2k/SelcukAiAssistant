"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  DOSYA ADI: main.py                                                            ║
║  AMAÇ: FastAPI backend uygulamasının ana giriş noktası                        ║
║  KULLANIM: uvicorn main:app --reload --host 0.0.0.0 --port 8000               ║
║  BAĞIMLILIKLAR: fastapi, uvicorn, pydantic, requests                          ║
║  YAZAN: esN2k - Selçuk Üniversitesi                                           ║
╚════════════════════════════════════════════════════════════════════════════════╝

DETAYLI AÇIKLAMA:
─────────────────
Bu dosya, Selçuk AI Akademik Asistan projesinin FastAPI backend'inin ana giriş
noktasıdır. HTTP endpoint'leri burada tanımlanır ve istemci istekleri işlenir.

ANA ENDPOINT'LER:
• GET  /          → Basit sağlık kontrolü
• GET  /health    → Sağlık durumu
• GET  /health/ollama → Ollama sağlık kontrolü
• GET  /health/hf → HuggingFace sağlık kontrolü
• GET  /models    → Kullanılabilir modellerin listesi
• POST /chat      → Senkron sohbet isteği
• POST /chat/stream → SSE tabanlı akış yanıtı

VERİ AKIŞI:
1. İstemci HTTP isteği gönderir
2. Mesajlar normalize edilir (sistem promptu eklenir)
3. RAG aktifse, ilgili belgeler aranır
4. LLM sağlayıcısı (Ollama/HuggingFace) çağrılır
5. Yanıt temizlenir ve doğruluk kontrolü yapılır
6. Sonuç istemciye döndürülür
"""

from __future__ import annotations

import asyncio
import logging
import time
import uuid
from typing import Any, Optional

from pathlib import Path
import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from config import Config
from error_handlers import register_error_handlers
from providers.base import CancellationToken, ModelProvider, Usage
from providers.huggingface_provider import HuggingFaceProvider
from providers.ollama_provider import OllamaProvider
from providers.registry import ModelRegistry
from api.endpoints.admin import router as admin_router
from api.endpoints.translate import router as translate_router
from analytics_service import analytics_service
from api import error_messages as mesajlar
from cache_service import cache_service
from critical_facts import apply_guard, get_critical_answer, is_selcuk_related, is_greeting
from prompts import build_rag_system_prompt, rag_no_source_message
from rag_guard import apply_rag_guard, is_context_relevant
from rag_service_improved import ImprovedRAGService
from rag_guard_improved import ImprovedRAGGuard
from quality.entegrasyon import KaliteliRAGPipeline
from quality.quality_tester import KaliteTesti
from knowledge.domain_knowledge import boost_priority_documents
from response_cleaner import StreamingResponseCleaner, clean_text
from repetition_detector import RepetitionDetector
from schemas import ChatRequest, ChatResponse, UsageInfo
from exceptions import DogrulamaHatasi, SunucuHatasi, ZamanAsimiHatasi
from utils import (
    clamp_max_tokens,
    normalize_messages,
    pick_language,
    sse_event,
    trim_messages_for_context,
)

# Translation router import
from api.endpoints.translate import router as translate_router

logger = logging.getLogger(__name__)

app = FastAPI(title="Selçuk AI Asistanı Backend")
register_error_handlers(app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(translate_router, prefix="/api", tags=["translation"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])

ollama_provider = OllamaProvider()
huggingface_provider = HuggingFaceProvider()

providers: dict[str, ModelProvider] = {
    "ollama": ollama_provider,
    "huggingface": huggingface_provider,
}
model_registry = ModelRegistry(providers)

improved_rag_service: Optional[ImprovedRAGService] = None
improved_rag_guard: Optional[ImprovedRAGGuard] = None
rag_system_ready = False

# Kalite modülü değişkenleri
kaliteli_pipeline: Optional[KaliteliRAGPipeline] = None
kalite_modu: bool = True  # Kalite modunu aktif et

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


@app.on_event("startup")
async def startup_event():
    """Başlangıçta geliştirilmiş RAG sistemini ve kalite pipeline'ını yükler."""
    global improved_rag_service, improved_rag_guard, rag_system_ready, kaliteli_pipeline, kalite_modu
    
    logger.info("="*60)
    logger.info("🚀 SELÇUK AI ASISTAN - BAŞLATILIYOR")
    logger.info("="*60)
    
    try:
        logger.info("🔄 Geliştirilmiş RAG sistemi LaBSE ile yükleniyor...")
        rag_data_path = Path("data/rag")
        
        improved_rag_service = ImprovedRAGService(rag_data_path)
        
        faiss_path = rag_data_path / "index_labse.faiss"
        metadata_path = rag_data_path / "metadata_labse.pkl"
        
        if faiss_path.exists() and metadata_path.exists():
            import faiss
            import pickle
            from rank_bm25 import BM25Okapi
            
            improved_rag_service.faiss_index = faiss.read_index(str(faiss_path))
            
            with open(metadata_path, 'rb') as f:
                data = pickle.load(f)
                improved_rag_service.documents = data['documents']
                improved_rag_service.metadata = data['metadata']
            
            tokenized_docs = [doc.lower().split() for doc in improved_rag_service.documents]
            improved_rag_service.bm25 = BM25Okapi(tokenized_docs)
            
            logger.info(f"✅ Geliştirilmiş RAG yüklendi: {improved_rag_service.faiss_index.ntotal} vektör (LaBSE 768-dim)")
            
            improved_rag_guard = ImprovedRAGGuard()
            logger.info("✅ Geliştirilmiş RAG Guard başlatıldı (5 katman)")
            
            rag_system_ready = True
            logger.info("✅ Geliştirilmiş RAG sistemi üretime hazır")
            
            # Kaliteli pipeline oluştur
            if kalite_modu:
                logger.info("🎯 Kaliteli RAG pipeline başlatılıyor...")
                kaliteli_pipeline = KaliteliRAGPipeline()
                logger.info("✅ Kaliteli pipeline hazır!")
                
                # Kalite testlerini çalıştır (opsiyonel - başlangıçta)
                try:
                    logger.info("🧪 Hızlı kalite kontrolü yapılıyor...")
                    
                    def test_query_func(sorgu: str) -> str:
                        """Test için basit query fonksiyonu"""
                        try:
                            contexts = improved_rag_service.hybrid_search(sorgu, top_k=5)
                            validated = improved_rag_guard.validate_and_rerank(sorgu, contexts)
                            
                            if not validated:
                                return "Bu konuda bilgim yok."
                            
                            cevap = f"Bulunan bilgiler:\n"
                            for i, ctx in enumerate(validated[:3], 1):
                                cevap += f"{i}. {ctx['content'][:200]}...\n"
                                cevap += f"   [Kaynak: {ctx.get('metadata', {}).get('source', 'Bilinmiyor')}]\n"
                            return cevap
                        except Exception as e:
                            return f"Bir hata oluştu: {e}"
                    
                    # Sadece öncelikli testleri çalıştır (hızlı başlangıç için)
                    tester = KaliteTesti(test_query_func)
                    rapor = tester.testleri_calistir(max_oncelik=1)
                    
                    logger.info("="*60)
                    logger.info("📊 KALİTE HIZLI TEST SONUÇLARI")
                    logger.info("="*60)
                    logger.info(f"✅ Başarılı: {rapor.basarili}/{rapor.toplam}")
                    logger.info(f"📈 Başarı Oranı: %{rapor.basari_orani*100:.1f}")
                    logger.info("="*60)
                except Exception as e:
                    logger.warning(f"⚠️ Kalite testi atlandı: {e}")
        else:
            logger.warning(f"⚠️ RAG indeks dosyaları bulunamadı: {rag_data_path}")
            logger.warning(f"   Beklenen dosyalar: {faiss_path} ve {metadata_path}")
        
        logger.info("✅ Sistem tamamen hazır!")
            
    except Exception as e:
        logger.error(f"❌ Geliştirilmiş RAG sistemi yüklenemedi: {e}")
        import traceback
        traceback.print_exc()


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


def _log_chat(question: str, answer: str) -> None:
    """Giriş: Soru ve yanıt metni.

    Çıkış: yok.
    İşleyiş: Appwrite aktifse oraya, değilse yerel dosyaya sohbet kaydı ekler.
    """
    import json
    from datetime import datetime, timezone

    timestamp = datetime.now(timezone.utc).isoformat()
    
    # 1. Appwrite Kaydı (Varsa)
    if appwrite_client and Config.APPWRITE_DATABASE_ID and Config.APPWRITE_COLLECTION_ID:
        import uuid as _uuid
        doc_id = f"chat_{_uuid.uuid4().hex[:16]}"
        payload = {
            "documentId": doc_id,
            "data": {
                "question": question[:4000],
                "answer": answer[:4000],
                "timestamp": timestamp,
                "chatId": doc_id,
                "senderId": "system",
                "receiverId": "user",
                "messageContent": question[:1000],
                "isRead": True,
            },
        }

        try:
            response = appwrite_client.post(
                f"{Config.APPWRITE_ENDPOINT}/databases/{Config.APPWRITE_DATABASE_ID}/collections/{Config.APPWRITE_COLLECTION_ID}/documents",
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
            return # Appwrite başarılı ise dosyaya yazmaya gerek yok (veya ikisine de yazılabilir)
        except requests.RequestException as exc:
            logger.warning("Appwrite kayıt hatası: %s. Yerel dosyaya yazılıyor.", exc)
    
    # 2. Yerel Dosya Kaydı (Fallback)
    try:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / "chat_history.jsonl"
        
        log_entry = {
            "timestamp": timestamp,
            "question": question,
            "answer": answer,
            "source": "local_fallback"
        }
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception as exc:
        logger.error("Sohbet günlüğe yazılamadı: %s", exc)


@app.get("/")
async def root() -> dict[str, str]:
    """Giriş: yok.

    Çıkış: Durum sözlüğü.
    İşleyiş: Basit sağlık mesajı döndürür.
    """
    return {"status": "ok", "message": "Selçuk AI Asistanı arka uç çalışıyor"}


@app.get("/health")
async def health() -> dict[str, Any]:
    """Giriş: yok.

    Çıkış: Durum sözlüğü.
    İşleyiş: Sağlık kontrolü için kısa mesaj döndürür.
    """
    health_info = {
        "status": "ok", 
        "message": "Selçuk AI Asistanı arka uç çalışıyor",
        "rag_system": {
            "enabled": rag_system_ready,
            "type": "improved_labse" if rag_system_ready else "legacy",
            "vectors": improved_rag_service.faiss_index.ntotal if (rag_system_ready and improved_rag_service) else 0,
            "documents": len(improved_rag_service.documents) if (rag_system_ready and improved_rag_service) else 0
        }
    }
    return health_info


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
        raise DogrulamaHatasi(detay=mesajlar.MODEL_SAGLAYICI_BULUNAMADI)

    rag_enabled = request.rag_enabled and Config.RAG_ENABLED
    rag_strict = (
        Config.RAG_STRICT_DEFAULT
        if request.rag_strict is None
        else request.rag_strict
    )
    rag_top_k = request.rag_top_k or Config.RAG_TOP_K

    messages = normalize_messages(request.messages, language)
    question = next((m.content for m in reversed(messages) if m.role == "user"), "")
    
    # Handle simple greetings with immediate response
    if is_greeting(question):
        greeting_response = (
            "Merhaba! Ben Selçuk AI Asistanı. Selçuk Üniversitesi hakkında "
            "size nasıl yardımcı olabilirim?" if language == "tr" else
            "Hello! I'm Selçuk AI Assistant. How can I help you with Selçuk University?"
        )
        _log_chat(question=question, answer=greeting_response)
        return ChatResponse(
            answer=greeting_response,
            request_id=request_id,
            provider=resolved.provider,
            model=resolved.model_id,
            usage=None,
            citations=None,
        )
    
    critical_answer = get_critical_answer(question, language)
    if critical_answer:
        _log_chat(question=question, answer=critical_answer)
        return ChatResponse(
            answer=critical_answer,
            request_id=request_id,
            provider=resolved.provider,
            model=resolved.model_id,
            usage=None,
            citations=None,
        )

    cached = cache_service.get_cached_response(
        question, request.model, rag_enabled
    )
    if cached:
        logger.info("request_id=%s event=cache_hit", request_id)
        return ChatResponse(**cached)
    rag_context = ""
    citations: list[str] = []

    if rag_enabled:
        try:
            if rag_system_ready and improved_rag_service and improved_rag_guard:
                logger.info("request_id=%s Geliştirilmiş RAG sistemi kullanılıyor (LaBSE + Hibrit)", request_id)
                contexts = improved_rag_service.hybrid_search(question, top_k=rag_top_k)
                contexts = boost_priority_documents(question, contexts)
                validated_contexts = improved_rag_guard.validate_and_rerank(question, contexts)
                
                if validated_contexts:
                    rag_context = "\n\n---\n\n".join([
                        f"[Kaynak: {Path(c['metadata']['source']).stem}]\n{c['content']}"
                        for c in validated_contexts[:3]
                    ])
                    citations = [Path(c['metadata']['source']).name for c in validated_contexts[:3]]
                    logger.info("request_id=%s Geliştirilmiş RAG: %d bağlam, %d kaynak", 
                               request_id, len(validated_contexts), len(citations))
                else:
                    logger.warning("request_id=%s Geliştirilmiş RAG: Tüm bağlamlar guard tarafından reddedildi", request_id)
                    rag_context = ""
                    citations = []
            else:
                logger.warning("request_id=%s Geliştirilmiş RAG hazır değil, eski sisteme geçiliyor", request_id)
                from rag_service import rag_service
                rag_context, citations = rag_service.get_context(question, top_k=rag_top_k)
        except RuntimeError as exc:
            raise SunucuHatasi(detay=mesajlar.RAG_HAZIR_DEGIL) from exc
        
        if not rag_context:
            logger.warning("request_id=%s RAG boş bağlam döndürdü, soru: %s", request_id, question)
            answer = rag_no_source_message(language)
            return ChatResponse(
                answer=answer,
                request_id=request_id,
                provider=resolved.provider,
                model=resolved.model_id,
                usage=None,
                citations=None,
            )
        
        if not rag_system_ready:
            context_relevant = is_context_relevant(question, rag_context, language)
            logger.info("request_id=%s RAG context_relevant=%s, context_len=%d, citations=%d", 
                       request_id, context_relevant, len(rag_context), len(citations))
            if not context_relevant:
                logger.warning("request_id=%s RAG bağlamı alakalı değil. Soru: %s, Bağlam önizleme: %s", 
                              request_id, question, rag_context[:200])
                answer = rag_no_source_message(language)
                return ChatResponse(
                    answer=answer,
                    request_id=request_id,
                    provider=resolved.provider,
                    model=resolved.model_id,
                    usage=None,
                    citations=None,
                )
        messages[0].content = build_rag_system_prompt(
            messages[0].content,
            rag_context,
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
        raise ZamanAsimiHatasi() from exc
    except RuntimeError as exc:
        raise SunucuHatasi(detay=mesajlar.MODEL_HATASI) from exc

    answer = clean_text(result.text, language=language)
    rag_guarded = False
    # RAG guard Config.RAG_GUARD_ENABLED ile kontrol edilir
    if Config.RAG_GUARD_ENABLED and rag_enabled and rag_context:
        answer, rag_guarded = apply_rag_guard(
            question,
            answer,
            rag_context,
            language,
        )
    # Kritik guard her zaman aktif (yanlış bilgileri düzeltir)
    answer, guard_applied = apply_guard(question, answer, language)
    if guard_applied or rag_guarded:
        citations = []
    _log_chat(question=question, answer=answer)

    latency_ms = (time.perf_counter() - start_time) * 1000
    await analytics_service.log_request(
        request_id=request_id,
        question=question,
        answer=answer,
        model=resolved.model_id,
        provider=resolved.provider,
        latency_ms=latency_ms,
        rag_enabled=rag_enabled,
        success=True,
    )

    response = ChatResponse(
        answer=answer,
        request_id=request_id,
        provider=resolved.provider,
        model=resolved.model_id,
        usage=_usage_to_schema(result.usage),
        citations=citations or None,
    )
    cache_service.set_cached_response(
        question, request.model, rag_enabled, response.model_dump()
    )

    logger.info(
        "request_id=%s event=chat_done model=%s provider=%s latency_s=%.3f",
        request_id,
        resolved.model_id,
        resolved.provider,
        latency_ms / 1000,
    )
    return response


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
        raise DogrulamaHatasi(detay=mesajlar.MODEL_SAGLAYICI_BULUNAMADI)

    rag_enabled = request.rag_enabled and Config.RAG_ENABLED
    rag_strict = (
        Config.RAG_STRICT_DEFAULT
        if request.rag_strict is None
        else request.rag_strict
    )
    rag_top_k = request.rag_top_k or Config.RAG_TOP_K

    messages = normalize_messages(request.messages, language)
    question = next((m.content for m in reversed(messages) if m.role == "user"), "")
    
    # Basit selamlamalara anında yanıt ver
    if is_greeting(question):
        greeting_response = (
            "Merhaba! Ben Selçuk AI Asistanı. Selçuk Üniversitesi hakkında "
            "size nasıl yardımcı olabilirim?" if language == "tr" else
            "Hello! I'm Selçuk AI Assistant. How can I help you with Selçuk University?"
        )
        
        async def greeting_generator() -> Any:
            yield sse_event(
                {
                    "type": "token",
                    "token": greeting_response,
                    "request_id": request_id,
                }
            )
            yield sse_event(
                {
                    "type": "end",
                    "usage": None,
                    "request_id": request_id,
                    "citations": None,
                }
            )
        
        _log_chat(question=question, answer=greeting_response)
        return StreamingResponse(
            greeting_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )
    
    critical_answer = get_critical_answer(question, language)
    citations: list[str] = []
    rag_context = ""
    rag_error: Optional[str] = None

    if critical_answer:
        async def event_generator() -> Any:
            yield sse_event(
                {
                    "type": "token",
                    "token": critical_answer,
                    "request_id": request_id,
                }
            )
            yield sse_event(
                {
                    "type": "end",
                    "usage": None,
                    "request_id": request_id,
                    "citations": None,
                }
            )

        _log_chat(question=question, answer=critical_answer)
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    if rag_enabled:
        try:
            if rag_system_ready and improved_rag_service and improved_rag_guard:
                contexts = improved_rag_service.hybrid_search(question, top_k=rag_top_k)
                from knowledge.domain_knowledge import boost_priority_documents
                contexts = boost_priority_documents(question, contexts)
                validated_contexts = improved_rag_guard.validate_and_rerank(question, contexts)
                
                if validated_contexts:
                    rag_context = "\n\n---\n\n".join([
                        f"[Kaynak: {Path(c['metadata']['source']).stem}]\n{c['content']}"
                        for c in validated_contexts[:3]
                    ])
                    citations = [Path(c['metadata']['source']).name for c in validated_contexts[:3]]
                else:
                    rag_context = ""
                    citations = []
            else:
                from rag_service import rag_service
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
    guard_stream = is_selcuk_related(question) or rag_enabled
    if guard_stream:
        async def event_generator() -> Any:
            if rag_error:
                yield sse_event(
                    {
                        "type": "error",
                        "message": rag_error,
                        "request_id": request_id,
                    }
                )
                return
            if rag_enabled and not rag_context:
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
                        "citations": None,
                    }
                )
                return
            if rag_enabled and not is_context_relevant(question, rag_context, language):
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
                        "citations": None,
                    }
                )
                return

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
            except TimeoutError:
                yield sse_event(
                    {
                        "type": "error",
                        "message": "İstek zaman aşımına uğradı.",
                        "request_id": request_id,
                    }
                )
                return
            except RuntimeError as exc:
                yield sse_event(
                    {
                        "type": "error",
                        "message": str(exc),
                        "request_id": request_id,
                    }
                )
                return

            answer = clean_text(result.text, language=language)
            rag_guarded = False
            # RAG guard Config.RAG_GUARD_ENABLED ile kontrol edilir
            if Config.RAG_GUARD_ENABLED and rag_enabled and rag_context:
                answer, rag_guarded = apply_rag_guard(
                    question,
                    answer,
                    rag_context,
                    language,
                )
            answer, guarded = apply_guard(question, answer, language)
            _log_chat(question=question, answer=answer)
            usage_schema = _usage_to_schema(result.usage)
            citations_out = None if (guarded or rag_guarded) else (citations or None)
            yield sse_event(
                {
                    "type": "token",
                    "token": answer,
                    "request_id": request_id,
                }
            )
            yield sse_event(
                {
                    "type": "end",
                    "usage": usage_schema.model_dump() if usage_schema else None,
                    "request_id": request_id,
                    "citations": citations_out,
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
        if rag_enabled and not rag_context:
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
                    "citations": None,
                }
            )
            return
        if rag_enabled and not is_context_relevant(question, rag_context, language):
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
                    "citations": None,
                }
            )
            return

        cleaner = StreamingResponseCleaner(language=language)
        repetition_detector = RepetitionDetector(window_size=5, similarity_threshold=0.8)
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
                            # Tekrarlama kontrolü
                            if repetition_detector.feed(cleaned):
                                logger.warning("request_id=%s Tekrarlama tespit edildi, akış durduruluyor", request_id)
                                cancel_token.cancel()
                                break
                            
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
                        _log_chat(question=question, answer=accumulated_response)
                        
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
                    "message": mesajlar.ZAMAN_ASIMI,
                    "request_id": request_id,
                }
            )
        except HTTPException as exc:
            cancel_token.cancel()
            if exc.status_code == 400:
                message = mesajlar.DOGRULAMA_HATASI
            elif exc.status_code == 401:
                message = mesajlar.YETKISIZ
            elif exc.status_code == 403:
                message = mesajlar.ERISIM_ENGELLENDI
            elif exc.status_code == 404:
                message = mesajlar.KAYNAK_BULUNAMADI
            elif exc.status_code == 422:
                message = mesajlar.DOGRULAMA_HATASI
            elif exc.status_code == 503:
                message = mesajlar.BAGLANTI_HATASI
            elif exc.status_code == 504:
                message = mesajlar.ZAMAN_ASIMI
            else:
                message = mesajlar.SUNUCU_HATASI
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
                    "message": mesajlar.BEKLENMEYEN_HATA,
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


@app.get("/rag/status")
async def rag_status() -> dict[str, Any]:
    """Detaylı RAG sistemi durumunu döndürür."""
    if not rag_system_ready:
        return {
            "enabled": False, 
            "reason": "Geliştirilmiş RAG sistemi yüklenemedi",
            "fallback": "legacy_rag_available"
        }
    
    return {
        "enabled": True,
        "type": "improved",
        "embedding_model": "LaBSE (768-dim)",
        "search_type": "Hybrid (FAISS + BM25)",
        "guard_layers": 5,
        "vectors": improved_rag_service.faiss_index.ntotal if improved_rag_service else 0,
        "documents": len(improved_rag_service.documents) if improved_rag_service else 0,
        "metadata_count": len(improved_rag_service.metadata) if improved_rag_service else 0,
        "index_file": "index_labse.faiss",
        "features": [
            "Semantic search (FAISS)",
            "Keyword search (BM25)",
            "Domain knowledge boosting",
            "Multi-layer guard validation",
            "Cross-encoder re-ranking"
        ]
    }


@app.post("/rag/test")
async def test_rag(query: str) -> dict[str, Any]:
    """LLM olmadan RAG aramasını test eder."""
    if not rag_system_ready or not improved_rag_service or not improved_rag_guard:
        return {
            "error": "Geliştirilmiş RAG sistemi hazır değil",
            "rag_system_ready": rag_system_ready
        }
    
    try:
        logger.info(f"🧪 RAG sorgu ile test ediliyor: {query}")
        
        # Hibrit arama
        contexts = improved_rag_service.hybrid_search(query, top_k=5)
        logger.info(f"   Hibrit aramadan {len(contexts)} bağlam bulundu")
        
        # Alan önceliklendirme
        contexts = boost_priority_documents(query, contexts)
        logger.info(f"   Alan önceliklendirme uygulandı")
        
        # Guard doğrulama
        validated = improved_rag_guard.validate_and_rerank(query, contexts)
        logger.info(f"   Doğrulama: {len(validated)} bağlam guard'ı geçti")
        
        return {
            "query": query,
            "total_found": len(contexts),
            "validated_count": len(validated),
            "rejected_count": len(contexts) - len(validated),
            "results": [
                {
                    "source": Path(c['metadata']['source']).name,
                    "score": round(c.get('rerank_score', c.get('guard_score', c['score'])), 3),
                    "content_preview": c['content'][:200] + "..." if len(c['content']) > 200 else c['content'],
                    "metadata": {
                        "type": c['metadata'].get('type', 'unknown'),
                        "chunk_id": c['metadata'].get('chunk_id', 0),
                        "priority": c['metadata'].get('priority', 1.0)
                    }
                }
                for c in validated[:3]
            ]
        }
    except Exception as e:
        logger.error(f"❌ RAG test hatası: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}


@app.get("/quality/status")
async def quality_status() -> dict[str, Any]:
    """
    Kalite modülü durumu
    """
    return {
        "quality_mode_enabled": kalite_modu,
        "quality_pipeline_loaded": kaliteli_pipeline is not None,
        "rag_enabled": rag_system_ready,
        "modules": {
            "document_validator": True,
            "chunk_optimizer": True,
            "retrieval_quality_gate": True,
            "response_validator": True,
            "quality_tester": True
        }
    }


@app.post("/quality/test")
async def run_quality_tests() -> dict[str, Any]:
    """
    Kalite testlerini manuel çalıştır
    """
    if not kaliteli_pipeline:
        raise HTTPException(status_code=503, detail="Kalite modülü yüklü değil")
    
    if not improved_rag_service or not improved_rag_guard:
        raise HTTPException(status_code=503, detail="RAG sistemi hazır değil")
    
    def test_func(sorgu: str) -> str:
        contexts = improved_rag_service.hybrid_search(sorgu, top_k=5)
        validated = improved_rag_guard.validate_and_rerank(sorgu, contexts)
        
        if not validated:
            return "Bu konuda bilgim yok."
        
        cevap = f"Bulunan bilgiler:\n"
        for i, ctx in enumerate(validated[:3], 1):
            cevap += f"{i}. {ctx['content'][:200]}...\n"
            cevap += f"   [Kaynak: {ctx.get('metadata', {}).get('source', 'Bilinmiyor')}]\n"
        return cevap
    
    tester = KaliteTesti(test_func)
    rapor = tester.testleri_calistir()
    
    return {
        "test_results": rapor.ozet(),
        "total_tests": rapor.toplam,
        "passed": rapor.basarili,
        "failed": rapor.basarisiz,
        "success_rate": rapor.basari_orani,
        "average_response_time_ms": rapor.ortalama_sure
    }


if __name__ == "__main__":
    import uvicorn

    logger.info("Sunucu başlatılıyor: %s:%s", Config.HOST, Config.PORT)
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)
