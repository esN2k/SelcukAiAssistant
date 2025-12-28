#!/usr/bin/env python3
"""Depo genelinde Türkçe mojibake ve BOM düzelticisi."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TARGET_EXTS = {
    ".arb",
    ".dart",
    ".md",
    ".py",
    ".yml",
    ".yaml",
    ".json",
    ".ps1",
    ".sh",
    ".txt",
    ".env",
}

IGNORE_DIRS = {
    ".git",
    ".dart_tool",
    ".idea",
    ".vscode",
    ".venv",
    "venv",
    "build",
    "ios",
    "android",
    "web",
    "windows",
    "benchmark",
}

EXTRA_FILES = {
    ".editorconfig",
    "pubspec.yaml",
    "analysis_options.yaml",
    "docker-compose.yml",
    "nginx.conf",
    "mypy.ini",
}

IGNORE_FILES = {
    "fix_mojibake.py",
}

SEQUENCE_REPLACEMENTS = {
    "\u00c3\u00a7": "\u00e7",
    "\u00c3\u0087": "\u00c7",
    "\u00c4\u00b1": "\u0131",
    "\u00c4\u00b0": "\u0130",
    "\u00c3\u00b6": "\u00f6",
    "\u00c3\u0096": "\u00d6",
    "\u00c3\u00bc": "\u00fc",
    "\u00c3\u009c": "\u00dc",
    "\u00c5\u017f": "\u015f",
    "\u00c5\u017d": "\u015e",
    "\u00c4\u017f": "\u011f",
    "\u00c4\u017d": "\u011e",
    "\u00c2\u00b0": "\u00b0",
    "\u00c2\u00a0": " ",
}

CHAR_REPLACEMENTS = {
    "\u2021": "\u00e7",
    "\u20ac": "\u00c7",
    "\u008d": "\u0131",
    "\u02dc": "\u0130",
    "\u0081": "\u00fc",
    "\u0161": "\u00dc",
    "\u0178": "\u015f",
    "\u017e": "\u015e",
    "\u00a7": "\u011f",
    "\u00a6": "\u011e",
}

WORD_REPLACEMENTS = {
    "\u201d": "\u00f6",
    "\u2122": "\u00d6",
}

WORD_PATTERN = re.compile(r"(?<=\w)([\u201d\u2122])(?=\w)")


def _configure_utf8_output() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except (AttributeError, ValueError):
                continue


def should_skip(path: Path) -> bool:
    """Dizin tabanlı hariç bırakma kuralı uygula."""
    for part in path.parts:
        if part in IGNORE_DIRS:
            return True
    return False


def iter_target_files(root: Path, paths: list[str]) -> list[Path]:
    """İşlenecek hedef dosyaları belirle."""
    if paths:
        targets: list[Path] = []
        for raw in paths:
            candidate = (root / raw).resolve()
            if not candidate.exists():
                continue
            if candidate.is_file():
                targets.append(candidate)
            else:
                targets.extend(
                    path
                    for path in candidate.rglob("*")
                    if path.is_file() and not should_skip(path)
                )
        return targets

    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if should_skip(path):
            continue
        if path.name in IGNORE_FILES:
            continue
        if path.suffix.lower() in TARGET_EXTS or path.name in EXTRA_FILES:
            files.append(path)
    return files


def _replace_word_chars(text: str) -> str:
    return WORD_PATTERN.sub(lambda match: WORD_REPLACEMENTS[match.group(1)], text)


def fix_text(text: str) -> str:
    """Mojibake ve bozuk Türkçe karakterleri düzelt."""
    fixed = text.replace("\ufeff", "")
    for bad, good in SEQUENCE_REPLACEMENTS.items():
        fixed = fixed.replace(bad, good)
    fixed = _replace_word_chars(fixed)
    for bad, good in CHAR_REPLACEMENTS.items():
        fixed = fixed.replace(bad, good)
    return fixed


def process_file(path: Path, dry_run: bool) -> tuple[bool, bool]:
    data = path.read_bytes()
    had_bom = data.startswith(b"\xef\xbb\xbf")
    if had_bom:
        data = data[3:]

    text = data.decode("utf-8", errors="replace")
    fixed = fix_text(text)

    if fixed == text and not had_bom:
        return False, False

    if dry_run:
        return True, had_bom

    path.write_text(fixed, encoding="utf-8")
    return True, had_bom


def main() -> int:
    _configure_utf8_output()
    parser = argparse.ArgumentParser(
        description="Depo genelinde mojibake ve BOM düzeltir."
    )
    parser.add_argument("--dry-run", action="store_true", help="Değişimleri raporla.")
    parser.add_argument(
        "--root",
        default=".",
        help="Repo kök dizini (varsayılan: .).",
    )
    parser.add_argument(
        "--paths",
        nargs="*",
        default=[],
        help="İşlenecek dosya veya klasör yolları (opsiyonel).",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    files = iter_target_files(root, args.paths)
    changed: list[Path] = []
    bom_fixed: list[Path] = []

    for path in files:
        did_change, had_bom = process_file(path, args.dry_run)
        if did_change:
            changed.append(path)
        if had_bom:
            bom_fixed.append(path)

    label = "Değiştirilecek" if args.dry_run else "Güncellenen"
    print(f"{label} dosya sayısı: {len(changed)}")
    if bom_fixed:
        print(f"BOM temizlenen dosya sayısı: {len(bom_fixed)}")
    for path in changed:
        print(f"- {path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
