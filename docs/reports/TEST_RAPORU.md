# Test ve CI Raporu

Bu rapor, Selçuk AI Akademik Asistan projesinin test ve sürekli entegrasyon (CI) sonuçlarını akademik formatta özetlemek amacıyla hazırlanmıştır.

## Test Ortamı
- CI (GitHub Actions):
  - Arka uç: ubuntu-latest
  - API duman testi: windows-latest
  - Flutter: ubuntu-latest
- Yerel geliştirme (örnek): Windows 10/11, Python 3.12 (önerilen), Flutter Stable
- Sanal ortam: `backend/.venv` veya `.venv`

## Arka Uç Kalitesi
- Testler `pytest -q` ile çalıştırılmıştır.
- Kod kalitesi denetimi `ruff check .` ile yapılmıştır.
- Tip denetimi `mypy .` ile gerçekleştirilmiştir.
- Kritik test dosyaları:
  - `backend/test_main.py` (API kontrat testleri)
  - `backend/test_extended.py` (RAG, yeniden deneme ve sağlık senaryoları)
  - `backend/test_response_cleaner.py` (metin temizleme)
  - `backend/test_reasoning_cleanup.py` (düşünce blokları temizliği)

## Ön Uç Kalitesi
- Statik analiz: `flutter analyze`
- Widget testleri: `flutter test`
- Kritik test dosyası: `test/widget_test.dart`

## Araçlar ve Betikler
- `tools/encoding_guard.py`: UTF-8/BOM/mojibake taraması
- `tools/test_api.ps1`: API duman testi (model yoksa SKIP)
- `tools/smoke_test.ps1`: geniş kapsamlı duman raporu
- `benchmark/ollama_quick.py`: Ollama hızlı performans ölçümü
- `benchmark/run.py`: Ayrıntılı model kıyaslaması (Ollama + HF)

## Sonuç Tablosu
| Komut | Amaç | Durum | Sonuç Detayı |
| --- | --- | --- | --- |
| `python -m pytest -q` | Arka uç birim testleri | ✅ Geçti | 50 test geçti, 1 DeprecationWarning (FAISS/NumPy) |
| `ruff check . --select=E9,F63,F7,F82` | Kritik kod hataları | ✅ Geçti | Kritik hata yok |
| `ruff check .` | Kod kalitesi (biçem denetimi) | ✅ Geçti | Kod stili sorunsuz |
| `mypy .` | Tip denetimi | ✅ Geçti | 18 kaynak dosyada tip hatası yok |
| `flutter analyze` | Flutter statik analiz | ⏭️ CI'da | CI ortamında çalıştırılıyor |
| `flutter test` | Flutter widget testleri | ⏭️ CI'da | CI ortamında çalıştırılıyor |
| `python tools/encoding_guard.py --root .` | Kodlama denetimi | ✅ Geçti | UTF-8/BOM ve mojibake taraması temiz |
| `tools/test_api.ps1` | API duman testi | ⏭️ CI'da | Model yoksa SKIP |
| `tools/smoke_test.ps1` | Geniş duman testi | ⏭️ CI'da | Model yoksa SKIP |

## Son Test Çalıştırma Tarihi
**Tarih:** 2026-01-01  
**Python Sürümü:** 3.12.3  
**Test Ortamı:** Ubuntu 22.04 (CI ortamı)

## Uyarılar
- FAISS ve NumPy uyumluluğu nedeniyle `DeprecationWarning` görülebilir; bu uyarının çalışabilirlik üzerinde etkisi bulunmamaktadır.
