# Mimari

Bu doküman, Selçuk AI Akademik Asistan’ın uçtan uca mimarisini ve veri akışını
özetler.

## 1) Yüksek seviye bileşenler
```
Flutter (UI) ──HTTP/SSE──> FastAPI ──> LLM (Ollama)
                         └──> RAG (FAISS + ChromaDB)
```

## 2) Bileşenler ve sorumluluklar
- **Flutter (GetX)**: UI, model seçimi, ayarlar, sohbet akışı.
- **FastAPI**: İstek doğrulama, model yönlendirme, RAG orkestrasyonu.
- **Ollama**: Yerel LLM çalıştırma (Llama 3.1).
- **RAG Katmanı**: FAISS indeksinden kaynak parçaları çekme.
- **ChromaDB**: Vektör veritabanı (persisted storage).

## 3) Veri akışı (chat)
1. Kullanıcı mesajı Flutter’dan **/chat** veya **/chat/stream** ile backend’e gider.
2. **RAG etkinse**: Soru metniyle FAISS üzerinde arama yapılır.
3. Bulunan kaynak parçaları sistem promptuna eklenir.
4. LLM yanıt üretir ve sonuç frontend’e döner.
5. /chat/stream için SSE ile parça parça yanıt akıtılır.

## 4) RAG bileşenleri
- **Embedding üretimi**: SentenceTransformer (çok dilli).
- **İndeksleme**: `rag_ingest.py` ile belgeler parçalanır ve FAISS’e yazılır.
- **Sorgu**: En yakın `top_k` parça çekilir, kaynak etiketi üretilir.

## 5) Hata dayanıklılığı
- Ollama veya RAG servisleri devre dışıysa kullanıcıya **Türkçe** hata mesajı döner.
- Zaman aşımı ve bağlantı hataları HTTP hata kodlarıyla raporlanır.

## 6) Konfigürasyon
Tüm ayarlar `backend/.env` üzerinden yönetilir. Önemli alanlar:
- `OLLAMA_BASE_URL`, `OLLAMA_MODEL`
- `RAG_ENABLED`, `RAG_VECTOR_DB_PATH`
- `MAX_CONTEXT_TOKENS`, `MAX_OUTPUT_TOKENS`

Detaylar için `docs/ARCHITECTURE.md` dosyasına bakın.
