# Test ve CI Raporu

Bu rapor, Selçuk AI Akademik Asistan projesinin test ve sürekli entegrasyon (CI) sonuçlarını akademik formatta özetlemek amacıyla hazırlanmıştır.

## Test Ortamı
- CI (GitHub Actions):
  - Backend: ubuntu-latest
  - API smoke: windows-latest
  - Flutter: ubuntu-latest
- Yerel geliştirme (örnek): Windows 10/11, Python 3.12 (önerilen), Flutter Stable
- Sanal ortam: `backend/.venv` veya `.venv`

## Backend Kalitesi
- Testler `pytest -q` ile çalıştırılmıştır.
- Kod kalitesi denetimi `ruff check .` ile yapılmıştır.
- Tip denetimi `mypy .` ile gerçekleştirilmiştir.
- Kritik test dosyaları:
  - `backend/test_main.py` (API kontrat testleri)
  - `backend/test_extended.py` (RAG, retry ve sağlık senaryoları)
  - `backend/test_response_cleaner.py` (metin temizleme)
  - `backend/test_reasoning_cleanup.py` (düşünce blokları temizliği)

## Frontend Kalitesi
- Statik analiz: `flutter analyze`
- Widget testleri: `flutter test`
- Kritik test dosyası: `test/widget_test.dart`

## Araçlar ve Script'ler
- `tools/encoding_guard.py`: UTF-8/BOM/mojibake taraması
- `tools/test_api.ps1`: API smoke (model yoksa SKIP)
- `tools/smoke_test.ps1`: geniş kapsamlı smoke raporu
- `benchmark/ollama_quick.py`: Ollama hızlı performans ölçümü
- `benchmark/run.py`: Ayrıntılı model benchmark (Ollama + HF)

## Sonuç Tablosu
| Komut | Amaç | Durum | Not |
| --- | --- | --- | --- |
| `python -m pytest -q` | Backend birim testleri | Uyarı | FAISS/NumPy DeprecationWarning görülebilir |
| `ruff check .` | Kod kalitesi (lint/biçem) | Geçti | - |
| `mypy .` | Tip denetimi | Geçti | - |
| `flutter analyze` | Flutter statik analiz | Geçti | - |
| `flutter test` | Flutter widget testleri | Geçti | - |
| `py -3 tools/encoding_guard.py --root .` | Encoding guard | Geçti | UTF-8/BOM ve mojibake taraması |
| `tools/test_api.ps1` | API smoke testi | Geçti | Model yoksa SKIP |
| `tools/smoke_test.ps1` | Geniş smoke testi | Geçti | Model yoksa SKIP |

## Uyarılar
- FAISS ve NumPy uyumluluğu nedeniyle `DeprecationWarning` görülebilir; bu uyarının çalışabilirlik üzerinde etkisi bulunmamaktadır.
