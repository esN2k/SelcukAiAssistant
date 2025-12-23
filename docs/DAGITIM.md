# Dagitim

Bu dokuman Selcuk YZ Asistan icin yerel, self-host ve konteyner dagitimini ozetler.

## Yerel calistirma
- Backend: `backend/.env` ayarlarini yapin ve `uvicorn main:app --reload` ile baslatin.
- Flutter: proje kokunde `.env` olusturun ve `flutter run` calistirin.

## Docker (tek servis)
```bash
cd backend
docker build -t selcuk-ai-backend .
docker run --rm -p 8000:8000 --env-file .env selcuk-ai-backend
```

## Docker Compose (backend + opsiyonel proxy)
- `docker-compose.yml` dosyasi backend servisini ayaga kaldirir.
- Proxy gerekiyorsa `nginx/` altindaki ornekleri kullanin.

## Nginx /api (SSE destekli)
- `nginx.conf` ve `nginx/` altindaki konfigler SSE icin uygun basliklari ekler.
- SSE icin `X-Accel-Buffering: no` ve `Cache-Control: no-cache` tavsiye edilir.

## Ortam degiskenleri
- Backend icin `backend/.env`, Flutter icin proje kokundeki `.env` kullanilir.
- RAG acilacaksa `RAG_ENABLED=true` ve FAISS indeks yolu belirtilmelidir.
