"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  DOSYA: intelligent_chunker.py                                                 ║
║  AMAÇ: Gelişmiş metin parçalama stratejileri                                  ║
║  ÖZELLİKLER:                                                                   ║
║    - Semantic Chunking (anlam tabanlı)                                         ║
║    - Recursive Character Chunking                                              ║
║    - Sentence-based Chunking                                                   ║
║    - Hybrid Chunking (en iyi sonuç için kombinasyon)                          ║
║    - Türkçe dil desteği                                                        ║
║    - Metadata koruma                                                           ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

import hashlib
import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# Optional imports
try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

try:
    import nltk
    from nltk.tokenize import sent_tokenize
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False


class ChunkingStrategy(Enum):
    """Chunking stratejileri"""
    FIXED_SIZE = "fixed_size"
    RECURSIVE = "recursive"
    SENTENCE = "sentence"
    PARAGRAPH = "paragraph"
    SEMANTIC = "semantic"
    HYBRID = "hybrid"


@dataclass
class Chunk:
    """Metin parçası veri yapısı"""
    content: str
    chunk_id: str = ""
    chunk_index: int = 0
    start_char: int = 0
    end_char: int = 0
    word_count: int = 0
    char_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.chunk_id:
            self.chunk_id = hashlib.md5(self.content.encode()).hexdigest()[:12]
        if not self.word_count:
            self.word_count = len(self.content.split())
        if not self.char_count:
            self.char_count = len(self.content)


class BaseChunker(ABC):
    """Temel chunker sınıfı"""
    
    @abstractmethod
    def chunk(self, text: str, **kwargs) -> List[Chunk]:
        """Metni parçalara ayır"""
        pass
    
    def _create_chunk(
        self,
        content: str,
        index: int,
        start: int,
        end: int,
        metadata: Optional[Dict] = None
    ) -> Chunk:
        """Chunk oluştur"""
        return Chunk(
            content=content.strip(),
            chunk_index=index,
            start_char=start,
            end_char=end,
            metadata=metadata or {}
        )


class FixedSizeChunker(BaseChunker):
    """Sabit boyutlu chunking"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk(self, text: str, **kwargs) -> List[Chunk]:
        chunks = []
        start = 0
        index = 0
        
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            
            if end < len(text):
                last_space = text.rfind(' ', start, end)
                if last_space > start:
                    end = last_space
            
            chunk_text = text[start:end].strip()
            
            if chunk_text:
                chunks.append(self._create_chunk(
                    chunk_text, index, start, end, kwargs.get('metadata')
                ))
                index += 1
            
            start = end - self.chunk_overlap
            if start >= len(text) - self.chunk_overlap:
                break
        
        return chunks


class RecursiveChunker(BaseChunker):
    """Recursive character text splitting"""
    
    DEFAULT_SEPARATORS = [
        "\n\n\n",
        "\n\n",
        "\n",
        ". ",
        "? ",
        "! ",
        "; ",
        ", ",
        " ",
        ""
    ]
    
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        separators: Optional[List[str]] = None
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or self.DEFAULT_SEPARATORS
    
    def chunk(self, text: str, **kwargs) -> List[Chunk]:
        chunks = self._split_text(text, self.separators)
        
        result = []
        for i, chunk_text in enumerate(chunks):
            if chunk_text.strip():
                result.append(self._create_chunk(
                    chunk_text, i, 0, len(chunk_text), kwargs.get('metadata')
                ))
        
        return result
    
    def _split_text(self, text: str, separators: List[str]) -> List[str]:
        """Recursive splitting"""
        if not text:
            return []
        
        if len(text) <= self.chunk_size:
            return [text]
        
        for sep in separators:
            if sep == "":
                return self._split_by_char(text)
            
            if sep in text:
                parts = text.split(sep)
                
                merged = self._merge_splits(parts, sep)
                
                result = []
                for part in merged:
                    if len(part) <= self.chunk_size:
                        result.append(part)
                    else:
                        remaining_seps = separators[separators.index(sep) + 1:]
                        result.extend(self._split_text(part, remaining_seps))
                
                return result
        
        return self._split_by_char(text)
    
    def _merge_splits(self, splits: List[str], separator: str) -> List[str]:
        """Küçük parçaları birleştir"""
        merged = []
        current = ""
        
        for split in splits:
            test = current + separator + split if current else split
            
            if len(test) <= self.chunk_size:
                current = test
            else:
                if current:
                    merged.append(current)
                current = split
        
        if current:
            merged.append(current)
        
        return merged
    
    def _split_by_char(self, text: str) -> List[str]:
        """Karakter bazında böl"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunks.append(text[start:end])
            start = end - self.chunk_overlap
        
        return chunks


class SentenceChunker(BaseChunker):
    """Cümle tabanlı chunking"""
    
    TURKISH_SENTENCE_PATTERN = re.compile(
        r'(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ])|'
        r'(?<=[.!?])(?=\s*$)|'
        r'(?<=\.)\s+(?=\d)|'
        r'(?<=[.!?])\s+(?=["\'"])'
    )
    
    def __init__(
        self,
        max_sentences_per_chunk: int = 5,
        min_chunk_size: int = 100,
        max_chunk_size: int = 1000
    ):
        self.max_sentences = max_sentences_per_chunk
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
    
    def chunk(self, text: str, **kwargs) -> List[Chunk]:
        sentences = self._split_sentences(text)
        
        chunks = []
        current_sentences = []
        current_length = 0
        index = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            if (current_length + len(sentence) > self.max_chunk_size and 
                current_length >= self.min_chunk_size):
                chunk_text = ' '.join(current_sentences)
                chunks.append(self._create_chunk(
                    chunk_text, index, 0, len(chunk_text), kwargs.get('metadata')
                ))
                index += 1
                current_sentences = []
                current_length = 0
            
            current_sentences.append(sentence)
            current_length += len(sentence) + 1
            
            if len(current_sentences) >= self.max_sentences:
                chunk_text = ' '.join(current_sentences)
                chunks.append(self._create_chunk(
                    chunk_text, index, 0, len(chunk_text), kwargs.get('metadata')
                ))
                index += 1
                current_sentences = []
                current_length = 0
        
        if current_sentences:
            chunk_text = ' '.join(current_sentences)
            chunks.append(self._create_chunk(
                chunk_text, index, 0, len(chunk_text), kwargs.get('metadata')
            ))
        
        return chunks
    
    def _split_sentences(self, text: str) -> List[str]:
        """Cümlelere ayır"""
        if NLTK_AVAILABLE:
            try:
                return sent_tokenize(text, language='turkish')
            except Exception:
                pass
        
        sentences = self.TURKISH_SENTENCE_PATTERN.split(text)
        return [s.strip() for s in sentences if s.strip()]


class ParagraphChunker(BaseChunker):
    """Paragraf tabanlı chunking"""
    
    def __init__(
        self,
        max_paragraphs_per_chunk: int = 3,
        min_chunk_size: int = 200,
        max_chunk_size: int = 1500
    ):
        self.max_paragraphs = max_paragraphs_per_chunk
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
    
    def chunk(self, text: str, **kwargs) -> List[Chunk]:
        paragraphs = re.split(r'\n\s*\n', text)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        chunks = []
        current_paragraphs = []
        current_length = 0
        index = 0
        
        for para in paragraphs:
            if (current_length + len(para) > self.max_chunk_size and 
                current_length >= self.min_chunk_size):
                chunk_text = '\n\n'.join(current_paragraphs)
                chunks.append(self._create_chunk(
                    chunk_text, index, 0, len(chunk_text), kwargs.get('metadata')
                ))
                index += 1
                current_paragraphs = []
                current_length = 0
            
            current_paragraphs.append(para)
            current_length += len(para) + 2
            
            if len(current_paragraphs) >= self.max_paragraphs:
                chunk_text = '\n\n'.join(current_paragraphs)
                chunks.append(self._create_chunk(
                    chunk_text, index, 0, len(chunk_text), kwargs.get('metadata')
                ))
                index += 1
                current_paragraphs = []
                current_length = 0
        
        if current_paragraphs:
            chunk_text = '\n\n'.join(current_paragraphs)
            chunks.append(self._create_chunk(
                chunk_text, index, 0, len(chunk_text), kwargs.get('metadata')
            ))
        
        return chunks


class SemanticChunker(BaseChunker):
    """Semantic similarity tabanlı chunking"""
    
    def __init__(
        self,
        embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        similarity_threshold: float = 0.5,
        min_chunk_size: int = 100,
        max_chunk_size: int = 1000
    ):
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise ImportError("Semantic chunking için sentence-transformers gerekli")
        
        self.model = SentenceTransformer(embedding_model)
        self.similarity_threshold = similarity_threshold
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
    
    def chunk(self, text: str, **kwargs) -> List[Chunk]:
        sentences = self._split_to_sentences(text)
        
        if len(sentences) <= 1:
            return [self._create_chunk(text, 0, 0, len(text), kwargs.get('metadata'))]
        
        embeddings = self.model.encode(sentences, convert_to_numpy=True)
        
        chunks = []
        current_sentences = [sentences[0]]
        current_embedding = embeddings[0]
        index = 0
        
        for i in range(1, len(sentences)):
            similarity = self._cosine_similarity(current_embedding, embeddings[i])
            current_length = sum(len(s) for s in current_sentences)
            
            should_split = (
                similarity < self.similarity_threshold and 
                current_length >= self.min_chunk_size
            ) or current_length >= self.max_chunk_size
            
            if should_split:
                chunk_text = ' '.join(current_sentences)
                chunks.append(self._create_chunk(
                    chunk_text, index, 0, len(chunk_text), kwargs.get('metadata')
                ))
                index += 1
                current_sentences = [sentences[i]]
                current_embedding = embeddings[i]
            else:
                current_sentences.append(sentences[i])
                current_embedding = np.mean([current_embedding, embeddings[i]], axis=0)
        
        if current_sentences:
            chunk_text = ' '.join(current_sentences)
            chunks.append(self._create_chunk(
                chunk_text, index, 0, len(chunk_text), kwargs.get('metadata')
            ))
        
        return chunks
    
    def _split_to_sentences(self, text: str) -> List[str]:
        """Metni cümlelere ayır"""
        pattern = r'(?<=[.!?])\s+'
        sentences = re.split(pattern, text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Cosine similarity hesapla"""
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


class HybridChunker(BaseChunker):
    """Hibrit chunking stratejisi - en iyi sonuçlar için"""
    
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        use_semantic: bool = False,
        semantic_threshold: float = 0.5
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.use_semantic = use_semantic and SENTENCE_TRANSFORMERS_AVAILABLE
        self.semantic_threshold = semantic_threshold
        
        self.paragraph_chunker = ParagraphChunker(
            max_chunk_size=chunk_size * 2
        )
        self.sentence_chunker = SentenceChunker(
            max_chunk_size=chunk_size
        )
        self.recursive_chunker = RecursiveChunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        if self.use_semantic:
            try:
                self.semantic_chunker = SemanticChunker(
                    similarity_threshold=semantic_threshold,
                    max_chunk_size=chunk_size
                )
            except Exception as e:
                logger.warning(f"Semantic chunker başlatılamadı: {e}")
                self.use_semantic = False
    
    def chunk(self, text: str, **kwargs) -> List[Chunk]:
        """
        Hibrit chunking stratejisi:
        1. Önce paragraflara ayır
        2. Büyük paragrafları cümlelere ayır
        3. Hala büyükse recursive split
        4. Opsiyonel: semantic merge
        """
        paragraph_chunks = self.paragraph_chunker.chunk(text, **kwargs)
        
        refined_chunks = []
        
        for para_chunk in paragraph_chunks:
            if para_chunk.char_count > self.chunk_size * 1.5:
                sentence_chunks = self.sentence_chunker.chunk(
                    para_chunk.content, **kwargs
                )
                
                for sent_chunk in sentence_chunks:
                    if sent_chunk.char_count > self.chunk_size * 1.5:
                        recursive_chunks = self.recursive_chunker.chunk(
                            sent_chunk.content, **kwargs
                        )
                        refined_chunks.extend(recursive_chunks)
                    else:
                        refined_chunks.append(sent_chunk)
            else:
                refined_chunks.append(para_chunk)
        
        if self.use_semantic and len(refined_chunks) > 2:
            refined_chunks = self._semantic_merge(refined_chunks)
        
        for i, chunk in enumerate(refined_chunks):
            chunk.chunk_index = i
        
        return refined_chunks
    
    def _semantic_merge(self, chunks: List[Chunk]) -> List[Chunk]:
        """Semantik olarak benzer chunk'ları birleştir"""
        if not self.use_semantic:
            return chunks
        
        texts = [c.content for c in chunks]
        embeddings = self.semantic_chunker.model.encode(texts, convert_to_numpy=True)
        
        merged = []
        i = 0
        
        while i < len(chunks):
            current = chunks[i]
            
            while i + 1 < len(chunks):
                next_chunk = chunks[i + 1]
                combined_length = current.char_count + next_chunk.char_count
                
                if combined_length > self.chunk_size * 1.5:
                    break
                
                similarity = self.semantic_chunker._cosine_similarity(
                    embeddings[i], embeddings[i + 1]
                )
                
                if similarity >= self.semantic_threshold:
                    current = Chunk(
                        content=current.content + "\n\n" + next_chunk.content,
                        metadata=current.metadata
                    )
                    i += 1
                else:
                    break
            
            merged.append(current)
            i += 1
        
        return merged


class IntelligentChunker:
    """
    Ana intelligent chunker sınıfı.
    
    Kullanım:
        chunker = IntelligentChunker(strategy=ChunkingStrategy.HYBRID)
        chunks = chunker.chunk(text)
    """
    
    def __init__(
        self,
        strategy: ChunkingStrategy = ChunkingStrategy.HYBRID,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        **kwargs
    ):
        self.strategy = strategy
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.kwargs = kwargs
        
        self._chunker = self._create_chunker()
    
    def _create_chunker(self) -> BaseChunker:
        """Strateji'ye göre chunker oluştur"""
        if self.strategy == ChunkingStrategy.FIXED_SIZE:
            return FixedSizeChunker(self.chunk_size, self.chunk_overlap)
        
        elif self.strategy == ChunkingStrategy.RECURSIVE:
            return RecursiveChunker(
                self.chunk_size, 
                self.chunk_overlap,
                self.kwargs.get('separators')
            )
        
        elif self.strategy == ChunkingStrategy.SENTENCE:
            return SentenceChunker(
                max_chunk_size=self.chunk_size,
                **{k: v for k, v in self.kwargs.items() 
                   if k in ['max_sentences_per_chunk', 'min_chunk_size']}
            )
        
        elif self.strategy == ChunkingStrategy.PARAGRAPH:
            return ParagraphChunker(
                max_chunk_size=self.chunk_size,
                **{k: v for k, v in self.kwargs.items() 
                   if k in ['max_paragraphs_per_chunk', 'min_chunk_size']}
            )
        
        elif self.strategy == ChunkingStrategy.SEMANTIC:
            return SemanticChunker(
                max_chunk_size=self.chunk_size,
                **{k: v for k, v in self.kwargs.items() 
                   if k in ['embedding_model', 'similarity_threshold', 'min_chunk_size']}
            )
        
        elif self.strategy == ChunkingStrategy.HYBRID:
            return HybridChunker(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                use_semantic=self.kwargs.get('use_semantic', False),
                semantic_threshold=self.kwargs.get('semantic_threshold', 0.5)
            )
        
        else:
            raise ValueError(f"Bilinmeyen strateji: {self.strategy}")
    
    def chunk(
        self, 
        text: str, 
        source: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> List[Chunk]:
        """
        Metni parçalara ayır.
        
        Args:
            text: İşlenecek metin
            source: Kaynak bilgisi
            metadata: Ek metadata
        
        Returns:
            Chunk listesi
        """
        if not text or not text.strip():
            return []
        
        chunk_metadata = metadata or {}
        if source:
            chunk_metadata['source'] = source
        
        chunks = self._chunker.chunk(text, metadata=chunk_metadata)
        
        for chunk in chunks:
            chunk.metadata.update(chunk_metadata)
        
        logger.debug(f"Chunking tamamlandı: {len(chunks)} parça oluşturuldu")
        return chunks
    
    def chunk_with_context(
        self,
        text: str,
        context_window: int = 1,
        **kwargs
    ) -> List[Chunk]:
        """
        Chunk'lara komşu bağlam ekle.
        
        Args:
            text: İşlenecek metin
            context_window: Kaç komşu chunk dahil edilsin
        
        Returns:
            Bağlamlı chunk listesi
        """
        chunks = self.chunk(text, **kwargs)
        
        for i, chunk in enumerate(chunks):
            context_before = ""
            context_after = ""
            
            for j in range(max(0, i - context_window), i):
                context_before += chunks[j].content[:100] + "... "
            
            for j in range(i + 1, min(len(chunks), i + context_window + 1)):
                context_after += "..." + chunks[j].content[:100] + " "
            
            chunk.metadata['context_before'] = context_before.strip()
            chunk.metadata['context_after'] = context_after.strip()
        
        return chunks


def chunk_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    strategy: ChunkingStrategy = ChunkingStrategy.HYBRID,
    **kwargs
) -> List[Chunk]:
    """
    Convenience function - metni parçalara ayır.
    
    Args:
        text: İşlenecek metin
        chunk_size: Hedef chunk boyutu
        chunk_overlap: Chunk örtüşmesi
        strategy: Chunking stratejisi
    
    Returns:
        Chunk listesi
    """
    chunker = IntelligentChunker(
        strategy=strategy,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        **kwargs
    )
    return chunker.chunk(text)


def chunk_document(
    document,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    strategy: ChunkingStrategy = ChunkingStrategy.HYBRID,
    **kwargs
) -> List[Chunk]:
    """
    ProcessedDocument'ı parçalara ayır.
    
    Args:
        document: ProcessedDocument instance
        chunk_size: Hedef chunk boyutu
        chunk_overlap: Chunk örtüşmesi
        strategy: Chunking stratejisi
    
    Returns:
        Chunk listesi
    """
    chunker = IntelligentChunker(
        strategy=strategy,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        **kwargs
    )
    
    metadata = {
        'source': document.source,
        'file_type': document.file_type,
        'title': document.title,
    }
    metadata.update(document.metadata)
    
    return chunker.chunk(document.content, source=document.source, metadata=metadata)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    sample_text = """
    Selçuk Üniversitesi, 1975 yılında Konya'da kurulmuştur. Türkiye'nin en büyük 
    üniversitelerinden biri olan Selçuk Üniversitesi, 23 fakülte, 6 enstitü ve 
    çok sayıda meslek yüksekokulu ile eğitim vermektedir.

    Akademik takvim 2024-2025 güz dönemi için önemli tarihler şunlardır:
    - Kayıt tarihleri: 2-6 Eylül 2024
    - Ders başlangıcı: 16 Eylül 2024
    - Vize sınavları: 11-22 Kasım 2024
    - Final sınavları: 6-17 Ocak 2025

    Bilgisayar Mühendisliği bölümü, Teknoloji Fakültesi bünyesinde yer almaktadır.
    Bölümde 4 yıllık lisans eğitimi verilmektedir.
    """
    
    print("=== Fixed Size Chunking ===")
    chunks = chunk_text(sample_text, strategy=ChunkingStrategy.FIXED_SIZE, chunk_size=200)
    for i, c in enumerate(chunks):
        print(f"[{i}] ({c.char_count} chars): {c.content[:50]}...")
    
    print("\n=== Hybrid Chunking ===")
    chunks = chunk_text(sample_text, strategy=ChunkingStrategy.HYBRID, chunk_size=300)
    for i, c in enumerate(chunks):
        print(f"[{i}] ({c.char_count} chars): {c.content[:50]}...")
