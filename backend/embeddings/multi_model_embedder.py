"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  DOSYA: multi_model_embedder.py                                                ║
║  AMAÇ: Multi-model ensemble embedding sistemi                                  ║
║  ÖZELLİKLER:                                                                   ║
║    - LaBSE (Türkçe için optimize)                                             ║
║    - BGE-M3 (çok dilli, state-of-art)                                         ║
║    - E5 (query-document çifti için)                                           ║
║    - Ensemble voting/averaging                                                 ║
║    - Embedding cache                                                           ║
║    - Batch processing                                                          ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

import hashlib
import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Union

import numpy as np

logger = logging.getLogger(__name__)

# Optional imports
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logger.warning("sentence-transformers mevcut değil")

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


class EmbeddingModel(Enum):
    """Desteklenen embedding modelleri"""
    LABSE = "sentence-transformers/LaBSE"
    BGE_M3 = "BAAI/bge-m3"
    E5_MULTILINGUAL = "intfloat/multilingual-e5-large"
    E5_BASE = "intfloat/multilingual-e5-base"
    MINILM = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    MPNET = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    
    @classmethod
    def get_dimension(cls, model: "EmbeddingModel") -> int:
        """Model embedding boyutunu döndür"""
        dimensions = {
            cls.LABSE: 768,
            cls.BGE_M3: 1024,
            cls.E5_MULTILINGUAL: 1024,
            cls.E5_BASE: 768,
            cls.MINILM: 384,
            cls.MPNET: 768,
        }
        return dimensions.get(model, 768)


@dataclass
class EmbeddingResult:
    """Embedding sonucu"""
    embeddings: np.ndarray
    model_name: str
    dimension: int
    text_count: int
    metadata: Dict[str, Any] = field(default_factory=dict)


class EmbeddingCache:
    """Disk tabanlı embedding cache"""
    
    def __init__(self, cache_dir: Optional[str] = None):
        self.cache_dir = Path(cache_dir) if cache_dir else Path("data/embedding_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._memory_cache: Dict[str, np.ndarray] = {}
        self._max_memory_items = 10000
    
    def _get_key(self, text: str, model_name: str) -> str:
        """Cache key oluştur"""
        content = f"{model_name}:{text}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def get(self, text: str, model_name: str) -> Optional[np.ndarray]:
        """Cache'den embedding al"""
        key = self._get_key(text, model_name)
        
        if key in self._memory_cache:
            return self._memory_cache[key]
        
        cache_file = self.cache_dir / f"{key}.npy"
        if cache_file.exists():
            try:
                embedding = np.load(cache_file)
                if len(self._memory_cache) < self._max_memory_items:
                    self._memory_cache[key] = embedding
                return embedding
            except Exception:
                pass
        
        return None
    
    def set(self, text: str, model_name: str, embedding: np.ndarray) -> None:
        """Embedding'i cache'e kaydet"""
        key = self._get_key(text, model_name)
        
        if len(self._memory_cache) < self._max_memory_items:
            self._memory_cache[key] = embedding
        
        cache_file = self.cache_dir / f"{key}.npy"
        try:
            np.save(cache_file, embedding)
        except Exception as e:
            logger.debug(f"Cache yazma hatası: {e}")
    
    def get_batch(
        self, 
        texts: List[str], 
        model_name: str
    ) -> tuple[List[int], List[np.ndarray]]:
        """
        Batch cache lookup.
        
        Returns:
            (cache_hit_indices, cached_embeddings)
        """
        hit_indices = []
        cached = []
        
        for i, text in enumerate(texts):
            embedding = self.get(text, model_name)
            if embedding is not None:
                hit_indices.append(i)
                cached.append(embedding)
        
        return hit_indices, cached
    
    def clear(self) -> None:
        """Cache temizle"""
        self._memory_cache.clear()
        for f in self.cache_dir.glob("*.npy"):
            f.unlink()


class BaseEmbedder(ABC):
    """Temel embedder sınıfı"""
    
    @property
    @abstractmethod
    def dimension(self) -> int:
        """Embedding boyutu"""
        pass
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Model adı"""
        pass
    
    @abstractmethod
    def embed(self, texts: Sequence[str]) -> np.ndarray:
        """Metinleri embed et"""
        pass
    
    def embed_query(self, query: str) -> np.ndarray:
        """Tek sorgu embed et"""
        return self.embed([query])[0]
    
    def embed_documents(self, documents: Sequence[str]) -> np.ndarray:
        """Dokümanları embed et"""
        return self.embed(documents)


class SentenceTransformerEmbedder(BaseEmbedder):
    """SentenceTransformer tabanlı embedder"""
    
    def __init__(
        self,
        model: Union[str, EmbeddingModel] = EmbeddingModel.LABSE,
        device: Optional[str] = None,
        batch_size: int = 32,
        normalize: bool = True,
        cache: Optional[EmbeddingCache] = None,
    ):
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise ImportError("sentence-transformers paketi gerekli")
        
        if isinstance(model, EmbeddingModel):
            self._model_name = model.value
            self._expected_dim = EmbeddingModel.get_dimension(model)
        else:
            self._model_name = model
            self._expected_dim = None
        
        self._device = self._resolve_device(device)
        self._batch_size = batch_size
        self._normalize = normalize
        self._cache = cache
        
        logger.info(f"Loading model: {self._model_name} on {self._device}")
        self._model = SentenceTransformer(self._model_name, device=self._device)
        self._dimension = self._model.get_sentence_embedding_dimension()
        
        logger.info(f"✅ {self._model_name} yüklendi (dim={self._dimension})")
    
    @staticmethod
    def _resolve_device(device: Optional[str]) -> str:
        """Uygun device seç"""
        if device:
            return device
        
        if TORCH_AVAILABLE:
            if torch.cuda.is_available():
                return "cuda"
            if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                return "mps"
        
        return "cpu"
    
    @property
    def dimension(self) -> int:
        return self._dimension
    
    @property
    def model_name(self) -> str:
        return self._model_name
    
    def embed(self, texts: Sequence[str]) -> np.ndarray:
        if not texts:
            return np.zeros((0, self._dimension), dtype="float32")
        
        texts = list(texts)
        
        if self._cache:
            hit_indices, cached = self._cache.get_batch(texts, self._model_name)
            
            if len(hit_indices) == len(texts):
                return np.array(cached, dtype="float32")
            
            miss_indices = [i for i in range(len(texts)) if i not in hit_indices]
            miss_texts = [texts[i] for i in miss_indices]
            
            if miss_texts:
                new_embeddings = self._model.encode(
                    miss_texts,
                    batch_size=self._batch_size,
                    show_progress_bar=False,
                    convert_to_numpy=True,
                    normalize_embeddings=self._normalize,
                )
                
                for i, idx in enumerate(miss_indices):
                    self._cache.set(texts[idx], self._model_name, new_embeddings[i])
            
            all_embeddings = np.zeros((len(texts), self._dimension), dtype="float32")
            
            for i, emb in zip(hit_indices, cached):
                all_embeddings[i] = emb
            
            for i, idx in enumerate(miss_indices):
                all_embeddings[idx] = new_embeddings[i]
            
            return all_embeddings
        
        embeddings = self._model.encode(
            texts,
            batch_size=self._batch_size,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=self._normalize,
        )
        
        return np.ascontiguousarray(embeddings, dtype="float32")
    
    def embed_query(self, query: str) -> np.ndarray:
        """E5 modelleri için query prefix ekle"""
        if "e5" in self._model_name.lower():
            query = f"query: {query}"
        return self.embed([query])[0]
    
    def embed_documents(self, documents: Sequence[str]) -> np.ndarray:
        """E5 modelleri için passage prefix ekle"""
        if "e5" in self._model_name.lower():
            documents = [f"passage: {doc}" for doc in documents]
        return self.embed(documents)


class EnsembleEmbedder(BaseEmbedder):
    """
    Multi-model ensemble embedder.
    
    Birden fazla modelin embedding'lerini birleştirerek
    daha güçlü representation oluşturur.
    """
    
    def __init__(
        self,
        models: Optional[List[Union[str, EmbeddingModel]]] = None,
        weights: Optional[List[float]] = None,
        combination_method: str = "concatenate",  # concatenate, average, weighted_average
        device: Optional[str] = None,
        cache: Optional[EmbeddingCache] = None,
    ):
        if models is None:
            models = [
                EmbeddingModel.LABSE,
                EmbeddingModel.E5_BASE,
            ]
        
        self._combination_method = combination_method
        self._cache = cache
        
        self._embedders: List[SentenceTransformerEmbedder] = []
        for model in models:
            embedder = SentenceTransformerEmbedder(
                model=model,
                device=device,
                cache=cache,
            )
            self._embedders.append(embedder)
        
        if weights is None:
            self._weights = [1.0 / len(self._embedders)] * len(self._embedders)
        else:
            total = sum(weights)
            self._weights = [w / total for w in weights]
        
        if combination_method == "concatenate":
            self._dimension = sum(e.dimension for e in self._embedders)
        else:
            self._dimension = self._embedders[0].dimension
        
        model_names = [e.model_name.split("/")[-1] for e in self._embedders]
        self._model_name = f"ensemble({','.join(model_names)})"
        
        logger.info(f"✅ Ensemble embedder: {self._model_name} (dim={self._dimension})")
    
    @property
    def dimension(self) -> int:
        return self._dimension
    
    @property
    def model_name(self) -> str:
        return self._model_name
    
    def embed(self, texts: Sequence[str]) -> np.ndarray:
        if not texts:
            return np.zeros((0, self._dimension), dtype="float32")
        
        all_embeddings = []
        for embedder in self._embedders:
            emb = embedder.embed(texts)
            all_embeddings.append(emb)
        
        if self._combination_method == "concatenate":
            combined = np.concatenate(all_embeddings, axis=1)
        
        elif self._combination_method == "average":
            stacked = np.stack(all_embeddings, axis=0)
            combined = np.mean(stacked, axis=0)
        
        elif self._combination_method == "weighted_average":
            combined = np.zeros_like(all_embeddings[0])
            for emb, weight in zip(all_embeddings, self._weights):
                combined += emb * weight
        
        else:
            raise ValueError(f"Bilinmeyen kombinasyon metodu: {self._combination_method}")
        
        norms = np.linalg.norm(combined, axis=1, keepdims=True)
        norms[norms == 0] = 1
        combined = combined / norms
        
        return combined.astype("float32")
    
    def embed_query(self, query: str) -> np.ndarray:
        all_embeddings = []
        for embedder in self._embedders:
            emb = embedder.embed_query(query)
            all_embeddings.append(emb)
        
        if self._combination_method == "concatenate":
            combined = np.concatenate(all_embeddings)
        elif self._combination_method == "average":
            combined = np.mean(all_embeddings, axis=0)
        elif self._combination_method == "weighted_average":
            combined = sum(e * w for e, w in zip(all_embeddings, self._weights))
        else:
            combined = np.concatenate(all_embeddings)
        
        return combined / np.linalg.norm(combined)
    
    def embed_documents(self, documents: Sequence[str]) -> np.ndarray:
        return self.embed(documents)


class MultiModelEmbedder:
    """
    Ana multi-model embedder sınıfı.
    
    Kullanım:
        embedder = MultiModelEmbedder(model=EmbeddingModel.LABSE)
        embeddings = embedder.embed(["text1", "text2"])
        
        # Ensemble
        embedder = MultiModelEmbedder(
            models=[EmbeddingModel.LABSE, EmbeddingModel.E5_BASE],
            ensemble=True
        )
    """
    
    def __init__(
        self,
        model: Optional[Union[str, EmbeddingModel]] = None,
        models: Optional[List[Union[str, EmbeddingModel]]] = None,
        ensemble: bool = False,
        combination_method: str = "concatenate",
        weights: Optional[List[float]] = None,
        device: Optional[str] = None,
        batch_size: int = 32,
        use_cache: bool = True,
        cache_dir: Optional[str] = None,
    ):
        self._use_cache = use_cache
        self._cache = EmbeddingCache(cache_dir) if use_cache else None
        
        if ensemble or (models is not None and len(models) > 1):
            if models is None:
                models = [EmbeddingModel.LABSE, EmbeddingModel.E5_BASE]
            
            self._embedder = EnsembleEmbedder(
                models=models,
                weights=weights,
                combination_method=combination_method,
                device=device,
                cache=self._cache,
            )
        else:
            if model is None:
                model = EmbeddingModel.LABSE
            
            self._embedder = SentenceTransformerEmbedder(
                model=model,
                device=device,
                batch_size=batch_size,
                cache=self._cache,
            )
    
    @property
    def dimension(self) -> int:
        return self._embedder.dimension
    
    @property
    def model_name(self) -> str:
        return self._embedder.model_name
    
    def embed(self, texts: Sequence[str]) -> EmbeddingResult:
        """
        Metinleri embed et.
        
        Args:
            texts: Metin listesi
        
        Returns:
            EmbeddingResult
        """
        embeddings = self._embedder.embed(texts)
        
        return EmbeddingResult(
            embeddings=embeddings,
            model_name=self._embedder.model_name,
            dimension=self._embedder.dimension,
            text_count=len(texts),
        )
    
    def embed_query(self, query: str) -> np.ndarray:
        """Sorgu embed et"""
        return self._embedder.embed_query(query)
    
    def embed_documents(self, documents: Sequence[str]) -> np.ndarray:
        """Dokümanları embed et"""
        return self._embedder.embed_documents(documents)
    
    def clear_cache(self) -> None:
        """Cache temizle"""
        if self._cache:
            self._cache.clear()


def get_embedder(
    model: Union[str, EmbeddingModel] = EmbeddingModel.LABSE,
    **kwargs
) -> MultiModelEmbedder:
    """
    Convenience function - embedder al.
    
    Args:
        model: Model adı veya EmbeddingModel enum
        **kwargs: MultiModelEmbedder parametreleri
    
    Returns:
        MultiModelEmbedder instance
    """
    return MultiModelEmbedder(model=model, **kwargs)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    texts = [
        "Selçuk Üniversitesi Konya'da bulunmaktadır.",
        "Akademik takvim 2024-2025 güz dönemi başlamıştır.",
        "Bilgisayar Mühendisliği bölümü 4 yıllık eğitim vermektedir.",
    ]
    
    print("=== Single Model (LaBSE) ===")
    embedder = get_embedder(EmbeddingModel.LABSE)
    result = embedder.embed(texts)
    print(f"Model: {result.model_name}")
    print(f"Dimension: {result.dimension}")
    print(f"Shape: {result.embeddings.shape}")
    
    print("\n=== Ensemble (LaBSE + E5) ===")
    ensemble_embedder = MultiModelEmbedder(
        models=[EmbeddingModel.LABSE, EmbeddingModel.E5_BASE],
        ensemble=True,
        combination_method="concatenate"
    )
    result = ensemble_embedder.embed(texts)
    print(f"Model: {result.model_name}")
    print(f"Dimension: {result.dimension}")
    print(f"Shape: {result.embeddings.shape}")
