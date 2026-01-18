#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  DOSYA ADI: scripts/download_translation_model.py                              ║
║  AMAÇ: TranslateGemma-4B modelini HuggingFace'den indirir                     ║
║  KULLANIM: python scripts/download_translation_model.py                        ║
║  BAĞIMLILIKLAR: huggingface_hub, tqdm                                         ║
║  YAZAN: esN2k - Selçuk Üniversitesi                                           ║
╚════════════════════════════════════════════════════════════════════════════════╝

DETAYLI AÇIKLAMA:
─────────────────
TranslateGemma-4B modelini HuggingFace Hub'dan indirir.

Kullanım:
    1. HF_TOKEN environment variable'ı ayarla:
       export HF_TOKEN=hf_your_token_here
    
    2. Script'i çalıştır:
       python scripts/download_translation_model.py

Not:
    - İlk indirmede ~8GB model indirilecek
    - Model ~/.cache/huggingface/ altına kaydedilir
"""
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Varsayılan model
DEFAULT_MODEL = "google/translategemma-4b-it"


def check_hf_token() -> str | None:
    """HuggingFace token'ını kontrol eder.

    Returns:
        Token string veya None.
    """
    token = os.environ.get("HF_TOKEN")
    if not token:
        # .env dosyasından yükle
        env_path = Path(__file__).parent.parent / ".env"
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    if line.startswith("HF_TOKEN="):
                        token = line.strip().split("=", 1)[1].strip('"').strip("'")
                        break
    return token


def download_model(model_name: str, token: str | None = None) -> bool:
    """Model dosyalarını indirir.

    Args:
        model_name: HuggingFace model ID.
        token: HuggingFace token (opsiyonel).

    Returns:
        Başarılı ise True.
    """
    try:
        from huggingface_hub import snapshot_download
    except ImportError:
        logger.error(
            "Gerekli kütüphaneler eksik. Şu komutu çalıştırın:\n"
            "pip install huggingface_hub tqdm"
        )
        return False

    logger.info("=" * 60)
    logger.info("🚀 TranslateGemma Model İndirme Aracı")
    logger.info("=" * 60)
    logger.info("📦 Model: %s", model_name)

    if token:
        logger.info("🔑 HF_TOKEN: ***%s", token[-4:])
    else:
        logger.warning(
            "⚠️ HF_TOKEN ayarlı değil. "
            "Private model erişimi için token gerekebilir."
        )

    logger.info("📥 İndirme başlıyor...")
    logger.info("⏳ Bu işlem birkaç dakika sürebilir (model ~8GB)")

    try:
        cache_dir = snapshot_download(
            repo_id=model_name,
            token=token,
            resume_download=True,
        )

        logger.info("=" * 60)
        logger.info("✅ Model başarıyla indirildi!")
        logger.info("📁 Konum: %s", cache_dir)

        # Boyut hesapla
        total_size = 0
        for dirpath, _, filenames in os.walk(cache_dir):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.isfile(fp):
                    total_size += os.path.getsize(fp)

        size_gb = total_size / (1024**3)
        logger.info("💾 Toplam boyut: %.2f GB", size_gb)
        logger.info("=" * 60)

        return True

    except Exception as e:
        logger.error("❌ İndirme hatası: %s", e)
        logger.error(
            "💡 İpucu: HuggingFace token'ınızı kontrol edin ve "
            "modele erişim izniniz olduğundan emin olun."
        )
        return False


def main() -> int:
    """Ana fonksiyon.

    Returns:
        Çıkış kodu (0=başarı, 1=hata).
    """
    # Model adını al (argüman veya varsayılan)
    model_name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODEL

    # Token kontrolü
    token = check_hf_token()

    # Model indir
    success = download_model(model_name, token)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
