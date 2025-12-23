# Modeller

## Kategoriler
- **Yerel (Ollama)**: Cihazda calisir, kurulum icin `ollama pull <model>` gerekir.
- **Yerel (HuggingFace)**: Backend uzerinde HF model onbellekleri gerekir.
- **Uzak (API)**: OpenAI/Anthropic/Gemini/xAI gibi servisler, sunucu tarafi API anahtari ister.

## Model secici notlari
- Uygulama modeli secilen kimlik ile saklar.
- Uygunluk rozetleri: `Uygun`, `API anahtari gerekli`, `Yuklu degil`.

## Kurulum ipucu
- Ollama icin ornek: `ollama pull llama3.1`
- HF icin: `backend/requirements-hf.txt` kurulu olmali ve model cache'i hazirlanmalidir.
