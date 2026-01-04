# Modeller

Bu doküman, sistemde kullanılan model tiplerini ve seçim mantığını özetler.

## 1) Kategoriler
- **Yerel (Ollama):** Cihazda çalışır. `ollama pull <model>` gerekir.
- **Yerel (HuggingFace / HF):** Arka uç üzerinde HF model önbelleği gerekir.
- **Uzak (API):** OpenAI/Anthropic/Gemini/xAI servisleri için API anahtarı gerekir.

## 2) Model Seçici Notları
- Uygulama, seçilen modeli cihazda saklar.
- Varsayılan (Ollama): `llama3.2:3b` (hız odaklı).
- Kalite odaklı alternatif: `turkcell-llm-7b` (Türkçe dengeli, LoRA planındaki birincil aday).
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
- Microsoft Visual C++ 2015-2022 Redistributable (dağıtım paketi) kurulu olmalıdır.
  - CPU kullanımında PyTorch CPU sürümü önerilir:
    ```powershell
    pip install torch --index-url https://download.pytorch.org/whl/cpu
    ```

## 4) HF Çevrimdışı ve Önbellek
**Amaç:** Model dosyaları önceden indirilerek çevrimdışı kullanım sağlanır.

Ortam değişkenleri:
- `HF_HOME` (önbellek kökü)
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

Disk planlama: küçük/orta modeller için 5-10 GB aralığı önerilir.

Modeli önceden indirme (İnternet açıkken):
```bash
python - <<'PY'
from huggingface_hub import snapshot_download
snapshot_download("Qwen/Qwen2.5-1.5B-Instruct")
PY
```

## 5) LoRA / QLoRA
- LoRA planı: `docs/reports/FINE_TUNING_REPORT.md`
- Veri hazırlama: `tools/prepare_lora_dataset.py`
- Örnek çıktı: `data/finetune/selcuk_lora.jsonl`
- Daha kaliteli çıktı için `--use-ollama` parametresi kullanılabilir.
