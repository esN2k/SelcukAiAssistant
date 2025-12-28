# Sürüm Kontrol Listesi

## Backend kalite kapıları
- `python -m pytest -q`
- `ruff check .`
- `mypy .`

## Flutter kalite kapıları
- `flutter pub get`
- `flutter analyze`
- `flutter test`

## Opsiyonel build kontrolleri
- `flutter build web --release`
- `flutter build windows`

## Smoke testler (backend çalışırken)
- `tools/test_api.ps1`
- `tools/smoke_test.ps1`

## Manuel kontroller
- Windows + Android + Web uygulama açılışı
- Streaming, durdurma, yeniden üretme
- Model seçici ve uygunluk rozetleri
- RAG aç/kapa ve kaynak gösterimi
