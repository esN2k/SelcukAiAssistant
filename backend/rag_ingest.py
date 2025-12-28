"""FAISS RAG indeksi için belge alma (ingest) aracı."""
from __future__ import annotations

import argparse
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from bs4 import BeautifulSoup
from pypdf import PdfReader

from config import Config
from rag_service import Document, RagIndex, SentenceTransformerBackend, chunk_text

logger = logging.getLogger(__name__)


def _configure_utf8_output() -> None:
    """Giriş: yok.

    Çıkış: yok.
    İşleyiş: stdout/stderr akışlarını UTF-8 olarak yapılandırır.
    """
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except (AttributeError, ValueError):
                continue


_configure_utf8_output()


@dataclass
class SourceChunk:
    """Giriş: İçerik ve sayfa bilgisi.

    Çıkış: Veri kapsülü.
    İşleyiş: Kaynak parçasını taşır.
    """

    content: str
    source: str
    page: int | None = None


def _read_text_file(path: Path) -> str:
    """Giriş: Dosya yolu.

    Çıkış: Metin.
    İşleyiş: UTF-8 okuyup temel temizlik uygular.
    """
    return path.read_text(encoding="utf-8", errors="ignore")


def _read_pdf(path: Path) -> list[SourceChunk]:
    """Giriş: PDF yolu.

    Çıkış: Sayfa parçaları.
    İşleyiş: Sayfa metinlerini ayrıştırır.
    """
    reader = PdfReader(str(path))
    chunks: list[SourceChunk] = []
    for page_index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        cleaned = text.strip()
        if cleaned:
            chunks.append(SourceChunk(content=cleaned, source=path.name, page=page_index))
    return chunks


def _read_html(path: Path) -> str:
    """Giriş: HTML yolu.

    Çıkış: Metin.
    İşleyiş: Görünür metni süzer.
    """
    html = path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())


def _load_chunks(path: Path) -> list[SourceChunk]:
    """Giriş: Dosya yolu.

    Çıkış: Kaynak parçaları.
    İşleyiş: Uzantıya göre içerik okur.
    """
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return _read_pdf(path)
    if suffix in {".html", ".htm"}:
        text = _read_html(path)
        return [SourceChunk(content=text, source=path.name)]
    text = _read_text_file(path)
    return [SourceChunk(content=text, source=path.name)]


def _chunk_source(
    source: SourceChunk,
    chunk_size: int,
    chunk_overlap: int,
) -> list[Document]:
    """Giriş: Kaynak ve parça ayarları.

    Çıkış: Document listesi.
    İşleyiş: chunk_text ile parçalara böler.
    """
    docs: list[Document] = []
    for idx, chunk in enumerate(chunk_text(source.content, chunk_size, chunk_overlap)):
        docs.append(
            Document(
                content=chunk,
                metadata={
                    "source": source.source,
                    "page": source.page,
                    "chunk": idx + 1,
                },
            )
        )
    return docs


def iter_input_files(input_path: Path, extensions: Sequence[str]) -> Iterable[Path]:
    """Giriş: Dizin ve uzantılar.

    Çıkış: Dosya yolu akışı.
    İşleyiş: rglob ile dosyaları tarar.
    """
    if input_path.is_file():
        yield input_path
        return
    for ext in extensions:
        yield from input_path.rglob(f"*{ext}")


def build_documents(
    input_path: Path,
    extensions: Sequence[str],
    chunk_size: int,
    chunk_overlap: int,
) -> list[Document]:
    """Giriş: Girdi yolu ve chunk ayarları.

    Çıkış: Document listesi.
    İşleyiş: Kaynakları yükler ve parçalara böler.
    """
    documents: list[Document] = []
    for path in iter_input_files(input_path, extensions):
        if not path.exists():
            continue
        sources = _load_chunks(path)
        for source in sources:
            documents.extend(_chunk_source(source, chunk_size, chunk_overlap))
    return documents


def ingest(
    input_path: Path,
    output_path: Path,
    embedding_model: str,
    chunk_size: int,
    chunk_overlap: int,
    extensions: Sequence[str],
    reset: bool,
    batch_size: int,
) -> int:
    """Giriş: Dosyalar ve ayarlar.

    Çıkış: Eklenen parça sayısı.
    İşleyiş: FAISS indeksini oluşturur ve kaydeder.
    """
    if reset and output_path.exists():
        for child in output_path.glob("*"):
            if child.is_file():
                child.unlink()

    embedder = SentenceTransformerBackend(embedding_model, batch_size=batch_size)
    index = RagIndex(output_path, embedder, batch_size=batch_size)
    docs = build_documents(input_path, extensions, chunk_size, chunk_overlap)
    added = index.add_documents(docs)
    index.save(
        meta_info={
            "embedding_model": embedding_model,
            "dimension": embedder.dimension,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "documents": added,
        }
    )
    return added


def parse_args() -> argparse.Namespace:
    """Giriş: CLI parametreleri.

    Çıkış: argparse Namespace.
    İşleyiş: Komut satırı argümanlarını tanımlar.
    """
    parser = argparse.ArgumentParser(
        description="Selçuk AI Asistanı RAG ingestion CLI (FAISS)",
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Girdi dosya veya klasörü (pdf/txt/md/html).",
    )
    parser.add_argument(
        "--output",
        default=Config.RAG_VECTOR_DB_PATH or "./data/rag",
        help="FAISS indeks ve metadata çıkış dizini.",
    )
    parser.add_argument(
        "--embedding-model",
        default=Config.RAG_EMBEDDING_MODEL,
        help="SentenceTransformer model adı.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=Config.RAG_CHUNK_SIZE,
        help="Karakter bazında parça boyu.",
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=Config.RAG_CHUNK_OVERLAP,
        help="Karakter bazında parça bindirmesi.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=Config.RAG_EMBEDDING_BATCH_SIZE,
        help="Gömleme üretimi için batch boyu.",
    )
    parser.add_argument(
        "--extensions",
        default=".pdf,.txt,.md,.html,.htm",
        help="Klasör için virgül ayrımlı uzantı listesi.",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Ingest öncesi mevcut indeks dosyalarını sil.",
    )
    return parser.parse_args()


def main() -> None:
    """Giriş: CLI.

    Çıkış: yok.
    İşleyiş: Ingest sürecini çalıştırır.
    """
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    extensions = [ext.strip() for ext in args.extensions.split(",") if ext.strip()]
    output_path.mkdir(parents=True, exist_ok=True)
    added = ingest(
        input_path=input_path,
        output_path=output_path,
        embedding_model=args.embedding_model,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        extensions=extensions,
        reset=args.reset,
        batch_size=args.batch_size,
    )
    logger.info("Ingest tamamlandı. Eklenen parça sayısı: %s", added)


if __name__ == "__main__":
    main()
