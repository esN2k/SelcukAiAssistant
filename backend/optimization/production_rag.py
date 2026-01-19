"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  DOSYA: production_rag.py                                                      ║
║  AMAÇ: Production-grade RAG servisi - Caching, Monitoring, Optimization       ║
║  ÖZELLİKLER:                                                                   ║
║    - Multi-level caching (Memory + Redis)                                      ║
║    - Request/Response monitoring                                               ║
║    - Performance metrics                                                       ║
║    - Auto-scaling configuration                                                ║
║    - Health checks                                                             ║
║    - Graceful degradation                                                      ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Deque, Dict, List, Optional, Tuple, TypeVar, Union

logger = logging.getLogger(__name__)

# Optional imports
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


class CacheLevel(Enum):
    """Cache seviyeleri"""
    MEMORY = "memory"
    DISK = "disk"
    REDIS = "redis"


@dataclass
class ProductionConfig:
    """Production konfigürasyonu"""
    cache_enabled: bool = True
    cache_ttl_seconds: int = 3600
    cache_max_size: int = 10000
    
    redis_url: Optional[str] = None
    redis_prefix: str = "rag:"
    
    monitoring_enabled: bool = True
    metrics_window_size: int = 1000
    
    max_concurrent_requests: int = 10
    request_timeout_seconds: float = 30.0
    
    fallback_enabled: bool = True
    min_confidence_threshold: float = 0.3
    
    log_queries: bool = True
    log_path: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> "ProductionConfig":
        """Environment variable'lardan config oluştur"""
        return cls(
            cache_enabled=os.getenv("RAG_CACHE_ENABLED", "true").lower() == "true",
            cache_ttl_seconds=int(os.getenv("RAG_CACHE_TTL", "3600")),
            cache_max_size=int(os.getenv("RAG_CACHE_MAX_SIZE", "10000")),
            redis_url=os.getenv("REDIS_URL"),
            monitoring_enabled=os.getenv("RAG_MONITORING", "true").lower() == "true",
            max_concurrent_requests=int(os.getenv("RAG_MAX_CONCURRENT", "10")),
            request_timeout_seconds=float(os.getenv("RAG_TIMEOUT", "30.0")),
            log_queries=os.getenv("RAG_LOG_QUERIES", "true").lower() == "true",
            log_path=os.getenv("RAG_LOG_PATH"),
        )


@dataclass
class CacheEntry:
    """Cache girişi"""
    key: str
    value: Any
    created_at: float
    ttl_seconds: int
    hit_count: int = 0
    
    @property
    def is_expired(self) -> bool:
        return time.time() - self.created_at > self.ttl_seconds


class MemoryCache:
    """LRU bellek cache"""
    
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self._max_size = max_size
        self._ttl_seconds = ttl_seconds
        self._cache: Dict[str, CacheEntry] = {}
        self._access_order: Deque[str] = deque()
        self._stats = {"hits": 0, "misses": 0, "evictions": 0}
    
    def _make_key(self, query: str, params: Optional[Dict] = None) -> str:
        """Cache key oluştur"""
        content = query
        if params:
            content += json.dumps(params, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()
    
    def get(self, query: str, params: Optional[Dict] = None) -> Optional[Any]:
        """Cache'den değer al"""
        key = self._make_key(query, params)
        
        if key not in self._cache:
            self._stats["misses"] += 1
            return None
        
        entry = self._cache[key]
        
        if entry.is_expired:
            del self._cache[key]
            self._stats["misses"] += 1
            return None
        
        entry.hit_count += 1
        self._stats["hits"] += 1
        
        if key in self._access_order:
            self._access_order.remove(key)
        self._access_order.append(key)
        
        return entry.value
    
    def set(
        self, 
        query: str, 
        value: Any, 
        params: Optional[Dict] = None,
        ttl_seconds: Optional[int] = None
    ) -> None:
        """Cache'e değer kaydet"""
        key = self._make_key(query, params)
        
        while len(self._cache) >= self._max_size:
            if self._access_order:
                oldest_key = self._access_order.popleft()
                if oldest_key in self._cache:
                    del self._cache[oldest_key]
                    self._stats["evictions"] += 1
            else:
                break
        
        self._cache[key] = CacheEntry(
            key=key,
            value=value,
            created_at=time.time(),
            ttl_seconds=ttl_seconds or self._ttl_seconds,
        )
        self._access_order.append(key)
    
    def clear(self) -> None:
        """Cache temizle"""
        self._cache.clear()
        self._access_order.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Cache istatistikleri"""
        total = self._stats["hits"] + self._stats["misses"]
        hit_rate = self._stats["hits"] / total if total > 0 else 0
        
        return {
            "size": len(self._cache),
            "max_size": self._max_size,
            "hits": self._stats["hits"],
            "misses": self._stats["misses"],
            "evictions": self._stats["evictions"],
            "hit_rate": hit_rate,
        }


class RedisCache:
    """Redis tabanlı dağıtık cache"""
    
    def __init__(
        self, 
        redis_url: str,
        prefix: str = "rag:",
        ttl_seconds: int = 3600
    ):
        if not REDIS_AVAILABLE:
            raise ImportError("redis paketi gerekli: pip install redis")
        
        self._client = redis.from_url(redis_url)
        self._prefix = prefix
        self._ttl_seconds = ttl_seconds
        
        try:
            self._client.ping()
            logger.info("✅ Redis bağlantısı başarılı")
        except Exception as e:
            raise ConnectionError(f"Redis bağlantı hatası: {e}")
    
    def _make_key(self, query: str, params: Optional[Dict] = None) -> str:
        """Cache key oluştur"""
        content = query
        if params:
            content += json.dumps(params, sort_keys=True)
        hash_key = hashlib.sha256(content.encode()).hexdigest()
        return f"{self._prefix}{hash_key}"
    
    def get(self, query: str, params: Optional[Dict] = None) -> Optional[Any]:
        """Redis'ten değer al"""
        key = self._make_key(query, params)
        
        try:
            value = self._client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.warning(f"Redis get hatası: {e}")
            return None
    
    def set(
        self, 
        query: str, 
        value: Any, 
        params: Optional[Dict] = None,
        ttl_seconds: Optional[int] = None
    ) -> None:
        """Redis'e değer kaydet"""
        key = self._make_key(query, params)
        
        try:
            self._client.setex(
                key,
                ttl_seconds or self._ttl_seconds,
                json.dumps(value, ensure_ascii=False)
            )
        except Exception as e:
            logger.warning(f"Redis set hatası: {e}")
    
    def clear(self) -> None:
        """Prefix ile başlayan tüm key'leri sil"""
        try:
            keys = self._client.keys(f"{self._prefix}*")
            if keys:
                self._client.delete(*keys)
        except Exception as e:
            logger.warning(f"Redis clear hatası: {e}")


class RAGCache:
    """Multi-level RAG cache sistemi"""
    
    def __init__(self, config: ProductionConfig):
        self.config = config
        
        self._memory_cache = MemoryCache(
            max_size=config.cache_max_size,
            ttl_seconds=config.cache_ttl_seconds,
        )
        
        self._redis_cache: Optional[RedisCache] = None
        if config.redis_url and REDIS_AVAILABLE:
            try:
                self._redis_cache = RedisCache(
                    redis_url=config.redis_url,
                    prefix=config.redis_prefix,
                    ttl_seconds=config.cache_ttl_seconds,
                )
            except Exception as e:
                logger.warning(f"Redis cache başlatılamadı: {e}")
    
    def get(self, query: str, params: Optional[Dict] = None) -> Optional[Any]:
        """Cache'den değer al (memory -> redis)"""
        result = self._memory_cache.get(query, params)
        if result is not None:
            return result
        
        if self._redis_cache:
            result = self._redis_cache.get(query, params)
            if result is not None:
                self._memory_cache.set(query, result, params)
                return result
        
        return None
    
    def set(
        self, 
        query: str, 
        value: Any, 
        params: Optional[Dict] = None,
        ttl_seconds: Optional[int] = None
    ) -> None:
        """Cache'e değer kaydet (memory + redis)"""
        self._memory_cache.set(query, value, params, ttl_seconds)
        
        if self._redis_cache:
            self._redis_cache.set(query, value, params, ttl_seconds)
    
    def clear(self) -> None:
        """Tüm cache'leri temizle"""
        self._memory_cache.clear()
        if self._redis_cache:
            self._redis_cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Cache istatistikleri"""
        return {
            "memory": self._memory_cache.get_stats(),
            "redis_available": self._redis_cache is not None,
        }


@dataclass
class RequestMetrics:
    """İstek metrikleri"""
    query: str
    start_time: float
    end_time: float = 0.0
    latency_ms: float = 0.0
    cache_hit: bool = False
    success: bool = True
    error: Optional[str] = None
    result_count: int = 0
    confidence_score: float = 0.0


class RAGMonitor:
    """RAG sistemi monitoring"""
    
    def __init__(self, config: ProductionConfig):
        self.config = config
        self._metrics: Deque[RequestMetrics] = deque(maxlen=config.metrics_window_size)
        self._error_counts: Dict[str, int] = {}
        self._start_time = time.time()
    
    def record_request(self, metrics: RequestMetrics) -> None:
        """İstek metriğini kaydet"""
        metrics.end_time = time.time()
        metrics.latency_ms = (metrics.end_time - metrics.start_time) * 1000
        self._metrics.append(metrics)
        
        if not metrics.success and metrics.error:
            error_type = metrics.error.split(":")[0]
            self._error_counts[error_type] = self._error_counts.get(error_type, 0) + 1
        
        if self.config.log_queries:
            self._log_request(metrics)
    
    def _log_request(self, metrics: RequestMetrics) -> None:
        """İsteği logla"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "query": metrics.query[:100],
            "latency_ms": round(metrics.latency_ms, 2),
            "cache_hit": metrics.cache_hit,
            "success": metrics.success,
            "result_count": metrics.result_count,
        }
        
        if self.config.log_path:
            log_file = Path(self.config.log_path)
            log_file.parent.mkdir(parents=True, exist_ok=True)
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        
        logger.debug(f"RAG Request: {log_entry}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Monitoring istatistikleri"""
        if not self._metrics:
            return {"status": "no_data"}
        
        latencies = [m.latency_ms for m in self._metrics]
        successes = [m for m in self._metrics if m.success]
        cache_hits = [m for m in self._metrics if m.cache_hit]
        
        return {
            "total_requests": len(self._metrics),
            "success_rate": len(successes) / len(self._metrics),
            "cache_hit_rate": len(cache_hits) / len(self._metrics),
            "latency": {
                "avg_ms": sum(latencies) / len(latencies),
                "min_ms": min(latencies),
                "max_ms": max(latencies),
                "p50_ms": sorted(latencies)[len(latencies) // 2],
                "p95_ms": sorted(latencies)[int(len(latencies) * 0.95)] if len(latencies) > 20 else max(latencies),
            },
            "error_counts": dict(self._error_counts),
            "uptime_seconds": time.time() - self._start_time,
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Sağlık kontrolü"""
        stats = self.get_stats()
        
        if stats.get("status") == "no_data":
            return {"status": "healthy", "message": "No requests yet"}
        
        issues = []
        
        if stats["success_rate"] < 0.9:
            issues.append(f"Low success rate: {stats['success_rate']:.2%}")
        
        if stats["latency"]["avg_ms"] > 5000:
            issues.append(f"High latency: {stats['latency']['avg_ms']:.0f}ms")
        
        if issues:
            return {
                "status": "degraded",
                "issues": issues,
                "stats": stats,
            }
        
        return {
            "status": "healthy",
            "stats": stats,
        }


class ProductionRAGService:
    """
    Production-grade RAG servisi.
    
    Özellikler:
        - Multi-level caching
        - Request monitoring
        - Graceful degradation
        - Health checks
        - Concurrent request limiting
    """
    
    def __init__(
        self,
        retriever,
        config: Optional[ProductionConfig] = None,
    ):
        self.retriever = retriever
        self.config = config or ProductionConfig.from_env()
        
        self._cache: Optional[RAGCache] = None
        if self.config.cache_enabled:
            self._cache = RAGCache(self.config)
        
        self._monitor: Optional[RAGMonitor] = None
        if self.config.monitoring_enabled:
            self._monitor = RAGMonitor(self.config)
        
        self._semaphore = asyncio.Semaphore(self.config.max_concurrent_requests)
        
        logger.info(f"✅ ProductionRAGService başlatıldı (cache: {self.config.cache_enabled})")
    
    def _create_cache_params(self, top_k: int, **kwargs) -> Dict:
        """Cache parametreleri oluştur"""
        return {"top_k": top_k, **{k: v for k, v in kwargs.items() if v is not None}}
    
    def get_context(
        self,
        query: str,
        top_k: int = 5,
        **kwargs
    ) -> Tuple[str, List[Dict]]:
        """
        Production-ready context retrieval.
        
        Args:
            query: Arama sorgusu
            top_k: Döndürülecek doküman sayısı
        
        Returns:
            (context_string, citations_list)
        """
        metrics = RequestMetrics(query=query, start_time=time.time())
        
        try:
            cache_params = self._create_cache_params(top_k, **kwargs)
            
            if self._cache:
                cached = self._cache.get(query, cache_params)
                if cached:
                    metrics.cache_hit = True
                    metrics.result_count = len(cached.get("citations", []))
                    metrics.confidence_score = cached.get("confidence", 0.0)
                    
                    if self._monitor:
                        self._monitor.record_request(metrics)
                    
                    return cached["context"], cached["citations"]
            
            context, citations = self.retriever.get_context(query, top_k=top_k)
            
            confidence = 0.0
            if citations:
                scores = [c.get("score", 0) for c in citations]
                confidence = sum(scores) / len(scores) if scores else 0.0
            
            if self.config.fallback_enabled and confidence < self.config.min_confidence_threshold:
                if not context:
                    context = "Bu konuda yeterli bilgi bulunamadı. Lütfen sorunuzu farklı şekilde ifade etmeyi deneyin."
                    citations = []
            
            if self._cache:
                self._cache.set(query, {
                    "context": context,
                    "citations": citations,
                    "confidence": confidence,
                }, cache_params)
            
            metrics.result_count = len(citations)
            metrics.confidence_score = confidence
            
            if self._monitor:
                self._monitor.record_request(metrics)
            
            return context, citations
            
        except Exception as e:
            metrics.success = False
            metrics.error = str(e)
            
            if self._monitor:
                self._monitor.record_request(metrics)
            
            logger.error(f"RAG error: {e}")
            
            if self.config.fallback_enabled:
                return "Bir hata oluştu. Lütfen daha sonra tekrar deneyin.", []
            
            raise
    
    async def get_context_async(
        self,
        query: str,
        top_k: int = 5,
        **kwargs
    ) -> Tuple[str, List[Dict]]:
        """Async context retrieval with concurrency limiting"""
        async with self._semaphore:
            return await asyncio.to_thread(
                self.get_context, query, top_k, **kwargs
            )
    
    def search(self, query: str, top_k: int = 10, **kwargs) -> List[Dict]:
        """Search with caching"""
        context, citations = self.get_context(query, top_k=top_k, **kwargs)
        return citations
    
    def clear_cache(self) -> None:
        """Cache temizle"""
        if self._cache:
            self._cache.clear()
            logger.info("Cache temizlendi")
    
    def get_stats(self) -> Dict[str, Any]:
        """Servis istatistikleri"""
        stats = {
            "cache": self._cache.get_stats() if self._cache else None,
            "monitor": self._monitor.get_stats() if self._monitor else None,
            "config": {
                "cache_enabled": self.config.cache_enabled,
                "monitoring_enabled": self.config.monitoring_enabled,
                "max_concurrent": self.config.max_concurrent_requests,
            },
        }
        
        if hasattr(self.retriever, 'document_count'):
            stats["document_count"] = self.retriever.document_count
        
        return stats
    
    def health_check(self) -> Dict[str, Any]:
        """Sağlık kontrolü"""
        health = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "components": {},
        }
        
        if self._monitor:
            monitor_health = self._monitor.health_check()
            health["components"]["monitor"] = monitor_health
            if monitor_health["status"] != "healthy":
                health["status"] = "degraded"
        
        if self._cache:
            cache_stats = self._cache.get_stats()
            health["components"]["cache"] = {
                "status": "healthy",
                "stats": cache_stats,
            }
        
        try:
            if hasattr(self.retriever, 'document_count'):
                doc_count = self.retriever.document_count
                health["components"]["retriever"] = {
                    "status": "healthy" if doc_count > 0 else "warning",
                    "document_count": doc_count,
                }
        except Exception as e:
            health["components"]["retriever"] = {
                "status": "unhealthy",
                "error": str(e),
            }
            health["status"] = "unhealthy"
        
        return health


def with_monitoring(func: Callable) -> Callable:
    """Monitoring decorator"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = (time.time() - start_time) * 1000
            logger.debug(f"{func.__name__} completed in {elapsed:.2f}ms")
            return result
        except Exception as e:
            elapsed = (time.time() - start_time) * 1000
            logger.error(f"{func.__name__} failed after {elapsed:.2f}ms: {e}")
            raise
    return wrapper


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("Production RAG module loaded")
    print(f"Redis available: {REDIS_AVAILABLE}")
    
    config = ProductionConfig()
    print(f"Default config: cache={config.cache_enabled}, monitoring={config.monitoring_enabled}")
