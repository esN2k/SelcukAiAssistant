#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import json
import os
import random
import sys
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from threading import Thread
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests

try:
    import psutil
except ImportError as exc:  # pragma: no cover - optional dependency guard
    raise SystemExit("psutil is required. Install from benchmark/requirements.txt") from exc

try:
    import pynvml  # type: ignore
except ImportError:  # pragma: no cover - optional dependency guard
    pynvml = None


torch = None
HfApi = None
login = None
snapshot_download = None
GatedRepoError = None
HfHubHTTPError = None
AutoModelForCausalLM = None
AutoTokenizer = None
BitsAndBytesConfig = None
TextIteratorStreamer = None


def require_torch():
    global torch
    if torch is None:
        try:
            import torch as torch_module
        except ImportError as exc:  # pragma: no cover - optional dependency guard
            raise SystemExit(
                "torch is required. Install from https://pytorch.org"
            ) from exc
        torch = torch_module
    return torch


def require_hf_hub():
    global HfApi, login, snapshot_download, GatedRepoError, HfHubHTTPError
    if HfApi is None:
        try:
            from huggingface_hub import HfApi as HfApiClass
            from huggingface_hub import login as hf_login
            from huggingface_hub import snapshot_download as hf_snapshot_download
            from huggingface_hub.errors import GatedRepoError as HfGatedRepoError
            from huggingface_hub.errors import HfHubHTTPError as HfHubHttpError
        except ImportError as exc:  # pragma: no cover - optional dependency guard
            raise SystemExit(
                "huggingface_hub is required. Install from benchmark/requirements.txt"
            ) from exc
        HfApi = HfApiClass
        login = hf_login
        snapshot_download = hf_snapshot_download
        GatedRepoError = HfGatedRepoError
        HfHubHTTPError = HfHubHttpError
    return HfApi, login, snapshot_download


def require_transformers():
    global AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TextIteratorStreamer
    if AutoTokenizer is None:
        try:
            from transformers import AutoModelForCausalLM as AutoModelForCausalLMClass
            from transformers import AutoTokenizer as AutoTokenizerClass
            from transformers import BitsAndBytesConfig as BitsAndBytesConfigClass
            from transformers import TextIteratorStreamer as TextIteratorStreamerClass
        except ImportError as exc:  # pragma: no cover - optional dependency guard
            raise SystemExit(
                "transformers is required. Install from benchmark/requirements.txt"
            ) from exc
        AutoModelForCausalLM = AutoModelForCausalLMClass
        AutoTokenizer = AutoTokenizerClass
        BitsAndBytesConfig = BitsAndBytesConfigClass
        TextIteratorStreamer = TextIteratorStreamerClass
    return AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TextIteratorStreamer


@dataclass
class Sample:
    sample_id: str
    task: str
    language: str
    prompt: Optional[str]
    messages: Optional[List[Dict[str, str]]]
    reference: Optional[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LLM benchmark runner (Transformers).")
    parser.add_argument(
        "--models",
        nargs="+",
        required=True,
        help="HF model ids to benchmark",
    )
    parser.add_argument(
        "--dataset",
        default="benchmark/data/sample.jsonl",
        help="JSONL dataset path",
    )
    parser.add_argument(
        "--output-dir",
        default="benchmark/outputs",
        help="Base output directory",
    )
    parser.add_argument(
        "--device",
        default="auto",
        choices=["auto", "cpu", "cuda", "mps"],
        help="Device selection",
    )
    parser.add_argument(
        "--quant",
        default="auto",
        choices=["auto", "4bit", "8bit", "fp16", "bf16", "fp32"],
        help="Quantization mode (HF only). auto => 4bit on cuda, fp32 otherwise.",
    )
    parser.add_argument(
        "--dtype",
        default="auto",
        choices=["auto", "float16", "bfloat16", "float32"],
        help="Torch dtype for model weights",
    )
    parser.add_argument("--max-new-tokens", type=int, default=256)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--top-k", type=int, default=40)
    parser.add_argument("--repetition-penalty", type=float, default=1.1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument(
        "--download-only",
        action="store_true",
        help="Prefetch HF model snapshots and exit without running samples.",
    )
    parser.add_argument(
        "--hf-token",
        default=None,
        help="HF access token (env HF_TOKEN is used if not set).",
    )
    parser.add_argument(
        "--hf-timeout",
        type=int,
        default=120,
        help="HF metadata timeout in seconds (etag timeout).",
    )
    parser.add_argument(
        "--hf-retries",
        type=int,
        default=3,
        help="Retries for HF download failures.",
    )
    parser.add_argument(
        "--hf-max-workers",
        type=int,
        default=8,
        help="Max workers for HF snapshot downloads.",
    )
    parser.add_argument("--trust-remote-code", action="store_true")
    parser.add_argument("--no-chat-template", action="store_true")
    parser.add_argument("--max-samples", type=int, default=None)
    parser.add_argument("--run-name", default=None)
    parser.add_argument(
        "--ollama-url",
        default="http://localhost:11434",
        help="Base URL for Ollama (for models prefixed with ollama:)",
    )
    return parser.parse_args()


def load_dataset(path: str, max_samples: Optional[int] = None) -> List[Sample]:
    samples: List[Sample] = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            prompt = record.get("prompt")
            messages = record.get("messages")
            if not prompt and not messages:
                raise ValueError("Each record must include prompt or messages")
            sample = Sample(
                sample_id=str(record.get("id", len(samples))),
                task=str(record.get("task", "unknown")),
                language=str(record.get("language", "unknown")),
                prompt=prompt,
                messages=messages,
                reference=record.get("reference"),
            )
            samples.append(sample)
            if max_samples and len(samples) >= max_samples:
                break
    return samples


def pick_device(device_arg: str) -> str:
    torch_module = require_torch()
    if device_arg != "auto":
        return device_arg
    if torch_module.cuda.is_available():
        return "cuda"
    if getattr(torch_module.backends, "mps", None) and torch_module.backends.mps.is_available():
        return "mps"
    return "cpu"


def pick_dtype(dtype_arg: str, device: str) -> torch.dtype:
    torch_module = require_torch()
    if dtype_arg == "float16":
        return torch_module.float16
    if dtype_arg == "bfloat16":
        return torch_module.bfloat16
    if dtype_arg == "float32":
        return torch_module.float32
    if device == "cuda":
        if torch_module.cuda.is_bf16_supported():
            return torch_module.bfloat16
        return torch_module.float16
    return torch_module.float32


def resolve_quant(quant_arg: str, device: str) -> str:
    if quant_arg == "auto":
        return "4bit" if device == "cuda" else "fp32"
    return quant_arg


def resolve_dtype(dtype_arg: str, device: str, quant: str) -> torch.dtype:
    torch_module = require_torch()
    if dtype_arg != "auto":
        return pick_dtype(dtype_arg, device)
    if quant == "fp16":
        return torch_module.float16
    if quant == "bf16":
        return torch_module.bfloat16
    if quant == "fp32":
        return torch_module.float32
    return pick_dtype("auto", device)


def build_prompt(
    sample: Sample, tokenizer: Any, use_chat_template: bool
) -> str:
    if sample.messages:
        if use_chat_template and hasattr(tokenizer, "apply_chat_template"):
            return tokenizer.apply_chat_template(
                sample.messages, tokenize=False, add_generation_prompt=True
            )
        lines = [f"{msg['role']}: {msg['content']}" for msg in sample.messages]
        lines.append("assistant:")
        return "\n".join(lines)
    return sample.prompt or ""


def build_prompt_text(sample: Sample) -> str:
    if sample.messages:
        lines = [f"{msg['role']}: {msg['content']}" for msg in sample.messages]
        lines.append("assistant:")
        return "\n".join(lines)
    return sample.prompt or ""


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, len(text) // 4)


def get_context_length(model: Any) -> Optional[int]:
    for attr in ("max_position_embeddings", "max_seq_len", "n_positions"):
        value = getattr(model.config, attr, None)
        if value:
            return int(value)
    return None


def system_info(with_torch: bool) -> Dict[str, Any]:
    info: Dict[str, Any] = {
        "python": sys.version.split()[0],
        "platform": sys.platform,
        "cpu": os.environ.get("PROCESSOR_IDENTIFIER") or os.environ.get("PROCESSOR_ARCHITECTURE") or "unknown",
        "torch": None,
        "cuda_available": False,
    }
    if with_torch:
        torch_module = require_torch()
        info["torch"] = torch_module.__version__
        info["cuda_available"] = torch_module.cuda.is_available()
        try:
            import transformers  # local import for version

            info["transformers"] = transformers.__version__
        except ImportError:
            info["transformers"] = None
        if torch_module.cuda.is_available():
            info["gpu"] = torch_module.cuda.get_device_name(0)
            info["gpu_total_vram_mb"] = int(
                torch_module.cuda.get_device_properties(0).total_memory / (1024 * 1024)
            )
    else:
        info["transformers"] = None
    return info


def maybe_login_hf(token: Optional[str]) -> None:
    if not token:
        return
    try:
        login(token=token)
    except Exception as exc:  # pragma: no cover - network/auth dependent
        raise SystemExit(f"HF login failed: {exc}") from exc


def preflight_ollama(base_url: str, model_id: str, timeout_s: int = 5) -> Tuple[bool, str]:
    try:
        resp = requests.get(f"{base_url}/api/tags", timeout=timeout_s)
        resp.raise_for_status()
        data = resp.json()
        names = [item.get("name", "") for item in data.get("models", [])]
        if model_id in names:
            return True, ""
        if any(name.split(":")[0] == model_id for name in names):
            return True, ""
        preview = ", ".join(names[:10])
        if len(names) > 10:
            preview += ", ..."
        return False, f"Ollama model '{model_id}' not found. Available: {preview}"
    except Exception as exc:
        return False, f"Ollama preflight failed: {exc}"


def preflight_hf(model_id: str, hf_api: HfApi, token: Optional[str]) -> Tuple[bool, str]:
    try:
        hf_api.model_info(model_id, token=token)
        return True, ""
    except GatedRepoError:
        return (
            False,
            "HF gated model: accept terms on Hugging Face and set HF_TOKEN.",
        )
    except HfHubHTTPError as exc:
        status = getattr(exc.response, "status_code", None)
        if status in (401, 403):
            return (
                False,
                "HF auth required: set HF_TOKEN and accept model terms.",
            )
        if status == 404:
            return False, "HF model not found (404)."
        return False, f"HF preflight failed: {exc}"
    except Exception as exc:
        return False, f"HF preflight failed: {exc}"


def snapshot_with_retries(
    model_id: str,
    token: Optional[str],
    timeout_s: int,
    retries: int,
    max_workers: int,
) -> Tuple[str, float, bool]:
    try:
        local_path = snapshot_download(
            model_id,
            token=token,
            local_files_only=True,
        )
        return local_path, 0.0, True
    except Exception:
        pass

    start_time = time.perf_counter()
    last_exc: Optional[Exception] = None
    for attempt in range(retries):
        try:
            local_path = snapshot_download(
                model_id,
                token=token,
                resume_download=True,
                local_files_only=False,
                etag_timeout=timeout_s,
                max_workers=max_workers,
            )
            return local_path, time.perf_counter() - start_time, False
        except Exception as exc:  # pragma: no cover - network dependent
            last_exc = exc
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    if last_exc:
        raise last_exc
    raise RuntimeError("HF snapshot download failed without exception")


def classify_error(message: str) -> str:
    msg = message.lower()
    if "gated" in msg:
        return "hf_gated"
    if "401" in msg or "403" in msg or "unauthorized" in msg or "forbidden" in msg:
        return "auth"
    if "404" in msg or "not found" in msg:
        return "not_found"
    if "timed out" in msg or "timeout" in msg:
        return "timeout"
    if "connection" in msg or "failed to establish" in msg or "max retries" in msg:
        return "network"
    if "out of memory" in msg or "cuda" in msg and "memory" in msg:
        return "oom"
    return "runtime_error"


def record_error(
    row: Dict[str, Any],
    error_reasons: Counter,
    exc: Exception,
    default_reason: Optional[str] = None,
) -> None:
    message = str(exc)
    reason = default_reason or classify_error(message)
    error_reasons[reason] += 1
    row["error"] = f"{reason}: {message}"


def get_nvml_handle() -> Optional[Any]:
    if pynvml is None:
        return None
    try:
        pynvml.nvmlInit()
        return pynvml.nvmlDeviceGetHandleByIndex(0)
    except Exception:
        return None


def read_nvml_vram_mb(handle: Any) -> Optional[int]:
    if pynvml is None or handle is None:
        return None
    try:
        mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
        return int(mem.used / (1024 * 1024))
    except Exception:
        return None


def build_result_row(
    model_id: str,
    provider: str,
    quant: str,
    device_label: str,
    dtype_label: str,
    sample: Sample,
    prompt_tokens: int,
) -> Dict[str, Any]:
    return {
        "model": model_id,
        "provider": provider,
        "quant": quant,
        "device": device_label,
        "dtype": dtype_label,
        "sample_id": sample.sample_id,
        "task": sample.task,
        "language": sample.language,
        "prompt_tokens": prompt_tokens,
        "output_tokens": None,
        "ttft_ms": None,
        "total_time_s": None,
        "tok_per_s": None,
        "output_text": None,
        "error": None,
    }


def bitsandbytes_available() -> bool:
    try:
        import bitsandbytes  # type: ignore

        return True
    except Exception:
        return False


def generate_with_streamer(
    model: Any,
    tokenizer: Any,
    input_ids: torch.Tensor,
    attention_mask: Optional[torch.Tensor],
    generation_kwargs: Dict[str, Any],
) -> Dict[str, Any]:
    streamer = TextIteratorStreamer(
        tokenizer, skip_prompt=True, skip_special_tokens=True
    )
    thread = Thread(
        target=model.generate,
        kwargs={
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "streamer": streamer,
            **generation_kwargs,
        },
    )

    start_time = time.perf_counter()
    thread.start()
    generated_text = ""
    ttft_s: Optional[float] = None

    for text in streamer:
        if ttft_s is None:
            ttft_s = time.perf_counter() - start_time
        generated_text += text

    thread.join()
    total_time_s = time.perf_counter() - start_time
    if ttft_s is None:
        ttft_s = total_time_s

    output_tokens = len(
        tokenizer.encode(generated_text, add_special_tokens=False)
    )
    return {
        "output_text": generated_text,
        "ttft_s": ttft_s,
        "total_time_s": total_time_s,
        "output_tokens": output_tokens,
    }


def run_ollama_sample(
    base_url: str,
    model_id: str,
    prompt: str,
    temperature: float,
    top_p: float,
    max_new_tokens: int,
) -> Dict[str, Any]:
    api_url = f"{base_url}/api/generate"
    payload = {
        "model": model_id,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": temperature,
            "top_p": top_p,
            "num_predict": max_new_tokens,
        },
    }

    start_time = time.perf_counter()
    ttft_s: Optional[float] = None
    output_text = ""
    prompt_tokens = None
    completion_tokens = None

    with requests.post(api_url, json=payload, stream=True, timeout=120) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines():
            if not line:
                continue
            data = json.loads(line.decode("utf-8"))
            token = data.get("response", "")
            if token:
                if ttft_s is None:
                    ttft_s = time.perf_counter() - start_time
                output_text += token
            if data.get("done"):
                prompt_tokens = data.get("prompt_eval_count")
                completion_tokens = data.get("eval_count")
                break

    total_time_s = time.perf_counter() - start_time
    if ttft_s is None:
        ttft_s = total_time_s

    output_tokens = completion_tokens
    if output_tokens is None:
        output_tokens = estimate_tokens(output_text)

    usage = {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
    }
    return {
        "output_text": output_text,
        "ttft_s": ttft_s,
        "total_time_s": total_time_s,
        "output_tokens": output_tokens,
        "usage": usage,
    }


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False))
            handle.write("\n")


def write_csv(
    path: Path, rows: List[Dict[str, Any]], fieldnames: Optional[List[str]] = None
) -> None:
    if not rows:
        return
    with open(path, "w", encoding="utf-8", newline="") as handle:
        headers = fieldnames or list(rows[0].keys())
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in headers})


def write_markdown(
    path: Path, rows: List[Dict[str, Any]], fieldnames: Optional[List[str]] = None
) -> None:
    if not rows:
        return
    headers = fieldnames or list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        values = [str(row.get(h, "")) for h in headers]
        lines.append("| " + " | ".join(values) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    random.seed(args.seed)
    use_chat_template = not args.no_chat_template
    has_hf_models = any(not model.startswith("ollama:") for model in args.models)
    hf_token = args.hf_token or os.getenv("HF_TOKEN")
    hf_api = None

    if has_hf_models:
        torch_module = require_torch()
        torch_module.manual_seed(args.seed)
        device = pick_device(args.device)
        quant = resolve_quant(args.quant, device)
        if device != "cuda" and quant in ("4bit", "8bit"):
            print(
                f"[warn] Quant {quant} requested on {device}; falling back to fp32."
            )
            quant = "fp32"
        dtype = resolve_dtype(args.dtype, device, quant)
        dtype_label = str(dtype).replace("torch.", "")
        require_hf_hub()
        require_transformers()
        maybe_login_hf(hf_token)
        hf_api = HfApi(token=hf_token)
    else:
        device = "ollama"
        quant = "n/a"
        dtype_label = "n/a"

    samples = load_dataset(args.dataset, args.max_samples)
    if not samples:
        raise SystemExit("Dataset is empty.")

    run_name = args.run_name or time.strftime("%Y%m%d_%H%M%S")
    output_dir = Path(args.output_dir) / run_name
    output_dir.mkdir(parents=True, exist_ok=True)

    config_path = output_dir / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "models": args.models,
                "dataset": args.dataset,
                "device": device,
                "quant": quant,
                "dtype": dtype_label,
                "generation": {
                    "max_new_tokens": args.max_new_tokens,
                    "temperature": args.temperature,
                    "top_p": args.top_p,
                    "top_k": args.top_k,
                    "repetition_penalty": args.repetition_penalty,
                },
                "use_chat_template": use_chat_template,
                "seed": args.seed,
                "download_only": args.download_only,
                "ollama_url": args.ollama_url,
                "hf": {
                    "token_provided": bool(hf_token),
                    "timeout_s": args.hf_timeout,
                    "retries": args.hf_retries,
                    "max_workers": args.hf_max_workers,
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    system_path = output_dir / "system.json"
    system_path.write_text(json.dumps(system_info(has_hf_models), indent=2), encoding="utf-8")

    results: List[Dict[str, Any]] = []
    summary_rows: List[Dict[str, Any]] = []

    process = psutil.Process(os.getpid())
    nvml_handle = get_nvml_handle() if device == "cuda" else None

    summary_columns = [
        "model",
        "provider",
        "quant",
        "device",
        "dtype",
        "params",
        "context",
        "avg_prompt_tokens",
        "max_prompt_tokens",
        "download_s",
        "load_s",
        "warmup_s",
        "avg_ttft_ms",
        "avg_tok_s",
        "avg_out_tokens",
        "avg_total_time_s",
        "peak_vram_mb",
        "peak_ram_mb",
        "errors",
        "error_reasons",
    ]

    for model_id in args.models:
        if model_id.startswith("ollama:"):
            provider = "ollama"
            device_label = "ollama"
            quant_label = ""
            dtype_out = ""
            ollama_model = model_id.split(":", 1)[1]
            error_reasons: Counter = Counter()
            prompt_token_values: List[int] = []

            preflight_ok, preflight_msg = preflight_ollama(
                base_url=args.ollama_url, model_id=ollama_model
            )
            if not preflight_ok:
                reason = (
                    "ollama_unreachable"
                    if preflight_msg.startswith("Ollama preflight failed")
                    else "ollama_model_missing"
                )
                if args.strict:
                    raise SystemExit(preflight_msg)
                for sample in samples:
                    prompt = build_prompt_text(sample)
                    prompt_tokens = estimate_tokens(prompt)
                    prompt_token_values.append(prompt_tokens)
                    row = build_result_row(
                        model_id,
                        provider,
                        quant_label,
                        device_label,
                        dtype_out,
                        sample,
                        prompt_tokens,
                    )
                    row["error"] = f"{reason}: {preflight_msg}"
                    results.append(row)
                error_reasons[reason] += len(samples)
                peak_rss = process.memory_info().rss
                avg_prompt = sum(prompt_token_values) / max(
                    len(prompt_token_values), 1
                )
                max_prompt = max(prompt_token_values) if prompt_token_values else 0
                summary_rows.append(
                    {
                        "model": model_id,
                        "provider": provider,
                        "quant": quant_label,
                        "device": device_label,
                        "dtype": dtype_out,
                        "params": "",
                        "context": "",
                        "avg_prompt_tokens": round(avg_prompt, 1),
                        "max_prompt_tokens": max_prompt,
                        "download_s": 0.0,
                        "load_s": 0.0,
                        "warmup_s": 0.0,
                        "avg_ttft_ms": 0.0,
                        "avg_tok_s": 0.0,
                        "avg_out_tokens": 0.0,
                        "avg_total_time_s": 0.0,
                        "peak_vram_mb": "",
                        "peak_ram_mb": int(peak_rss / (1024 * 1024)),
                        "errors": len(samples),
                        "error_reasons": json.dumps(dict(error_reasons)),
                    }
                )
                continue

            if args.download_only:
                print(f"[info] download-only: skipping ollama model {model_id}")
                continue

            peak_rss = 0
            successful = 0
            ttft_values: List[float] = []
            tok_values: List[float] = []
            out_token_values: List[int] = []
            total_time_values: List[float] = []
            errors = 0

            total_samples = len(samples)
            print(f"[ollama] starting {ollama_model} ({total_samples} ornek)", flush=True)

            for idx, sample in enumerate(samples, start=1):
                print(f"[ollama] {ollama_model} ornek {idx}/{total_samples}", flush=True)
                prompt = build_prompt_text(sample)
                prompt_tokens = estimate_tokens(prompt)
                prompt_token_values.append(prompt_tokens)

                row = build_result_row(
                    model_id,
                    provider,
                    quant_label,
                    device_label,
                    dtype_out,
                    sample,
                    prompt_tokens,
                )

                try:
                    output = run_ollama_sample(
                        base_url=args.ollama_url,
                        model_id=ollama_model,
                        prompt=prompt,
                        temperature=args.temperature,
                        top_p=args.top_p,
                        max_new_tokens=args.max_new_tokens,
                    )
                    output_tokens = output["output_tokens"]
                    total_time_s = output["total_time_s"]
                    ttft_ms = output["ttft_s"] * 1000.0
                    tok_per_s = (
                        output_tokens / total_time_s if total_time_s > 0 else 0.0
                    )

                    row.update(
                        {
                            "output_tokens": output_tokens,
                            "ttft_ms": round(ttft_ms, 2),
                            "total_time_s": round(total_time_s, 4),
                            "tok_per_s": round(tok_per_s, 3),
                            "output_text": output["output_text"],
                        }
                    )
                    successful += 1
                    ttft_values.append(ttft_ms)
                    tok_values.append(tok_per_s)
                    out_token_values.append(output_tokens)
                    total_time_values.append(total_time_s)
                except Exception as exc:  # pragma: no cover
                    record_error(row, error_reasons, exc)
                    errors += 1

                results.append(row)

                rss = process.memory_info().rss
                if rss > peak_rss:
                    peak_rss = rss

            avg_prompt = sum(prompt_token_values) / max(len(prompt_token_values), 1)
            max_prompt = max(prompt_token_values) if prompt_token_values else 0

            summary_rows.append(
                {
                    "model": model_id,
                    "provider": provider,
                    "quant": quant_label,
                    "device": device_label,
                    "dtype": dtype_out,
                    "params": "",
                    "context": "",
                    "avg_prompt_tokens": round(avg_prompt, 1),
                    "max_prompt_tokens": max_prompt,
                    "download_s": 0.0,
                    "load_s": 0.0,
                    "warmup_s": 0.0,
                    "avg_ttft_ms": round(
                        sum(ttft_values) / max(successful, 1), 2
                    ),
                    "avg_tok_s": round(sum(tok_values) / max(successful, 1), 2),
                    "avg_out_tokens": round(
                        sum(out_token_values) / max(successful, 1), 1
                    ),
                    "avg_total_time_s": round(
                        sum(total_time_values) / max(successful, 1), 3
                    ),
                    "peak_vram_mb": "",
                    "peak_ram_mb": int(peak_rss / (1024 * 1024)),
                    "errors": errors,
                    "error_reasons": json.dumps(dict(error_reasons)),
                }
            )
            continue

        provider = "huggingface"
        device_label = device
        quant_label = quant
        dtype_out = dtype_label
        error_reasons = Counter()
        prompt_token_values = []

        preflight_ok, preflight_msg = preflight_hf(model_id, hf_api, hf_token)
        if not preflight_ok:
            msg_lower = preflight_msg.lower()
            if "gated" in msg_lower:
                reason = "hf_gated"
            elif "auth required" in msg_lower:
                reason = "hf_auth"
            elif "not found" in msg_lower:
                reason = "hf_not_found"
            else:
                reason = "hf_preflight_failed"
            if args.strict:
                raise SystemExit(preflight_msg)
            for sample in samples:
                prompt = build_prompt_text(sample)
                prompt_tokens = estimate_tokens(prompt)
                prompt_token_values.append(prompt_tokens)
                row = build_result_row(
                    model_id,
                    provider,
                    quant_label,
                    device_label,
                    dtype_out,
                    sample,
                    prompt_tokens,
                )
                row["error"] = f"{reason}: {preflight_msg}"
                results.append(row)
            error_reasons[reason] += len(samples)
            avg_prompt = sum(prompt_token_values) / max(len(prompt_token_values), 1)
            max_prompt = max(prompt_token_values) if prompt_token_values else 0
            summary_rows.append(
                {
                    "model": model_id,
                    "provider": provider,
                    "quant": quant_label,
                    "device": device_label,
                    "dtype": dtype_out,
                    "params": "",
                    "context": "",
                    "avg_prompt_tokens": round(avg_prompt, 1),
                    "max_prompt_tokens": max_prompt,
                    "download_s": 0.0,
                    "load_s": 0.0,
                    "warmup_s": 0.0,
                    "avg_ttft_ms": 0.0,
                    "avg_tok_s": 0.0,
                    "avg_out_tokens": 0.0,
                    "avg_total_time_s": 0.0,
                    "peak_vram_mb": "",
                    "peak_ram_mb": "",
                    "errors": len(samples),
                    "error_reasons": json.dumps(dict(error_reasons)),
                }
            )
            continue

        if quant in ("4bit", "8bit") and not bitsandbytes_available():
            msg = "bitsandbytes is required for 4bit/8bit quantization."
            if args.strict:
                raise SystemExit(msg)
            for sample in samples:
                prompt = build_prompt_text(sample)
                prompt_tokens = estimate_tokens(prompt)
                prompt_token_values.append(prompt_tokens)
                row = build_result_row(
                    model_id,
                    provider,
                    quant_label,
                    device_label,
                    dtype_out,
                    sample,
                    prompt_tokens,
                )
                row["error"] = f"bitsandbytes_missing: {msg}"
                results.append(row)
            error_reasons["bitsandbytes_missing"] += len(samples)
            avg_prompt = sum(prompt_token_values) / max(len(prompt_token_values), 1)
            max_prompt = max(prompt_token_values) if prompt_token_values else 0
            summary_rows.append(
                {
                    "model": model_id,
                    "provider": provider,
                    "quant": quant_label,
                    "device": device_label,
                    "dtype": dtype_out,
                    "params": "",
                    "context": "",
                    "avg_prompt_tokens": round(avg_prompt, 1),
                    "max_prompt_tokens": max_prompt,
                    "download_s": 0.0,
                    "load_s": 0.0,
                    "warmup_s": 0.0,
                    "avg_ttft_ms": 0.0,
                    "avg_tok_s": 0.0,
                    "avg_out_tokens": 0.0,
                    "avg_total_time_s": 0.0,
                    "peak_vram_mb": "",
                    "peak_ram_mb": "",
                    "errors": len(samples),
                    "error_reasons": json.dumps(dict(error_reasons)),
                }
            )
            continue

        try:
            _, download_s, _ = snapshot_with_retries(
                model_id=model_id,
                token=hf_token,
                timeout_s=args.hf_timeout,
                retries=args.hf_retries,
                max_workers=args.hf_max_workers,
            )
        except Exception as exc:  # pragma: no cover - network dependent
            if args.strict:
                raise SystemExit(f"HF download failed: {exc}") from exc
            for sample in samples:
                prompt = build_prompt_text(sample)
                prompt_tokens = estimate_tokens(prompt)
                prompt_token_values.append(prompt_tokens)
                row = build_result_row(
                    model_id,
                    provider,
                    quant_label,
                    device_label,
                    dtype_out,
                    sample,
                    prompt_tokens,
                )
                row["error"] = f"hf_download_failed: {exc}"
                results.append(row)
            error_reasons["hf_download_failed"] += len(samples)
            avg_prompt = sum(prompt_token_values) / max(len(prompt_token_values), 1)
            max_prompt = max(prompt_token_values) if prompt_token_values else 0
            summary_rows.append(
                {
                    "model": model_id,
                    "provider": provider,
                    "quant": quant_label,
                    "device": device_label,
                    "dtype": dtype_out,
                    "params": "",
                    "context": "",
                    "avg_prompt_tokens": round(avg_prompt, 1),
                    "max_prompt_tokens": max_prompt,
                    "download_s": 0.0,
                    "load_s": 0.0,
                    "warmup_s": 0.0,
                    "avg_ttft_ms": 0.0,
                    "avg_tok_s": 0.0,
                    "avg_out_tokens": 0.0,
                    "avg_total_time_s": 0.0,
                    "peak_vram_mb": "",
                    "peak_ram_mb": "",
                    "errors": len(samples),
                    "error_reasons": json.dumps(dict(error_reasons)),
                }
            )
            continue

        if args.download_only:
            summary_rows.append(
                {
                    "model": model_id,
                    "provider": provider,
                    "quant": quant_label,
                    "device": device_label,
                    "dtype": dtype_out,
                    "params": "",
                    "context": "",
                    "avg_prompt_tokens": "",
                    "max_prompt_tokens": "",
                    "download_s": round(download_s, 2),
                    "load_s": 0.0,
                    "warmup_s": 0.0,
                    "avg_ttft_ms": 0.0,
                    "avg_tok_s": 0.0,
                    "avg_out_tokens": 0.0,
                    "avg_total_time_s": 0.0,
                    "peak_vram_mb": "",
                    "peak_ram_mb": "",
                    "errors": 0,
                    "error_reasons": json.dumps({}),
                }
            )
            continue

        quant_config = None
        if quant == "4bit":
            quant_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=dtype,
            )
        elif quant == "8bit":
            quant_config = BitsAndBytesConfig(load_in_8bit=True)

        load_start = time.perf_counter()
        try:
            tokenizer = AutoTokenizer.from_pretrained(
                model_id,
                use_fast=True,
                trust_remote_code=args.trust_remote_code,
                local_files_only=True,
            )
            if tokenizer.pad_token is None and tokenizer.eos_token is not None:
                tokenizer.pad_token = tokenizer.eos_token

            model = AutoModelForCausalLM.from_pretrained(
                model_id,
                torch_dtype=dtype,
                device_map="auto" if device == "cuda" else None,
                trust_remote_code=args.trust_remote_code,
                local_files_only=True,
                quantization_config=quant_config,
            )
        except Exception as exc:  # pragma: no cover - runtime dependent
            if args.strict:
                raise SystemExit(f"HF load failed: {exc}") from exc
            for sample in samples:
                prompt = build_prompt_text(sample)
                prompt_tokens = estimate_tokens(prompt)
                prompt_token_values.append(prompt_tokens)
                row = build_result_row(
                    model_id,
                    provider,
                    quant_label,
                    device_label,
                    dtype_out,
                    sample,
                    prompt_tokens,
                )
                row["error"] = f"hf_load_failed: {exc}"
                results.append(row)
            error_reasons["hf_load_failed"] += len(samples)
            avg_prompt = sum(prompt_token_values) / max(len(prompt_token_values), 1)
            max_prompt = max(prompt_token_values) if prompt_token_values else 0
            summary_rows.append(
                {
                    "model": model_id,
                    "provider": provider,
                    "quant": quant_label,
                    "device": device_label,
                    "dtype": dtype_out,
                    "params": "",
                    "context": "",
                    "avg_prompt_tokens": round(avg_prompt, 1),
                    "max_prompt_tokens": max_prompt,
                    "download_s": round(download_s, 2),
                    "load_s": 0.0,
                    "warmup_s": 0.0,
                    "avg_ttft_ms": 0.0,
                    "avg_tok_s": 0.0,
                    "avg_out_tokens": 0.0,
                    "avg_total_time_s": 0.0,
                    "peak_vram_mb": "",
                    "peak_ram_mb": "",
                    "errors": len(samples),
                    "error_reasons": json.dumps(dict(error_reasons)),
                }
            )
            continue

        if device != "cuda":
            model.to(device)
        model.eval()
        load_time_s = time.perf_counter() - load_start

        params = int(sum(p.numel() for p in model.parameters()))
        context_length = get_context_length(model)

        if device == "cuda":
            torch.cuda.reset_peak_memory_stats()

        peak_rss = 0
        successful = 0
        ttft_values = []
        tok_values = []
        out_token_values = []
        total_time_values = []
        errors = 0
        peak_vram_nvml = 0

        generation_kwargs = {
            "max_new_tokens": args.max_new_tokens,
            "temperature": args.temperature,
            "top_p": args.top_p,
            "top_k": args.top_k,
            "repetition_penalty": args.repetition_penalty,
            "do_sample": args.temperature > 0,
        }

        warmup_s = 0.0
        try:
            warmup_sample = Sample(
                sample_id="warmup",
                task="warmup",
                language="tr",
                prompt=None,
                messages=[{"role": "user", "content": "Merhaba."}],
                reference=None,
            )
            warmup_prompt = build_prompt(
                warmup_sample, tokenizer, use_chat_template
            )
            warmup_inputs = tokenizer(warmup_prompt, return_tensors="pt")
            warmup_ids = warmup_inputs["input_ids"].to(device)
            warmup_mask = warmup_inputs.get("attention_mask")
            if warmup_mask is not None:
                warmup_mask = warmup_mask.to(device)
            warmup_kwargs = dict(generation_kwargs)
            warmup_kwargs["max_new_tokens"] = min(args.max_new_tokens, 32)
            warmup_output = generate_with_streamer(
                model,
                tokenizer,
                warmup_ids,
                warmup_mask,
                warmup_kwargs,
            )
            warmup_s = round(warmup_output["total_time_s"], 3)
        except Exception as exc:  # pragma: no cover - runtime dependent
            error_reasons["warmup_failed"] += 1
            warmup_s = 0.0

        for sample in samples:
            prompt = build_prompt(sample, tokenizer, use_chat_template)
            inputs = tokenizer(prompt, return_tensors="pt")
            input_ids = inputs["input_ids"].to(device)
            attention_mask = inputs.get("attention_mask")
            if attention_mask is not None:
                attention_mask = attention_mask.to(device)
            prompt_tokens = int(input_ids.shape[-1])
            prompt_token_values.append(prompt_tokens)

            row = build_result_row(
                model_id,
                provider,
                quant_label,
                device_label,
                dtype_out,
                sample,
                prompt_tokens,
            )

            try:
                output = generate_with_streamer(
                    model,
                    tokenizer,
                    input_ids,
                    attention_mask,
                    generation_kwargs,
                )
                output_tokens = output["output_tokens"]
                total_time_s = output["total_time_s"]
                ttft_ms = output["ttft_s"] * 1000.0
                tok_per_s = (
                    output_tokens / total_time_s if total_time_s > 0 else 0.0
                )

                row.update(
                    {
                        "output_tokens": output_tokens,
                        "ttft_ms": round(ttft_ms, 2),
                        "total_time_s": round(total_time_s, 4),
                        "tok_per_s": round(tok_per_s, 3),
                        "output_text": output["output_text"],
                    }
                )
                successful += 1
                ttft_values.append(ttft_ms)
                tok_values.append(tok_per_s)
                out_token_values.append(output_tokens)
                total_time_values.append(total_time_s)
            except Exception as exc:  # pragma: no cover - runtime errors vary
                record_error(row, error_reasons, exc)
                errors += 1

            results.append(row)

            rss = process.memory_info().rss
            if rss > peak_rss:
                peak_rss = rss

            vram_now = read_nvml_vram_mb(nvml_handle)
            if vram_now and vram_now > peak_vram_nvml:
                peak_vram_nvml = vram_now

        peak_vram_mb: Optional[int] = None
        if device == "cuda":
            torch_peak = int(torch.cuda.max_memory_allocated() / (1024 * 1024))
            if peak_vram_nvml:
                peak_vram_mb = max(torch_peak, peak_vram_nvml)
            else:
                peak_vram_mb = torch_peak

        avg_prompt = sum(prompt_token_values) / max(len(prompt_token_values), 1)
        max_prompt = max(prompt_token_values) if prompt_token_values else 0

        summary_rows.append(
            {
                "model": model_id,
                "provider": provider,
                "quant": quant_label,
                "device": device_label,
                "dtype": dtype_out,
                "params": params,
                "context": context_length or "",
                "avg_prompt_tokens": round(avg_prompt, 1),
                "max_prompt_tokens": max_prompt,
                "download_s": round(download_s, 2),
                "load_s": round(load_time_s, 2),
                "warmup_s": warmup_s,
                "avg_ttft_ms": round(sum(ttft_values) / max(successful, 1), 2),
                "avg_tok_s": round(sum(tok_values) / max(successful, 1), 2),
                "avg_out_tokens": round(
                    sum(out_token_values) / max(successful, 1), 1
                ),
                "avg_total_time_s": round(
                    sum(total_time_values) / max(successful, 1), 3
                ),
                "peak_vram_mb": peak_vram_mb if peak_vram_mb is not None else "",
                "peak_ram_mb": int(peak_rss / (1024 * 1024)),
                "errors": errors,
                "error_reasons": json.dumps(dict(error_reasons)),
            }
        )

        del model
        if device == "cuda":
            torch.cuda.empty_cache()
    write_jsonl(output_dir / "results.jsonl", results)
    write_csv(output_dir / "summary.csv", summary_rows, summary_columns)
    write_markdown(output_dir / "summary.md", summary_rows, summary_columns)

    print(f"Results saved to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
