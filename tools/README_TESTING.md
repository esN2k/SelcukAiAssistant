# API Smoke Testleri (Windows PowerShell)

Bu repo, UTF-8 (BOM yok) JSON yazan ve `curl.exe --data-binary` kullanan Windows uyumlu smoke test scriptleri icerir.

## Onkosullar
- Backend hedef URL'de calismali (varsayilan: `http://localhost:8000`)
- `curl.exe` PATH icinde olmalidir

## Calistirma
```powershell
powershell -ExecutionPolicy Bypass -File tools\test_api.ps1
```

Opsiyonel:
```powershell
powershell -ExecutionPolicy Bypass -File tools\test_api.ps1 -BaseUrl http://localhost:8000 -TimeoutSec 25
```

## Kapsam
- `GET /health`
- `GET /models`
- `POST /chat` (ollama + huggingface, uygunsa)
- `POST /chat/stream` (ollama + huggingface, uygunsa)

Script payloadlari `tools\.tmp\` altina UTF-8 (BOM yok) olarak yazar.
