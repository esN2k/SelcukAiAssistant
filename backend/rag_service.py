"""RAG (Retrieval-Augmented Generation) servisi ve FAISS tabanlı indeks yönetimi."""
from __future__ import annotations

import json
import logging
import re
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional, Sequence

import numpy as np

from api import error_messages as mesajlar
from config import Config

logger = logging.getLogger(__name__)

try:  # pragma: no cover - exercised via runtime imports
    import faiss  # type: ignore
except Exception:  # pragma: no cover - allow import failure when RAG is disabled
    faiss = None


@dataclass
class Document:
    """Giriş: İçerik ve metadata alır.

    Çıkış: Arama sonucunda doc_id ve score doldurulabilir.
    İşleyiş: Basit veri kapsülü olarak kullanılır.
    """

    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    doc_id: Optional[str] = None
    score: Optional[float] = None


class EmbeddingBackend:
    """Giriş: Metin listesi alır.

    Çıkış: float32 gömleme vektörü döndürür.
    İşleyiş: Alt sınıflar dimension ve embed metodlarını sağlar.
    """

    @property
    def dimension(self) -> int:
        """Giriş: yok.

        Çıkış: Vektör boyutu.
        İşleyiş: Alt sınıflar tarafından uygulanır.
        """
        raise NotImplementedError

    def embed(self, texts: Sequence[str]) -> np.ndarray:
        """Giriş: Metin listesi.

        Çıkış: Gömleme vektörleri (float32).
        İşleyiş: Alt sınıflar tarafından uygulanır.
        """
        raise NotImplementedError


class SentenceTransformerBackend(EmbeddingBackend):
    """Giriş: Model adı ve batch size.

    Çıkış: Normalize edilmiş gömlemeler.
    İşleyiş: SentenceTransformer encode ile vektör üretir.
    """

    def __init__(
        self,
        model_name: str,
        batch_size: int = 32,
        device: Optional[str] = None,
    ) -> None:
        """Giriş: Model adı ve batch size.

        Çıkış: Nesne.
        İşleyiş: SentenceTransformer modelini yükler.
        """
        from sentence_transformers import SentenceTransformer

        self.model_name = model_name
        resolved_device = self._resolve_device(device)
        if resolved_device:
            self._model = SentenceTransformer(model_name, device=resolved_device)
        else:
            self._model = SentenceTransformer(model_name)
        self._batch_size = max(1, batch_size)
        dimension = self._model.get_sentence_embedding_dimension()
        if dimension is None:
            raise RuntimeError(mesajlar.RAG_GOMLEME_BOYUTU_ALINAMADI)
        self._dimension = int(dimension)

    @staticmethod
    def _resolve_device(device: Optional[str]) -> Optional[str]:
        if not device or device == "auto":
            try:
                import torch
            except Exception:
                return None
            if torch.cuda.is_available():
                return "cuda"
            if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
                return "mps"
            return "cpu"
        try:
            import torch
        except Exception:
            return device
        if device == "cuda" and not torch.cuda.is_available():
            logger.warning(mesajlar.RAG_CUDA_YOK)
            return "cpu"
        if device == "mps" and not (
            getattr(torch.backends, "mps", None)
            and torch.backends.mps.is_available()
        ):
            logger.warning(mesajlar.RAG_MPS_YOK)
            return "cpu"
        return device

    @property
    def dimension(self) -> int:
        """Giriş: yok.

        Çıkış: Gömleme boyutu.
        İşleyiş: Modelden alınan boyutu döndürür.
        """
        return self._dimension

    def embed(self, texts: Sequence[str]) -> np.ndarray:
        """Giriş: Metin listesi.

        Çıkış: Gömleme vektörleri.
        İşleyiş: Encode işlemi ile normalize edilmiş vektör üretir.
        """
        if not texts:
            return np.zeros((0, self._dimension), dtype="float32")
        embeddings = self._model.encode(
            list(texts),
            batch_size=self._batch_size,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        return np.ascontiguousarray(embeddings, dtype="float32")


def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """Giriş: Ham metin, parça boyu ve bindirme.

    Çıkış: Parça listesi.
    İşleyiş: Paragraf ayrımı yapar, gerekiyorsa bindirmeli keser.
    """
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
    """Giriş: Kök dizin, gömleme üretici ve batch boyu.

    Çıkış: Arama sonucu dokümanlar ve indeks dosyaları.
    İşleyiş: FAISS indeks dosyası ile metadata.json senkron tutulur.
    """

    def __init__(
        self,
        root: Path,
        embedder: EmbeddingBackend,
        batch_size: int = 32,
    ) -> None:
        """Giriş: İndeks dizini ve gömleme altyapısı.

        Çıkış: Nesne.
        İşleyiş: Dosya yollarını ve gömleyiciyi hazırlar.
        """
        if faiss is None:
            raise RuntimeError(mesajlar.RAG_FAISS_EKSIK)
        self.root = root
        self.embedder = embedder
        self.index_path = self.root / "index.faiss"
        self.meta_path = self.root / "metadata.json"
        self.meta_info_path = self.root / "index_meta.json"
        self.batch_size = max(1, batch_size)
        self.index: Any = None
        self.metadata: list[dict[str, Any]] = []
        self._load_existing()

    def _load_existing(self) -> None:
        """Giriş: yok.

        Çıkış: yok.
        İşleyiş: Mevcut indeks dosyalarını okur ve doğrular.
        """
        if not self.index_path.exists():
            return
        self.index = faiss.read_index(str(self.index_path))
        if self.meta_path.exists():
            try:
                self.metadata = json.loads(self.meta_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                raise RuntimeError(mesajlar.RAG_METADATA_OKUNAMADI) from exc
        if self.index is not None and self.metadata:
            if self.index.ntotal != len(self.metadata):
                raise RuntimeError(
                    mesajlar.RAG_INDEKS_TUTARSIZ.format(
                        index_total=self.index.ntotal,
                        meta_total=len(self.metadata),
                    )
                )

    def _ensure_index(self) -> None:
        """Giriş: yok.

        Çıkış: yok.
        İşleyiş: İndeks yoksa FAISS IndexFlatIP oluşturur.
        """
        if self.index is None:
            self.index = faiss.IndexFlatIP(self.embedder.dimension)

    def add_documents(self, documents: Sequence[Document]) -> int:
        """Giriş: Doküman listesi.

        Çıkış: Eklenen doküman sayısı.
        İşleyiş: Batch halinde gömleme üretip indekse ekler.
        """
        if not documents:
            return 0
        self._ensure_index()
        assert self.index is not None
        added = 0
        batch_size = max(1, self.batch_size)
        for start in range(0, len(documents), batch_size):
            batch = documents[start : start + batch_size]
            embeddings = self.embedder.embed([doc.content for doc in batch])
            if embeddings.size == 0:
                continue
            embeddings = np.ascontiguousarray(embeddings, dtype="float32")
            self.index.add(embeddings)
            for doc in batch:
                doc_id = doc.doc_id or uuid.uuid4().hex
                payload = {
                    "id": doc_id,
                    "content": doc.content,
                    **doc.metadata,
                }
                self.metadata.append(payload)
            added += len(batch)
        return added

    def search(self, query: str, top_k: int) -> list[Document]:
        """Giriş: Sorgu metni ve top_k.

        Çıkış: En yakın dokümanlar.
        İşleyiş: FAISS indeksinde arama yapar.
        """
        if not query.strip() or self.index is None or self.index.ntotal == 0:
            return []
        top_k = max(1, min(top_k, self.index.ntotal))
        embeddings = self.embedder.embed([query])
        if embeddings.size == 0:
            return []
        embeddings = np.ascontiguousarray(embeddings, dtype="float32")
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
        """Giriş: Opsiyonel meta bilgi.

        Çıkış: yok.
        İşleyiş: İndeks ve metadata'yı diske yazar.
        """
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
    """Giriş: Metadata sözlüğü.

    Çıkış: Kaynak etiketi.
    İşleyiş: Kaynak ve sayfa bilgisini birleştirir.
    """
    source = meta.get("source") or "Bilinmeyen kaynak"
    page = meta.get("page")
    if page:
        return f"{source} (sayfa {page})"
    return source


class RAGService:
    """Giriş: RAG ayarları, embedder ve indeks yolu.

    Çıkış: Kaynaklı bağlam ve alıntı listesi.
    İşleyiş: İndeks hazırsa arama yapar, değilse anlamlı hata verir.
    """

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
        embedding_batch_size: Optional[int] = None,
        embedding_device: Optional[str] = None,
    ) -> None:
        """Giriş: RAG yapılandırma parametreleri.

        Çıkış: Nesne.
        İşleyiş: RAG hizmetini hazırlar ve indeksi yükler.
        """
        self.enabled = enabled
        self.available = False
        self.error_message: Optional[str] = None
        self.vector_db_path = vector_db_path
        self.collection_name = collection_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model = embedding_model or Config.RAG_EMBEDDING_MODEL
        self.top_k = top_k
        self.embedding_batch_size = (
            embedding_batch_size or Config.RAG_EMBEDDING_BATCH_SIZE
        )
        self.embedding_device = embedding_device or Config.RAG_EMBEDDING_DEVICE
        self._embedder = embedder
        self._index: Optional[RagIndex] = None

        if not self.enabled:
            logger.info(mesajlar.RAG_DEVRE_DISI)
            return

        if not self.vector_db_path:
            self.error_message = mesajlar.RAG_PATH_EKSIK
            logger.warning(self.error_message)
            return
        if faiss is None:
            self.error_message = mesajlar.RAG_FAISS_EKSIK
            logger.warning(self.error_message)
            return

        try:
            self._embedder = self._embedder or SentenceTransformerBackend(
                self.embedding_model,
                batch_size=self.embedding_batch_size,
                device=self.embedding_device,
            )
            self._index = RagIndex(
                Path(self.vector_db_path),
                self._embedder,
                batch_size=self.embedding_batch_size,
            )
            self.available = True
            logger.info(
                "RAG servisi başlatıldı: path=%s collection=%s model=%s",
                self.vector_db_path,
                self.collection_name,
                self.embedding_model,
            )
        except Exception as exc:
            self.error_message = f"{mesajlar.RAG_BASLATILAMADI}: {exc}"
            logger.exception(self.error_message)

    def search(self, query: str, top_k: Optional[int] = None) -> list[Document]:
        """Giriş: Sorgu metni ve opsiyonel top_k.

        Çıkış: Doküman listesi.
        İşleyiş: İndeks üzerinden arama yapar.
        """
        if not self.enabled:
            return []
        if not self.available or self._index is None:
            raise RuntimeError(self.error_message or mesajlar.RAG_HAZIR_DEGIL)
        return self._index.search(query, top_k or self.top_k)

    def get_context(
        self,
        query: str,
        top_k: Optional[int] = None,
    ) -> tuple[str, list[str]]:
        """Giriş: Sorgu metni ve opsiyonel top_k.

        Çıkış: Bağlam metni ve kaynak listesi.
        İşleyiş: Sorgu sonuçlarını numaralı bağlam haline getirir.
        """
        if not self.enabled:
            return "", []
        if not self.available:
            raise RuntimeError(self.error_message or mesajlar.RAG_HAZIR_DEGIL)
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
        """Giriş: Doküman listesi.

        Çıkış: Eklenen doküman sayısı.
        İşleyiş: İndeks üzerinden ekleme yapar.
        """
        if not self.enabled or self._index is None:
            raise RuntimeError(mesajlar.RAG_ETKIN_DEGIL)
        if not self.available:
            raise RuntimeError(self.error_message or mesajlar.RAG_HAZIR_DEGIL)
        return self._index.add_documents(documents)

    def save_index(self, meta_info: Optional[dict[str, Any]] = None) -> None:
        """Giriş: Opsiyonel meta bilgi.

        Çıkış: yok.
        İşleyiş: İndeks ve metadata bilgisini diske yazar.
        """
        if not self.enabled or self._index is None:
            return
        if not self.available:
            raise RuntimeError(self.error_message or mesajlar.RAG_HAZIR_DEGIL)
        self._index.save(meta_info=meta_info)


rag_service = RAGService(
    enabled=Config.RAG_ENABLED,
    vector_db_path=Config.RAG_VECTOR_DB_PATH,
    collection_name=Config.RAG_COLLECTION_NAME,
    chunk_size=Config.RAG_CHUNK_SIZE,
    chunk_overlap=Config.RAG_CHUNK_OVERLAP,
    embedding_model=Config.RAG_EMBEDDING_MODEL,
    top_k=Config.RAG_TOP_K,
    embedding_batch_size=Config.RAG_EMBEDDING_BATCH_SIZE,
)
