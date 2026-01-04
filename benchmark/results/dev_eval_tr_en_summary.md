Bu tablo, `benchmark/run.py` özet çıktısıdır. Başlıklar Türkçeleştirilmiştir; değerler aynıdır.

| model | sağlayıcı | nicemleme | cihaz | veri_türü | parametre_sayısı | bağlam | ort_girdi_belirteç | maks_girdi_belirteç | indirme_sn | yükleme_sn | ısınma_sn | ort_ttft_ms | ort_belirteç_sn | ort_çıktı_belirteç | ort_toplam_süre_sn | tepe_vram_mb | tepe_ram_mb | hata | hata_nedenleri |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ollama:selcuk_ai_assistant | ollama |  | ollama |  |  |  | 20.1 | 43 | 0.0 | 0.0 | 0.0 | 1326.27 | 7.1 | 63.2 | 9.029 |  | 278 | 0 | {} |
| Qwen/Qwen2.5-1.5B-Instruct | huggingface | fp32 | cpu | float32 | 1543714304 | 32768 | 27.4 | 72 | 0.0 | 3.57 | 4.277 | 857.51 | 3.35 | 61.2 | 18.165 |  | 6340 | 0 | {} |
| HuggingFaceTB/SmolLM2-1.7B-Instruct | huggingface | fp32 | cpu | float32 | 1711376384 | 8192 | 30.4 | 78 | 0.0 | 3.19 | 1.858 | 1016.51 | 2.04 | 27.1 | 8.711 |  | 9774 | 0 | {} |
