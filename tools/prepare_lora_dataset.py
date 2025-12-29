#!/usr/bin/env python
"""Prepare a lightweight LoRA dataset from cleaned university documents."""

from __future__ import annotations

import argparse
import json
import re
import textwrap
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple

import requests

ENCODING_FALLBACKS: Sequence[str] = (
    "utf-8",
    "utf-8-sig",
    "cp1254",
    "iso-8859-9",
    "cp1252",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare JSONL dataset for LoRA/QLoRA training."
    )
    parser.add_argument(
        "--input",
        default="data/processed_web/docs",
        help="Directory with cleaned text documents",
    )
    parser.add_argument(
        "--output",
        default="data/finetune/selcuk_lora.jsonl",
        help="Output JSONL path",
    )
    parser.add_argument("--chunk-chars", type=int, default=1200)
    parser.add_argument("--chunk-overlap", type=int, default=120)
    parser.add_argument("--min-chars", type=int, default=400)
    parser.add_argument("--max-docs", type=int, default=None)
    parser.add_argument("--max-samples", type=int, default=None)
    parser.add_argument("--use-ollama", action="store_true")
    parser.add_argument(
        "--ollama-url",
        default="http://localhost:11435",
        help="Ollama base URL",
    )
    parser.add_argument(
        "--ollama-model",
        default="selcuk_ai_assistant",
        help="Ollama model id",
    )
    parser.add_argument("--ollama-retries", type=int, default=3)
    parser.add_argument("--ollama-timeout", type=int, default=240)
    return parser.parse_args()


def extract_source(text: str) -> Tuple[Optional[str], str]:
    lines = text.splitlines()
    source_url = None
    if lines and lines[0].startswith("SOURCE_URL:"):
        source_url = lines[0].replace("SOURCE_URL:", "").strip()
        lines = lines[1:]
    cleaned = "\n".join(line.strip() for line in lines if line.strip())
    return source_url, cleaned


def read_text_with_fallbacks(
    path: Path,
    encodings: Sequence[str] = ENCODING_FALLBACKS,
) -> Tuple[str, str]:
    last_exc: Optional[UnicodeDecodeError] = None
    for encoding in encodings:
        try:
            return path.read_text(encoding=encoding), encoding
        except UnicodeDecodeError as exc:
            last_exc = exc
    if last_exc:
        print(f"[warn] Encoding fallback for {path.name}: {last_exc}")
    return path.read_text(encoding="utf-8", errors="replace"), "utf-8-replace"


def normalize_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text


def split_sentences(text: str) -> List[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if s.strip()]


def draft_summary(text: str, max_sentences: int = 2) -> str:
    sentences = split_sentences(text)
    if not sentences:
        return text[:200].strip()
    return " ".join(sentences[:max_sentences])


def chunk_text(text: str, chunk_chars: int, overlap: int) -> Iterable[str]:
    if chunk_chars <= 0:
        yield text
        return
    start = 0
    length = len(text)
    while start < length:
        end = min(length, start + chunk_chars)
        yield text[start:end]
        if end == length:
            break
        start = max(0, end - overlap)


def generate_with_ollama(
    base_url: str,
    model_id: str,
    prompt: str,
    retries: int,
    timeout: int,
) -> str:
    payload = {
        "model": model_id,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2, "top_p": 0.9, "num_predict": 160},
    }
    last_error: Exception | None = None
    for _ in range(retries):
        try:
            resp = requests.post(
                f"{base_url}/api/generate", json=payload, timeout=timeout
            )
            resp.raise_for_status()
            return resp.json().get("response", "").strip()
        except Exception as exc:
            last_error = exc
    raise RuntimeError(f"Ollama generation failed: {last_error}") from last_error


def build_instruction() -> str:
    return (
        "Aşağıdaki Selçuk Üniversitesi metnini 2-3 cümle ile "
        "akademik ve resmi bir dille özetleyin."
    )


def build_prompt(text: str) -> str:
    return textwrap.dedent(
        f"""
        Görev: Metni 2-3 cümle ile özetleyin.
        Dil: Türkçe, akademik ve resmi.
        Metin:
        {text}
        """
    ).strip()


def main() -> int:
    args = parse_args()
    input_dir = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc_paths = sorted(input_dir.glob("*.txt"))
    if args.max_docs:
        doc_paths = doc_paths[: args.max_docs]

    samples = []
    instruction = build_instruction()

    for doc_path in doc_paths:
        raw, encoding_used = read_text_with_fallbacks(doc_path)
        if encoding_used not in ("utf-8", "utf-8-sig"):
            print(
                f"[warn] Non-UTF8 encoding for {doc_path.name}: {encoding_used}"
            )
        source_url, text = extract_source(raw)
        text = normalize_text(text)
        if len(text) < args.min_chars:
            continue
        for chunk in chunk_text(text, args.chunk_chars, args.chunk_overlap):
            if len(chunk) < args.min_chars:
                continue
            if args.use_ollama:
                try:
                    output = generate_with_ollama(
                        args.ollama_url,
                        args.ollama_model,
                        build_prompt(chunk),
                        retries=args.ollama_retries,
                        timeout=args.ollama_timeout,
                    )
                    output_source = "ollama"
                except Exception as exc:
                    print(f"[warn] Ollama failed: {exc}; using draft summary.")
                    output = draft_summary(chunk)
                    output_source = "fallback"
            else:
                output = draft_summary(chunk)
                output_source = "draft"
            samples.append(
                {
                    "instruction": instruction,
                    "input": chunk,
                    "output": output,
                    "source_url": source_url,
                    "source_doc": doc_path.name,
                    "output_source": output_source,
                }
            )
            if args.max_samples and len(samples) >= args.max_samples:
                break
        if args.max_samples and len(samples) >= args.max_samples:
            break

    with output_path.open("w", encoding="utf-8") as handle:
        for sample in samples:
            handle.write(json.dumps(sample, ensure_ascii=False) + "\n")

    print(f"Wrote {len(samples)} samples -> {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
