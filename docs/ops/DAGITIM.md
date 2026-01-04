# Dağıtım

Bu doküman Selçuk AI Asistanı için yerel, self-host ve konteyner dağıtımını özetler.

## 1) Yerel Çalıştırma
- Backend: `backend/.env` ayarlarını yapın ve `uvicorn main:app --reload` ile başlatın.
- Flutter: proje kökünde `.env` oluşturun ve `flutter run` çalıştırın.
- HuggingFace (HF) kullanacaksanız `backend/requirements-hf.txt` kurulumunu yapın.
  Windows’ta DLL (Dinamik Bağlantı Kütüphanesi) bağımlılıkları için
  `docs/SORUN_GIDERME.md` notlarına bakın.

## 2) Docker (Tek Servis)
```bash
cd backend
docker build -t selcuk-ai-backend .
docker run --rm -p 8000:8000 --env-file .env selcuk-ai-backend
```

## 3) Docker Compose (Backend + Opsiyonel Proxy)
- `docker-compose.yml` dosyası backend servisini ayağa kaldırır.
- Proxy gerekiyorsa `nginx/` altındaki örnekleri kullanın.
> Not: HF modelleri konteyner içinde ek disk alanı ve (GPU varsa) CUDA runtime gerektirir.

HF bağımlılıklarıyla build etmek için:
```bash
INSTALL_HF=true docker compose build
INSTALL_HF=true docker compose up
```

HF önbelleğini kalıcı yapmak için compose volume `hf-cache` kullanılmaktadır.

## 4) Nginx /api (SSE Destekli)
- `nginx/nginx.conf` ve `nginx/` altındaki konfigler SSE için uygun başlıkları ekler.
- SSE için `X-Accel-Buffering: no` ve `Cache-Control: no-cache` tavsiye edilir.

## 5) Ortam Değişkenleri
- Backend için `backend/.env`, Flutter için proje kökündeki `.env` kullanılır.
- RAG açılacaksa `RAG_ENABLED=true` ve FAISS indeks yolu belirtilmelidir.
