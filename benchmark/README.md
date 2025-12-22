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

Optional GPU extras:

- 4-bit/8-bit quantization: `pip install bitsandbytes`
- VRAM tracking: `pip install pynvml`

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

Download-only (prefetch HF snapshots and exit):

```bash
python benchmark/run.py --models Qwen/Qwen2.5-1.5B-Instruct --download-only
```

## CPU vs GPU

- CPU: `--device cpu` (defaults to fp32)
- GPU: `--device cuda` (defaults to 4-bit on CUDA unless `--quant` is set)

Example (RTX 3060 6GB):

```bash
python benchmark/run.py ^
  --dataset benchmark/datasets/dev_eval_tr_en.jsonl ^
  --models Qwen/Qwen2.5-1.5B-Instruct HuggingFaceTB/SmolLM2-1.7B-Instruct ^
  --device cuda ^
  --quant 4bit ^
  --max-new-tokens 256
```

## Preflight + auth

- Ollama models use the `ollama:` prefix. The runner checks Ollama is reachable
  and that the model exists. Use `--strict` to fail fast.
- Gated Hugging Face models require accepting the model terms on HF and setting
  `HF_TOKEN` (or `--hf-token`).

## HF download robustness

Tunable flags:

- `--hf-timeout` (metadata timeout, seconds)
- `--hf-retries` (retry count)
- `--hf-max-workers` (parallel download workers)

Optional transfer speed-up:

```bash
set HF_HUB_ENABLE_HF_TRANSFER=1
```

## Outputs

Each run creates a timestamped folder in `benchmark/outputs/` with:

- `results.jsonl`: per-sample outputs + metrics
- `summary.csv`: per-model aggregated metrics
- `summary.md`: markdown table for quick comparison
- `config.json`: run configuration
- `system.json`: system metadata

The summary tables now include provider, quantization, device, dtype, prompt token
stats, download/load/warmup timing, and grouped error reasons.

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

| model | provider | quant | device | dtype | params | context | avg_prompt_tokens | max_prompt_tokens | download_s | load_s | warmup_s | avg_ttft_ms | avg_tok_s | avg_out_tokens | avg_total_time_s | peak_vram_mb | peak_ram_mb | errors | error_reasons |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ollama:selcuk_ai_assistant | ollama |  | ollama |  |  |  | 20.1 | 43 | 0.0 | 0.0 | 0.0 | 1326.27 | 7.1 | 63.2 | 9.029 |  | 278 | 0 | {} |
| Qwen/Qwen2.5-1.5B-Instruct | huggingface | fp32 | cpu | float32 | 1543714304 | 32768 | 27.4 | 72 | 0.0 | 3.57 | 4.277 | 857.51 | 3.35 | 61.2 | 18.165 |  | 6340 | 0 | {} |
| HuggingFaceTB/SmolLM2-1.7B-Instruct | huggingface | fp32 | cpu | float32 | 1711376384 | 8192 | 30.4 | 78 | 0.0 | 3.19 | 1.858 | 1016.51 | 2.04 | 27.1 | 8.711 |  | 9774 | 0 | {} |

Notes:
- Ollama baseline ran successfully in this pass.
- Gated models (e.g., google/gemma-2-2b-it) require HF auth; set `HF_TOKEN`.

Raw summaries are stored in `benchmark/results/`.
