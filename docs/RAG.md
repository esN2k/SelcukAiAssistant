# RAG (Kaynak Destekli Yanitlar)

## Genel bakis
RAG, belgelerden alinmis parcalari modele baglam olarak vererek yanit kalitesini artirir.

## Ingestion (FAISS indeks)
CLI araci: `backend/rag_ingest.py`

Ornek:
```bash
cd backend
python rag_ingest.py --input ./docs --output ./data/rag
```

PDF, TXT/MD ve HTML dosyalari desteklenir. Her parca icin kaynak (dosya adi) ve sayfa bilgisi saklanir.

## Backend ayarlari (.env)
```
RAG_ENABLED=true
RAG_VECTOR_DB_PATH=./data/rag
RAG_TOP_K=4
RAG_EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-mpnet-base-v2
RAG_STRICT_DEFAULT=true
```

## Strict mod
- RAG acikken kaynak bulunamazsa backend `Bu bilgi kaynaklarda yok.` cevabi dondurur.
- Istek bazinda `rag_strict` ile override edilebilir.

## Citations
- /chat cevabinda `citations` alani doner.
- /chat/stream sonunda `citations` end event'inde iletilir.
