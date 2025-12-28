# RAG (Kaynak Destekli Yanıtlar)

RAG (Retrieval-Augmented Generation), modelin yanıtlarını kaynak belgelerle
desteklemesini sağlar. Bu sayede akademik doğruluk artar ve kaynak gösterimi
kolaylaşır.

## 1) Genel Akış
```
Soru -> Embedding -> FAISS -> En yakın parçalar -> Prompt -> Yanıt + Kaynaklar
```

## 2) İndeksleme (Ingestion)
CLI aracı: `backend/rag_ingest.py`

Örnek:
```bash
cd backend
python rag_ingest.py --input ../docs --output ./data/rag
```

Desteklenen formatlar:
- PDF
- TXT / MD
- HTML

Her parça için kaynak (dosya adı) ve sayfa bilgisi saklanır.

## 3) Backend Ayarları (.env)
```
RAG_ENABLED=true
RAG_VECTOR_DB_PATH=./data/rag
RAG_TOP_K=4
RAG_EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-mpnet-base-v2
RAG_STRICT_DEFAULT=true
```

## 4) Strict Mod
- RAG açıkken kaynak bulunamazsa backend: **“Bu bilgi kaynaklarda yok.”** döner.
- İstek bazında `rag_strict` ile override edilebilir.

## 5) Citations
- `/chat` cevabında `citations` alanı döner.
- `/chat/stream` sonunda `end` event içinde `citations` taşınır.
