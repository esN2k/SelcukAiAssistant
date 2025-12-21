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

## Project dataset

Use `benchmark/datasets/dev_eval_tr_en.jsonl` for Turkish + English evaluation.

Example run:

```bash
python benchmark/run.py --dataset benchmark/datasets/dev_eval_tr_en.jsonl --models Qwen/Qwen2.5-1.5B-Instruct
```

Ollama baseline (requires Ollama running locally):

```bash
python benchmark/run.py --dataset benchmark/datasets/dev_eval_tr_en.jsonl --models ollama:selcuk_ai_assistant
```

## Latest Results (dev_eval_tr_en)

Environment: CPU only (torch.cuda.is_available() == False). Max new tokens: 64.

| model | params | context | load_s | avg_ttft_ms | avg_tok_s | avg_out_tokens | avg_total_time_s | peak_vram_mb | peak_ram_mb | errors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ollama:selcuk_ai_assistant |  |  | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  | 277 | 25 |
| Qwen/Qwen2.5-1.5B-Instruct | 1543714304 | 32768 | 6.48 | 995.7 | 3.03 | 60.1 | 19.677 |  | 6331 | 0 |
| HuggingFaceTB/SmolLM2-1.7B-Instruct | 1711376384 | 8192 | 576.09 | 1162.62 | 1.86 | 26.7 | 9.869 |  | 9746 | 0 |

Notes:
- Ollama baseline returned 25 errors because the local Ollama service was not reachable during the run.
- google/gemma-2-2b-it is gated; download requires HF auth (401).
- microsoft/Phi-3-mini-4k-instruct download timed out on the first attempt.

Raw summaries are stored in `benchmark/results/`.
