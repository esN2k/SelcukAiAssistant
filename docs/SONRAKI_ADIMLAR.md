# Sonraki Adımlar

## 1) LoRA Veri Seti (Ollama destekli)
- Hedef: Selçuk Üniversitesi metinlerinden 200 örneklik LoRA dataseti üretmek.
- Önerilen model: llama3.2:3b (daha hızlı ve stabil)
- Komut:
```powershell
python tools\prepare_lora_dataset.py ^
  --input data\processed_web\docs ^
  --output data\finetune\selcuk_lora_ollama_200.jsonl ^
  --use-ollama --ollama-model llama3.2:3b ^
  --max-samples 200 --ollama-timeout 120 --ollama-retries 2
```
- Çıktı: data/finetune/selcuk_lora_ollama_200.jsonl (200 örnek)
- Durum: tamamlandı (2025-12-29)

## 2) Varsayılan Model Seçimi
- Mevcut varsayılan: llama3.2:3b
- Kalite odaklı alternatif: turkcell-llm-7b
- Karar sonrası güncelleme dosyaları:
  - backend/.env (lokal çalıştırma)
  - backend/.env.example (dokümantasyon)
  - docs/MODELLER.md (notlar)
- Durum: tamamlandı (2025-12-29)

## 3) Kalite Doğrulama
- Benchmark raporuna göre seçilen modelle 12 örnek tam koşum (max_samples=12)
- Komut:
```powershell
python benchmark\run.py ^
  --models ollama:llama3.2:3b ^
  --dataset benchmark\data\selcuk_tr.jsonl ^
  --ollama-url http://127.0.0.1:11435 ^
  --max-new-tokens 96 --temperature 0.2 --max-samples 12
```
- Sonuç: benchmark/outputs/20251229_204933/summary.csv
- Durum: tamamlandı (2025-12-29)
