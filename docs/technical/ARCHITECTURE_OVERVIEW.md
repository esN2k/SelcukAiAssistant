# Mimari

Bu doküman, Selçuk AI Akademik Asistan’ın uçtan uca mimarisini ve veri akışını
özetler.

## 1) Yüksek seviye bileşenler
```
Flutter (arayüz) ──HTTP/SSE──> FastAPI ──> LLM (Ollama / HuggingFace)
                         └──> RAG (FAISS + ChromaDB)
```

## 2) Bileşenler ve sorumluluklar
- **Flutter (GetX)**: Arayüz, model seçimi, ayarlar, sohbet akışı.
- **FastAPI**: İstek doğrulama, model yönlendirme, RAG orkestrasyonu.
- **Ollama**: Yerel LLM çalıştırma (Llama 3.1).
- **HuggingFace (HF)**: İsteğe bağlı yerel model akışı (torch/transformers bağımlı).
- **RAG Katmanı**: FAISS indeksinden kaynak parçaları çekme.
- **ChromaDB**: Vektör veritabanı (kalıcı depolama).
- **Sağlayıcı Deseni**: `backend/providers/` ile çoklu sağlayıcı yönlendirme.

## 3) Veri akışı (chat)
1. Kullanıcı mesajı Flutter’dan **/chat** veya **/chat/stream** ile arka uca gider.
2. **RAG etkinse**: Soru metniyle FAISS üzerinde arama yapılır.
3. Bulunan kaynak parçaları sistem istemine eklenir.
4. LLM yanıt üretir ve sonuç ön uca döner.
5. /chat/stream için SSE ile parça parça yanıt akıtılır.

## 4) RAG bileşenleri
- **Gömme üretimi**: SentenceTransformer (çok dilli).
- **İndeksleme**: `rag_ingest.py` ile belgeler parçalanır ve FAISS’e yazılır.
- **Sorgu**: En yakın `top_k` parça çekilir, kaynak etiketi üretilir.

## 5) Hata dayanıklılığı
- Ollama veya RAG servisleri devre dışıysa kullanıcıya **Türkçe** hata mesajı döner.
- Zaman aşımı ve bağlantı hataları HTTP hata kodlarıyla raporlanır.

## 6) Yapılandırma
Tüm ayarlar `backend/.env` üzerinden yönetilir. Önemli alanlar:
- `OLLAMA_BASE_URL`, `OLLAMA_MODEL`
- `MODEL_BACKEND` (varsayılan sağlayıcı)
- `RAG_ENABLED`, `RAG_VECTOR_DB_PATH`
- `MAX_CONTEXT_TOKENS`, `MAX_OUTPUT_TOKENS`

Detaylar için `docs/technical/ARCHITECTURE.md` dosyasına bakın.
