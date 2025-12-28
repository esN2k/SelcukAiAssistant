# Kurulum Rehberi (Windows / Linux / macOS)

Bu doküman, Selçuk AI Akademik Asistan projesini yerel ortamda çalıştırmak için
gerekli adımları içerir. Backend (FastAPI) ve frontend (Flutter) birlikte
çalıştırılır.

## 1) Önkoşullar
- **Python 3.11+ (öneri: 3.12)**
- **Flutter (Stable)**
- **Git**
- **Ollama** (yerel LLM için)
- (Opsiyonel) **Docker** ve **Docker Compose**

> Not: Backend bağımlılıklarında (pydantic-core, faiss-cpu, torch) Python 3.14 için
> hazır wheel bulunmayabilir. Yerel geliştirme ve testler için Python 3.12 önerilir.

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

> Windows'ta birden fazla Python sürümü varsa 3.12 ile venv oluşturun:
> `py -3.12 -m venv .venv`

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

### 4.1) HuggingFace (HF) opsiyonel kurulum
> HuggingFace (HF), yerel modelleri indirmek için kullanılan açık model deposudur.

```bash
cd backend
pip install -r requirements-hf.txt
```

### 4.2) HF Offline / Önbellek (Cache) Ayarları
**Amaç:** Model dosyaları önceden indirilerek çevrimdışı (offline) kullanım sağlanır.

Önerilen ortam değişkenleri:
- `HF_HOME`: HuggingFace ana dizini (cache kökü)
- `TRANSFORMERS_CACHE`: Transformers cache dizini
- `HUGGINGFACE_HUB_CACHE`: Hub cache dizini
- `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`: çevrimdışı mod

**Windows (PowerShell):**
```powershell
$env:HF_HOME="D:\hf_cache"
$env:TRANSFORMERS_CACHE="$env:HF_HOME\transformers"
$env:HUGGINGFACE_HUB_CACHE="$env:HF_HOME\hub"
$env:HF_HUB_OFFLINE=1
$env:TRANSFORMERS_OFFLINE=1
```

**Linux/macOS:**
```bash
export HF_HOME="$HOME/.cache/huggingface"
export TRANSFORMERS_CACHE="$HF_HOME/transformers"
export HUGGINGFACE_HUB_CACHE="$HF_HOME/hub"
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
```

**Model önceden indirme (internet açıkken):**
```bash
python - <<'PY'
from huggingface_hub import snapshot_download
snapshot_download("Qwen/Qwen2.5-1.5B-Instruct")
PY
```

**Disk planlama:** 5–10 GB aralığı küçük/orta modeller için önerilir.

**Doğrulama adımı (cache kontrolü):**
```powershell
dir $env:HF_HOME
```

**Windows DLL (Dinamik Bağlantı Kütüphanesi) notu:**
- `WinError 126` veya `torch_python.dll` hatası alırsanız:
  1. **Microsoft Visual C++ 2015–2022 Redistributable** kurulu olmalı (çalışma zamanı bağımlılığı).
  2. CPU kullanacaksanız PyTorch CPU sürümünü kurun:
     ```powershell
     pip install torch --index-url https://download.pytorch.org/whl/cpu
     ```
  3. GPU kullanacaksanız PyTorch sürümünüz CUDA sürümüyle uyumlu olmalı.
  4. Geçici çözüm olarak terminal oturumunda `torch\lib` dizinini PATH'e ekleyin:
     ```powershell
     $env:Path += ";$env:VIRTUAL_ENV\\Lib\\site-packages\\torch\\lib"
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
