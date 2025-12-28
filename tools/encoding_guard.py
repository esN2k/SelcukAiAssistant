#!/usr/bin/env python3
"""UTF-8/BOM ve mojibake denetimi için CI aracı."""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

BOM = b"\xef\xbb\xbf"

TEXT_EXTS = {
    ".arb",
    ".cfg",
    ".dart",
    ".env",
    ".ini",
    ".json",
    ".md",
    ".ps1",
    ".py",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

EXTRA_FILES = {
    ".editorconfig",
    "pubspec.yaml",
    "analysis_options.yaml",
    "docker-compose.yml",
    "nginx.conf",
    "mypy.ini",
}

EXCLUDE_DIRS = {
    ".git",
    ".dart_tool",
    ".idea",
    ".vscode",
    ".venv",
    "venv",
    "build",
    "android",
    "ios",
    "windows",
    "web",
    "benchmark",
}

EXCLUDE_PATHS = {
    Path("backend") / "data" / "rag",
    Path("docs") / "logo",
    Path("docs") / "vize_raporu",
    Path("docs") / "final_raporu",
    Path("tools") / ".tmp",
}

# \u00C3., \u00C5., \u00C4., \u00C2., \u00D0. ve \u00DE. kalıpları, UTF-8'in
# ISO-8859-1/Windows-1252 gibi tek baytlık kodlamalarla yanlış çözümlenmesinden
# kaynaklanan tipik 2 baytlık mojibake dizilerini yakalar; U+FFFD de burada
# aynı taramanın parçası olarak dahil edilmiştir.
MOJIBAKE_REGEX = re.compile(r"(\u00c3.|\u00c5.|\u00c4.|\u00c2.|\u00d0.|\u00de.|\uFFFD)")
C1_CONTROLS = re.compile(r"[\u0080-\u009f]")


def _configure_utf8_output() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except (AttributeError, ValueError):
                continue


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = Path(dirpath).relative_to(root)
        if rel_dir in EXCLUDE_PATHS:
            dirnames[:] = []
            continue
        dirnames[:] = [
            name
            for name in dirnames
            if name not in EXCLUDE_DIRS and (rel_dir / name) not in EXCLUDE_PATHS
        ]
        for filename in filenames:
            path = Path(dirpath) / filename
            if path.suffix.lower() not in TEXT_EXTS and path.name not in EXTRA_FILES:
                continue
            files.append(path)
    return files


def check_file(path: Path) -> list[str]:
    errors: list[str] = []
    data = path.read_bytes()
    if data.startswith(BOM):
        errors.append("BOM tespit edildi")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        errors.append("UTF-8 dışı içerik")
        return errors
    if "\ufffd" in text:
        errors.append("Unicode replacement char (U+FFFD) bulundu")
    if C1_CONTROLS.search(text):
        errors.append("C1 kontrol karakteri bulundu")
    if MOJIBAKE_REGEX.search(text):
        errors.append("Mojibake dizisi bulundu")
    return errors


def main() -> int:
    _configure_utf8_output()
    parser = argparse.ArgumentParser(description="UTF-8 ve mojibake denetimi.")
    parser.add_argument(
        "--root",
        default=".",
        help="Repo kök dizini (varsayılan: .).",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    problems: dict[Path, list[str]] = {}
    for path in iter_files(root):
        issues = check_file(path)
        if issues:
            problems[path] = issues

    if not problems:
        print("Encoding kontrolü: sorun bulunmadı.")
        return 0

    print("Encoding kontrolü: sorun bulundu.")
    for path, issues in sorted(problems.items()):
        issue_text = "; ".join(issues)
        print(f"- {path.relative_to(root)}: {issue_text}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
