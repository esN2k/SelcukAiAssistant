# DeepSeek Model Kurulumu (Opsiyonel)

Bu dokuman, yerel DeepSeek modelini Ollama uzerinden kurmak icin kisa bir ozet sunar.

## Otomatik kurulum (Windows)
```powershell
cd backend
.\setup_deepseek.ps1
```

## Manuel kurulum
```bash
ollama serve
ollama pull deepseek-r1:8b
```

## Notlar
- Model boyutu buyuktur; indirme suresi internete baglidir.
- GPU kullanimi icin uygun suruculerin kurulu oldugundan emin olun.
