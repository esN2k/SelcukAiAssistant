# SelcukAiAssistant

esN2k/SelcukAiAssistant · "SelcukAiAssistant"

## 1. Özet ve Özellikler

- **Hibrit mimari**: Python FastAPI backend + Flutter (Android, iOS, Web, Desktop) istemci;
  opsiyonel C++ hızlandırıcı katmanı.
- **Ollama tabanlı LLM**: Llama 3.1 veya `selcuk_ai_assistant` modeli ile yerel, düşük gecikmeli
  yanıtlar.
- **RAG hazırlığı**: ChromaDB destekli belge alımı ve vektör araması için hazır iskelet (şimdilik
  devre dışı).
- **Streaming & güvenlik**: SSE tabanlı akış, giriş doğrulama, XSS koruması ve isteğe bağlı CORS
  kısıtları.
- **Konteyner ve otomasyon**: Docker tabanlı çalışma, GitHub Actions (dart.yml) ile kalite kontrol,
  gelecekte ek pipeline'lara hazır yapı.

## 2. Mimari ve Teknoloji Yığını

| Katman          | Teknolojiler                                       | Detay                                                                 |
|-----------------|----------------------------------------------------|-----------------------------------------------------------------------|
| **Frontend**    | Flutter 3.x, Dart, GetX, flutter_dotenv, Hive      | Mobil/web arayüzü, `.env` ile `BACKEND_URL` okur                      |
| **Backend**     | Python 3.11+, FastAPI, Uvicorn, Pydantic, Requests | `/chat`, `/chat/stream`, `/health` uç noktaları, Ollama proxy         |
| **LLM Katmanı** | Ollama + (Llama3.1 \| selcuk_ai_assistant)         | Yerel inference, retry/backoff, UTF-8 desteği                         |
| **RAG**         | ChromaDB (planlanan), sentence-transformers, pypdf | `rag_service.py` içinde hazırlanan entegrasyon iskeleti               |
| **Native**      | C++/CMake, platform-specific runner dosyaları      | Flutter masaüstü/webview eklentileri ve izin köprüleri                |
| **CI/CD**       | GitHub Actions (`.github/workflows/dart.yml`)      | `flutter analyze`, `flutter test`, gelecekte `pytest`, `ruff`, `mypy` |
| **Dağıtım**     | Docker, Opsiyonel K8s/VM                           | Backend konteyneri + Ollama servisi, reverse proxy üzerinden TLS      |

```
Flutter UI → FastAPI Backend (/chat, /chat/stream) → Ollama → (Opsiyonel) RAG ChromaDB
```

## 3. Kurulum Önkoşulları

- **Zorunlu**: Git, Python 3.11+, Flutter SDK 3.24+, Node/Android toolchain (hedef platformlara
  göre), CMake 3.28+ (masaüstü).
- **Yapay Zeka**: [Ollama](https://ollama.com/) + `ollama pull llama3.1` veya özel model.
- **Opsiyonel**: Docker Desktop/Engine, GPU sürücüleri, Appwrite hesabı (`<APPWRITE_PROJECT_ID>`
  vb.).

### Kurulum Adımları
```bash
# 1) Depoyu alın
git clone https://github.com/esN2k/SelcukAiAssistant.git
cd SelcukAiAssistant

# 2) Backend kurulumu
cd backend
python -m venv .venv
.venv\Scripts\activate    # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # değerleri aşağıdaki tabloya göre düzenleyin

# 3) Flutter kurulumu
cd ..
flutter pub get
cp .env.example .env       # BACKEND_URL vb. için
```

## 4. Çalıştırma

- **Ollama**
  ```bash
  ollama serve &
  ollama pull selcuk_ai_assistant   # yoksa: ollama pull llama3.1
  ```
- **Backend (geliştirme)**
  ```bash
  cd backend
  .venv\Scripts\activate
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
  ```
- **Backend (production)**
  ```bash
  uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 4
  ```
- **Flutter istemci**
  ```bash
  flutter run                  # otomatik cihaz seçimi
  flutter run -d chrome        # web
  flutter run -d <device-id>   # belirli hedef
  ```
- **Docker (backend)**
  ```bash
  cd backend
  docker build -t selcuk-ai-backend .
  docker run --rm -p 8000:8000 --env-file .env selcuk-ai-backend
  ```

## 5. Yapılandırma (.env)

| Anahtar               | Konum                            | Örnek Değer                      | Açıklama                          |
|-----------------------|----------------------------------|----------------------------------|-----------------------------------|
| `BACKEND_URL`         | Proje kökü `.env`                | `http://10.0.2.2:8000`           | Flutter istemcisinin API tabanı   |
| `API_KEY`             | Proje kökü `.env`                | (boş)                            | Eski Gemini uyumluluğu, opsiyonel |
| `HOST`                | `backend/.env`                   | `0.0.0.0`                        | FastAPI bind adresi               |
| `PORT`                | `backend/.env`                   | `8000`                           | FastAPI portu                     |
| `ALLOWED_ORIGINS`     | `backend/.env`                   | `https://app.example.com`        | CORS listesi                      |
| `OLLAMA_BASE_URL`     | `backend/.env`                   | `http://localhost:11434`         | Ollama API adresi                 |
| `OLLAMA_MODEL`        | `backend/.env`                   | `selcuk_ai_assistant`            | Varsayılan model                  |
| `OLLAMA_TIMEOUT`      | `backend/.env`                   | `120`                            | Saniye cinsinden timeout          |
| `OLLAMA_MAX_RETRIES`  | `backend/.env`                   | `3`                              | Retry sayısı                      |
| `LOG_LEVEL`           | `backend/.env`                   | `INFO`                           | FastAPI/uvicorn log seviyesi      |
| `RAG_ENABLED`         | `backend/.env`                   | `false`                          | ChromaDB entegrasyonu             |
| `RAG_VECTOR_DB_PATH`  | `backend/.env`                   | `./data/chromadb`                | Vektör veritabanı yolu            |
| `APPWRITE_ENDPOINT`   | `<backend/.env veya proje .env>` | `<https://cloud.appwrite.io/v1>` | Gelecek Appwrite entegrasyonu     |
| `APPWRITE_PROJECT_ID` | `<...>`                          | `<proj-id>`                      | Opsiyonel                         |
| `APPWRITE_API_KEY`    | `<...>`                          | `<api-key>`                      | Opsiyonel                         |

> Not: Üretimde gizli anahtarlar için `<Secret Manager>` veya GitHub Actions Secrets tercih edin.

## 6. Klasör Yapısı
```
SelcukAiAssistant/
├─ lib/                    # Flutter ekranları, controller, service, widget
├─ assets/                 # Görseller, lottie animasyonları, fonts
├─ backend/
│  ├─ main.py
│  ├─ config.py
│  ├─ ollama_service.py
│  ├─ rag_service.py       # RAG placeholder
│  ├─ prompts.py
│  ├─ test_main.py
│  ├─ test_extended.py
│  ├─ requirements*.txt
│  └─ README.md
├─ android/, ios/, web/, windows/   # Platform hedefleri
├─ docs/ (final_raporu, vize_raporu)
├─ ARCHITECTURE.md, MIGRATION.md, QUICKSTART.md, SUMMARY.md
└─ test/ (Flutter widget testleri)
```

## 7. Komut Referansı

| Amaç                       | Komut                                                                                         |
|----------------------------|-----------------------------------------------------------------------------------------------|
| Flutter bağımlılıkları     | `flutter pub get`                                                                             
| Flutter temiz build        | `flutter clean && flutter pub get`                                                            
| Flutter çalıştır           | `flutter run -d <device>`                                                                     
| Backend bağımlılık         | `pip install -r backend/requirements.txt`                                                     
| Backend testleri           | `cd backend && pytest -v`                                                                     
| Backend lint               | `cd backend && ruff check .`                                                                  
| Backend type-check         | `cd backend && mypy .`                                                                        
| Backend format (opsiyonel) | `cd backend && ruff format .`                                                                 
| Docker build/run           | `docker build -t selcuk-ai-backend backend && docker run --rm -p 8000:8000 selcuk-ai-backend` 

## 8. Test · Lint · Tip Kontrol · CI

| Kapsam                 | Araç/Komut                                | Durum                                                                         |
|------------------------|-------------------------------------------|-------------------------------------------------------------------------------|
| Backend birim testleri | `pytest test_main.py test_extended.py -v` | 30+ senaryo, Ollama mock, health, SSE                                         |
| Backend lint           | `ruff check .`                            | PEP8 + import sırası                                                          |
| Backend type-check     | `mypy .`                                  | (isteğe bağlı, `<mypy.ini>` yoksa ekleyin)                                    |
| Flutter analiz         | `flutter analyze`                         | CI `dart.yml` içinde çalışır                                                  |
| Flutter test           | `flutter test`                            | Varsayılan widget testi + eklenebilir                                         |
| Güvenlik taraması      | `<pip-audit veya safety>`                 | Opsiyonel                                                                     |
| Backend CI             | `.github/workflows/backend.yml`           | Push/PR tetikleyicisi (`ruff`, `mypy`, `pytest` işlerini çalıştırır)          |
| Flutter CI             | `.github/workflows/dart.yml`              | Push/PR tetikleyicisi (`flutter analyze`, `flutter test` işlerini çalıştırır) |

## 9. Dağıtım Stratejileri

- **Docker tek sunucu**: FastAPI konteyneri + aynı hostta Ollama. Reverse proxy (nginx/Caddy) ile
  HTTPS, `ALLOWED_ORIGINS` kısıtlı.
- **Çift düğüm**: FastAPI (Fly.io/Railway/Render) + GPU'lu Ollama VM (RunPod, LambdaLabs).
  BACKEND_URL ve OLLAMA_BASE_URL güncellenir.
- **Kubernetes**: `Deployment` (FastAPI) + `StatefulSet` (Ollama) + `PersistentVolume` (model
  cache). HPA ve node selector ile kaynak yönetimi.
- **CI/CD**: `<Preferred provider>` üzerinden container push + ortam değişkeni yönetimi (
  `<Vault/Secret Manager>`).
- **Versiyonlama**: SemVer (`1.0.2+2`) Flutter tarafında tutulur; backend için `<git tag>` önerilir.

## 10. Gözlemlenebilirlik

- **Loglama**: Uvicorn/Flutter logları varsayılan olarak stdout'a düşer. Prod'da JSON log formatı
  için `LOG_LEVEL=INFO` + `uvicorn --log-config`. Flutter'da `<Crashlytics/Sentry>` entegrasyonu
  önerilir.
- **Health Check**: `GET /` ve `GET /health/ollama` endpoint'leri uptime monitörlerine bağlanabilir.
- **Metric/Trace**: `<Prometheus/OpenTelemetry>` entegrasyonu planlanıyor. FastAPI için
  `prometheus-fastapi-instrumentator`, Flutter için `<analytics SDK>` değerlendirilebilir.
- **Alerting**: `<Grafana Cloud / Azure Monitor / CloudWatch>` ile CPU, RAM, model gecikmeleri
  izlenebilir.
- **Log rotation**: Docker/K8s ortamlarında merkezi log (ELK/EFK/Loki) önerilir.
- **Prometheus/Grafana Kurulumu (Örnek)**:
  ```bash
  # prometheus-fastapi-instrumentator kurulumu (backend)
  pip install prometheus-fastapi-instrumentator
  # main.py içine: Instrumentator().instrument(app).expose(app)
  # prometheus.yml config dosyası oluşturup FastAPI portunu (8000) dinlemeye başlayın.
  ```

## 11. Yol Haritası

1. **Kısa vade (<3 ay)**: RAG pipeline'ını etkinleştirme, `rag_service.py` + ChromaDB + ingestion
   araçları.
2. **Orta vade (<6 ay)**: Appwrite kimlik doğrulama + kullanıcı oturumu, mobil UI'da sohbet geçmişi
   eşitleme.
3. **Uzun vade**: Çoklu model desteği (GPU/CPU), otomatik benchmark, Prometheus/Grafana tabanlı
   gözlemlenebilirlik paketi, `<Kurumsal dağıtım hedefi>`.
4. **Sürekli**: Test kapsamasını artırma (Flutter widget, backend contract test), CI'da güvenlik
   taramaları.

## 12. Katkı Rehberi

- Depoyu fork'layın, `feature/<kısa-ad>` dalı açın.
- Değişiklik öncesi `flutter analyze`, `flutter test`, `pytest`, `ruff`, `mypy` komutlarını
  çalıştırın.
- Gerekli yerlerde dokümantasyonu güncelleyin (`README`, `ARCHITECTURE`, `.env.example`).
- PR açıklamasında: kapsam, test sonuçları, ilgili issue/link.
- Kod tarzı: Python için PEP8 + type hints, Dart için `dart format` (`flutter format`) uygulanmalı.
- Büyük özellikler için önce issue açarak tartışın; iletişim kanalı `<Discord/Slack/Email>` olarak
  belirlenecek.

## 13. Lisans

- Proje **MIT Lisansı** ile yayımlanır. Ayrıntılar için `LICENSE` dosyasını kontrol edin veya yoksa
  aşağıdaki ifadeyi kullanın:
  ```text
  MIT License
  Copyright (c) <2024> <esN2k>
  ...
  ```
- Üçüncü parti bileşenler (Ollama modelleri, Appwrite SDK'ları) kendi lisanslarına tabidir.

---
> Eksik bilgiler `<...>` ile işaretlenmiştir. Örn. Appwrite değişkenleri, tercih edilen cloud
> sağlayıcısı veya gözlemlenebilirlik araçları netleştiğinde README güncellenmelidir.
