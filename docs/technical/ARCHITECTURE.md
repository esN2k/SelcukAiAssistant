# Mimari (Detaylı)

Bu doküman, Flutter → FastAPI → Ollama/FAISS etkileşimini detaylandırır.

## 1) Katmanlar
```
Sunum Katmanı  : Flutter + GetX (Arayüz/Durum)
Uygulama Katmanı: FastAPI (yönlendirme, doğrulama)
Zeka Katmanı   : Ollama (Llama 3.1) / HuggingFace (HF, isteğe bağlı)
Bilgi Katmanı  : RAG (FAISS + ChromaDB)
```

## 2) İstek Akışı
1. **Flutter** kullanıcının mesajını alır.
2. **FastAPI** `ChatRequest` şemasını doğrular.
3. **RAG etkinse**:
   - Soru metni ile FAISS üzerinde arama yapılır.
   - En ilgili parçalar sistem istemine eklenir.
4. **Model çağrısı** yapılır (Ollama/HF).
5. **Yanıt** temizlenir ve istemciye dönülür.

### 2.1) Model Yönlendirme
- Varsayılan sağlayıcı `MODEL_BACKEND` ile belirlenir.
- `/models` listesi **uygunluk (kullanılabilirlik)** durumunu döner.
- HuggingFace modelleri yalnızca bağımlılıklar (torch/transformers) **içe aktarılabiliyorsa**
  ve model **önbellekte** ise uygun kabul edilir.

## 3) Akış (SSE)
```
İstemci ── /chat/stream ──> Sunucu
Sunucu ── belirteç olayları ──> İstemci
Sunucu ── bitiş olayı ─────> İstemci
```
- Her belirteç, `data:` satırlarıyla iletilir.
- İstemci bağlantıyı keserse iptal sinyali gönderilir.

## 4) RAG Akışı
```
Belge -> Parçalama -> Gömme -> FAISS -> Sorgu -> Kaynaklı Yanıt
```
Örnek içe aktarım:
```bash
cd backend
python rag_ingest.py --input ../docs --output ./data/rag
```

## 5) Sağlık Uçları
- `/health`: Arka uç sağlık kontrolü
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
