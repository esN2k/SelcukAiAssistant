# API Duman Testleri (Windows PowerShell)

Bu depo, UTF-8 (BOM'suz) JSON yazan ve `curl.exe --data-binary` kullanan Windows uyumlu duman testi betikleri içerir.

## Önkoşullar
- Arka uç hedef URL'de çalışmalı (varsayılan: `http://localhost:8000`)
- `curl.exe` PATH içinde olmalıdır

## Çalıştırma
```powershell
powershell -ExecutionPolicy Bypass -File tools\test_api.ps1
```

İsteğe bağlı:
```powershell
powershell -ExecutionPolicy Bypass -File tools\test_api.ps1 -BaseUrl http://localhost:8000 -TimeoutSec 25
```

Yerel model yoksa testleri atlamak için:
```powershell
powershell -ExecutionPolicy Bypass -File tools\test_api.ps1 -AllowNoModel
```

Raporlu duman testi:
```powershell
powershell -ExecutionPolicy Bypass -File tools\smoke_test.ps1 -AllowNoModel
```

## Kapsam
- `GET /health`
- `GET /models`
- `POST /chat` (Ollama + HuggingFace, uygunsa)
- `POST /chat/stream` (Ollama + HuggingFace, uygunsa)

Betik istek yüklerini `tools\.tmp\` altına UTF-8 (BOM'suz) olarak yazar.
