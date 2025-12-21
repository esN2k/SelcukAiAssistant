# Benchmarking

This folder contains a simple, reproducible benchmarking harness for Hugging Face
instruction models using the Transformers backend.

## Setup

Install Python deps:

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r benchmark/requirements.txt
```

Install PyTorch separately using the official selector:
https://pytorch.org/get-started/locally/

## Run

Basic run (CPU):

```bash
python benchmark/run.py --models Qwen/Qwen2.5-1.5B-Instruct
```

GPU run with multiple models:

```bash
python benchmark/run.py ^
  --models Qwen/Qwen2.5-7B-Instruct mistralai/Mistral-7B-Instruct-v0.3 ^
  --device cuda ^
  --dtype bfloat16 ^
  --max-new-tokens 256
```

Limit samples:

```bash
python benchmark/run.py --models Qwen/Qwen2.5-1.5B-Instruct --max-samples 3
```

## Outputs

Each run creates a timestamped folder in `benchmark/outputs/` with:

- `results.jsonl`: per-sample outputs + metrics
- `summary.csv`: per-model aggregated metrics
- `summary.md`: markdown table for quick comparison
- `config.json`: run configuration
- `system.json`: system metadata

## Dataset format

JSONL records support either `prompt` or `messages`:

```json
{"id":"s1","task":"qa","language":"en","prompt":"What is DNS?"}
{"id":"s2","task":"chat","language":"en","messages":[{"role":"system","content":"You are helpful."},{"role":"user","content":"Explain TLS in 3 bullets."}]}
```

Note: the sample dataset is ASCII-only. Add your own Turkish prompts as needed.
