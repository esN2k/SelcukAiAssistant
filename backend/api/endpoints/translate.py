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

logger = logging.getLogger(__name__)

router = APIRouter()

# Ollama API Config
OLLAMA_API_URL = f"{Config.OLLAMA_BASE_URL}/api/generate"
TRANSLATE_MODEL = Config.TRANSLATE_MODEL_NAME or "gemma:2b"

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
        # Metrik başlangıcı
        start_time = time.perf_counter()
        
        if request.source_lang == "auto":
            detected_lang = _detect_language(request.text)
        else:
            detected_lang = request.source_lang

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

        prompt = _build_prompt(request.text, detected_lang, request.target_lang)
        
        payload = {
            "model": TRANSLATE_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3, # Llama 3.2 biraz daha esneklik sever ama çeviri için düşük tutalım
                "num_ctx": 4096,    # Daha büyük bağlam
                "num_predict": -1   # Otomatik
            }
        }

        # Ollama İsteği
        api_start = time.perf_counter()
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        api_end = time.perf_counter()
        
        response.raise_for_status()
        result_json = response.json()
        translated_text = result_json.get("response", "").strip()
        
        # Olası tırnak işaretlerini temizle (Llama bazen ekler)
        if translated_text.startswith('"') and translated_text.endswith('"'):
            translated_text = translated_text[1:-1]

        # Metrik Hesaplama
        end_time = time.perf_counter()
        total_latency_ms = int((end_time - start_time) * 1000)
        api_latency_ms = int((api_end - api_start) * 1000)
        
        # Karakter/saniye hızı (çıktı üzerinden)
        char_count = len(translated_text)
        chars_ps = char_count / (total_latency_ms / 1000) if total_latency_ms > 0 else 0

        # Model yükleme süresi tahmini (eval_count vs total_duration'dan çıkarılabilir ama basitçe API süresi farkı diyelim)
        # Ollama 'total_duration', 'load_duration' döner, bunları kullanalım:
        ollama_load_duration = result_json.get("load_duration", 0) / 1_000_000 # nanosaniye -> milisaniye

        return TranslateResponse(
            original=request.text,
            translated=translated_text,
            source_lang=detected_lang,
            target_lang=request.target_lang,
            metrics=TranslateMetrics(
                total_latency_ms=total_latency_ms,
                chars_per_second=round(chars_ps, 2),
                model_load_time_ms=int(ollama_load_duration)
            ),
            model_info={
                "provider": "ollama", 
                "model": TRANSLATE_MODEL,
                "api_latency_ms": api_latency_ms
            }
        )

    except requests.RequestException as e:
        logger.error("Ollama translate hatası: %s", e)
        raise HTTPException(status_code=503, detail="Ollama servisine ulaşılamadı. Model yüklü mü?")
    except Exception as e:
        logger.exception("Çeviri hatası: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/translate/batch", response_model=BatchTranslateResponse)
async def batch_translate(request: BatchTranslateRequest) -> BatchTranslateResponse:
    # Ollama şu an native batch desteklemiyor, sırayla yapıyoruz (paralel de yapılabilir ama VRAM riski)
    try:
        start = time.time()
        results = []
        
        for text in request.texts:
            # İç fonksiyonu çağırmak yerine direkt logic tekrarı veya helper kullanımı
            # Basitlik için döngüde istek atıyoruz
            prompt = _build_prompt(text, request.source_lang, request.target_lang)
            payload = {
                "model": TRANSLATE_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.1}
            }
            
            try:
                resp = requests.post(OLLAMA_API_URL, json=payload, timeout=30)
                if resp.status_code == 200:
                    trans = resp.json().get("response", "").strip()
                else:
                    trans = "[Hata]"
            except:
                trans = "[Hata]"
            
            results.append({"original": text, "translated": trans})

        total_ms = int((time.time() - start) * 1000)
        
        return BatchTranslateResponse(
            translations=results,
            total_time_ms=total_ms,
            model_info={"provider": "ollama", "model": TRANSLATE_MODEL}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/translate/info")
async def get_info() -> Dict[str, Any]:
    return {
        "provider": "ollama",
        "model": TRANSLATE_MODEL,
        "backend_url": Config.OLLAMA_BASE_URL,
        "description": "Ollama tabanlı hafif çeviri servisi (gemma:2b)"
    }

