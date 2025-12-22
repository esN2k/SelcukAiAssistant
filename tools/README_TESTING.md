# API Smoke Tests (Windows PowerShell)

This repo includes a Windows-safe API smoke test script that writes JSON payloads as UTF-8 (no BOM) and uses `curl.exe --data-binary` for POST requests.

## Prereqs
- Backend running on the target URL (default: `http://localhost:8000`)
- `curl.exe` available in PATH (Windows includes it)

## Run
```powershell
powershell -ExecutionPolicy Bypass -File tools\test_api.ps1
```

Optional override:
```powershell
powershell -ExecutionPolicy Bypass -File tools\test_api.ps1 -BaseUrl http://localhost:8000 -TimeoutSec 25
```

## What it tests
- `GET /health`
- `GET /models`
- `POST /chat` (ollama + huggingface, when available)
- `POST /chat/stream` (ollama + huggingface, when available)

The script writes payloads to `tools\.tmp\` using UTF-8 (no BOM).
