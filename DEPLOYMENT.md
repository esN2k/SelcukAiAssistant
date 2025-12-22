# Deployment Guide

This project ships as a Flutter web app with a FastAPI backend. The web build
expects the backend to be available at the same origin under `/api`.

## 1) Build Flutter Web

From the repo root:

```powershell
D:\Flutter\flutter\bin\flutter.bat build web --release
```

Upload `build/web` to your web server (nginx/Caddy/etc).

## 2) Backend Production Run

Create a venv, install deps, and run:

```powershell
cd backend
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000
```

For a production process manager:

```powershell
.\.venv\Scripts\python.exe -m pip install "gunicorn>=21"
.\.venv\Scripts\python.exe -m gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

## 3) Environment Variables (Backend)

Copy `backend/.env.example` to `backend/.env` and update:

- `ALLOWED_ORIGINS` (prefer explicit origins)
- `OLLAMA_BASE_URL`, `OLLAMA_MODEL`
- `MODEL_BACKEND` (`ollama` or `huggingface`)
- `MAX_CONTEXT_TOKENS`, `MAX_OUTPUT_TOKENS`, `REQUEST_TIMEOUT`
- Optional API keys for remote models:
  - `OPENAI_API_KEY`
  - `ANTHROPIC_API_KEY`
  - `GOOGLE_API_KEY` or `GEMINI_API_KEY`
  - `XAI_API_KEY`

Note: If `ALLOWED_ORIGINS="*"`, credentials are disabled by the backend.

## 4) Reverse Proxy (nginx)

Use the provided `nginx.conf` as a starting point. It serves the Flutter web
build at `/` and proxies the backend at `/api` with SSE-friendly settings.

## 5) HTTPS

Terminate TLS at the proxy (nginx/Caddy). Ensure your backend is reachable only
from the proxy in production.
