"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  DOSYA: rag_production.py                                                      ║
║  AMAÇ: Production-Grade RAG Sistemi - Tüm Bileşenlerin Entegrasyonu           ║
║  VERSİYON: 2.0                                                                 ║
║  ÖZELLİKLER:                                                                   ║
║    - Multi-format document processing (PDF, DOCX, Excel, HTML)                ║
║    - Intelligent chunking (semantic, hybrid)                                   ║
║    - Multi-model embeddings (LaBSE, E5, ensemble)                             ║
║    - Hybrid retrieval (Dense + Sparse + Reranking)                            ║
║    - Quality evaluation (RAGAS metrics)                                        ║
║    - Production optimization (caching, monitoring)                             ║
╚════════════════════════════════════════════════════════════════════════════════╝

KULLANIM:
─────────
from rag_production import ProductionRAG

# Başlat
rag = ProductionRAG()

# Doküman ekle
rag.ingest_documents("data/documents/")

# Sorgu yap
context, citations = rag.get_context("Akademik takvim ne zaman?")

# Değerlendir
evaluation = rag.evaluate_response(query, answer, context)
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

logger = logging.getLogger(__name__)

# Core imports
try:
    from processors.document_processor import DocumentProcessor, ProcessedDocument, process_directory
    PROCESSORS_AVAILABLE = True
except ImportError:
    PROCESSORS_AVAILABLE = False
    logger.warning("processors modülü yüklenemedi")

try:
    from chunkers.intelligent_chunker import IntelligentChunker, ChunkingStrategy, Chunk
    CHUNKERS_AVAILABLE = True
except ImportError:
    CHUNKERS_AVAILABLE = False
    logger.warning("chunkers modülü yüklenemedi")

try:
    from embeddings.multi_model_embedder import MultiModelEmbedder, EmbeddingModel
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    logger.warning("embeddings modülü yüklenemedi")

try:
    from retrieval.advanced_retriever import AdvancedRetriever, RetrievalConfig, SearchMethod
    RETRIEVAL_AVAILABLE = True
except ImportError:
    RETRIEVAL_AVAILABLE = False
    logger.warning("retrieval modülü yüklenemedi")

try:
    from evaluation.rag_evaluator import RAGEvaluator, EvaluationResult
    EVALUATION_AVAILABLE = True
except ImportError:
    EVALUATION_AVAILABLE = False
    logger.warning("evaluation modülü yüklenemedi")

try:
    from optimization.production_rag import ProductionRAGService, ProductionConfig, RAGCache
    OPTIMIZATION_AVAILABLE = True
except ImportError:
    OPTIMIZATION_AVAILABLE = False
    logger.warning("optimization modülü yüklenemedi")


@dataclass
class RAGConfig:
    """Production RAG konfigürasyonu"""
    embedding_model: str = "sentence-transformers/LaBSE"
    use_ensemble: bool = False
    ensemble_models: List[str] = None
    
    chunk_size: int = 500
    chunk_overlap: int = 50
    chunking_strategy: str = "hybrid"
    
    search_method: str = "hybrid"
    top_k: int = 5
    use_reranking: bool = True
    
    cache_enabled: bool = True
    cache_ttl: int = 3600
    
    index_path: str = "data/rag/index"
    
    def __post_init__(self):
        if self.ensemble_models is None:
            self.ensemble_models = [
                "sentence-transformers/LaBSE",
                "intfloat/multilingual-e5-base",
            ]


class ProductionRAG:
    """
    Production-Grade RAG Sistemi.
    
    Bu sınıf tüm RAG bileşenlerini (document processing, chunking, 
    embedding, retrieval, evaluation, caching) tek bir arayüzde birleştirir.
    
    Attributes:
        config: RAG konfigürasyonu
        embedder: Multi-model embedder
        retriever: Advanced retriever
        evaluator: RAG evaluator
        service: Production service wrapper
    
    Example:
        >>> rag = ProductionRAG()
        >>> rag.ingest_documents("data/docs/")
        >>> context, citations = rag.get_context("Sınav tarihleri nedir?")
    """
    
    def __init__(
        self,
        config: Optional[RAGConfig] = None,
        auto_load: bool = True,
    ):
        self.config = config or RAGConfig()
        
        self._embedder: Optional[MultiModelEmbedder] = None
        self._retriever: Optional[AdvancedRetriever] = None
        self._evaluator: Optional[RAGEvaluator] = None
        self._service: Optional[ProductionRAGService] = None
        self._chunker: Optional[IntelligentChunker] = None
        
        self._initialized = False
        self._document_count = 0
        
        if auto_load:
            self._initialize()
    
    def _initialize(self) -> None:
        """Bileşenleri başlat"""
        logger.info("🚀 ProductionRAG başlatılıyor...")
        
        if EMBEDDINGS_AVAILABLE:
            if self.config.use_ensemble:
                self._embedder = MultiModelEmbedder(
                    models=[EmbeddingModel(m) if hasattr(EmbeddingModel, m.split("/")[-1].upper()) 
                           else m for m in self.config.ensemble_models],
                    ensemble=True,
                    use_cache=True,
                )
            else:
                self._embedder = MultiModelEmbedder(
                    model=self.config.embedding_model,
                    use_cache=True,
                )
            logger.info(f"✅ Embedder: {self._embedder.model_name}")
        
        if CHUNKERS_AVAILABLE:
            strategy = ChunkingStrategy[self.config.chunking_strategy.upper()]
            self._chunker = IntelligentChunker(
                strategy=strategy,
                chunk_size=self.config.chunk_size,
                chunk_overlap=self.config.chunk_overlap,
            )
            logger.info(f"✅ Chunker: {self.config.chunking_strategy}")
        
        if RETRIEVAL_AVAILABLE and self._embedder:
            self._retriever = AdvancedRetriever(
                embedder=self._embedder,
                config=RetrievalConfig(
                    top_k=self.config.top_k,
                    search_method=SearchMethod[self.config.search_method.upper()],
                    use_reranking=self.config.use_reranking,
                ),
            )
            logger.info("✅ Retriever initialized")
        
        if EVALUATION_AVAILABLE:
            self._evaluator = RAGEvaluator(use_llm=True)
            logger.info("✅ Evaluator initialized")
        
        if OPTIMIZATION_AVAILABLE and self._retriever:
            prod_config = ProductionConfig(
                cache_enabled=self.config.cache_enabled,
                cache_ttl_seconds=self.config.cache_ttl,
            )
            self._service = ProductionRAGService(
                retriever=self._retriever,
                config=prod_config,
            )
            logger.info("✅ Production service initialized")
        
        if os.path.exists(self.config.index_path):
            self._load_index()
        
        self._initialized = True
        logger.info("🎉 ProductionRAG hazır!")
    
    def _load_index(self) -> None:
        """Mevcut index'i yükle"""
        index_meta = Path(self.config.index_path) / "index_meta.json"
        if index_meta.exists():
            try:
                meta = json.loads(index_meta.read_text())
                self._document_count = meta.get("document_count", 0)
                logger.info(f"📂 Index yüklendi: {self._document_count} doküman")
            except Exception as e:
                logger.warning(f"Index meta yüklenemedi: {e}")
    
    def ingest_file(
        self,
        file_path: Union[str, Path],
        metadata: Optional[Dict] = None,
    ) -> int:
        """
        Tek dosya işle ve index'e ekle.
        
        Args:
            file_path: Dosya yolu
            metadata: Ek metadata
        
        Returns:
            Eklenen chunk sayısı
        """
        if not PROCESSORS_AVAILABLE:
            raise ImportError("Document processors modülü gerekli")
        
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Dosya bulunamadı: {file_path}")
        
        doc = DocumentProcessor.process(file_path)
        
        chunks = self._process_document(doc, metadata)
        
        added = self._add_chunks_to_index(chunks)
        
        logger.info(f"📄 {file_path.name}: {added} chunk eklendi")
        return added
    
    def ingest_documents(
        self,
        directory: Union[str, Path],
        extensions: Optional[List[str]] = None,
        recursive: bool = True,
    ) -> int:
        """
        Dizindeki tüm dokümanları işle ve index'e ekle.
        
        Args:
            directory: Dizin yolu
            extensions: İşlenecek uzantılar (None = tümü)
            recursive: Alt dizinleri de tara
        
        Returns:
            Toplam eklenen chunk sayısı
        """
        if not PROCESSORS_AVAILABLE:
            raise ImportError("Document processors modülü gerekli")
        
        directory = Path(directory)
        if not directory.exists():
            raise FileNotFoundError(f"Dizin bulunamadı: {directory}")
        
        documents = process_directory(
            directory,
            recursive=recursive,
            extensions=extensions,
        )
        
        total_added = 0
        for doc in documents:
            chunks = self._process_document(doc)
            added = self._add_chunks_to_index(chunks)
            total_added += added
        
        self._save_index_meta()
        
        logger.info(f"📁 {len(documents)} dosya işlendi, {total_added} chunk eklendi")
        return total_added
    
    def ingest_text(
        self,
        text: str,
        source: str = "manual",
        metadata: Optional[Dict] = None,
    ) -> int:
        """
        Ham metin ekle.
        
        Args:
            text: Metin içeriği
            source: Kaynak bilgisi
            metadata: Ek metadata
        
        Returns:
            Eklenen chunk sayısı
        """
        if not self._chunker:
            raise RuntimeError("Chunker başlatılmamış")
        
        meta = metadata or {}
        meta["source"] = source
        
        chunks = self._chunker.chunk(text, source=source, metadata=meta)
        added = self._add_chunks_to_index(chunks)
        
        logger.info(f"📝 Manuel metin: {added} chunk eklendi")
        return added
    
    def _process_document(
        self,
        doc: ProcessedDocument,
        extra_metadata: Optional[Dict] = None,
    ) -> List[Chunk]:
        """Dokümanı chunk'lara ayır"""
        if not self._chunker:
            raise RuntimeError("Chunker başlatılmamış")
        
        metadata = {
            "source": doc.source,
            "file_type": doc.file_type,
            "title": doc.title,
        }
        metadata.update(doc.metadata)
        if extra_metadata:
            metadata.update(extra_metadata)
        
        return self._chunker.chunk(doc.content, source=doc.source, metadata=metadata)
    
    def _add_chunks_to_index(self, chunks: List[Chunk]) -> int:
        """Chunk'ları retriever'a ekle"""
        if not self._retriever:
            raise RuntimeError("Retriever başlatılmamış")
        
        if not chunks:
            return 0
        
        documents = [c.content for c in chunks]
        doc_ids = [c.chunk_id for c in chunks]
        metadata = [c.metadata for c in chunks]
        
        added = self._retriever.add_documents(
            documents=documents,
            doc_ids=doc_ids,
            metadata=metadata,
        )
        
        self._document_count += added
        return added
    
    def _save_index_meta(self) -> None:
        """Index metadata kaydet"""
        index_path = Path(self.config.index_path)
        index_path.mkdir(parents=True, exist_ok=True)
        
        meta = {
            "document_count": self._document_count,
            "embedding_model": self.config.embedding_model,
            "chunk_size": self.config.chunk_size,
            "updated_at": datetime.utcnow().isoformat(),
        }
        
        meta_file = index_path / "index_meta.json"
        meta_file.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    
    def get_context(
        self,
        query: str,
        top_k: Optional[int] = None,
    ) -> Tuple[str, List[Dict]]:
        """
        Sorgu için bağlam getir.
        
        Args:
            query: Arama sorgusu
            top_k: Döndürülecek doküman sayısı
        
        Returns:
            (context_string, citations_list)
        """
        if self._service:
            return self._service.get_context(query, top_k=top_k or self.config.top_k)
        
        if self._retriever:
            return self._retriever.get_context(query, top_k=top_k or self.config.top_k)
        
        raise RuntimeError("Retriever başlatılmamış")
    
    def search(
        self,
        query: str,
        top_k: Optional[int] = None,
    ) -> List[Dict]:
        """
        Arama yap ve sonuçları döndür.
        
        Args:
            query: Arama sorgusu
            top_k: Döndürülecek sonuç sayısı
        
        Returns:
            Sonuç listesi
        """
        if self._service:
            return self._service.search(query, top_k=top_k or self.config.top_k)
        
        if self._retriever:
            results = self._retriever.retrieve(query, top_k=top_k or self.config.top_k)
            return [r.to_dict() for r in results]
        
        raise RuntimeError("Retriever başlatılmamış")
    
    def evaluate_response(
        self,
        query: str,
        answer: str,
        context: str,
        ground_truth: Optional[str] = None,
    ) -> EvaluationResult:
        """
        Yanıtı değerlendir.
        
        Args:
            query: Orijinal soru
            answer: Sistem yanıtı
            context: Kullanılan bağlam
            ground_truth: Doğru yanıt (opsiyonel)
        
        Returns:
            EvaluationResult
        """
        if not self._evaluator:
            raise RuntimeError("Evaluator başlatılmamış")
        
        return self._evaluator.evaluate(
            query=query,
            answer=answer,
            context=context,
            ground_truth=ground_truth,
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """Sistem istatistikleri"""
        stats = {
            "initialized": self._initialized,
            "document_count": self._document_count,
            "config": {
                "embedding_model": self.config.embedding_model,
                "chunk_size": self.config.chunk_size,
                "search_method": self.config.search_method,
                "use_reranking": self.config.use_reranking,
            },
        }
        
        if self._service:
            stats["service"] = self._service.get_stats()
        
        if self._embedder:
            stats["embedder"] = {
                "model": self._embedder.model_name,
                "dimension": self._embedder.dimension,
            }
        
        return stats
    
    def health_check(self) -> Dict[str, Any]:
        """Sağlık kontrolü"""
        if self._service:
            return self._service.health_check()
        
        return {
            "status": "healthy" if self._initialized else "not_initialized",
            "document_count": self._document_count,
        }
    
    def clear_cache(self) -> None:
        """Cache temizle"""
        if self._service:
            self._service.clear_cache()
        if self._embedder:
            self._embedder.clear_cache()
        logger.info("🗑️ Cache temizlendi")
    
    @property
    def document_count(self) -> int:
        """Toplam doküman sayısı"""
        return self._document_count


def create_production_rag(
    embedding_model: str = "sentence-transformers/LaBSE",
    use_ensemble: bool = False,
    **kwargs
) -> ProductionRAG:
    """
    Production RAG oluştur (factory function).
    
    Args:
        embedding_model: Embedding model adı
        use_ensemble: Ensemble kullan mı
        **kwargs: Ek konfigürasyon parametreleri
    
    Returns:
        ProductionRAG instance
    """
    config = RAGConfig(
        embedding_model=embedding_model,
        use_ensemble=use_ensemble,
        **kwargs
    )
    return ProductionRAG(config=config)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("=" * 60)
    print("🎯 Production RAG System v2.0")
    print("=" * 60)
    print(f"Processors available: {PROCESSORS_AVAILABLE}")
    print(f"Chunkers available: {CHUNKERS_AVAILABLE}")
    print(f"Embeddings available: {EMBEDDINGS_AVAILABLE}")
    print(f"Retrieval available: {RETRIEVAL_AVAILABLE}")
    print(f"Evaluation available: {EVALUATION_AVAILABLE}")
    print(f"Optimization available: {OPTIMIZATION_AVAILABLE}")
    print("=" * 60)
