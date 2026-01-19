"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  MODÜL: quality                                                                ║
║  AMAÇ: RAG sistemi için kapsamlı kalite kontrol modülleri                     ║
║  YAZAN: Selçuk Üniversitesi AI Asistanı                                       ║
╚════════════════════════════════════════════════════════════════════════════════╝

Bu modül şunları içerir:
- Doküman kalite doğrulama
- Chunk optimizasyonu
- Retrieval kalite kapıları
- Cevap doğrulama
- Kalite testi
- Gelişmiş prompt şablonları

KULLANIM:
─────────
from quality import (
    DokumanKaliteDogrulayici,
    ChunkOptimizer,
    RetrievalKaliteKapisi,
    CevapDogrulayici,
    KaliteTesti,
)
"""

# Doküman doğrulama
from quality.document_validator import (
    DokumanKaliteDogrulayici,
    DokumanKaliteSonucu,
    DokumanKaliteAyarlari,
    KaliteDurumu,
    RedNedeni,
    kalite_filtresi_uygula,
)

# Chunk optimizasyonu
from quality.chunk_optimizer import (
    ChunkOptimizer,
    ChunkOptimizerAyarlar,
    OptimizeEdilmisChunk,
    DokumanTipi,
    DokumanKategorisi,
    chunk_kalitesini_hesapla,
)

# Retrieval kalite kapısı
from quality.retrieval_quality_gate import (
    RetrievalKaliteKapisi,
    KaliteKapisiAyarlar,
    KaliteliContext,
    dusuk_kaliteli_contextleri_filtrele,
)

# Cevap doğrulama
from quality.response_validator import (
    CevapDogrulayici,
    DogrulayiciAyarlar,
    DogrulamaSonucu,
    halusinasyon_kontrol,
    kaynak_ekle,
)

# Kalite testi
from quality.quality_tester import (
    KaliteTesti,
    TestSorusu,
    TestSonucu,
    TestRaporu,
    TestDurumu,
    STANDART_TEST_SORULARI,
    kalite_testlerini_calistir,
    test_sorusu_ekle,
)

# Gelişmiş prompt şablonları
from quality.prompts_kalite import (
    KRITIK_KURALLAR_TR,
    KRITIK_KURALLAR_EN,
    CEVAP_FORMAT_TR,
    CEVAP_FORMAT_EN,
    sistem_promptu_olustur,
    kullanici_sorusu_sablonu,
    hata_mesaji_olustur,
    context_zenginlestir,
)

__all__ = [
    # Doküman doğrulama
    "DokumanKaliteDogrulayici",
    "DokumanKaliteSonucu",
    "DokumanKaliteAyarlari",
    "KaliteDurumu",
    "RedNedeni",
    "kalite_filtresi_uygula",
    # Chunk optimizasyonu
    "ChunkOptimizer",
    "ChunkOptimizerAyarlar",
    "OptimizeEdilmisChunk",
    "DokumanTipi",
    "DokumanKategorisi",
    "chunk_kalitesini_hesapla",
    # Retrieval kalite kapısı
    "RetrievalKaliteKapisi",
    "KaliteKapisiAyarlar",
    "KaliteliContext",
    "dusuk_kaliteli_contextleri_filtrele",
    # Cevap doğrulama
    "CevapDogrulayici",
    "DogrulayiciAyarlar",
    "DogrulamaSonucu",
    "halusinasyon_kontrol",
    "kaynak_ekle",
    # Kalite testi
    "KaliteTesti",
    "TestSorusu",
    "TestSonucu",
    "TestRaporu",
    "TestDurumu",
    "STANDART_TEST_SORULARI",
    "kalite_testlerini_calistir",
    "test_sorusu_ekle",
    # Gelişmiş promptlar
    "KRITIK_KURALLAR_TR",
    "KRITIK_KURALLAR_EN",
    "CEVAP_FORMAT_TR",
    "CEVAP_FORMAT_EN",
    "sistem_promptu_olustur",
    "kullanici_sorusu_sablonu",
    "hata_mesaji_olustur",
    "context_zenginlestir",
]
