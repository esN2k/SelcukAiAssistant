#!/usr/bin/env python3
"""Clean raw HTML/PDF/TXT files into normalized text for RAG."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Dict, Iterable, Optional

from bs4 import BeautifulSoup
from pypdf import PdfReader
from charset_normalizer import from_bytes


SUPPORTED_EXTS = {".html", ".htm", ".pdf", ".txt", ".md"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean RAG corpus")
    parser.add_argument("--input", default="data/raw", help="Raw data root")
    parser.add_argument("--output", default="data/processed", help="Output root")
    parser.add_argument("--min-chars", type=int, default=200)
    parser.add_argument("--min-line", type=int, default=3)
    return parser.parse_args()


def load_manifest_map(raw_root: Path) -> Dict[Path, str]:
    manifest = raw_root / "manifest.jsonl"
    if not manifest.exists():
        return {}
    mapping: Dict[Path, str] = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        rel = record.get("saved_path")
        url = record.get("url")
        if rel and url:
            mapping[raw_root / rel] = url
    return mapping




def decode_bytes(data: bytes) -> str:
    if not data:
        return ""
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        best = from_bytes(data).best()
        if best is not None:
            return str(best)
        return data.decode("cp1254", errors="ignore")


def extract_text_html(path: Path) -> str:
    raw = path.read_bytes()
    soup = BeautifulSoup(raw, "html.parser")
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside", "form"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    return text


def extract_text_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    parts = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            parts.append(text)
    return "\n".join(parts)


def extract_text_plain(path: Path) -> str:
    return decode_bytes(path.read_bytes())


def normalize_text(text: str, min_line: int) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [line.strip() for line in text.splitlines()]
    filtered = []
    seen = set()
    for line in lines:
        if len(line) < min_line:
            continue
        if line in seen:
            continue
        seen.add(line)
        filtered.append(line)
    return "\n".join(filtered).strip()


def slugify(text: str, limit: int = 60) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text[:limit] or "document"


def iter_files(root: Path) -> Iterable[Path]:
    for ext in SUPPORTED_EXTS:
        yield from root.rglob(f"*{ext}")


def main() -> int:
    args = parse_args()
    raw_root = Path(args.input)
    out_root = Path(args.output)
    out_docs = out_root / "docs"
    out_docs.mkdir(parents=True, exist_ok=True)

    url_map = load_manifest_map(raw_root)
    manifest_path = out_root / "manifest.jsonl"

    processed = 0
    with manifest_path.open("w", encoding="utf-8") as manifest:
        for path in iter_files(raw_root):
            suffix = path.suffix.lower()
            if suffix not in SUPPORTED_EXTS:
                continue

            if suffix in {".html", ".htm"}:
                text = extract_text_html(path)
            elif suffix == ".pdf":
                text = extract_text_pdf(path)
            else:
                text = extract_text_plain(path)

            text = normalize_text(text, args.min_line)
            if len(text) < args.min_chars:
                continue

            url = url_map.get(path)
            if url:
                text = f"SOURCE_URL: {url}\n\n" + text

            slug = slugify(path.stem)
            h = hashlib.sha1(str(path).encode("utf-8")).hexdigest()[:10]
            out_path = out_docs / f"{slug}-{h}.txt"
            out_path.write_text(text, encoding="utf-8")

            record = {
                "source_path": str(path),
                "output_path": str(out_path),
                "url": url,
                "chars": len(text),
            }
            manifest.write(json.dumps(record, ensure_ascii=False) + "\n")
            processed += 1

    stats = {"processed": processed, "output": str(out_root)}
    (out_root / "stats.json").write_text(
        json.dumps(stats, indent=2), encoding="utf-8"
    )
    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
