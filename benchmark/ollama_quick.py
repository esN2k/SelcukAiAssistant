#!/usr/bin/env python
"""Quick Ollama-only benchmark runner (no HF/torch dependencies)."""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests


@dataclass
class Sample:
    sample_id: str
    task: str
    language: str
    prompt: Optional[str]
    messages: Optional[List[Dict[str, str]]]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Quick benchmark for Ollama models."
    )
    parser.add_argument(
        "--models",
        nargs="+",
        required=True,
        help="Ollama model ids (without prefix).",
    )
    parser.add_argument(
        "--dataset",
        default="benchmark/data/selcuk_tr.jsonl",
        help="JSONL dataset path",
    )
    parser.add_argument(
        "--output-dir",
        default="benchmark/outputs",
        help="Base output directory",
    )
    parser.add_argument(
        "--run-name",
        default=None,
        help="Run name for output directory",
    )
    parser.add_argument(
        "--ollama-url",
        default="http://localhost:11434",
        help="Base URL for Ollama",
    )
    parser.add_argument("--max-samples", type=int, default=None)
    parser.add_argument("--max-new-tokens", type=int, default=128)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--top-p", type=float, default=0.9)
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
            samples.append(
                Sample(
                    sample_id=str(record.get("id", len(samples))),
                    task=str(record.get("task", "unknown")),
                    language=str(record.get("language", "unknown")),
                    prompt=prompt,
                    messages=messages,
                )
            )
            if max_samples and len(samples) >= max_samples:
                break
    return samples


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


def preflight_ollama(
    base_url: str, model_id: str, timeout_s: int = 5
) -> Tuple[bool, str]:
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

    with requests.post(api_url, json=payload, stream=True, timeout=240) as resp:
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


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        return
    with open(path, "w", encoding="utf-8", newline="") as handle:
        headers = list(rows[0].keys())
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in headers})


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
                "max_new_tokens": args.max_new_tokens,
                "temperature": args.temperature,
                "top_p": args.top_p,
                "ollama_url": args.ollama_url,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    results: List[Dict[str, Any]] = []
    summary_rows: List[Dict[str, Any]] = []

    for model_id in args.models:
        error_reasons: Counter = Counter()
        prompt_token_values: List[int] = []
        ttft_values: List[float] = []
        tok_values: List[float] = []
        out_token_values: List[int] = []
        total_time_values: List[float] = []
        errors = 0
        successful = 0

        preflight_ok, preflight_msg = preflight_ollama(
            base_url=args.ollama_url, model_id=model_id
        )
        if not preflight_ok:
            error_reasons["ollama_preflight_failed"] += len(samples)
            for sample in samples:
                prompt = build_prompt_text(sample)
                prompt_tokens = estimate_tokens(prompt)
                prompt_token_values.append(prompt_tokens)
                results.append(
                    {
                        "model": model_id,
                        "sample_id": sample.sample_id,
                        "task": sample.task,
                        "language": sample.language,
                        "prompt_tokens": prompt_tokens,
                        "output_tokens": None,
                        "ttft_ms": None,
                        "total_time_s": None,
                        "tok_per_s": None,
                        "error": preflight_msg,
                    }
                )
            summary_rows.append(
                {
                    "model": model_id,
                    "avg_prompt_tokens": round(
                        sum(prompt_token_values)
                        / max(len(prompt_token_values), 1),
                        1,
                    ),
                    "max_prompt_tokens": max(prompt_token_values)
                    if prompt_token_values
                    else 0,
                    "avg_ttft_ms": 0.0,
                    "avg_tok_s": 0.0,
                    "avg_out_tokens": 0.0,
                    "avg_total_time_s": 0.0,
                    "errors": len(samples),
                    "error_reasons": json.dumps(dict(error_reasons)),
                }
            )
            continue

        for sample in samples:
            prompt = build_prompt_text(sample)
            prompt_tokens = estimate_tokens(prompt)
            prompt_token_values.append(prompt_tokens)

            row = {
                "model": model_id,
                "sample_id": sample.sample_id,
                "task": sample.task,
                "language": sample.language,
                "prompt_tokens": prompt_tokens,
                "output_tokens": None,
                "ttft_ms": None,
                "total_time_s": None,
                "tok_per_s": None,
                "error": None,
            }

            try:
                output = run_ollama_sample(
                    base_url=args.ollama_url,
                    model_id=model_id,
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
                    }
                )
                successful += 1
                ttft_values.append(ttft_ms)
                tok_values.append(tok_per_s)
                out_token_values.append(output_tokens)
                total_time_values.append(total_time_s)
            except Exception as exc:
                errors += 1
                error_reasons["runtime_error"] += 1
                row["error"] = str(exc)

            results.append(row)

        avg_prompt = sum(prompt_token_values) / max(len(prompt_token_values), 1)
        max_prompt = max(prompt_token_values) if prompt_token_values else 0
        summary_rows.append(
            {
                "model": model_id,
                "avg_prompt_tokens": round(avg_prompt, 1),
                "max_prompt_tokens": max_prompt,
                "avg_ttft_ms": round(sum(ttft_values) / max(successful, 1), 2),
                "avg_tok_s": round(sum(tok_values) / max(successful, 1), 2),
                "avg_out_tokens": round(
                    sum(out_token_values) / max(successful, 1), 1
                ),
                "avg_total_time_s": round(
                    sum(total_time_values) / max(successful, 1), 3
                ),
                "errors": errors,
                "error_reasons": json.dumps(dict(error_reasons)),
            }
        )

    write_jsonl(output_dir / "results.jsonl", results)
    write_csv(output_dir / "summary.csv", summary_rows)
    write_markdown(output_dir / "summary.md", summary_rows)
    print(f"Results saved to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

