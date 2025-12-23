# Mimari

## Genel akis
- Flutter istemci (Android, Windows, Web) -> FastAPI backend (/chat, /chat/stream)
- Backend -> model saglayici (Ollama veya HuggingFace)
- RAG acik ise FAISS indeksinden baglam cekilir

## Bilesenler
- **Flutter UI**: sohbet, model secici, ayarlar, diagnostik ekranlari
- **Depolama**: Hive (konusmalar, model secimi), secure storage (anahtarlar)
- **Backend**: FastAPI + provider katmani
- **RAG**: FAISS indeks + sentence-transformers embedding
- **Streaming**: SSE ile parcali yanit

## Veri akis notlari
1. Kullanici mesaji -> backend
2. (Opsiyonel) RAG baglami cekilir ve prompta eklenir
3. Modelden yanit alinir
4. Yanit ve varsa kaynaklar istemciye doner
