# Selçuk AI Akademik Asistan

Selçuk Üniversitesi “Bilgisayar Mühendisliği Uygulamaları” dersi için geliştirilen,
gizliliğe odaklı bir **yerel yapay zeka akademik asistan** projesidir. Sistem,
Google Gemini API kullanımından tamamen vazgeçmiş ve **yerel Ollama (Llama 3.1)**
altyapısına geçirilmiştir.

## Amaç
- Öğrenci, akademisyen ve idari personel için güvenilir akademik bilgi desteği sağlamak.
- Yerel LLM kullanımıyla veri gizliliğini korumak.
- RAG (Retrieval-Augmented Generation) ile kaynak gösteren yanıt üretmek.

## Teknoloji Yığını
- **Frontend:** Flutter + GetX (Material 3, çoklu platform)
- **Backend:** Python + FastAPI
- **Yerel LLM:** Ollama (Llama 3.1)
- **RAG:** LangChain (orchestrator), FAISS (vektör arama), ChromaDB (vektör DB)

## Mimari Özet
```
Flutter (UI) ──HTTP/SSE──> FastAPI ──> LLM (Ollama)
                         └──> RAG (FAISS + ChromaDB)
```
- **/chat** ve **/chat/stream** uçları ile istek/akış yanıtı.
- RAG açıksa, önce kaynak parçaları toplanır ve prompta eklenir.

## Hızlı Başlangıç
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

## RAG Kullanımı
```bash
cd backend
python rag_ingest.py --input ../docs --output ./data/rag
```
Ardından `backend/.env` içinde:
```
RAG_ENABLED=true
RAG_VECTOR_DB_PATH=./data/rag
```

## Dokümantasyon
- `INSTALL.md`
- `ARCHITECTURE.md`
- `docs/ARCHITECTURE.md`
- `docs/API_CONTRACT.md`
- `docs/DAGITIM.md`
- `docs/RAG.md`
- `docs/MODELLER.md`
- `docs/SORUN_GIDERME.md`
- `docs/YOL_HARITASI.md`
- `docs/SURUM_KONTROL_LISTESI.md`

## Test / Kalite Kapıları
Backend:
- `python -m pytest -q`
- `ruff check .`
- `mypy .`

Flutter:
- `flutter analyze`
- `flutter test`

Smoke test (backend çalışırken):
- `tools/test_api.ps1`
- `tools/smoke_test.ps1`
