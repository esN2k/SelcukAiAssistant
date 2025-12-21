#!/usr/bin/env python
import argparse
import csv
import json
import os
import platform
import random
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from threading import Thread
from typing import Any, Dict, Iterable, List, Optional

try:
    import psutil
except ImportError as exc:  # pragma: no cover - optional dependency guard
    raise SystemExit("psutil is required. Install from benchmark/requirements.txt") from exc

try:
    import torch
except ImportError as exc:  # pragma: no cover - optional dependency guard
    raise SystemExit("torch is required. Install from https://pytorch.org") from exc

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
except ImportError as exc:  # pragma: no cover - optional dependency guard
    raise SystemExit(
        "transformers is required. Install from benchmark/requirements.txt"
    ) from exc


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
    parser.add_argument("--trust-remote-code", action="store_true")
    parser.add_argument("--no-chat-template", action="store_true")
    parser.add_argument("--max-samples", type=int, default=None)
    parser.add_argument("--run-name", default=None)
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
    if device_arg != "auto":
        return device_arg
    if torch.cuda.is_available():
        return "cuda"
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def pick_dtype(dtype_arg: str, device: str) -> torch.dtype:
    if dtype_arg == "float16":
        return torch.float16
    if dtype_arg == "bfloat16":
        return torch.bfloat16
    if dtype_arg == "float32":
        return torch.float32
    if device == "cuda":
        if torch.cuda.is_bf16_supported():
            return torch.bfloat16
        return torch.float16
    return torch.float32


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


def get_context_length(model: Any) -> Optional[int]:
    for attr in ("max_position_embeddings", "max_seq_len", "n_positions"):
        value = getattr(model.config, attr, None)
        if value:
            return int(value)
    return None


def system_info() -> Dict[str, Any]:
    info: Dict[str, Any] = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "cpu": platform.processor(),
        "torch": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
    }
    try:
        import transformers  # local import for version

        info["transformers"] = transformers.__version__
    except ImportError:
        info["transformers"] = None
    if torch.cuda.is_available():
        info["gpu"] = torch.cuda.get_device_name(0)
        info["gpu_total_vram_mb"] = int(
            torch.cuda.get_device_properties(0).total_memory / (1024 * 1024)
        )
    return info


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


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False))
            handle.write("\n")


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        return
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        return
    headers = list(rows[0].keys())
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
    torch.manual_seed(args.seed)

    device = pick_device(args.device)
    dtype = pick_dtype(args.dtype, device)
    use_chat_template = not args.no_chat_template

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
                "dtype": str(dtype).replace("torch.", ""),
                "generation": {
                    "max_new_tokens": args.max_new_tokens,
                    "temperature": args.temperature,
                    "top_p": args.top_p,
                    "top_k": args.top_k,
                    "repetition_penalty": args.repetition_penalty,
                },
                "use_chat_template": use_chat_template,
                "seed": args.seed,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    system_path = output_dir / "system.json"
    system_path.write_text(json.dumps(system_info(), indent=2), encoding="utf-8")

    results: List[Dict[str, Any]] = []
    summary_rows: List[Dict[str, Any]] = []

    process = psutil.Process(os.getpid())

    for model_id in args.models:
        load_start = time.perf_counter()
        tokenizer = AutoTokenizer.from_pretrained(
            model_id, use_fast=True, trust_remote_code=args.trust_remote_code
        )
        if tokenizer.pad_token is None and tokenizer.eos_token is not None:
            tokenizer.pad_token = tokenizer.eos_token

        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=dtype,
            device_map="auto" if device == "cuda" else None,
            trust_remote_code=args.trust_remote_code,
        )
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
        ttft_values: List[float] = []
        tok_values: List[float] = []
        out_token_values: List[int] = []
        total_time_values: List[float] = []
        errors = 0

        generation_kwargs = {
            "max_new_tokens": args.max_new_tokens,
            "temperature": args.temperature,
            "top_p": args.top_p,
            "top_k": args.top_k,
            "repetition_penalty": args.repetition_penalty,
            "do_sample": args.temperature > 0,
        }

        for sample in samples:
            prompt = build_prompt(sample, tokenizer, use_chat_template)
            inputs = tokenizer(prompt, return_tensors="pt")
            input_ids = inputs["input_ids"].to(device)
            attention_mask = inputs.get("attention_mask")
            if attention_mask is not None:
                attention_mask = attention_mask.to(device)
            prompt_tokens = int(input_ids.shape[-1])

            row: Dict[str, Any] = {
                "model": model_id,
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
                tok_per_s = output_tokens / total_time_s if total_time_s > 0 else 0.0

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
                row["error"] = str(exc)
                errors += 1

            results.append(row)

            rss = process.memory_info().rss
            if rss > peak_rss:
                peak_rss = rss

        peak_vram_mb = None
        if device == "cuda":
            peak_vram_mb = int(torch.cuda.max_memory_allocated() / (1024 * 1024))

        summary_rows.append(
            {
                "model": model_id,
                "params": params,
                "context": context_length or "",
                "load_s": round(load_time_s, 2),
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
            }
        )

        # Free memory between models
        del model
        if device == "cuda":
            torch.cuda.empty_cache()

    write_jsonl(output_dir / "results.jsonl", results)
    write_csv(output_dir / "summary.csv", summary_rows)
    write_markdown(output_dir / "summary.md", summary_rows)

    print(f"Results saved to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
