#!/usr/bin/env python3
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
}

MOJIBAKE_MARKERS = re.compile(r"[\u00c3\u00c5\u00c4\u00c2\u00d0\u00de\u0080-\u009f]")
MOJIBAKE_SEGMENT = re.compile(
    r"""[A-Za-z0-9"'`/\\:_.()[\]{}-]*"""
    r"[\u00c3\u00c5\u00c4\u00c2\u00d0\u00de\u0080-\u009f]"
    r"""[A-Za-z0-9"'`/\\:_.()[\]{}-]*"""
)

DIRECT_MAP = {
    "\u00c3\u00a7": "ç",
    "\u00c3\u0087": "Ç",
    "\u00c4\u00b1": "ı",
    "\u00c4\u00b0": "İ",
    "\u00c3\u00b6": "ö",
    "\u00c3\u0096": "Ö",
    "\u00c3\u00bc": "ü",
    "\u00c3\u009c": "Ü",
    "\u00c5\u00bf": "ş",
    "\u00c5\u017e": "Ş",
    "\u00c5\u009e": "Ş",
    "\u00c4\u017f": "ğ",
    "\u00c4\u017d": "Ğ",
    "\u00c5\u00bd\u00c3\u00b1": "ı",
}


def should_skip(path: Path) -> bool:
    for part in path.parts:
        if part in IGNORE_DIRS:
            return True
    return False


def iter_target_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if should_skip(path):
            continue
        if path.suffix.lower() not in TARGET_EXTS:
            continue
        files.append(path)
    return files


def fix_text(text: str) -> str:
    for bad, good in DIRECT_MAP.items():
        text = text.replace(bad, good)

    def repl(match: re.Match[str]) -> str:
        segment = match.group(0)
        try:
            return segment.encode("cp1252").decode("utf-8")
        except Exception:
            return segment

    return MOJIBAKE_SEGMENT.sub(repl, text)


def process_file(path: Path, dry_run: bool) -> tuple[bool, bool]:
    data = path.read_bytes()
    had_bom = data.startswith(b"\xef\xbb\xbf")
    if had_bom:
        data = data[3:]

    text = data.decode("utf-8", errors="replace")
    had_markers = bool(MOJIBAKE_MARKERS.search(text)) or "\ufffd" in text
    fixed = fix_text(text) if had_markers else text

    if fixed == text and not had_bom:
        return False, False

    if dry_run:
        return True, had_bom

    path.write_bytes(fixed.encode("utf-8"))
    return True, had_bom


def main() -> int:
    parser = argparse.ArgumentParser(description="Repo geneli mojibake düzeltici.")
    parser.add_argument("--dry-run", action="store_true", help="Dosyaları yazmadan raporla.")
    parser.add_argument("--root", default=".", help="Repo kök dizini (varsayılan: .)")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    files = iter_target_files(root)
    changed: list[Path] = []
    bom_fixed: list[Path] = []

    for path in files:
        did_change, had_bom = process_file(path, args.dry_run)
        if did_change:
            changed.append(path)
        if had_bom:
            bom_fixed.append(path)

    if args.dry_run:
        print(f"Değiştirilecek dosya sayısı: {len(changed)}")
    else:
        print(f"Güncellenen dosya sayısı: {len(changed)}")
    if bom_fixed:
        print(f"BOM temizlenen dosya sayısı: {len(bom_fixed)}")
    if changed:
        for path in changed:
            print(f"- {path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
