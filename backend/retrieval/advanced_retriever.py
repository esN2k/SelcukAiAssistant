"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  DOSYA: advanced_retriever.py                                                  ║
║  AMAÇ: Gelişmiş retrieval sistemi - Hybrid Search, Reranking, Query Expansion ║
║  ÖZELLİKLER:                                                                   ║
║    - Hybrid Search (FAISS + BM25)                                             ║
║    - Cross-encoder Reranking                                                   ║
║    - Query Expansion (synonyms, HyDE)                                         ║
║    - Multi-query retrieval                                                     ║
║    - Reciprocal Rank Fusion (RRF)                                             ║
║    - Metadata filtering                                                        ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np

logger = logging.getLogger(__name__)

# Optional imports
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False

try:
    from rank_bm25 import BM25Okapi
    BM25_AVAILABLE = True
except ImportError:
    BM25_AVAILABLE = False

try:
    from sentence_transformers import CrossEncoder
    CROSS_ENCODER_AVAILABLE = True
except ImportError:
    CROSS_ENCODER_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class SearchMethod(Enum):
    """Arama yöntemleri"""
    DENSE = "dense"  # Vector search (FAISS)
    SPARSE = "sparse"  # BM25
    HYBRID = "hybrid"  # Dense + Sparse fusion


@dataclass
class RetrievalConfig:
    """Retrieval konfigürasyonu"""
    top_k: int = 10
    top_k_rerank: int = 5
    search_method: SearchMethod = SearchMethod.HYBRID
    dense_weight: float = 0.6
    sparse_weight: float = 0.4
    use_reranking: bool = True
    use_query_expansion: bool = False
    min_score: float = 0.0
    metadata_filters: Optional[Dict[str, Any]] = None


@dataclass
class RetrievalResult:
    """Retrieval sonucu"""
    content: str
    score: float
    doc_id: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    source: str = ""
    method: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "score": self.score,
            "doc_id": self.doc_id,
            "metadata": self.metadata,
            "source": self.source,
            "method": self.method,
        }


class TokenizerTurkish:
    """Türkçe tokenizer"""
    
    STOPWORDS = {
        "bir", "bu", "şu", "o", "ve", "ile", "için", "de", "da", "mi", "mı",
        "mu", "mü", "ki", "gibi", "kadar", "daha", "en", "çok", "az", "var",
        "yok", "olan", "olarak", "üzere", "göre", "sonra", "önce", "ise",
        "ancak", "fakat", "ama", "lakin", "veya", "ya", "hem", "ne", "her",
        "tüm", "bütün", "bazı", "hiç", "sadece", "yalnız", "bile", "dahi",
    }
    
    @classmethod
    def tokenize(cls, text: str, remove_stopwords: bool = True) -> List[str]:
        """Metni tokenize et"""
        text = text.lower()
        text = re.sub(r'[^\w\sçğıöşüâîû]', ' ', text)
        tokens = text.split()
        
        if remove_stopwords:
            tokens = [t for t in tokens if t not in cls.STOPWORDS and len(t) > 1]
        
        return tokens


class BM25Index:
    """BM25 sparse retrieval index"""
    
    def __init__(self):
        if not BM25_AVAILABLE:
            raise ImportError("rank_bm25 paketi gerekli: pip install rank_bm25")
        
        self._documents: List[str] = []
        self._metadata: List[Dict] = []
        self._doc_ids: List[str] = []
        self._tokenized: List[List[str]] = []
        self._bm25: Optional[BM25Okapi] = None
    
    def add_documents(
        self,
        documents: List[str],
        doc_ids: Optional[List[str]] = None,
        metadata: Optional[List[Dict]] = None,
    ) -> None:
        """Doküman ekle"""
        if doc_ids is None:
            start_id = len(self._documents)
            doc_ids = [f"doc_{start_id + i}" for i in range(len(documents))]
        
        if metadata is None:
            metadata = [{} for _ in documents]
        
        self._documents.extend(documents)
        self._doc_ids.extend(doc_ids)
        self._metadata.extend(metadata)
        
        new_tokenized = [TokenizerTurkish.tokenize(doc) for doc in documents]
        self._tokenized.extend(new_tokenized)
        
        self._bm25 = BM25Okapi(self._tokenized)
    
    def search(self, query: str, top_k: int = 10) -> List[Tuple[int, float]]:
        """BM25 araması"""
        if self._bm25 is None or not self._documents:
            return []
        
        query_tokens = TokenizerTurkish.tokenize(query)
        scores = self._bm25.get_scores(query_tokens)
        
        top_indices = np.argsort(scores)[::-1][:top_k]
        results = [(int(idx), float(scores[idx])) for idx in top_indices if scores[idx] > 0]
        
        return results
    
    def get_document(self, idx: int) -> Tuple[str, str, Dict]:
        """İndeks ile doküman al"""
        return self._documents[idx], self._doc_ids[idx], self._metadata[idx]


class DenseIndex:
    """FAISS dense retrieval index"""
    
    def __init__(self, dimension: int, use_gpu: bool = False):
        if not FAISS_AVAILABLE:
            raise ImportError("faiss paketi gerekli: pip install faiss-cpu")
        
        self._dimension = dimension
        self._documents: List[str] = []
        self._metadata: List[Dict] = []
        self._doc_ids: List[str] = []
        
        self._index = faiss.IndexFlatIP(dimension)
        
        if use_gpu:
            try:
                res = faiss.StandardGpuResources()
                self._index = faiss.index_cpu_to_gpu(res, 0, self._index)
            except Exception:
                logger.warning("GPU kullanılamıyor, CPU kullanılacak")
    
    def add_documents(
        self,
        embeddings: np.ndarray,
        documents: List[str],
        doc_ids: Optional[List[str]] = None,
        metadata: Optional[List[Dict]] = None,
    ) -> None:
        """Doküman ve embedding ekle"""
        if doc_ids is None:
            start_id = len(self._documents)
            doc_ids = [f"doc_{start_id + i}" for i in range(len(documents))]
        
        if metadata is None:
            metadata = [{} for _ in documents]
        
        embeddings = np.ascontiguousarray(embeddings, dtype="float32")
        
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1
        embeddings = embeddings / norms
        
        self._index.add(embeddings)
        self._documents.extend(documents)
        self._doc_ids.extend(doc_ids)
        self._metadata.extend(metadata)
    
    def search(
        self, 
        query_embedding: np.ndarray, 
        top_k: int = 10
    ) -> List[Tuple[int, float]]:
        """Dense arama"""
        if self._index.ntotal == 0:
            return []
        
        query_embedding = query_embedding.reshape(1, -1).astype("float32")
        norm = np.linalg.norm(query_embedding)
        if norm > 0:
            query_embedding = query_embedding / norm
        
        top_k = min(top_k, self._index.ntotal)
        scores, indices = self._index.search(query_embedding, top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0:
                results.append((int(idx), float(score)))
        
        return results
    
    def get_document(self, idx: int) -> Tuple[str, str, Dict]:
        """İndeks ile doküman al"""
        return self._documents[idx], self._doc_ids[idx], self._metadata[idx]
    
    @property
    def total(self) -> int:
        return self._index.ntotal


class QueryExpander:
    """Query expansion stratejileri"""
    
    TURKISH_SYNONYMS = {
        "sınav": ["imtihan", "test", "yoklama"],
        "takvim": ["program", "schedule", "ajanda"],
        "ders": ["kurs", "müfredat", "eğitim"],
        "kayıt": ["tescil", "registration", "enroll"],
        "öğrenci": ["talebe", "student"],
        "fakülte": ["fakulte", "faculty"],
        "bölüm": ["department", "program"],
        "final": ["dönem sonu", "bitirme"],
        "vize": ["ara sınav", "midterm"],
        "not": ["puan", "grade", "skor"],
        "ücret": ["harç", "fee", "tuition"],
        "mezuniyet": ["graduation", "diploma"],
        "staj": ["internship", "pratik"],
        "yurt": ["dormitory", "konaklama"],
        "yemekhane": ["kafeterya", "kantin"],
        "kütüphane": ["library"],
    }
    
    def __init__(self, use_llm: bool = False, gemini_api_key: Optional[str] = None):
        self.use_llm = use_llm and GEMINI_AVAILABLE
        
        if self.use_llm and gemini_api_key:
            import os
            genai.configure(api_key=gemini_api_key or os.getenv("GEMINI_API_KEY"))
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        else:
            self.model = None
    
    def expand_with_synonyms(self, query: str) -> List[str]:
        """Synonym tabanlı query expansion"""
        queries = [query]
        query_lower = query.lower()
        
        for word, synonyms in self.TURKISH_SYNONYMS.items():
            if word in query_lower:
                for syn in synonyms[:2]:
                    expanded = query_lower.replace(word, syn)
                    if expanded != query_lower:
                        queries.append(expanded)
        
        return queries[:5]
    
    def expand_with_hyde(self, query: str) -> List[str]:
        """HyDE (Hypothetical Document Embedding) expansion"""
        if not self.use_llm or not self.model:
            return [query]
        
        prompt = f"""Aşağıdaki soruya kısa bir cevap yaz (sanki bir üniversite web sitesinden alınmış gibi):

Soru: {query}

Kısa cevap (2-3 cümle):"""
        
        try:
            response = self.model.generate_content(prompt)
            hypothetical_doc = response.text.strip()
            return [query, hypothetical_doc]
        except Exception as e:
            logger.warning(f"HyDE expansion hatası: {e}")
            return [query]
    
    def expand_multi_query(self, query: str) -> List[str]:
        """Multi-query expansion - farklı perspektifler"""
        if not self.use_llm or not self.model:
            return self.expand_with_synonyms(query)
        
        prompt = f"""Aşağıdaki sorunun 3 farklı versiyonunu yaz (aynı anlama gelen farklı sorular):

Orijinal: {query}

3 farklı versiyon (her satıra bir tane):"""
        
        try:
            response = self.model.generate_content(prompt)
            lines = [l.strip() for l in response.text.strip().split('\n') if l.strip()]
            queries = [query] + lines[:3]
            return queries
        except Exception as e:
            logger.warning(f"Multi-query expansion hatası: {e}")
            return self.expand_with_synonyms(query)
    
    def expand(self, query: str, method: str = "synonyms") -> List[str]:
        """Query expansion uygula"""
        if method == "synonyms":
            return self.expand_with_synonyms(query)
        elif method == "hyde":
            return self.expand_with_hyde(query)
        elif method == "multi_query":
            return self.expand_multi_query(query)
        else:
            return [query]


class Reranker:
    """Cross-encoder reranking"""
    
    DEFAULT_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    TURKISH_MODEL = "emrecan/bert-base-turkish-cased-mean-nli-stsb-tr"
    
    def __init__(
        self, 
        model_name: Optional[str] = None,
        device: Optional[str] = None,
    ):
        if not CROSS_ENCODER_AVAILABLE:
            raise ImportError("Cross-encoder için sentence-transformers gerekli")
        
        self._model_name = model_name or self.DEFAULT_MODEL
        self._model = CrossEncoder(self._model_name, device=device)
        
        logger.info(f"✅ Reranker yüklendi: {self._model_name}")
    
    def rerank(
        self,
        query: str,
        results: List[RetrievalResult],
        top_k: Optional[int] = None,
    ) -> List[RetrievalResult]:
        """Sonuçları rerank et"""
        if not results:
            return []
        
        pairs = [(query, r.content) for r in results]
        scores = self._model.predict(pairs)
        
        for i, result in enumerate(results):
            result.score = float(scores[i])
            result.method = f"{result.method}+rerank"
        
        ranked = sorted(results, key=lambda x: x.score, reverse=True)
        
        if top_k:
            ranked = ranked[:top_k]
        
        return ranked


class ReciprocaRankFusion:
    """Reciprocal Rank Fusion (RRF) for combining multiple rankings"""
    
    @staticmethod
    def fuse(
        rankings: List[List[Tuple[str, float]]],
        k: int = 60,
    ) -> List[Tuple[str, float]]:
        """
        RRF ile birden fazla ranking'i birleştir.
        
        Args:
            rankings: List of [(doc_id, score), ...] rankings
            k: RRF parametresi (genellikle 60)
        
        Returns:
            Fused ranking [(doc_id, rrf_score), ...]
        """
        rrf_scores: Dict[str, float] = {}
        
        for ranking in rankings:
            for rank, (doc_id, _) in enumerate(ranking):
                if doc_id not in rrf_scores:
                    rrf_scores[doc_id] = 0.0
                rrf_scores[doc_id] += 1.0 / (k + rank + 1)
        
        fused = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        return fused


class AdvancedRetriever:
    """
    Gelişmiş retrieval sistemi.
    
    Özellikler:
        - Hybrid Search (Dense + Sparse)
        - Cross-encoder Reranking
        - Query Expansion
        - Reciprocal Rank Fusion
        - Metadata filtering
    """
    
    def __init__(
        self,
        embedder,
        config: Optional[RetrievalConfig] = None,
        use_reranker: bool = True,
        reranker_model: Optional[str] = None,
    ):
        self.embedder = embedder
        self.config = config or RetrievalConfig()
        
        self._dense_index = DenseIndex(embedder.dimension)
        self._sparse_index = BM25Index() if BM25_AVAILABLE else None
        
        self._query_expander = QueryExpander(use_llm=False)
        
        self._reranker: Optional[Reranker] = None
        if use_reranker and CROSS_ENCODER_AVAILABLE:
            try:
                self._reranker = Reranker(model_name=reranker_model)
            except Exception as e:
                logger.warning(f"Reranker yüklenemedi: {e}")
        
        self._doc_store: Dict[str, Dict] = {}
    
    def add_documents(
        self,
        documents: List[str],
        doc_ids: Optional[List[str]] = None,
        metadata: Optional[List[Dict]] = None,
    ) -> int:
        """
        Dokümanları index'e ekle.
        
        Args:
            documents: Doküman içerikleri
            doc_ids: Doküman ID'leri
            metadata: Doküman metadata'ları
        
        Returns:
            Eklenen doküman sayısı
        """
        if not documents:
            return 0
        
        if doc_ids is None:
            start_id = len(self._doc_store)
            doc_ids = [f"doc_{start_id + i}" for i in range(len(documents))]
        
        if metadata is None:
            metadata = [{} for _ in documents]
        
        embeddings = self.embedder.embed_documents(documents)
        
        self._dense_index.add_documents(
            embeddings=embeddings,
            documents=documents,
            doc_ids=doc_ids,
            metadata=metadata,
        )
        
        if self._sparse_index:
            self._sparse_index.add_documents(
                documents=documents,
                doc_ids=doc_ids,
                metadata=metadata,
            )
        
        for doc_id, doc, meta in zip(doc_ids, documents, metadata):
            self._doc_store[doc_id] = {"content": doc, "metadata": meta}
        
        logger.info(f"✅ {len(documents)} doküman eklendi (toplam: {self._dense_index.total})")
        return len(documents)
    
    def _search_dense(
        self, 
        query: str, 
        top_k: int
    ) -> List[RetrievalResult]:
        """Dense (vector) arama"""
        query_embedding = self.embedder.embed_query(query)
        results = self._dense_index.search(query_embedding, top_k)
        
        retrieval_results = []
        for idx, score in results:
            content, doc_id, metadata = self._dense_index.get_document(idx)
            retrieval_results.append(RetrievalResult(
                content=content,
                score=score,
                doc_id=doc_id,
                metadata=metadata,
                source=metadata.get("source", ""),
                method="dense",
            ))
        
        return retrieval_results
    
    def _search_sparse(
        self, 
        query: str, 
        top_k: int
    ) -> List[RetrievalResult]:
        """Sparse (BM25) arama"""
        if not self._sparse_index:
            return []
        
        results = self._sparse_index.search(query, top_k)
        
        retrieval_results = []
        for idx, score in results:
            content, doc_id, metadata = self._sparse_index.get_document(idx)
            retrieval_results.append(RetrievalResult(
                content=content,
                score=score,
                doc_id=doc_id,
                metadata=metadata,
                source=metadata.get("source", ""),
                method="sparse",
            ))
        
        return retrieval_results
    
    def _search_hybrid(
        self,
        query: str,
        top_k: int,
        dense_weight: float = 0.6,
        sparse_weight: float = 0.4,
    ) -> List[RetrievalResult]:
        """Hybrid arama (Dense + Sparse with RRF)"""
        dense_results = self._search_dense(query, top_k * 2)
        sparse_results = self._search_sparse(query, top_k * 2)
        
        if not sparse_results:
            return dense_results[:top_k]
        
        dense_ranking = [(r.doc_id, r.score) for r in dense_results]
        sparse_ranking = [(r.doc_id, r.score) for r in sparse_results]
        
        fused = ReciprocaRankFusion.fuse([dense_ranking, sparse_ranking])
        
        doc_map = {}
        for r in dense_results + sparse_results:
            if r.doc_id not in doc_map:
                doc_map[r.doc_id] = r
        
        hybrid_results = []
        for doc_id, rrf_score in fused[:top_k]:
            if doc_id in doc_map:
                result = doc_map[doc_id]
                result.score = rrf_score
                result.method = "hybrid"
                hybrid_results.append(result)
        
        return hybrid_results
    
    def _apply_metadata_filter(
        self,
        results: List[RetrievalResult],
        filters: Dict[str, Any],
    ) -> List[RetrievalResult]:
        """Metadata filtreleme"""
        if not filters:
            return results
        
        filtered = []
        for result in results:
            match = True
            for key, value in filters.items():
                if key not in result.metadata:
                    match = False
                    break
                if isinstance(value, list):
                    if result.metadata[key] not in value:
                        match = False
                        break
                elif result.metadata[key] != value:
                    match = False
                    break
            
            if match:
                filtered.append(result)
        
        return filtered
    
    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        config: Optional[RetrievalConfig] = None,
    ) -> List[RetrievalResult]:
        """
        Sorgu için doküman retrieve et.
        
        Args:
            query: Arama sorgusu
            top_k: Döndürülecek doküman sayısı
            config: Retrieval konfigürasyonu
        
        Returns:
            RetrievalResult listesi
        """
        config = config or self.config
        top_k = top_k or config.top_k
        
        queries = [query]
        if config.use_query_expansion:
            queries = self._query_expander.expand(query, method="synonyms")
        
        all_results: List[RetrievalResult] = []
        
        for q in queries:
            if config.search_method == SearchMethod.DENSE:
                results = self._search_dense(q, top_k)
            elif config.search_method == SearchMethod.SPARSE:
                results = self._search_sparse(q, top_k)
            else:
                results = self._search_hybrid(
                    q, top_k,
                    dense_weight=config.dense_weight,
                    sparse_weight=config.sparse_weight,
                )
            
            all_results.extend(results)
        
        seen_ids = set()
        unique_results = []
        for r in all_results:
            if r.doc_id not in seen_ids:
                seen_ids.add(r.doc_id)
                unique_results.append(r)
        
        unique_results.sort(key=lambda x: x.score, reverse=True)
        unique_results = unique_results[:top_k * 2]
        
        if config.metadata_filters:
            unique_results = self._apply_metadata_filter(
                unique_results, 
                config.metadata_filters
            )
        
        if config.use_reranking and self._reranker:
            unique_results = self._reranker.rerank(
                query,
                unique_results,
                top_k=config.top_k_rerank or top_k,
            )
        else:
            unique_results = unique_results[:top_k]
        
        if config.min_score > 0:
            unique_results = [r for r in unique_results if r.score >= config.min_score]
        
        return unique_results
    
    def get_context(
        self,
        query: str,
        top_k: Optional[int] = None,
        config: Optional[RetrievalConfig] = None,
    ) -> Tuple[str, List[Dict]]:
        """
        Sorgu için bağlam ve citations döndür.
        
        Args:
            query: Arama sorgusu
            top_k: Döndürülecek doküman sayısı
            config: Retrieval konfigürasyonu
        
        Returns:
            (context_string, citations_list)
        """
        results = self.retrieve(query, top_k=top_k, config=config)
        
        if not results:
            return "", []
        
        context_parts = []
        citations = []
        
        for i, result in enumerate(results, 1):
            context_parts.append(f"[{i}] {result.content}")
            citations.append({
                "index": i,
                "source": result.source or result.metadata.get("source", ""),
                "score": result.score,
                "doc_id": result.doc_id,
            })
        
        context = "\n\n".join(context_parts)
        return context, citations
    
    @property
    def document_count(self) -> int:
        """Toplam doküman sayısı"""
        return self._dense_index.total


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("Advanced Retriever module loaded successfully")
    print(f"FAISS available: {FAISS_AVAILABLE}")
    print(f"BM25 available: {BM25_AVAILABLE}")
    print(f"Cross-encoder available: {CROSS_ENCODER_AVAILABLE}")
