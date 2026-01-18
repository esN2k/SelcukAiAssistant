#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  DOSYA ADI: tests/benchmark_translation.py                                     ║
║  AMAÇ: TranslateGemma-4B performans testi                                     ║
║  KULLANIM: python tests/benchmark_translation.py                               ║
║  BAĞIMLILIKLAR: providers.translate_gemma                                      ║
║  YAZAN: esN2k - Selçuk Üniversitesi                                           ║
╚════════════════════════════════════════════════════════════════════════════════╝

DETAYLI AÇIKLAMA:
─────────────────
RTX 3060 üzerinde TranslateGemma-4B performans testi.

Test Dil Çiftleri:
- TR → EN (Türkçe → İngilizce)
- EN → TR (İngilizce → Türkçe)
- AR → TR (Arapça → Türkçe)
- FA → TR (Farsça → Türkçe)
- DE → TR (Almanca → Türkçe)
- RU → TR (Rusça → Türkçe)

Beklenen Sonuçlar (RTX 3060):
- VRAM: ~2GB
- Ortalama süre: 400-600ms
"""
from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Proje kök dizinini path'e ekle
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def run_benchmark() -> List[Dict[str, Any]]:
    """TranslateGemma-4B benchmark testini çalıştırır.

    Returns:
        Test sonuçları listesi.
    """
    from providers.translate_gemma import TranslateGemmaProvider

    # Test senaryoları
    test_cases: List[Tuple[str, str, str]] = [
        ("Selçuk Üniversitesi Konya'da bulunmaktadır.", "tr", "en"),
        ("Where is the library?", "en", "tr"),
        ("مرحبا بكم في جامعة سلجوق", "ar", "tr"),
        ("کتابخانه کجاست؟", "fa", "tr"),
        ("Guten Tag, wie geht es Ihnen?", "de", "tr"),
        ("Привет мир", "ru", "tr"),
    ]

    print("🚀 TranslateGemma-4B Benchmark")
    print("=" * 60)
    print()

    # Model yükle
    print("⏳ Model yükleniyor...")
    translator = TranslateGemmaProvider(use_4bit=True)
    # Model ilk çeviride lazy load olacak

    results: List[Dict[str, Any]] = []

    for i, (text, src, tgt) in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}/{len(test_cases)}: {src} → {tgt}")
        print(f"   Input:  {text}")

        start = time.time()
        try:
            translated = translator.translate(text, src, tgt)
            duration_ms = int((time.time() - start) * 1000)

            result = {
                "pair": f"{src}→{tgt}",
                "time_ms": duration_ms,
                "input": text,
                "output": translated,
                "success": True,
                "error": None,
            }

            print(f"   Output: {translated}")
            print(f"   ⏱️  Süre: {duration_ms}ms")

        except Exception as e:
            duration_ms = int((time.time() - start) * 1000)
            result = {
                "pair": f"{src}→{tgt}",
                "time_ms": duration_ms,
                "input": text,
                "output": None,
                "success": False,
                "error": str(e),
            }
            print(f"   ❌ Hata: {e}")

        results.append(result)

    return results


def print_summary(results: List[Dict[str, Any]]) -> None:
    """Benchmark özeti yazdırır.

    Args:
        results: Test sonuçları.
    """
    from providers.translate_gemma import TranslateGemmaProvider

    print("\n" + "=" * 60)
    print("📊 SONUÇ ÖZETİ")
    print("=" * 60)

    # Başarılı testler
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    print(f"\n✅ Başarılı: {len(successful)}/{len(results)}")
    print(f"❌ Başarısız: {len(failed)}/{len(results)}")

    if successful:
        times = [r["time_ms"] for r in successful]
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)

        print("\n⏱️  Çeviri Süreleri:")
        print(f"   Ortalama: {avg_time:.0f}ms")
        print(f"   Minimum:  {min_time}ms")
        print(f"   Maximum:  {max_time}ms")

    # Model bilgisi
    try:
        translator = TranslateGemmaProvider(use_4bit=True)
        info = translator.get_model_info()

        print("\n💻 Model Bilgileri:")
        print(f"   Model:   {info['model_name']}")
        print(f"   Device:  {info['device']}")
        print(f"   VRAM:    {info['vram_usage_gb']:.2f} GB")
        print(f"   Max VRAM: {info['max_vram_gb']:.2f} GB")
        print(f"   Quantization: {info['quantization']}")
        print(f"   Diller:  {', '.join(info['supported_languages'])}")
    except Exception:
        pass

    # Detaylı sonuç tablosu
    print("\n" + "-" * 60)
    print("DETAYLI SONUÇLAR")
    print("-" * 60)
    print(f"{'Dil Çifti':<12} {'Süre (ms)':<12} {'Durum':<10}")
    print("-" * 60)

    for r in results:
        status = "✅" if r["success"] else "❌"
        print(f"{r['pair']:<12} {r['time_ms']:<12} {status}")

    print("=" * 60)


def main() -> int:
    """Ana fonksiyon.

    Returns:
        Çıkış kodu.
    """
    try:
        results = run_benchmark()
        print_summary(results)

        # Başarı kontrolü
        successful = [r for r in results if r["success"]]
        if len(successful) == len(results):
            print("\n🎉 Tüm testler başarılı!")
            return 0
        elif len(successful) > 0:
            print(f"\n⚠️ Bazı testler başarısız ({len(results) - len(successful)})")
            return 0
        else:
            print("\n❌ Tüm testler başarısız!")
            return 1

    except ImportError as e:
        print(f"❌ Bağımlılık hatası: {e}")
        print("💡 Çözüm: pip install torch transformers bitsandbytes accelerate")
        return 1
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
