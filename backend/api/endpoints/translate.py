"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  DOSYA ADI: api/endpoints/translate.py                                         ║
║  AMAÇ: TranslateGemma çeviri API endpoint'leri                                ║
║  KULLANIM: from api.endpoints.translate import router                          ║
║  BAĞIMLILIKLAR: fastapi, pydantic, providers.translate_gemma                   ║
║  YAZAN: esN2k - Selçuk Üniversitesi                                           ║
╚════════════════════════════════════════════════════════════════════════════════╝

DETAYLI AÇIKLAMA:
─────────────────
TranslateGemma-4B modeli ile çeviri API'si.

ENDPOINT'LER:
• POST /translate       → Tekil çeviri
• POST /translate/batch → Toplu çeviri (max 10 metin)
• GET  /translate/info  → Model bilgileri

Desteklenen Diller: TR, EN, AR, FA, DE, RU

Performans (RTX 3060):
• Ortalama: 400-600ms
• VRAM: ~2GB (4-bit)
"""
from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter()

# Global instance (singleton) - lazy loading
_translator: Optional[Any] = None


def get_translator() -> Any:
    """TranslateGemma provider singleton'ı döndürür.

    Returns:
        TranslateGemmaProvider instance.

    Raises:
        HTTPException: Model yüklenemezse.
    """
    global _translator
    if _translator is None:
        try:
            from providers.translate_gemma import TranslateGemmaProvider

            _translator = TranslateGemmaProvider(use_4bit=True)
        except ImportError as exc:
            logger.error("TranslateGemma bağımlılıkları yüklenemedi: %s", exc)
            raise HTTPException(
                status_code=503,
                detail="Çeviri servisi kullanılamıyor. Bağımlılıklar eksik.",
            ) from exc
    return _translator


# Request/Response Models
class TranslateRequest(BaseModel):
    """Tekil çeviri isteği.

    Attributes:
        text: Çevrilecek metin (max 2048 karakter).
        source_lang: Kaynak dil kodu (auto/tr/en/ar/fa/de/ru).
        target_lang: Hedef dil kodu.
        num_beams: Beam search sayısı (1=hızlı, 4=kaliteli).
    """

    text: str = Field(..., max_length=2048, description="Çevrilecek metin")
    source_lang: str = Field(
        "auto", description="Kaynak dil (auto/tr/en/ar/fa/de/ru)"
    )
    target_lang: str = Field("tr", description="Hedef dil")
    num_beams: int = Field(
        4, ge=1, le=8, description="Beam search (1=hızlı, 4=kaliteli)"
    )


class BatchTranslateRequest(BaseModel):
    """Toplu çeviri isteği.

    Attributes:
        texts: Çevrilecek metinler listesi (max 10).
        source_lang: Kaynak dil kodu.
        target_lang: Hedef dil kodu.
    """

    texts: List[str] = Field(
        ..., max_length=10, description="Çevrilecek metinler (max 10)"
    )
    source_lang: str = Field(..., description="Kaynak dil kodu")
    target_lang: str = Field(..., description="Hedef dil kodu")


class TranslateResponse(BaseModel):
    """Tekil çeviri yanıtı.

    Attributes:
        original: Orijinal metin.
        translated: Çevrilmiş metin.
        source_lang: Algılanan/kullanılan kaynak dil.
        target_lang: Hedef dil.
        inference_time_ms: Çeviri süresi (ms).
        model_info: Model bilgileri.
    """

    original: str
    translated: str
    source_lang: str
    target_lang: str
    inference_time_ms: int
    model_info: Dict[str, Any]


class BatchTranslateResponse(BaseModel):
    """Toplu çeviri yanıtı.

    Attributes:
        translations: Çeviri sonuçları listesi.
        total_time_ms: Toplam çeviri süresi (ms).
        model_info: Model bilgileri.
    """

    translations: List[Dict[str, str]]
    total_time_ms: int
    model_info: Dict[str, Any]


def _detect_language(text: str) -> str:
    """Basit dil algılama.

    Args:
        text: Analiz edilecek metin.

    Returns:
        Algılanan dil kodu (tr/en/ar/fa/de/ru).
    """
    text_lower = text.lower()

    # Türkçe karakterler
    if any(c in text_lower for c in "çğıöşü"):
        return "tr"

    # Arapça/Farsça Unicode aralığı (U+0600-U+06FF)
    arabic_chars = [c for c in text if "\u0600" <= c <= "\u06ff"]
    if arabic_chars:
        # Farsça'ya özgü karakterler
        if any(c in text for c in "پچژگک"):
            return "fa"
        return "ar"

    # Kiril alfabesi (Rusça)
    if any("\u0400" <= c <= "\u04ff" for c in text):
        return "ru"

    # Almanca karakterler
    if any(c in text_lower for c in "äöüß"):
        return "de"

    # Varsayılan: İngilizce
    return "en"


@router.post("/translate", response_model=TranslateResponse)
async def translate_text(request: TranslateRequest) -> TranslateResponse:
    """Tekil çeviri endpoint'i.

    Metni kaynak dilden hedef dile çevirir.

    **Performans (RTX 3060):**
    - Ortalama: 400-600ms
    - VRAM: ~2GB

    **Desteklenen Diller:**
    - 🇹🇷 tr, 🇬🇧 en, 🇸🇦 ar, 🇮🇷 fa, 🇩🇪 de, 🇷🇺 ru

    Args:
        request: Çeviri isteği.

    Returns:
        Çeviri yanıtı.

    Raises:
        HTTPException: Çeviri hatası durumunda.
    """
    try:
        translator = get_translator()

        # Otomatik dil algılama
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
                inference_time_ms=0,
                model_info=translator.get_model_info(),
            )

        # Çeviri
        start = time.time()
        translated = translator.translate(
            text=request.text,
            source_lang=detected_lang,
            target_lang=request.target_lang,
            num_beams=request.num_beams,
        )
        inference_ms = int((time.time() - start) * 1000)

        return TranslateResponse(
            original=request.text,
            translated=translated,
            source_lang=detected_lang,
            target_lang=request.target_lang,
            inference_time_ms=inference_ms,
            model_info=translator.get_model_info(),
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.exception("Çeviri hatası: %s", e)
        raise HTTPException(status_code=500, detail=f"Çeviri hatası: {e!s}") from e


@router.post("/translate/batch", response_model=BatchTranslateResponse)
async def batch_translate(request: BatchTranslateRequest) -> BatchTranslateResponse:
    """Toplu çeviri endpoint'i (max 10 metin).

    Birden fazla metni aynı anda çevirir.

    **Avantaj:** 10 ayrı istek yerine 1 batch → ~3x daha hızlı

    Args:
        request: Toplu çeviri isteği.

    Returns:
        Toplu çeviri yanıtı.

    Raises:
        HTTPException: Çeviri hatası durumunda.
    """
    try:
        translator = get_translator()

        start = time.time()
        translations = translator.batch_translate(
            texts=request.texts,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
        )
        total_ms = int((time.time() - start) * 1000)

        results = [
            {"original": orig, "translated": trans}
            for orig, trans in zip(request.texts, translations)
        ]

        return BatchTranslateResponse(
            translations=results,
            total_time_ms=total_ms,
            model_info=translator.get_model_info(),
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.exception("Toplu çeviri hatası: %s", e)
        raise HTTPException(
            status_code=500, detail=f"Toplu çeviri hatası: {e!s}"
        ) from e


@router.get("/translate/info")
async def get_info() -> Dict[str, Any]:
    """Model bilgileri endpoint'i.

    Çeviri modelinin durumu ve istatistiklerini döndürür.

    Returns:
        Model bilgileri sözlüğü.
    """
    try:
        translator = get_translator()
        return translator.get_model_info()
    except HTTPException:
        # Model yüklenemedi
        return {
            "model_name": "google/translategemma-4b-it",
            "device": "not_loaded",
            "vram_usage_gb": 0.0,
            "max_vram_gb": 0.0,
            "quantization": "4-bit NF4",
            "supported_languages": ["tr", "en", "ar", "fa", "de", "ru"],
            "loaded": False,
            "error": "Model henüz yüklenmedi veya bağımlılıklar eksik",
        }
