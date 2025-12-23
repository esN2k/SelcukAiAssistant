"""RAG (Retrieval-Augmented Generation) service and FAISS-backed index."""
from __future__ import annotations

import json
import logging
import re
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional, Sequence

import numpy as np

from config import Config

logger = logging.getLogger(__name__)

try:  # pragma: no cover - exercised via runtime imports
    import faiss  # type: ignore
except Exception:  # pragma: no cover - allow import failure when RAG is disabled
    faiss = None


@dataclass
class Document:
    """Single document chunk with metadata."""

    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    doc_id: Optional[str] = None
    score: Optional[float] = None


class EmbeddingBackend:
    """Embedding backend contract."""

    @property
    def dimension(self) -> int:
        raise NotImplementedError

    def embed(self, texts: Sequence[str]) -> np.ndarray:
        raise NotImplementedError


class SentenceTransformerBackend(EmbeddingBackend):
    """SentenceTransformers embedding backend."""

    def __init__(self, model_name: str) -> None:
        from sentence_transformers import SentenceTransformer

        self.model_name = model_name
        self._model = SentenceTransformer(model_name)
        dimension = self._model.get_sentence_embedding_dimension()
        if dimension is None:
            raise RuntimeError("Embedding dimension not available")
        self._dimension = int(dimension)

    @property
    def dimension(self) -> int:
        return self._dimension

    def embed(self, texts: Sequence[str]) -> np.ndarray:
        if not texts:
            return np.zeros((0, self._dimension), dtype="float32")
        embeddings = self._model.encode(
            list(texts),
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        return embeddings.astype("float32")


def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """Chunk text with simple paragraph-aware splitting."""
    cleaned = text.replace("\r", "\n")
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    if not cleaned:
        return []

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", cleaned) if p.strip()]
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for paragraph in paragraphs:
        paragraph_len = len(paragraph)
        if current_len + paragraph_len + 2 <= chunk_size:
            current.append(paragraph)
            current_len += paragraph_len + 2
            continue

        if current:
            chunk = "\n\n".join(current).strip()
            if chunk:
                chunks.append(chunk)
            if chunk_overlap > 0 and chunk:
                overlap_text = chunk[-chunk_overlap:]
                current = [overlap_text]
                current_len = len(overlap_text)
            else:
                current = []
                current_len = 0

        if paragraph_len >= chunk_size:
            start = 0
            step = max(1, chunk_size - chunk_overlap)
            while start < paragraph_len:
                end = min(start + chunk_size, paragraph_len)
                chunk = paragraph[start:end].strip()
                if chunk:
                    chunks.append(chunk)
                start += step
            current = []
            current_len = 0
        else:
            current = [paragraph]
            current_len = paragraph_len

    if current:
        chunk = "\n\n".join(current).strip()
        if chunk:
            chunks.append(chunk)

    return chunks


class RagIndex:
    """FAISS index with JSON metadata storage."""

    def __init__(
        self,
        root: Path,
        embedder: EmbeddingBackend,
    ) -> None:
        if faiss is None:
            raise RuntimeError("faiss-cpu is not installed")
        self.root = root
        self.embedder = embedder
        self.index_path = self.root / "index.faiss"
        self.meta_path = self.root / "metadata.json"
        self.meta_info_path = self.root / "index_meta.json"
        self.index: Any = None
        self.metadata: list[dict[str, Any]] = []
        self._load_existing()

    def _load_existing(self) -> None:
        if not self.index_path.exists():
            return
        self.index = faiss.read_index(str(self.index_path))
        if self.meta_path.exists():
            self.metadata = json.loads(self.meta_path.read_text(encoding="utf-8"))
        if self.index is not None and self.metadata:
            if self.index.ntotal != len(self.metadata):
                raise RuntimeError(
                    "Index/metadata mismatch: "
                    f"{self.index.ntotal} vs {len(self.metadata)}"
                )

    def _ensure_index(self) -> None:
        if self.index is None:
            self.index = faiss.IndexFlatIP(self.embedder.dimension)

    def add_documents(self, documents: Sequence[Document]) -> int:
        if not documents:
            return 0
        self._ensure_index()
        assert self.index is not None
        embeddings = self.embedder.embed([doc.content for doc in documents])
        if embeddings.size == 0:
            return 0
        self.index.add(embeddings)
        for doc in documents:
            doc_id = doc.doc_id or uuid.uuid4().hex
            payload = {
                "id": doc_id,
                "content": doc.content,
                **doc.metadata,
            }
            self.metadata.append(payload)
        return len(documents)

    def search(self, query: str, top_k: int) -> list[Document]:
        if not query.strip() or self.index is None or self.index.ntotal == 0:
            return []
        top_k = max(1, min(top_k, self.index.ntotal))
        embeddings = self.embedder.embed([query])
        if embeddings.size == 0:
            return []
        scores, indices = self.index.search(embeddings, top_k)
        results: list[Document] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue
            meta = self.metadata[idx]
            results.append(
                Document(
                    content=meta.get("content", ""),
                    metadata={k: v for k, v in meta.items() if k != "content"},
                    doc_id=meta.get("id"),
                    score=float(score),
                )
            )
        return results

    def save(self, meta_info: Optional[dict[str, Any]] = None) -> None:
        if self.index is None:
            return
        self.root.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.index_path))
        self.meta_path.write_text(
            json.dumps(self.metadata, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        if meta_info is not None:
            self.meta_info_path.write_text(
                json.dumps(meta_info, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )


def _citation_label(meta: dict[str, Any]) -> str:
    source = meta.get("source") or "Bilinmeyen kaynak"
    page = meta.get("page")
    if page:
        return f"{source} (sayfa {page})"
    return source


class RAGService:
    """Runtime RAG retriever wrapper."""

    def __init__(
        self,
        enabled: bool = False,
        vector_db_path: Optional[str] = None,
        collection_name: str = "selcuk_documents",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        embedding_model: Optional[str] = None,
        top_k: int = 3,
        embedder: Optional[EmbeddingBackend] = None,
    ) -> None:
        self.enabled = enabled
        self.vector_db_path = vector_db_path
        self.collection_name = collection_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model = embedding_model or Config.RAG_EMBEDDING_MODEL
        self.top_k = top_k
        self._embedder = embedder
        self._index: Optional[RagIndex] = None

        if not self.enabled:
            logger.info("RAG service disabled (RAG_ENABLED=false)")
            return

        if not self.vector_db_path:
            raise ValueError("RAG_VECTOR_DB_PATH must be set when RAG is enabled")
        if faiss is None:
            raise RuntimeError("faiss-cpu is required for RAG")

        self._embedder = self._embedder or SentenceTransformerBackend(
            self.embedding_model
        )
        self._index = RagIndex(Path(self.vector_db_path), self._embedder)
        logger.info(
            "RAG service initialized: path=%s collection=%s model=%s",
            self.vector_db_path,
            self.collection_name,
            self.embedding_model,
        )

    def search(self, query: str, top_k: Optional[int] = None) -> list[Document]:
        if not self.enabled or self._index is None:
            return []
        return self._index.search(query, top_k or self.top_k)

    def get_context(
        self, query: str, top_k: Optional[int] = None
    ) -> tuple[str, list[str]]:
        if not self.enabled:
            return "", []
        docs = self.search(query, top_k=top_k)
        if not docs:
            return "", []

        context_parts: list[str] = []
        citations: list[str] = []
        for idx, doc in enumerate(docs, 1):
            citations.append(_citation_label(doc.metadata))
            context_parts.append(f"[{idx}] {doc.content}")
        return "\n\n".join(context_parts), citations

    def add_documents(self, documents: Sequence[Document]) -> int:
        if not self.enabled or self._index is None:
            raise RuntimeError("RAG service is not enabled")
        return self._index.add_documents(documents)

    def save_index(self, meta_info: Optional[dict[str, Any]] = None) -> None:
        if not self.enabled or self._index is None:
            return
        self._index.save(meta_info=meta_info)


rag_service = RAGService(
    enabled=Config.RAG_ENABLED,
    vector_db_path=Config.RAG_VECTOR_DB_PATH,
    collection_name=Config.RAG_COLLECTION_NAME,
    chunk_size=Config.RAG_CHUNK_SIZE,
    chunk_overlap=Config.RAG_CHUNK_OVERLAP,
    embedding_model=Config.RAG_EMBEDDING_MODEL,
    top_k=Config.RAG_TOP_K,
)
