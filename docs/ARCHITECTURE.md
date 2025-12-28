# Mimari (Detaylı)

Bu doküman, Flutter → FastAPI → Ollama/FAISS etkileşimini detaylandırır.

## 1) Katmanlar
```
Sunum Katmanı  : Flutter + GetX (UI/State)
Uygulama Katmanı: FastAPI (yönlendirme, doğrulama)
Zeka Katmanı   : Ollama (Llama 3.1)
Bilgi Katmanı  : RAG (FAISS + ChromaDB)
```

## 2) İstek Akışı
1. **Flutter** kullanıcının mesajını alır.
2. **FastAPI** `ChatRequest` şemasını doğrular.
3. **RAG etkinse**:
   - Soru metni ile FAISS üzerinde arama yapılır.
   - En ilgili parçalar sistem promptuna eklenir.
4. **Model çağrısı** yapılır (Ollama/HF).
5. **Yanıt** temizlenir ve istemciye dönülür.

## 3) Streaming (SSE)
```
Client ── /chat/stream ──> Server
Server ── token events ──> Client
Server ── end event ─────> Client
```
- Her token, `data:` satırlarıyla iletilir.
- İstemci bağlantıyı keserse iptal sinyali gönderilir.

## 4) RAG Pipeline
```
Belge -> Parçalama -> Embedding -> FAISS -> Sorgu -> Kaynaklı Yanıt
```
Örnek ingestion:
```bash
cd backend
python rag_ingest.py --input ../docs --output ./data/rag
```

## 5) Sağlık Uçları
- `/health`: Backend sağlık kontrolü
- `/health/ollama`: Ollama servisi ve model uygunluğu
- `/health/hf`: HuggingFace bağımlılıkları/GPU durumu

## 6) Yapılandırma Notları
Örnek `.env` alanları:
```
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1
RAG_ENABLED=true
RAG_VECTOR_DB_PATH=./data/rag
```
