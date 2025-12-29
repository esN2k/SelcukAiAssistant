#!/usr/bin/env python3
"""Collect public Selcuk University pages (HTML/PDF) for RAG."""
from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import json
import time
import re
from collections import deque
from dataclasses import dataclass
from typing import Iterable, Optional
from urllib.parse import urljoin, urlparse, urldefrag, parse_qsl, urlencode
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET

import requests
import urllib3
from bs4 import BeautifulSoup


TRACKING_KEYS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "fbclid",
    "gclid",
}


@dataclass
class CrawlConfig:
    allowed_domains: list[str]
    seeds: list[str]
    sitemaps: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Website crawler for RAG sources")
    parser.add_argument(
        "--config",
        default="tools/sources_selcuk.json",
        help="JSON config with seeds/domains",
    )
    parser.add_argument(
        "--output",
        default="data/raw",
        help="Output directory for raw downloads",
    )
    parser.add_argument("--max-pages", type=int, default=400)
    parser.add_argument("--max-depth", type=int, default=3)
    parser.add_argument("--delay", type=float, default=0.6)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--max-bytes", type=int, default=15_000_000)
    parser.add_argument(
        "--user-agent",
        default="SelcukAIResearchBot/1.0 (+research)",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable TLS certificate verification",
    )
    parser.add_argument(
        "--ca-bundle",
        default=None,
        help="Path to a CA bundle for HTTPS verification.",
    )
    return parser.parse_args()


def load_config(path: str) -> CrawlConfig:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return CrawlConfig(
        allowed_domains=[d.lower() for d in data.get("allowed_domains", [])],
        seeds=data.get("seeds", []),
        sitemaps=data.get("sitemaps", []),
    )


def normalize_url(url: str) -> str:
    url, _ = urldefrag(url)
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return ""
    query = [(k, v) for k, v in parse_qsl(parsed.query) if k not in TRACKING_KEYS]
    new_query = urlencode(query, doseq=True)
    normalized = parsed._replace(query=new_query).geturl()
    return normalized.rstrip("/") if normalized.endswith("/") else normalized


def is_allowed_domain(url: str, allowed_domains: Iterable[str]) -> bool:
    netloc = urlparse(url).netloc.lower()
    return any(netloc == d or netloc.endswith("." + d) for d in allowed_domains)


def extract_links(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    links: list[str] = []
    for tag in soup.find_all("a", href=True):
        href = tag.get("href")
        if not href:
            continue
        if href.startswith("mailto:") or href.startswith("tel:"):
            continue
        if href.startswith("javascript:"):
            continue
        links.append(urljoin(base_url, href))
    return links


def slugify(text: str, limit: int = 60) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text[:limit] or "page"


def save_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def load_sitemap_urls(session: requests.Session, url: str, timeout: int) -> list[str]:
    urls: list[str] = []
    try:
        resp = session.get(url, timeout=timeout)
        resp.raise_for_status()
    except Exception:
        return urls
    try:
        root = ET.fromstring(resp.content)
    except ET.ParseError:
        return urls
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    if root.tag.endswith("sitemapindex"):
        for loc in root.findall(f"{ns}sitemap/{ns}loc"):
            if loc.text:
                urls.extend(load_sitemap_urls(session, loc.text.strip(), timeout))
        return urls
    for loc in root.findall(f"{ns}url/{ns}loc"):
        if loc.text:
            urls.append(loc.text.strip())
    return urls


def get_robot_parser(session: requests.Session, base_url: str, user_agent: str) -> RobotFileParser:
    parsed = urlparse(base_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    parser = RobotFileParser()
    parser.set_url(robots_url)
    try:
        resp = session.get(robots_url, timeout=10)
        if resp.status_code == 200:
            parser.parse(resp.text.splitlines())
        else:
            parser.parse("")
    except Exception:
        parser.parse("")
    return parser


def main() -> int:
    args = parse_args()
    config = load_config(args.config)

    raw_root = Path(args.output)
    raw_html = raw_root / "html"
    raw_pdf = raw_root / "pdf"
    manifest_path = raw_root / "manifest.jsonl"

    session = requests.Session()
    session.headers.update({"User-Agent": args.user_agent})
    session.headers.update({"Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"})
    verify: Optional[bool | str] = True
    if args.ca_bundle:
        verify = args.ca_bundle
    if args.insecure:
        verify = False
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    session.verify = verify

    robots_cache: dict[str, RobotFileParser] = {}
    def can_fetch(url: str) -> bool:
        parsed = urlparse(url)
        key = parsed.netloc.lower()
        if key not in robots_cache:
            robots_cache[key] = get_robot_parser(session, url, args.user_agent)
        return robots_cache[key].can_fetch(args.user_agent, url)

    queue = deque()
    seen: set[str] = set()
    for seed in config.seeds:
        normalized = normalize_url(seed)
        if normalized:
            queue.append((normalized, 0))

    for sitemap in config.sitemaps:
        for url in load_sitemap_urls(session, sitemap, args.timeout):
            normalized = normalize_url(url)
            if normalized:
                queue.append((normalized, 0))

    saved = 0
    visited = 0
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("w", encoding="utf-8") as manifest:
        while queue and saved < args.max_pages:
            url, depth = queue.popleft()
            if url in seen:
                continue
            seen.add(url)
            visited += 1
            if not is_allowed_domain(url, config.allowed_domains):
                continue
            if not can_fetch(url):
                continue

            try:
                resp = session.get(url, timeout=args.timeout)
            except Exception:
                continue
            content_type = resp.headers.get("content-type", "").lower()
            status = resp.status_code

            if status != 200:
                continue

            data = resp.content
            if len(data) > args.max_bytes:
                continue

            is_pdf = "application/pdf" in content_type or url.lower().endswith(".pdf")
            if is_pdf:
                slug = slugify(Path(urlparse(url).path).stem or "document")
                h = hashlib.sha1(url.encode("utf-8")).hexdigest()[:10]
                out_path = raw_pdf / f"{slug}-{h}.pdf"
                save_bytes(out_path, data)
                record = {
                    "url": url,
                    "content_type": content_type,
                    "status": status,
                    "saved_path": str(out_path.relative_to(raw_root)),
                    "bytes": len(data),
                }
                manifest.write(json.dumps(record, ensure_ascii=False) + "\n")
                saved += 1
            elif "text/html" in content_type:
                slug = slugify(Path(urlparse(url).path).stem or "page")
                h = hashlib.sha1(url.encode("utf-8")).hexdigest()[:10]
                out_path = raw_html / f"{slug}-{h}.html"
                save_bytes(out_path, data)
                record = {
                    "url": url,
                    "content_type": content_type,
                    "status": status,
                    "saved_path": str(out_path.relative_to(raw_root)),
                    "bytes": len(data),
                }
                manifest.write(json.dumps(record, ensure_ascii=False) + "\n")
                saved += 1

                if depth < args.max_depth:
                    html = resp.text
                    for link in extract_links(html, url):
                        normalized = normalize_url(link)
                        if not normalized:
                            continue
                        if not is_allowed_domain(normalized, config.allowed_domains):
                            continue
                        if normalized in seen:
                            continue
                        queue.append((normalized, depth + 1))
            else:
                continue

            if args.delay:
                time.sleep(args.delay)

    stats = {
        "visited": visited,
        "saved": saved,
        "max_pages": args.max_pages,
        "output": str(raw_root),
    }
    (raw_root / "stats.json").write_text(
        json.dumps(stats, indent=2), encoding="utf-8"
    )
    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
