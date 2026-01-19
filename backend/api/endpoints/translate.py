"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  DOSYA ADI: api/endpoints/translate.py                                         ║
║  AMAÇ: Ollama üzerinden Çeviri API endpoint'leri (Gemma:2b)                    ║
║  KULLANIM: from api.endpoints.translate import router                          ║
║  BAĞIMLILIKLAR: fastapi, pydantic, requests, config                            ║
║  YAZAN: esN2k - Selçuk Üniversitesi                                           ║
╚════════════════════════════════════════════════════════════════════════════════╝

DETAYLI AÇIKLAMA:
─────────────────
Bu modül, Ollama üzerinde çalışan hafif modelleri (önerilen: gemma:2b) kullanarak
metin çevirisi yapar. HuggingFace transformers kütüphanesi yerine Ollama API
kullanılarak sunucu belleği (VRAM) optimize edilmiştir.

ENDPOINT'LER:
• POST /translate       → Tekil çeviri
• POST /translate/batch → Toplu çeviri (max 10 metin)
• GET  /translate/info  → Model bilgileri

Desteklenen Diller (Prompt Mühendisliği ile):
• TR, EN, AR, FA, DE, RU ve daha fazlası.
"""
from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional
import requests
import json

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from config import Config
from services.translategemma_service import TranslateGemmaService

logger = logging.getLogger(__name__)

router = APIRouter()

# TranslateGemma Service
translate_service = TranslateGemmaService()
TRANSLATE_MODEL = "translategemma:4b"

# Request/Response Models
class TranslateRequest(BaseModel):
    text: str = Field(..., max_length=8192, description="Çevrilecek metin (8k context)")
    source_lang: str = Field(
        "auto", description="Kaynak dil (auto/tr/en/ar/fa/de/ru)"
    )
    target_lang: str = Field("tr", description="Hedef dil")

class BatchTranslateRequest(BaseModel):
    texts: List[str] = Field(..., max_length=10, description="Çevrilecek metinler (max 10)")
    source_lang: str = Field(..., description="Kaynak dil kodu")
    target_lang: str = Field(..., description="Hedef dil kodu")

class TranslateMetrics(BaseModel):
    """Çeviri performans metrikleri."""
    total_latency_ms: int = Field(..., description="Toplam işlem süresi")
    chars_per_second: float = Field(..., description="Saniyede işlenen karakter")
    model_load_time_ms: Optional[int] = Field(None, description="Model yükleme süresi (soğuk başlangıç)")

class TranslateResponse(BaseModel):
    original: str
    translated: str
    source_lang: str
    target_lang: str
    metrics: TranslateMetrics
    model_info: Dict[str, Any]

class BatchTranslateResponse(BaseModel):
    translations: List[Dict[str, str]]
    total_time_ms: int
    model_info: Dict[str, Any]

def _detect_language(text: str) -> str:
    """Basit dil algılama."""
    text_lower = text.lower()
    if any(c in text_lower for c in "çğıöşü"):
        return "tr"
    if any(c in text for c in "\u0600\u06ff"): # Arapça/Farsça aralığı
        return "ar"
    if any("\u0400" <= c <= "\u04ff" for c in text):
        return "ru"
    if any(c in text_lower for c in "äöüß"):
        return "de"
    return "en"

def _build_prompt(text: str, source_lang: str, target_lang: str) -> str:
    """Llama 3.2 için optimize edilmiş çeviri promptu."""
    lang_names = {
        "tr": "Turkish", "en": "English", "ar": "Arabic", 
        "fa": "Persian", "de": "German", "ru": "Russian",
        "auto": "the detected language"
    }
    
    src = lang_names.get(source_lang, source_lang)
    tgt = lang_names.get(target_lang, target_lang)
    
    # Llama 3.2 System/User prompt formatı daha verimlidir ama
    # Ollama /api/generate raw modda basit talimatları iyi anlar.
    return f"""You are a professional academic translator.
Task: Translate the following text from {src} to {tgt}.
Rules:
1. Preserve the original meaning and tone.
2. Do not add any explanations, notes, or conversational filler.
3. Output ONLY the translation.

Text to translate:
{text}

Translation:"""

@router.post("/translate", response_model=TranslateResponse)
async def translate_text(request: TranslateRequest) -> TranslateResponse:
    try:
        start_time = time.perf_counter()
        
        # Auto-detect için basit kontrol
        if request.source_lang == "auto":
            detected_lang = _detect_language(request.text)
        else:
            detected_lang = request.source_lang

        # Aynı dil kontrolü
        if detected_lang == request.target_lang:
            return TranslateResponse(
                original=request.text,
                translated=request.text,
                source_lang=detected_lang,
                target_lang=request.target_lang,
                metrics=TranslateMetrics(
                    total_latency_ms=0,
                    chars_per_second=0,
                ),
                model_info={"provider": "ollama", "model": TRANSLATE_MODEL}
            )

        # TranslateGemma service kullan
        translated_text = await translate_service.translate(
            text=request.text,
            source_lang=detected_lang,
            target_lang=request.target_lang
        )

        # Metrik hesaplama
        end_time = time.perf_counter()
        total_latency_ms = int((end_time - start_time) * 1000)
        
        char_count = len(translated_text)
        chars_ps = char_count / (total_latency_ms / 1000) if total_latency_ms > 0 else 0

        return TranslateResponse(
            original=request.text,
            translated=translated_text,
            source_lang=detected_lang,
            target_lang=request.target_lang,
            metrics=TranslateMetrics(
                total_latency_ms=total_latency_ms,
                chars_per_second=round(chars_ps, 2),
            ),
            model_info={
                "provider": "ollama", 
                "model": TRANSLATE_MODEL
            }
        )

    except Exception as e:
        logger.exception("Çeviri hatası: %s", e)
        raise HTTPException(status_code=503, detail="Ollama servisine ulaşılamadı. Model yüklü mü?")


@router.post("/translate/batch", response_model=BatchTranslateResponse)
async def batch_translate(request: BatchTranslateRequest) -> BatchTranslateResponse:
    try:
        start = time.time()
        
        # TranslateGemma service batch kullan
        translations = await translate_service.translate_batch(
            texts=request.texts,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
        
        results = [
            {"original": text, "translated": trans}
            for text, trans in zip(request.texts, translations)
        ]

        total_ms = int((time.time() - start) * 1000)
        
        return BatchTranslateResponse(
            translations=results,
            total_time_ms=total_ms,
            model_info={"provider": "ollama", "model": TRANSLATE_MODEL}
        )
    except Exception as e:
        logger.exception("Batch çeviri hatası: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/translate/info")
async def get_info() -> Dict[str, Any]:
    return {
        "provider": "ollama",
        "model": TRANSLATE_MODEL,
        "backend_url": Config.OLLAMA_BASE_URL,
        "description": "Ollama tabanlı hafif çeviri servisi (gemma:2b)"
    }

