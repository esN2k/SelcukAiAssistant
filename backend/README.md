# /backend Klasörü - Python FastAPI Backend

## 📖 Genel Bakış

Bu klasör, Selçuk AI Akademik Asistan projesinin **Python FastAPI backend** servisini içerir.
Backend, Flutter uygulamasından gelen istekleri işler ve yerel LLM (Ollama) ile iletişim kurar.

## 📁 Klasör Yapısı

```
backend/
├── main.py              # FastAPI uygulaması (ana giriş noktası)
├── config.py            # Ortam değişkenleri ve yapılandırma
├── schemas.py           # Pydantic veri modelleri
├── prompts.py           # LLM sistem promptları
├── utils.py             # Yardımcı fonksiyonlar
├── accuracy_guard.py    # Doğruluk kontrolü ve düzeltme
├── rag_service.py       # RAG servisi (FAISS vektör araması)
├── rag_ingest.py        # RAG belge indeksleme
├── response_cleaner.py  # Yanıt temizleme
├── ollama_service.py    # Ollama API sarmalayıcı
├── selcuk_data.py       # Selçuk Üniversitesi verileri
├── providers/           # LLM sağlayıcı adaptörleri
│   ├── base.py          # Temel arayüz (interface)
│   ├── ollama_provider.py
│   ├── huggingface_provider.py
│   └── registry.py      # Model kataloğu
├── data/                # Veri dosyaları
│   ├── rag/             # FAISS indeksleri
│   └── selcuk_knowledge_base.json
├── requirements.txt     # Bağımlılıklar
├── requirements-hf.txt  # HuggingFace bağımlılıkları
├── .env.example         # Ortam değişkenleri şablonu
├── Dockerfile           # Docker imajı
└── test_*.py            # Test dosyaları
```

## 🚀 Çalıştırma

### Hızlı Başlangıç

```bash
cd backend

# Sanal ortam oluştur
python -m venv .venv

# Windows'ta aktifleştir
.venv\Scripts\activate

# Linux/macOS'ta aktifleştir
source .venv/bin/activate

# Bağımlılıkları kur
pip install -r requirements.txt

# Ortam değişkenlerini ayarla
copy .env.example .env  # Windows
cp .env.example .env    # Linux/macOS

# Sunucuyu başlat
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Swagger UI
Tarayıcıda açın: http://localhost:8000/docs

## 📡 API Endpoint'leri

| Endpoint | Metod | Açıklama |
|----------|-------|----------|
| `/` | GET | Basit sağlık kontrolü |
| `/health` | GET | Sistem sağlık durumu |
| `/health/ollama` | GET | Ollama sağlık kontrolü |
| `/health/hf` | GET | HuggingFace sağlık kontrolü |
| `/models` | GET | Kullanılabilir model listesi |
| `/chat` | POST | Senkron sohbet isteği |
| `/chat/stream` | POST | Akış (SSE) sohbet isteği |

### /chat İstek Örneği

```json
{
  "messages": [
    {"role": "user", "content": "Selçuk Üniversitesi nerede?"}
  ],
  "model": "llama3.1",
  "temperature": 0.2,
  "rag_enabled": true
}
```

### /chat Yanıt Örneği

```json
{
  "answer": "Selçuk Üniversitesi **Konya**'dadır...",
  "request_id": "abc123",
  "provider": "ollama",
  "model": "llama3.1",
  "citations": ["docs/README.md (sayfa 1)"]
}
```

## 🔧 Yapılandırma (.env)

```env
# Sunucu
HOST=0.0.0.0
PORT=8000

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1
OLLAMA_TIMEOUT=120

# RAG
RAG_ENABLED=true
RAG_VECTOR_DB_PATH=./data/rag
RAG_TOP_K=4

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

## 📚 RAG (Retrieval-Augmented Generation)

RAG, yanıtları belgelerle destekleyerek doğruluğu artırır.

### RAG İndeksleme

```bash
python rag_ingest.py --input ../docs --output ./data/rag
```

### RAG Ayarları

| Değişken | Açıklama | Varsayılan |
|----------|----------|------------|
| `RAG_ENABLED` | RAG aktif mi | false |
| `RAG_VECTOR_DB_PATH` | İndeks dizini | - |
| `RAG_TOP_K` | Döndürülecek parça sayısı | 4 |
| `RAG_CHUNK_SIZE` | Parça boyutu | 500 |

## 🧪 Testler

```bash
# Tüm testleri çalıştır
python -m pytest -v

# Belirli test dosyası
python -m pytest test_main.py -v

# Kod kalitesi
ruff check .
mypy .
```

## 📁 Ana Dosyaların Açıklaması

| Dosya | Ne Yapar |
|-------|----------|
| **main.py** | FastAPI uygulaması, tüm endpoint'ler burada |
| **config.py** | .env dosyasını okur, ayarları doğrular |
| **schemas.py** | Pydantic ile istek/yanıt doğrulama |
| **prompts.py** | Selçuk Üniversitesi sistem promptları |
| **accuracy_guard.py** | Yanlış bilgi tespiti ve düzeltme |
| **rag_service.py** | FAISS vektör araması ve RAG mantığı |
| **response_cleaner.py** | LLM çıktısından meta içerik temizleme |

## 🏗️ Provider Pattern

Farklı LLM sağlayıcıları aynı arayüz üzerinden çağrılır:

```
ModelProvider (Interface)
       │
       ├── OllamaProvider
       │
       └── HuggingFaceProvider
```

Bu sayede yeni sağlayıcılar kolayca eklenebilir.

## 📝 Notlar

- Ollama kurulu ve çalışıyor olmalı (`ollama serve`)
- RAG için `faiss-cpu` ve `sentence-transformers` gerekli
- HuggingFace için `requirements-hf.txt` kurulmalı
- Windows'ta UTF-8 kodlama otomatik ayarlanır

## Sunucu profili (OMEN RTX 3060)
- Hazır ayarlar: `backend/.env.omen`
- Kullanım (PowerShell): `Copy-Item backend\\.env.omen backend\\.env`

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

