"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  DOSYA ADI: config.py                                                          ║
║  AMAÇ: Backend yapılandırma yönetimi ve ortam değişkenleri                    ║
║  KULLANIM: from config import Config şeklinde import edilir                   ║
║  BAĞIMLILIKLAR: python-dotenv (opsiyonel), logging                            ║
║  YAZAN: esN2k - Selçuk Üniversitesi                                           ║
╚════════════════════════════════════════════════════════════════════════════════╝

DETAYLI AÇIKLAMA:
─────────────────
Bu dosya, backend uygulamasının tüm yapılandırma ayarlarını merkezi olarak yönetir.
Ortam değişkenleri (.env dosyası veya sistem değişkenleri) okunur ve doğrulanır.

YAPILANDIRMA KATEGORİLERİ:
• Sunucu ayarları (HOST, PORT)
• CORS ayarları (ALLOWED_ORIGINS)
• Ollama ayarları (OLLAMA_BASE_URL, OLLAMA_MODEL, timeout, retry)
• HuggingFace ayarları (HF_MODEL_NAME, HF_DEVICE, vb.)
• RAG ayarları (RAG_ENABLED, vektör DB yolu, embedding modeli)
• Appwrite ayarları (opsiyonel, sohbet kaydı için)
• Güvenlik sınırları (MAX_CONTEXT_TOKENS, MAX_OUTPUT_TOKENS)

DOĞRULAMA:
Config.validate() metodu kritik ayarları doğrular ve hatalıysa ValueError fırlatır.

ÖRNEK KULLANIM:
──────────────
from config import Config

print(Config.OLLAMA_BASE_URL)  # http://localhost:11434
print(Config.RAG_ENABLED)       # True veya False
"""
from __future__ import annotations

import logging
import os
import sys
from enum import Enum
from pathlib import Path
from typing import Callable, Optional


def _configure_utf8_environment() -> None:
    """Giriş: yok.

    Çıkış: yok.
    İşleyiş: Windows'ta stdout/stderr yeniden yapılandırılır; diğer sistemlerde
    uygun locale denenir.
    """
    running_pytest = os.environ.get("PYTEST_CURRENT_TEST") is not None

    if sys.platform == "win32":
        if running_pytest:
            return

        for stream_name in ("stdout", "stderr"):
            stream = getattr(sys, stream_name, None)
            if stream is None:
                continue

            reconfigured = False
            if hasattr(stream, "reconfigure"):
                try:
                    stream.reconfigure(encoding="utf-8")
                    reconfigured = True
                except (AttributeError, ValueError):
                    pass

            if not reconfigured:
                buffer = getattr(stream, "buffer", None)
                if buffer is None:
                    continue
                import io

                setattr(sys, stream_name, io.TextIOWrapper(buffer, encoding="utf-8"))
    else:
        import locale

        try:
            locale.setlocale(locale.LC_ALL, "tr_TR.UTF-8")
        except locale.Error:
            try:
                locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
            except locale.Error:
                logging.warning(
                    "UTF-8 locale ayarlanamadı. Türkçe karakterler "
                    "görüntülenmeyebilir."
                )


_configure_utf8_environment()

load_dotenv: Optional[Callable[..., bool]]
try:
    from dotenv import load_dotenv as _load_dotenv
except ImportError:  # pragma: no cover - opsiyonel bağımlılık
    load_dotenv = None
    logging.warning(
        "python-dotenv kurulu değil; ortam değişkenlerini manuel ayarlayın."
    )
else:
    load_dotenv = _load_dotenv

backend_dir = Path(__file__).resolve().parent
env_path = backend_dir / ".env"
if load_dotenv is not None:
    if env_path.exists():
        load_dotenv(env_path)
        logging.info(".env yüklendi: %s", env_path)
    else:
        logging.warning(".env bulunamadı: %s", env_path)


class ModelType(Enum):
    """Giriş: Model türü değerleri.

    Çıkış: Enum üyeleri.
    İşleyiş: Model seçiminde tekil kaynak sağlar.
    """

    TURKCELL_BASE = "TURKCELL/Turkcell-LLM-7b-v1"
    SELCUK_FINETUNED = "backend/models/selcuk-assistant-v1"
    GEMMA_TR = "google/gemma-2-9b-it"


# Model seçim ve üretim ayarları.
DEFAULT_MODEL = ModelType.SELCUK_FINETUNED
DEFAULT_OLLAMA_MODEL = os.getenv("DEFAULT_OLLAMA_MODEL", "selcuk-assistant-v1")
DEFAULT_HF_MODEL = os.getenv("DEFAULT_HF_MODEL", DEFAULT_MODEL.value)

MODEL_CONFIG = {
    "max_new_tokens": 512,
    "temperature": 0.7,
    "top_p": 0.9,
    "repetition_penalty": 1.15,
    "do_sample": True,
}

USE_4BIT_QUANTIZATION = os.getenv("USE_4BIT_QUANTIZATION", "true").lower() == "true"
USE_FLASH_ATTENTION_2 = os.getenv("USE_FLASH_ATTENTION_2", "true").lower() == "true"


class Config:
    """Giriş: Ortam değişkenleri ve `.env` değerleri.

    Çıkış: Uygulama ayarları ve doğrulama sonuçları.
    İşleyiş: Tüm konfigürasyon alanlarını merkezi olarak toplar.
    """

    CONFIG_WARNINGS: list[str] = []

    # Server configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # CORS configuration
    ALLOWED_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv("ALLOWED_ORIGINS", "").split(",")
        if origin.strip()
    ]
    ALLOWED_ORIGINS_STRICT: bool = (
        os.getenv("ALLOWED_ORIGINS_STRICT", "false").lower() == "true"
    )

    # Ollama configuration
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL)
    OLLAMA_TIMEOUT: int = int(os.getenv("OLLAMA_TIMEOUT", "180"))
    OLLAMA_MAX_RETRIES: int = int(os.getenv("OLLAMA_MAX_RETRIES", "3"))
    OLLAMA_RETRY_DELAY: float = float(os.getenv("OLLAMA_RETRY_DELAY", "1.0"))

    # Logging configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Model routing configuration
    MODEL_BACKEND: str = os.getenv("MODEL_BACKEND", "ollama").lower()
    MODEL_ALIASES: str = os.getenv("MODEL_ALIASES", "")

    # Hugging Face configuration
    HF_MODEL_NAME: str = os.getenv("HF_MODEL_NAME", DEFAULT_HF_MODEL)
    HF_LOAD_IN_4BIT: bool = os.getenv("HF_LOAD_IN_4BIT", "true").lower() == "true"
    HF_DEVICE: str = os.getenv("HF_DEVICE", "auto")
    HF_DTYPE: str = os.getenv("HF_DTYPE", "float16")
    HF_ATTENTION_IMPL: str = os.getenv("HF_ATTENTION_IMPL", "sdpa")
    HF_TOKEN: Optional[str] = os.getenv("HF_TOKEN") or None
    TRANSLATE_MODEL_NAME: str = os.getenv(
        "TRANSLATE_MODEL_NAME", "google/translategemma-4b-it"
    )

    # Cache configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))

    # Analytics configuration
    POSTGRES_DSN: Optional[str] = os.getenv("POSTGRES_DSN") or None

    # Guardrails
    MAX_CONTEXT_TOKENS: int = int(os.getenv("MAX_CONTEXT_TOKENS", "4096"))
    MAX_OUTPUT_TOKENS: int = int(os.getenv("MAX_OUTPUT_TOKENS", "512"))
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "180"))

    # RAG configuration
    RAG_ENABLED: bool = os.getenv("RAG_ENABLED", "true").lower() == "true"
    RAG_VECTOR_DB_PATH: Optional[str] = os.getenv("RAG_VECTOR_DB_PATH", None)
    RAG_COLLECTION_NAME: str = os.getenv("RAG_COLLECTION_NAME", "selcuk_documents")
    RAG_CHUNK_SIZE: int = int(os.getenv("RAG_CHUNK_SIZE", "500"))
    RAG_CHUNK_OVERLAP: int = int(os.getenv("RAG_CHUNK_OVERLAP", "50"))
    RAG_TOP_K: int = int(os.getenv("RAG_TOP_K", "4"))
    RAG_EMBEDDING_BATCH_SIZE: int = int(
        os.getenv("RAG_EMBEDDING_BATCH_SIZE", "16")
    )
    RAG_EMBEDDING_DEVICE: str = os.getenv("RAG_EMBEDDING_DEVICE", "auto")
    RAG_EMBEDDING_MODEL: str = os.getenv(
        "RAG_EMBEDDING_MODEL",
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    )
    RAG_STRICT_DEFAULT: bool = (
        os.getenv("RAG_STRICT_DEFAULT", "true").lower() == "true"
    )

    # Appwrite configuration (optional)
    APPWRITE_ENDPOINT: Optional[str] = os.getenv("APPWRITE_ENDPOINT") or None
    APPWRITE_PROJECT_ID: Optional[str] = os.getenv("APPWRITE_PROJECT_ID") or None
    APPWRITE_API_KEY: Optional[str] = os.getenv("APPWRITE_API_KEY") or None
    APPWRITE_DATABASE_ID: Optional[str] = os.getenv("APPWRITE_DATABASE_ID") or None
    APPWRITE_COLLECTION_ID: Optional[str] = (
        os.getenv("APPWRITE_COLLECTION_ID") or None
    )

    @classmethod
    def validate(cls) -> None:
        """Giriş: Sınıf alanları.

        Çıkış: Hatalı durumda ValueError.
        İşleyiş: Kritik alanları doğrular, opsiyoneller için uyarı üretir.
        """
        errors: list[str] = []
        warnings: list[str] = []

        if cls.OLLAMA_TIMEOUT < 1:
            errors.append("OLLAMA_TIMEOUT en az 1 saniye olmalıdır.")
        if cls.OLLAMA_MAX_RETRIES < 1:
            errors.append("OLLAMA_MAX_RETRIES en az 1 olmalı.")
        if cls.OLLAMA_RETRY_DELAY < 0:
            errors.append("OLLAMA_RETRY_DELAY negatif olamaz.")
        if cls.PORT < 1 or cls.PORT > 65535:
            errors.append("PORT 1-65535 aralığında olmalı.")
        if not cls.OLLAMA_MODEL:
            errors.append("OLLAMA_MODEL boş olamaz.")
        if not cls.OLLAMA_BASE_URL:
            errors.append("OLLAMA_BASE_URL boş olamaz.")
        if cls.MODEL_BACKEND not in {"ollama", "huggingface"}:
            errors.append("MODEL_BACKEND yalnızca 'ollama' veya 'huggingface' olabilir.")
        if cls.MAX_CONTEXT_TOKENS < 256:
            errors.append("MAX_CONTEXT_TOKENS en az 256 olmalı.")
        if cls.MAX_OUTPUT_TOKENS < 1:
            errors.append("MAX_OUTPUT_TOKENS en az 1 olmalı.")
        if cls.REQUEST_TIMEOUT < 1:
            errors.append("REQUEST_TIMEOUT en az 1 saniye olmalı.")
        if cls.CACHE_TTL_SECONDS < 1:
            errors.append("CACHE_TTL_SECONDS en az 1 olmalı.")

        if cls.RAG_ENABLED:
            if not cls.RAG_VECTOR_DB_PATH:
                warnings.append("RAG etkin ama RAG_VECTOR_DB_PATH ayarlanmamış.")
            if cls.RAG_CHUNK_SIZE < 1:
                errors.append("RAG_CHUNK_SIZE en az 1 olmalı.")
            if cls.RAG_CHUNK_OVERLAP < 0:
                errors.append("RAG_CHUNK_OVERLAP negatif olamaz.")
            if cls.RAG_CHUNK_OVERLAP >= cls.RAG_CHUNK_SIZE:
                errors.append(
                    "RAG_CHUNK_OVERLAP, RAG_CHUNK_SIZE'dan küçük olmalı."
                )
            if cls.RAG_TOP_K < 1:
                errors.append("RAG_TOP_K en az 1 olmalı.")
            if cls.RAG_EMBEDDING_BATCH_SIZE < 1:
                errors.append("RAG_EMBEDDING_BATCH_SIZE en az 1 olmalı.")

        if (
            cls.APPWRITE_ENDPOINT
            or cls.APPWRITE_PROJECT_ID
            or cls.APPWRITE_API_KEY
            or cls.APPWRITE_DATABASE_ID
            or cls.APPWRITE_COLLECTION_ID
        ):
            missing = [
                name
                for name, value in (
                    ("APPWRITE_ENDPOINT", cls.APPWRITE_ENDPOINT),
                    ("APPWRITE_PROJECT_ID", cls.APPWRITE_PROJECT_ID),
                    ("APPWRITE_API_KEY", cls.APPWRITE_API_KEY),
                    ("APPWRITE_DATABASE_ID", cls.APPWRITE_DATABASE_ID),
                    ("APPWRITE_COLLECTION_ID", cls.APPWRITE_COLLECTION_ID),
                )
                if not value
            ]
            if missing:
                errors.append(
                    "Appwrite ayarları eksik: " + ", ".join(sorted(missing))
                )

        cls.CONFIG_WARNINGS = warnings
        if errors:
            raise ValueError("; ".join(errors))

    @classmethod
    def setup_logging(cls) -> None:
        """Giriş: yok.

        Çıkış: yok.
        İşleyiş: UTF-8 çıktı ve zaman damgalı log formatını uygular.
        """
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, cls.LOG_LEVEL.upper(), logging.INFO))

        if hasattr(handler.stream, "reconfigure"):
            try:
                handler.stream.reconfigure(encoding="utf-8")
            except (AttributeError, ValueError):
                pass

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)

        logging.basicConfig(
            level=getattr(logging, cls.LOG_LEVEL.upper(), logging.INFO),
            handlers=[handler],
            force=True,
        )


Config.setup_logging()
Config.validate()
for warning in Config.CONFIG_WARNINGS:
    logging.warning(warning)
