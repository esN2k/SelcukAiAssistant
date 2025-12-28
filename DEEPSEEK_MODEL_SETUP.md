# DeepSeek Model Kurulumu (Opsiyonel)

Bu doküman, yerel DeepSeek modelini Ollama üzerinden kurmak için kısa bir özet sunar.

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
- Model boyutu büyüktür; indirme süresi internete bağlıdır.
- GPU kullanımı için uygun sürücülerin kurulu olduğundan emin olun.
