# Backend (FastAPI)

Bu klasor Selcuk YZ Asistan backend servisidir.

## Calistirma
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Uc noktalar
- `GET /health`
- `GET /models`
- `POST /chat`
- `POST /chat/stream`

## RAG
- FAISS indeksleri icin `rag_ingest.py` kullanilir.
- Ayarlar: `RAG_ENABLED`, `RAG_VECTOR_DB_PATH`, `RAG_TOP_K`.

## Testler
```bash
pytest -q
ruff check .
mypy .
```
