# Modeller

Bu doküman, sistemde kullanılan model tiplerini ve seçim mantığını özetler.

## 1) Kategoriler
- **Yerel (Ollama):** Cihazda çalışır. `ollama pull <model>` gerekir.
- **Yerel (HuggingFace / HF):** Backend üzerinde HF model önbelleği (cache/önbellek) gerekir.
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

**Windows notu (DLL / Dinamik Bağlantı Kütüphanesi):**
- `WinError 126` veya `torch_python.dll` hatası alırsanız:
  - Microsoft Visual C++ 2015–2022 Redistributable kurulu olmalı.
  - CPU kullanımı için PyTorch CPU sürümü önerilir:
    ```powershell
    pip install torch --index-url https://download.pytorch.org/whl/cpu
    ```
