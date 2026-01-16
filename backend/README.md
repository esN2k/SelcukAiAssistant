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

## Sunucu profili (OMEN RTX 3060)
- Hazır ayarlar: `backend/.env.omen`
- Kullanım (PowerShell): `Copy-Item backend\\.env.omen backend\\.env`

## Uç noktalar
- `GET /health`
- `GET /models`
- `POST /chat`
- `POST /chat/stream`

## RAG
- FAISS indeksleri için `rag_ingest.py` kullanılır.
- Doküman güncellendiğinde indeksi yenilemek için `refresh_rag_index.ps1` kullanılır.
- Ayarlar: `RAG_ENABLED`, `RAG_VECTOR_DB_PATH`, `RAG_TOP_K`, `RAG_EMBEDDING_DEVICE`.

## Veri Toplama (Kapsamlı Scraper)
Scraper çıktıları `backend/data/rag/scraped` altında tutulur.

```bash
python backend/scrape_comprehensive.py --domains-file backend/data/scrape_domains.txt
```

DOCX desteği için:
```bash
pip install -r backend/requirements-scraper.txt
```

## QLoRA (Opsiyonel)
```bash
pip install -r backend/requirements-training.txt
python backend/train_qlora.py --data backend/data/selcuk_qa_dataset.jsonl
python backend/merge_adapter.py --base-model Turkcell/Turkcell-LLM-7b-v1 --adapter output/selcuk-qlora --output-dir output/selcuk-merged
```

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
