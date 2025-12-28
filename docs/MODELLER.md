# Modeller

Bu doküman, sistemde kullanılan model tiplerini ve seçim mantığını özetler.

## 1) Kategoriler
- **Yerel (Ollama):** Cihazda çalışır. `ollama pull <model>` gerekir.
- **Yerel (HuggingFace):** Backend üzerinde HF model önbelleği gerekir.
- **Uzak (API):** OpenAI/Anthropic/Gemini/xAI gibi servisler için API anahtarı gerekir.

## 2) Model Seçici Notları
- Uygulama, seçilen modeli cihazda saklar.
- Uygunluk rozetleri:
  - `Uygun`
  - `API anahtarı gerekli`
  - `Yüklü değil`

## 3) Kurulum İpuçları
Ollama:
```bash
ollama pull llama3.1
```

HuggingFace:
```bash
cd backend
pip install -r requirements-hf.txt
```
Model ağırlıkları ilk çalışmada indirilecektir.
