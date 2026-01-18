"""Comprehensive scraper for Selcuk University web properties.

Features:
- Sitemap discovery + robots.txt sitemaps
- Domain allowlist with normalization
- Robots.txt compliance
- Per-domain rate limiting
- HTML/PDF/DOCX extraction
- Deduplication by content hash
- Metadata JSONL output
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import logging
import re
import time
from dataclasses import dataclass
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Iterable, Optional
from urllib.parse import urljoin, urlparse, urlunparse
from urllib.robotparser import RobotFileParser

import httpx
from bs4 import BeautifulSoup
from pypdf import PdfReader

logger = logging.getLogger(__name__)

try:  # Optional dependency
    import docx  # type: ignore
except Exception:  # pragma: no cover - optional
    docx = None

_TURKISH_DOMAIN_MAP = str.maketrans(
    {
        "ç": "c",
        "ğ": "g",
        "ı": "i",
        "İ": "i",
        "ö": "o",
        "ş": "s",
        "ü": "u",
    }
)

DEFAULT_DOMAINS = [
    "selcuk.edu.tr",
    "bologna.selcuk.edu.tr",
    "obis.selcuk.edu.tr",
    "akademik.selcuk.edu.tr",
    "ogrenci.selcuk.edu.tr",
    "arsivadmin.selcuk.edu.tr",
    "muhendislik.selcuk.edu.tr",
    "bilgisayar.selcuk.edu.tr",
    "teknoloji.selcuk.edu.tr",
    "fen.selcuk.edu.tr",
    "mimtasarim.selcuk.edu.tr",
    "hastane.selcuk.edu.tr",
    "tip.selcuk.edu.tr",
    "dishekimligi.selcuk.edu.tr",
    "saglik.selcuk.edu.tr",
    "veteriner.selcuk.edu.tr",
    "eczacilik.selcuk.edu.tr",
    "iibf.selcuk.edu.tr",
    "edebiyat.selcuk.edu.tr",
    "ilahiyat.selcuk.edu.tr",
    "hukuk.selcuk.edu.tr",
    "iletisim.selcuk.edu.tr",
    "turizm.selcuk.edu.tr",
    "spor.selcuk.edu.tr",
    "egitim.selcuk.edu.tr",
    "guzelsanatlar.selcuk.edu.tr",
    "konservatuar.selcuk.edu.tr",
    "aksehir.selcuk.edu.tr",
    "beysehir.selcuk.edu.tr",
    "ziraat.selcuk.edu.tr",
    "fbe.selcuk.edu.tr",
    "sbe.selcuk.edu.tr",
    "sagens.selcuk.edu.tr",
    "ebe.selcuk.edu.tr",
    "mevlanaenstitusu.selcuk.edu.tr",
    "selcukluarastirmalari.selcuk.edu.tr",
    "turkiyat.selcuk.edu.tr",
    "ardek.selcuk.edu.tr",
    "sudem.selcuk.edu.tr",
    "library.selcuk.edu.tr",
    "bap.selcuk.edu.tr",
    "sulabs.selcuk.edu.tr",
    "cukurovamyo.selcuk.edu.tr",
    "cumramyo.selcuk.edu.tr",
    "karapinarmyo.selcuk.edu.tr",
    "taskentmyo.selcuk.edu.tr",
    "sosyalbilmyo.selcuk.edu.tr",
    "saglikmyo.selcuk.edu.tr",
    "teknikmyo.selcuk.edu.tr",
    "uzaktanegitim.selcuk.edu.tr",
    "aday.selcuk.edu.tr",
    "kariyer.selcuk.edu.tr",
    "engelsiz.selcuk.edu.tr",
    "psikolojikdanisma.selcuk.edu.tr",
    "yabancilar.selcuk.edu.tr",
    "erasmus.selcuk.edu.tr",
    "duyuru.selcuk.edu.tr",
    "mevzuat.selcuk.edu.tr",
    "senato.selcuk.edu.tr",
    "sinav.selcuk.edu.tr",
    "akademiktakvim.selcuk.edu.tr",
    "dergisosyalbil.selcuk.edu.tr",
    "yok.selcuk.edu.tr",
]

BLOCKED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".svg",
    ".ico",
    ".css",
    ".js",
    ".zip",
    ".rar",
    ".7z",
    ".tar",
    ".gz",
    ".mp3",
    ".mp4",
    ".avi",
    ".mov",
    ".wav",
    ".xml",
}

def normalize_domain(raw: str) -> str:
    value = raw.strip().lower()
    if not value:
        return ""
    if value.startswith("http://") or value.startswith("https://"):
        value = urlparse(value).netloc
    value = value.replace("www.", "")
    value = value.replace(" ", "")
    value = value.translate(_TURKISH_DOMAIN_MAP)
    value = value.split("/")[0]
    return value


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    parsed = parsed._replace(fragment="")
    return urlunparse(parsed)


def load_domains(domains_file: Optional[Path], domains_arg: Optional[str]) -> list[str]:
    domains: list[str] = []
    if domains_file and domains_file.exists():
        for line in domains_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            domains.append(normalize_domain(line))
    if domains_arg:
        for item in domains_arg.split(","):
            item = item.strip()
            if not item:
                continue
            domains.append(normalize_domain(item))
    if not domains:
        domains = [normalize_domain(domain) for domain in DEFAULT_DOMAINS]
    return sorted(set(filter(None, domains)))


def is_allowed_domain(netloc: str, allowed_domains: Iterable[str]) -> bool:
    if not netloc:
        return False
    netloc = netloc.lower()
    for domain in allowed_domains:
        if netloc == domain or netloc.endswith(f".{domain}"):
            return True
    return False


def clean_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines).strip()


@dataclass
class ScrapeConfig:
    output_dir: Path
    metadata_jsonl: Path
    max_depth: int
    max_pages: int
    max_links_per_page: int
    concurrency: int
    rate_limit: float
    timeout: float
    user_agent: str
    min_chars: int
    allow_queries: bool
    allowed_domains: list[str]


class RobotsCache:
    def __init__(self, client: httpx.AsyncClient, user_agent: str) -> None:
        self._client = client
        self._user_agent = user_agent
        self._cache: dict[str, RobotFileParser] = {}
        self._lock = asyncio.Lock()

    async def allowed(self, url: str) -> bool:
        parsed = urlparse(url)
        domain = parsed.netloc
        if not domain:
            return False
        if domain in self._cache:
            return self._cache[domain].can_fetch(self._user_agent, url)

        async with self._lock:
            if domain in self._cache:
                return self._cache[domain].can_fetch(self._user_agent, url)
            robots_url = f"{parsed.scheme}://{domain}/robots.txt"
            parser = RobotFileParser()
            try:
                resp = await self._client.get(robots_url)
                if resp.status_code == 200:
                    parser.parse(resp.text.splitlines())
                else:
                    parser.parse([])
            except Exception:
                parser.parse([])
            self._cache[domain] = parser
            return parser.can_fetch(self._user_agent, url)


class RateLimiter:
    def __init__(self, interval: float) -> None:
        self._interval = max(0.0, interval)
        self._next_time: dict[str, float] = {}
        self._lock = asyncio.Lock()

    async def wait(self, key: str) -> None:
        if self._interval <= 0:
            return
        async with self._lock:
            now = time.monotonic()
            next_allowed = self._next_time.get(key, now)
            wait_for = max(0.0, next_allowed - now)
            self._next_time[key] = max(next_allowed, now) + self._interval
        if wait_for:
            await asyncio.sleep(wait_for)


class SelcukComprehensiveScraper:
    def __init__(self, config: ScrapeConfig) -> None:
        self._config = config
        self._queue: asyncio.Queue[tuple[str, int]] = asyncio.Queue()
        self._visited_urls: set[str] = set()
        self._visited_hashes: set[str] = set()
        self._lock = asyncio.Lock()
        self._pages_scraped = 0
        self._stop = False

    async def _enqueue(self, url: str, depth: int) -> None:
        if self._stop:
            return
        url = normalize_url(url)
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return
        if not is_allowed_domain(parsed.netloc, self._config.allowed_domains):
            return
        if not self._config.allow_queries and parsed.query:
            return
        if parsed.fragment:
            return
        async with self._lock:
            if url in self._visited_urls:
                return
            self._visited_urls.add(url)
        await self._queue.put((url, depth))

    async def _reserve_page(self) -> bool:
        async with self._lock:
            if self._pages_scraped >= self._config.max_pages:
                self._stop = True
                return False
            self._pages_scraped += 1
            if self._pages_scraped >= self._config.max_pages:
                self._stop = True
            return True

    async def _write_metadata(self, record: dict[str, Any]) -> None:
        record_line = json.dumps(record, ensure_ascii=False)
        async with self._lock:
            self._config.metadata_jsonl.parent.mkdir(parents=True, exist_ok=True)
            with self._config.metadata_jsonl.open("a", encoding="utf-8") as handle:
                handle.write(record_line + "\n")

    async def _discover_sitemaps(self, client: httpx.AsyncClient, domain: str) -> list[str]:
        urls: list[str] = []
        base = f"https://{domain}"
        candidates = [
            f"{base}/sitemap.xml",
            f"{base}/sitemap_index.xml",
            f"{base}/robots.txt",
        ]
        seen: set[str] = set()
        for candidate in candidates:
            try:
                resp = await client.get(candidate)
                if resp.status_code != 200:
                    continue
                if candidate.endswith("robots.txt"):
                    for line in resp.text.splitlines():
                        if line.lower().startswith("sitemap:"):
                            sitemap_url = line.split(":", 1)[1].strip()
                            if sitemap_url:
                                urls.extend(
                                    await self._collect_sitemap_urls(
                                        client, sitemap_url, seen
                                    )
                                )
                    continue
                urls.extend(await self._collect_sitemap_urls(client, candidate, seen))
            except Exception:
                continue
        return urls

    def _parse_sitemap(self, xml_text: str) -> list[str]:
        urls: list[str] = []
        for loc in re.findall(r"<loc>(.*?)</loc>", xml_text, flags=re.IGNORECASE):
            url = loc.strip()
            if url:
                urls.append(url)
        return urls

    async def _collect_sitemap_urls(
        self,
        client: httpx.AsyncClient,
        sitemap_url: str,
        seen: set[str],
    ) -> list[str]:
        if sitemap_url in seen:
            return []
        seen.add(sitemap_url)
        try:
            resp = await client.get(sitemap_url)
            if resp.status_code != 200:
                return []
        except Exception:
            return []

        urls = self._parse_sitemap(resp.text)
        collected: list[str] = []
        for url in urls:
            if url.lower().endswith(".xml"):
                collected.extend(await self._collect_sitemap_urls(client, url, seen))
            else:
                collected.append(url)
        return collected

    async def _scrape_html(
        self,
        client: httpx.AsyncClient,
        url: str,
    ) -> tuple[Optional[str], list[str], Optional[str]]:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code >= 400:
            return None, [], f"http_{resp.status_code}"

        content_type = resp.headers.get("content-type", "")
        if "text/html" not in content_type and not url.lower().endswith((".html", ".htm")):
            return None, [], "not_html"

        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
        title = soup.title.get_text(strip=True) if soup.title else ""
        text = clean_text(soup.get_text(separator="\n"))
        links = []
        for link in soup.find_all("a", href=True):
            href = link.get("href", "").strip()
            if not href or href.startswith("#"):
                continue
            new_url = urljoin(url, href)
            links.append(new_url)
        return text, links, title

    async def _scrape_pdf(
        self,
        client: httpx.AsyncClient,
        url: str,
    ) -> tuple[Optional[str], Optional[str]]:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code >= 400:
            return None, f"http_{resp.status_code}"
        try:
            reader = PdfReader(BytesIO(resp.content))
        except Exception:
            return None, "pdf_parse_failed"
        text_parts = []
        for page in reader.pages:
            page_text = page.extract_text() or ""
            if page_text.strip():
                text_parts.append(page_text)
        text = clean_text("\n".join(text_parts))
        return text, None

    async def _scrape_docx(
        self,
        client: httpx.AsyncClient,
        url: str,
    ) -> tuple[Optional[str], Optional[str]]:
        if docx is None:
            return None, "docx_dependency_missing"
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code >= 400:
            return None, f"http_{resp.status_code}"
        try:
            document = docx.Document(BytesIO(resp.content))  # type: ignore[union-attr]
        except Exception:
            return None, "docx_parse_failed"
        text_parts = [para.text for para in document.paragraphs if para.text.strip()]
        text = clean_text("\n".join(text_parts))
        return text, None

    def _should_skip_url(self, url: str) -> bool:
        parsed = urlparse(url)
        path = parsed.path.lower()
        if any(path.endswith(ext) for ext in BLOCKED_EXTENSIONS):
            return True
        return False

    async def _handle_url(
        self,
        client: httpx.AsyncClient,
        robots: RobotsCache,
        limiter: RateLimiter,
        url: str,
        depth: int,
    ) -> list[str]:
        if self._stop:
            return []
        parsed = urlparse(url)
        domain = parsed.netloc
        if not domain:
            return []
        if self._should_skip_url(url):
            return []
        allowed = await robots.allowed(url)
        if not allowed:
            return []
        await limiter.wait(domain)

        if not await self._reserve_page():
            return []

        extension = Path(parsed.path).suffix.lower()
        text: Optional[str] = None
        title: Optional[str] = None
        error: Optional[str] = None
        links: list[str] = []

        if extension == ".pdf":
            text, error = await self._scrape_pdf(client, url)
        elif extension in {".doc", ".docx"}:
            text, error = await self._scrape_docx(client, url)
        else:
            text, links, title = await self._scrape_html(client, url)

        if error:
            await self._write_metadata(
                {
                    "url": url,
                    "status": "error",
                    "error": error,
                    "scraped_at": datetime.utcnow().isoformat(),
                }
            )
            return []

        if not text or len(text) < self._config.min_chars:
            await self._write_metadata(
                {
                    "url": url,
                    "status": "skipped",
                    "reason": "empty_or_short",
                    "scraped_at": datetime.utcnow().isoformat(),
                }
            )
            return []

        content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        async with self._lock:
            if content_hash in self._visited_hashes:
                return []
            self._visited_hashes.add(content_hash)

        filename = f"{domain}_{content_hash[:10]}.txt"
        output_path = self._config.output_dir / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        header_lines = [
            f"SOURCE_URL: {url}",
            f"TITLE: {title or ''}",
            f"SCRAPED_AT: {datetime.utcnow().isoformat()}",
            f"CONTENT_HASH: {content_hash}",
        ]
        output_path.write_text(
            "\n".join(header_lines) + "\n\n" + text,
            encoding="utf-8",
        )

        await self._write_metadata(
            {
                "url": url,
                "title": title,
                "content_hash": content_hash,
                "file": str(output_path),
                "scraped_at": datetime.utcnow().isoformat(),
                "length": len(text),
                "depth": depth,
            }
        )

        if depth >= self._config.max_depth:
            return []

        if not links:
            return []

        filtered_links: list[str] = []
        for link in links:
            if len(filtered_links) >= self._config.max_links_per_page:
                break
            if self._should_skip_url(link):
                continue
            parsed_link = urlparse(link)
            if not is_allowed_domain(parsed_link.netloc, self._config.allowed_domains):
                continue
            filtered_links.append(link)
        return filtered_links

    async def _worker(
        self,
        client: httpx.AsyncClient,
        robots: RobotsCache,
        limiter: RateLimiter,
    ) -> None:
        while True:
            item = await self._queue.get()
            if item is None:  # type: ignore[comparison-overlap]
                self._queue.task_done()
                break
            url, depth = item
            try:
                new_links = await self._handle_url(client, robots, limiter, url, depth)
                for link in new_links:
                    await self._enqueue(link, depth + 1)
            except Exception as exc:
                await self._write_metadata(
                    {
                        "url": url,
                        "status": "error",
                        "error": str(exc),
                        "scraped_at": datetime.utcnow().isoformat(),
                    }
                )
            finally:
                self._queue.task_done()

    async def run(self, seeds: list[str]) -> None:
        async with httpx.AsyncClient(
            headers={"User-Agent": self._config.user_agent},
            timeout=self._config.timeout,
        ) as client:
            robots = RobotsCache(client, self._config.user_agent)
            limiter = RateLimiter(self._config.rate_limit)

            for seed in seeds:
                await self._enqueue(seed, 0)

            workers = [
                asyncio.create_task(self._worker(client, robots, limiter))
                for _ in range(self._config.concurrency)
            ]

            await self._queue.join()
            for _ in workers:
                await self._queue.put(None)  # type: ignore[arg-type]
            await asyncio.gather(*workers, return_exceptions=True)


def build_config(domains: list[str], args: argparse.Namespace) -> ScrapeConfig:
    output_dir = Path(args.output_dir)
    metadata_jsonl = Path(args.metadata_jsonl)
    return ScrapeConfig(
        output_dir=output_dir,
        metadata_jsonl=metadata_jsonl,
        max_depth=args.max_depth,
        max_pages=args.max_pages,
        max_links_per_page=args.max_links_per_page,
        concurrency=args.concurrency,
        rate_limit=args.rate_limit,
        timeout=args.timeout,
        user_agent=args.user_agent,
        min_chars=args.min_chars,
        allow_queries=args.allow_queries,
        allowed_domains=domains,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Comprehensive Selcuk scraper")
    parser.add_argument(
        "--domains-file",
        default="data/scrape_domains.txt",
        help="Domain list file (one per line).",
    )
    parser.add_argument(
        "--domains",
        default=None,
        help="Comma-separated domains or URLs to include.",
    )
    parser.add_argument(
        "--output-dir",
        default="data/rag/scraped",
        help="Output directory for scraped text files.",
    )
    parser.add_argument(
        "--metadata-jsonl",
        default="data/rag/scraped/metadata.jsonl",
        help="JSONL metadata output path.",
    )
    parser.add_argument("--max-depth", type=int, default=3)
    parser.add_argument("--max-pages", type=int, default=10000)
    parser.add_argument("--max-links-per-page", type=int, default=50)
    parser.add_argument("--concurrency", type=int, default=5)
    parser.add_argument("--rate-limit", type=float, default=1.5)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument(
        "--user-agent",
        default="SelcukAIAssistantBot/1.0 (+https://www.selcuk.edu.tr)",
    )
    parser.add_argument("--min-chars", type=int, default=400)
    parser.add_argument("--allow-queries", action="store_true")
    parser.add_argument("--no-sitemap", action="store_true")
    return parser.parse_args()


async def build_seed_urls(domains: list[str], use_sitemap: bool) -> list[str]:
    seeds: list[str] = []
    async with httpx.AsyncClient(timeout=15.0) as client:
        scraper = SelcukComprehensiveScraper(
            ScrapeConfig(
                output_dir=Path("data/rag/scraped"),
                metadata_jsonl=Path("data/rag/scraped/metadata.jsonl"),
                max_depth=0,
                max_pages=0,
                max_links_per_page=0,
                concurrency=1,
                rate_limit=0,
                timeout=10,
                user_agent="SelcukAIAssistantBot/1.0 (+https://www.selcuk.edu.tr)",
                min_chars=0,
                allow_queries=False,
                allowed_domains=domains,
            )
        )
        for domain in domains:
            seeds.append(f"https://{domain}/")
            if not use_sitemap:
                continue
            sitemap_urls = await scraper._discover_sitemaps(client, domain)
            for url in sitemap_urls:
                if is_allowed_domain(urlparse(url).netloc, domains):
                    seeds.append(url)
    return sorted(set(seeds))


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    args = parse_args()
    domains = load_domains(Path(args.domains_file), args.domains)
    if not domains:
        logger.error("No domains provided.")
        return

    config = build_config(domains, args)
    config.output_dir.mkdir(parents=True, exist_ok=True)
    seed_urls = await build_seed_urls(domains, use_sitemap=not args.no_sitemap)

    logger.info("Domains: %s", ", ".join(domains))
    logger.info("Seeds: %d urls", len(seed_urls))
    logger.info("Output: %s", config.output_dir)

    scraper = SelcukComprehensiveScraper(config)
    await scraper.run(seed_urls)

    summary = {
        "domains": domains,
        "seed_count": len(seed_urls),
        "output_dir": str(config.output_dir),
        "metadata_jsonl": str(config.metadata_jsonl),
        "scraped_at": datetime.utcnow().isoformat(),
    }
    summary_path = config.metadata_jsonl.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    asyncio.run(main())
