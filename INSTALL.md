# Kurulum Rehberi (Windows / Linux / macOS)

Bu doküman, Selçuk AI Akademik Asistan projesini yerel ortamda çalıştırmak için
gerekli adımları içerir. Backend (FastAPI) ve frontend (Flutter) birlikte
çalıştırılır.

## 1) Önkoşullar
- **Python 3.11+**
- **Flutter (Stable)**
- **Git**
- **Ollama** (yerel LLM için)
- (Opsiyonel) **Docker** ve **Docker Compose**

## 2) Depoyu klonlama
```bash
git clone <repo-url>
cd SelcukAiAssistant
```

## 3) Ollama kurulumu ve model indirme
### Windows
1. https://ollama.com/download adresinden Windows sürümünü kurun.
2. Komut satırında modeli indirin:
   ```bash
   ollama pull llama3.1
   ```

### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1
```

### macOS
```bash
brew install ollama
ollama pull llama3.1
```

> Not: Özel model kullanıyorsanız `backend/Modelfile` veya `backend/Modelfile.deepseek`
> üzerinden `ollama create` ile özel model oluşturabilirsiniz.

## 4) Backend kurulumu (FastAPI)
```bash
cd backend
python -m venv .venv
```

### Windows
```bash
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Linux / macOS
```bash
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 5) Flutter kurulumu ve çalıştırma
```bash
flutter pub get
```

### Windows
```bash
copy .env.example .env
flutter run
```

### Linux / macOS
```bash
cp .env.example .env
flutter run
```

## 6) RAG (Kaynaklı Yanıt) kurulumu
1. Belgeleri indeksleyin:
   ```bash
   cd backend
   python rag_ingest.py --input ../docs --output ./data/rag
   ```
2. `backend/.env` dosyasını güncelleyin:
   ```
   RAG_ENABLED=true
   RAG_VECTOR_DB_PATH=./data/rag
   ```

## 7) Sağlık kontrolü
```bash
curl http://localhost:8000/health
curl http://localhost:8000/models
```

## 8) Sorun giderme
Detaylı hata senaryoları için `docs/SORUN_GIDERME.md` dosyasına bakın.
