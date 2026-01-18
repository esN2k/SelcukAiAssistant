# Güncel Durum Özeti - Selçuk AI Akademik Asistan

**Oluşturulma Tarihi:** 5 Ocak 2025  
**Proje Durumu:** Aktif Geliştirme  
**Repository:** https://github.com/esN2k/SelcukAiAssistant  
**Lisans:** MIT

---

## 1. Proje Tanımı

Selçuk AI Akademik Asistan, Selçuk Üniversitesi öğrencileri, akademisyenleri ve idari personeli için geliştirilmiş, gizlilik odaklı bir yapay zeka destekli bilgi asistanıdır. Sistem, tamamen yerel büyük dil modelleri (LLM) kullanarak kullanıcı verilerinin gizliliğini korumakta ve Retrieval-Augmented Generation (RAG) tekniği ile üniversiteye özgü bilgi tabanından kaynak gösterimli yanıtlar üretmektedir.

**Temel Özellikler:**
- **Tam Gizlilik:** Tüm veri işleme yerel ortamda gerçekleştirilmektedir
- **Çevrimdışı Çalışma:** İnternet bağlantısı olmadan temel işlevler çalışmaktadır  
- **Kaynak Gösterimi:** RAG ile her yanıt kaynak dokümanlarıyla ilişkilendirilmektedir
- **Çoklu Platform:** iOS, Android ve Web desteği sağlanmaktadır
- **Çoklu Model:** Ollama ve HuggingFace sağlayıcıları desteklenmektedir

---

## 2. Güncel Mimari

```
┌─────────────────────────────────────────────────────────────────┐
│                    KULLANICI KATMANI                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   iOS App    │  │  Android App │  │   Web App    │          │
│  │  (Flutter)   │  │  (Flutter)   │  │  (Flutter)   │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
└─────────┼──────────────────┼──────────────────┼─────────────────┘
          │                  │                  │
          └──────────────────┴──────────────────┘
                             │
                    HTTP/HTTPS (REST + SSE)
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│                   UYGULAMA KATMANI (FastAPI)                     │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  main.py - Ana Routing ve Middleware                      │  │
│  │  • CORS Handler                                           │  │
│  │  • Request Validation (Pydantic schemas.py)               │  │
│  │  • Error Handling & Logging                               │  │
│  └────────┬─────────────────────────────────────┬────────────┘  │
│           │                                     │               │
│  ┌────────▼───────────┐              ┌─────────▼──────────────┐ │
│  │ Model Registry     │              │  RAG Service           │ │
│  │ (registry.py)      │              │  (rag_service.py)      │ │
│  │                    │              │  • FAISS Vector DB     │ │
│  │ Provider Pattern:  │              │  • Sentence Transform  │ │
│  │ ┌────────────────┐ │              │  • Citation Builder    │ │
│  │ │OllamaProvider  │ │              └───────────────────────┘ │
│  │ │(ollama_prov.py)│ │                                        │
│  │ └────────────────┘ │                                        │
│  │ ┌────────────────┐ │                                        │
│  │ │HuggingFaceProvr│ │                                        │
│  │ │(hf_provider.py)│ │                                        │
│  │ └────────────────┘ │                                        │
│  └────────┬───────────┘                                        │
└───────────┼────────────────────────────────────────────────────┘
            │
    ┌───────┴────────┐
    │                │
┌───▼─────────┐  ┌──▼──────────────┐
│Ollama Server│  │  HuggingFace    │
│• Llama 3.1  │  │  • Qwen2        │
│• Llama 3.2  │  │  • (Offline)    │
│• Deepseek   │  │  • Local Cache  │
│• Local GPU  │  │                 │
└─────────────┘  └─────────────────┘
```

---

## 3. Modül Bazlı Teknik Özet

### 3.1. Backend (Python FastAPI)

**Dosya Sayısı:** 26 Python dosyası  
**Toplam Kod:** ~5,000 satır  
**Temel Bağımlılıklar:** FastAPI 0.115.5, Pydantic 2.10.3, FAISS 1.9.0

#### 3.1.1. Ana Routing (main.py)
- **Kaynak:** `backend/main.py` (538 satır)
- **Sorumluluk:** HTTP endpoint yönetimi, middleware konfigürasyonu
- **Endpoint'ler:**
  - `GET /` - Sağlık kontrolü
  - `GET /health` - Detaylı sistem durumu
  - `GET /health/ollama` - Ollama bağlantı kontrolü
  - `GET /health/hf` - HuggingFace kullanılabilirlik
  - `GET /models` - Mevcut modeller listesi
  - `POST /chat` - Tek yanıt sohbet
  - `POST /chat/stream` - SSE streaming sohbet

#### 3.1.2. Provider Pattern
- **Kaynak:** `backend/providers/` klasörü
- **Dosyalar:**
  - `base.py` - ModelProvider abstract sınıfı
  - `ollama_provider.py` - Ollama implementasyonu  
  - `huggingface_provider.py` - HuggingFace implementasyonu
  - `registry.py` - Model kayıt ve yönlendirme

**Örnek Kod (base.py):**
```python
class ModelProvider(ABC):
    @abstractmethod
    async def generate(
        self,
        messages: List[Dict[str, str]],
        model_id: str,
        temperature: float = 0.7,
        max_tokens: int = 512,
        cancellation_token: Optional[CancellationToken] = None,
    ) -> ChatResponse:
        pass
```

#### 3.1.3. Request/Response Şemaları
- **Kaynak:** `backend/schemas.py` (221 satır)
- **Pydantic Modeller:**
  - `ChatMessage` - Mesaj validasyonu (role, content)
  - `ChatRequest` - İstek parametreleri (model, messages, RAG ayarları)
  - `ChatResponse` - Yanıt formatı
  - `UsageInfo` - Token kullanım istatistikleri

**Örnek ChatRequest Şeması:**
```python
class ChatRequest(BaseModel):
    model: Optional[str] = None
    messages: list[ChatMessage] = Field(..., min_length=1)
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    max_tokens: int = Field(default=256, ge=1, le=8192)
    stream: bool = False
    rag_enabled: bool = False
    rag_strict: Optional[bool] = None
    rag_top_k: Optional[int] = Field(default=None, ge=1, le=20)
```

#### 3.1.4. Hata Yönetimi
- **Kaynak:** `backend/main.py` içinde exception handler'lar
- **Türkçe Hata Mesajları:** Tüm hatalar kullanıcı dostu Türkçe mesajlarla dönülmektedir
- **Timeout Yönetimi:** Ollama ve HF istekleri için konfigüre edilebilir timeout
- **Retry Logic:** Geçici hatalarda otomatik yeniden deneme

### 3.2. RAG (Retrieval-Augmented Generation)

**Dosya:** `backend/rag_service.py` (467 satır)

#### 3.2.1. Veri Akışı
```
1. Doküman İngest:
   raw_docs → Chunking (200-500 token) → Embedding → FAISS Index
   
2. Sorgu Akışı:
   query → Embedding → FAISS Similarity Search → Top-K Docs → Context
```

#### 3.2.2. Embedding Modeli
- **Model:** `paraphrase-multilingual-MiniLM-L12-v2`
- **Boyut:** 768 dimensions
- **Diller:** 50+ dil (Türkçe dahil)
- **Kaynak:** Sentence Transformers library

#### 3.2.3. Citation Formatı
```python
{
    "context": "... doküman metni ...",
    "citations": [
        {"source": "01_genel_bilgiler.txt", "chunk_id": 3},
        {"source": "04_sss.txt", "chunk_id": 7}
    ]
}
```

### 3.3. Frontend (Flutter + GetX)

**Dosya Sayısı:** 65 Dart dosyası  
**Toplam Kod:** ~5,000 satır  
**Framework:** Flutter 3.x, Dart 3.x

#### 3.3.1. State Yönetimi (GetX)
- **Kaynak:** `lib/controller/` klasörü
- **Ana Controller:** `chat_controller.dart`
- **Sorumluluklar:**
  - Mesaj gönderme/alma
  - Model seçimi
  - RAG toggle
  - Streaming yanıt yönetimi

#### 3.3.2. Ayarlar Kalıcılığı
- **Kaynak:** `lib/controller/settings_controller.dart`
- **Teknoloji:** `shared_preferences` paketi
- **Saklanan Değerler:**
  - Seçili model
  - RAG aktif/pasif durumu
  - Tema tercihi (light/dark)
  - API endpoint URL

#### 3.3.3. UI Akışı
- **Material Design 3:** Tüm ekranlar MD3 standartlarına uyumludur
- **Responsive:** Telefon, tablet ve web layout'ları
- **Markdown Rendering:** `flutter_markdown` ile yanıt görüntüleme

---

## 4. API Sözleşmesi (Gerçek Şema)

### 4.1. GET /health
**Amaç:** Backend sağlık kontrolü

**İstek:** Parametre yok

**Yanıt:**
```json
{
  "status": "ok",
  "message": "Selçuk AI Asistanı backend çalışıyor",
  "timestamp": "2025-01-05T02:15:00Z"
}
```
**Kaynak:** `backend/main.py:150-155`

### 4.2. GET /models
**Amaç:** Mevcut modellerin listesini döndürür

**İstek:** Parametre yok

**Yanıt:**
```json
{
  "models": [
    {
      "id": "ollama:llama3.2:3b",
      "provider": "ollama",
      "model_id": "llama3.2:3b",
      "display_name": "Llama 3.2 3B",
      "local_or_remote": "local",
      "requires_api_key": false,
      "available": true,
      "reason_unavailable": "",
      "context_length": 4096,
      "is_default": true
    },
    {
      "id": "ollama:qwen2:7b",
      "provider": "ollama",
      "model_id": "qwen2:7b",
      "display_name": "Qwen2 7B",
      "available": true,
      "context_length": 4096
    }
  ]
}
```
**Kaynak:** `backend/providers/registry.py:45-80`

### 4.3. POST /chat
**Amaç:** Tek yanıt sohbet

**İstek:**
```json
{
  "model": "ollama:llama3.2:3b",
  "messages": [
    {"role": "user", "content": "Selçuk Üniversitesi nerede?"}
  ],
  "temperature": 0.7,
  "max_tokens": 512,
  "rag_enabled": true,
  "rag_top_k": 4
}
```

**Yanıt:**
```json
{
  "answer": "Selçuk Üniversitesi Konya'dadır. 1975 yılında kurulmuştur...",
  "request_id": "req_abc123...",
  "provider": "ollama",
  "model": "llama3.2:3b",
  "usage": {
    "prompt_tokens": 156,
    "completion_tokens": 89,
    "total_tokens": 245
  },
  "citations": [
    "01_genel_bilgiler.txt",
    "04_sss.txt"
  ]
}
```
**Kaynak:** `backend/main.py:200-280`, `backend/schemas.py:95-120`

### 4.4. POST /chat/stream
**Amaç:** Server-Sent Events ile streaming yanıt

**İstek:** `/chat` ile aynı, `stream: true` eklenmeli

**Yanıt (SSE Format):**
```
data: {"type":"token","token":"Sel"}

data: {"type":"token","token":"çuk"}

data: {"type":"token","token":" Üni"}

data: {"type":"done","usage":{"prompt_tokens":156,"completion_tokens":89}}
```
**Kaynak:** `backend/main.py:282-350`

---

## 5. Çalıştırma Senaryoları

### 5.1. Yerel Geliştirme

#### Backend Başlatma:
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
cp .env.example .env
# .env dosyasını düzenle
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Ollama Başlatma:
```bash
ollama serve
ollama pull llama3.2:3b
ollama pull qwen2:7b
```

#### Flutter Başlatma:
```bash
flutter pub get
cp .env.example .env
flutter run -d chrome  # Web için
flutter run  # Varsayılan cihaz için
```

### 5.2. RAG İndeksleme
```bash
cd backend
python rag_ingest.py --input ../docs --output ./data/rag
# .env dosyasında RAG_ENABLED=true ayarla
```

### 5.3. Docker Deployment (Opsiyonel)
```bash
docker-compose up -d
```

---

## 6. Bilinen Sınırlılıklar ve Riskler

### 6.1. HuggingFace Bağımlılıkları
- **Sorun:** Windows'ta `torch_python.dll` WinError 126 hatası
- **Çözüm:** `docs/SORUN_GIDERME.md:45-78` referans
- **Geçici Çözüm:** Ollama kullanımı önerilmektedir

### 6.2. Offline Kullanım Riskleri
- **Model Cache:** HF modelleri ilk kullanımda internete ihtiyaç duyar
- **Disk Alanı:** 7B modeller ~4-8 GB disk alanı gerektirir
- **Çözüm:** `HF_HOME` ve `TRANSFORMERS_CACHE` ortam değişkenleri

### 6.3. Ollama Timeout
- **Varsayılan:** 120 saniye
- **Büyük Modeller:** 7B+ modeller timeout'a neden olabilir
- **Çözüm:** `OLLAMA_REQUEST_TIMEOUT` ortam değişkeni

### 6.4. RAG İndeks Boyutu
- **Vektör Boyutu:** 768 float32 per document chunk
- **Bellek Kullanımı:** ~1 GB RAM per 100,000 chunks
- **Çözüm:** Chunk size optimizasyonu

---

## 7. Jüri Sunumu için Kanıtlar

### 7.1. CI/CD İş Akışları

#### Backend CI (`github/workflows/backend.yml`)
```yaml
- pytest (50 test, %93 coverage)
- ruff check (kritik + tam lint)
- mypy (18 kaynak dosya, tip hatası yok)
- encoding guard (UTF-8/BOM kontrolü)
```

#### Flutter CI (`.github/workflows/dart.yml`)
```yaml
- flutter analyze
- flutter test
```

### 7.2. Test Komutları

**Backend:**
```bash
python -m pytest -v  # Tüm testler
python -m pytest backend/test_critical_facts.py  # Kritik bilgi testleri
ruff check backend/  # Linting
mypy backend/  # Type checking
```

**Frontend:**
```bash
flutter analyze  # Statik analiz
flutter test  # Widget testleri
```

### 7.3. Smoke Test Script'leri

**API Test:**
```powershell
tools/test_api.ps1
```
Kontrol eder: /health, /models, /chat endpoint'leri

**Encoding Guard:**
```bash
python tools/encoding_guard.py --root .
```
Kontrol eder: UTF-8/BOM, mojibake, karakter encoding

### 7.4. Doğrulanmış Metrikler

| Metrik | Değer | Kanıt |
|--------|-------|-------|
| Backend Dosya Sayısı | 26 | `find backend -name "*.py" \| wc -l` |
| Frontend Dosya Sayısı | 65 | `find lib -name "*.dart" \| wc -l` |
| Test Coverage | %93 | `pytest --cov=backend --cov-report=html` |
| Test Geçme Oranı | 50/50 | `docs/TEST_RAPORU.md:38` |
| Kritik Bilgi Doğruluğu | %100 | `backend/test_critical_facts.py` |

---

## 8. Değişiklik Geçmişi

### Son Güncellemeler (Ocak 2025)
- ✅ Provider Pattern mimarisi implement edildi
- ✅ HuggingFace offline/cache desteği eklendi
- ✅ Flutter Material Design 3 güncellemesi
- ✅ RAG citation formatı iyileştirildi
- ✅ CI/CD pipeline optimize edildi

### Kaldırılan Özellikler
- ❌ Google Gemini API desteği (gizlilik nedeniyle)
- ❌ Appwrite zorunluluğu (opsiyonel hale getirildi)

---

**Son Güncelleme:** 5 Ocak 2025  
**Doküman Sahibi:** Proje Ekibi  
**Versiyon:** 1.0
