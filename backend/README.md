# Arka Uç (FastAPI)

Bu klasör Selçuk AI Asistanı arka uç servisidir.

## Çalıştırma
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Uç noktalar
- `GET /health`
- `GET /models`
- `POST /chat`
- `POST /chat/stream`

## RAG
- FAISS indeksleri için `rag_ingest.py` kullanılır.
- Doküman güncellendiğinde indeksi yenilemek için `refresh_rag_index.ps1` kullanılır.
- Ayarlar: `RAG_ENABLED`, `RAG_VECTOR_DB_PATH`, `RAG_TOP_K`.

İndeksi repo kökünden tek komutla yenilemek için:
```bash
python backend/rag_ingest.py --input backend/data/rag/selcuk --output backend/data/rag --reset
```

## Testler
```bash
pytest -q
ruff check .
mypy .
```
