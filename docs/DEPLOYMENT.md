# Selçuk YZ Asistan Deployment

This guide focuses on the official web deployment using `/api` reverse proxying
and SSE-friendly settings.

## Build the web app

```powershell
flutter build web --release
```

Copy `build/web` to your web server (nginx/Caddy).

## Run the backend

```powershell
cd backend
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000
```

## Environment variables

- `ALLOWED_ORIGINS` (comma-separated list)
- `ALLOWED_ORIGINS_STRICT=true` to disable dev localhost fallback
- `OLLAMA_BASE_URL`, `OLLAMA_MODEL`
- Optional API keys for remote providers

## Nginx reverse proxy

Use `nginx/selcuk-ai.conf` (SSE-safe). It serves static Flutter web output and
proxies `/api` to the backend with buffering disabled.

## Docker Compose

`docker-compose.yml` includes `backend`, `nginx`, and optional `ollama`:

```powershell
docker compose up --build
docker compose --profile ollama up --build
```

## SSE notes

- Ensure `proxy_buffering off` and `X-Accel-Buffering no`.
- Set a long `proxy_read_timeout` (300s+).
