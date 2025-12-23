# Selcuk YZ Asistan

Selcuk Universitesi icin gelistirilen ChatGPT benzeri yapay zeka asistani.

## Kisa ozet
- Flutter istemci + FastAPI backend
- Yerel/uzak model destegi (Ollama, HuggingFace, API)
- Streaming ve Markdown destekli sohbet
- RAG (FAISS) ile kaynakli yanitlar

## Hizli baslangic
### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Flutter
```bash
flutter pub get
copy .env.example .env
flutter run
```

## Dokumanlar
- `docs/ARCHITECTURE.md`
- `docs/API_CONTRACT.md`
- `docs/DAGITIM.md`
- `docs/RAG.md`
- `docs/MODELLER.md`
- `docs/YOL_HARITASI.md`
- `docs/SURUM_KONTROL_LISTESI.md`
- `docs/SORUN_GIDERME.md`

## Test / kalite kapilari
Backend:
- `python -m pytest -q`
- `ruff check .`
- `mypy .`

Flutter:
- `flutter pub get`
- `flutter analyze`
- `flutter test`

Smoke test (backend calisirken):
- `tools/test_api.ps1`
- `tools/smoke_test.ps1`
