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

## 4) HF Offline ve Önbellek (Cache)
**Amaç:** Model dosyaları önceden indirilerek çevrimdışı (offline) kullanım sağlanır.

Ortam değişkenleri:
- `HF_HOME` (cache kökü)
- `TRANSFORMERS_CACHE` (transformers önbelleği)
- `HUGGINGFACE_HUB_CACHE` (hub önbelleği)
- `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`

Örnek (Windows):
```powershell
$env:HF_HOME="D:\hf_cache"
$env:TRANSFORMERS_CACHE="$env:HF_HOME\transformers"
$env:HUGGINGFACE_HUB_CACHE="$env:HF_HOME\hub"
$env:HF_HUB_OFFLINE=1
$env:TRANSFORMERS_OFFLINE=1
```

Disk planlama: küçük/orta modeller için 5–10 GB aralığı önerilir.

Modeli önceden indirme (internet açıkken):
```bash
python - <<'PY'
from huggingface_hub import snapshot_download
snapshot_download("Qwen/Qwen2.5-1.5B-Instruct")
PY
```
