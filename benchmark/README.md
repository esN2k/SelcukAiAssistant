# Kıyaslama

Bu klasör model karşılaştırma testleri içindir.

## Çalıştırma
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r benchmark/requirements.txt
python benchmark/run.py --models Qwen/Qwen2.5-1.5B-Instruct
```

Sonuçlar `benchmark/results/` altında saklanır.
