"""
═══════════════════════════════════════════════════════════════════════════════
GELİŞTİRİLMİŞ RAG (Retrieval-Augmented Generation) SERVİSİ
═══════════════════════════════════════════════════════════════════════════════

Modül: rag_service_improved.py
Açıklama: Hybrid search (semantic + keyword) ile bilgi getirme sistemi

Mimari:
    1. Embedding Layer    - LaBSE ile metni 768-dim vektöre dönüştürme
    2. FAISS Index        - 14,151 vektörde hızlı semantic arama
    3. BM25 Ranker        - Keyword-based probabilistic ranking
    4. Hybrid Merge       - 0.6*semantic + 0.4*keyword birleştirme
    5. Metadata Manager   - Kaynak bilgisi yönetimi

İş Akışı:
    Kullanıcı Sorgusu
        ↓
    LaBSE Embedding (768-dim)
        ↓
    ┌─────────────────────────────┐
    │  Parallel Search            │
    │  - FAISS (semantic)         │
    │  - BM25 (keyword)           │
    └─────────────────────────────┘
        ↓
    Score Birleştirme
        ↓
    Top-K Sonuç (metadata ile)

Performans:
    - Embedding: ~50ms
    - FAISS arama: ~10ms
    - BM25 arama: ~5ms
    - Toplam: ~100ms (çok hızlı)

İndeks Bilgisi:
    - Vektör sayısı: 14,151
    - Boyut: 768 (LaBSE)
    - Dosya boyutu: 41.46 MB
    - Dokuman sayısı: 650+

Yazar: SelçukAI Ekibi
═══════════════════════════════════════════════════════════════════════════════
"""
import logging
import pickle
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
import numpy as np

logger = logging.getLogger(__name__)

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logger.warning("sentence-transformers mevcut değil")

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logger.warning("FAISS mevcut değil")

try:
    from rank_bm25 import BM25Okapi
    BM25_AVAILABLE = True
except ImportError:
    BM25_AVAILABLE = False
    logger.warning("rank-bm25 mevcut değil")


class ImprovedRAGService:
    """
    Geliştirilmiş RAG Servisi.
    
    Bu sınıf, hibrit arama (FAISS semantic + BM25 keyword) yaparak
    en ilgili dokümanları bulur ve LLM'e bağlam olarak sunar.
    
    Özellikler:
        - LaBSE embedding (768-dim, Türkçe için optimize)
        - Hibrit arama (FAISS + BM25)
        - Akıllı parçalama (chunking)
        - Zengin metadata yönetimi
    
    Attributes:
        embedding_model: LaBSE embedding modeli (768-dim)
        faiss_index: FAISS vektör indeksi
        bm25: BM25 keyword ranker
        documents: İndekslenmiş dokümanlar
        metadata: Doküman kaynak bilgileri
    """
    
    def __init__(self, data_path: Path):
        self.data_path = Path(data_path)
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        # LaBSE - En iyi çok dilli model
        logger.info("🔄 LaBSE embedding modeli yükleniyor...")
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            self.embedding_model = SentenceTransformer('sentence-transformers/LaBSE')
            logger.info("✅ LaBSE yüklendi (768-dim)")
        else:
            self.embedding_model = None
            logger.error("❌ sentence-transformers mevcut değil")
        
        # FAISS index
        self.dimension = 768
        self.faiss_index = None
        if FAISS_AVAILABLE:
            self.faiss_index = faiss.IndexFlatIP(self.dimension)
        
        # BM25 keyword arama için
        self.bm25 = None
        self.documents = []
        self.metadata = []
        
        # Mevcut indeksi yükle (varsa)
        self._load_index()
    
    def index_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        Dokümanları hibrit yaklaşımla indeksler.
        
        Args:
            documents: İndekslenecek doküman listesi
        """
        logger.info(f"📊 {len(documents)} doküman indeksleniyor...")
        
        if not self.embedding_model:
            logger.error("❌ İndeksleme yapılamaz: embedding modeli mevcut değil")
            return
        
        # Mevcut verileri temizle
        self.documents = []
        self.metadata = []
        
        # Verileri hazırla
        texts = []
        for doc in documents:
            # Akıllı parçalama
            chunks = self._smart_chunk(doc['text'], doc.get('type', 'text'))
            
            for i, chunk in enumerate(chunks):
                self.documents.append(chunk)
                self.metadata.append({
                    'source': doc.get('source', 'unknown'),
                    'type': doc.get('type', 'text'),
                    'chunk_id': i,
                    'total_chunks': len(chunks),
                    'priority': self._calculate_priority(doc),
                    'keywords': self._extract_keywords(chunk),
                    'has_dates': bool(self._extract_dates(chunk)),
                })
                texts.append(chunk)
        
        # FAISS indeksleme (semantic)
        if self.faiss_index and texts:
            logger.info("🔄 Embedding'ler oluşturuluyor...")
            embeddings = self.embedding_model.encode(
                texts, 
                batch_size=32,
                show_progress_bar=True,
                normalize_embeddings=True
            )
            
            # İndeksi sıfırla
            self.faiss_index = faiss.IndexFlatIP(self.dimension)
            self.faiss_index.add(embeddings.astype('float32'))
            logger.info(f"✅ FAISS indeksi: {self.faiss_index.ntotal} vektör")
        
        # BM25 indeksleme (keyword)
        if BM25_AVAILABLE and texts:
            tokenized_docs = [doc.lower().split() for doc in texts]
            self.bm25 = BM25Okapi(tokenized_docs)
            logger.info("✅ BM25 indeksi oluşturuldu")
        
        # İndeksi kaydet
        self._save_index()
    
    def _smart_chunk(self, text: str, doc_type: str) -> List[str]:
        """
        Akıllı chunking stratejisi
        """
        if doc_type == 'pdf':
            # Paragraf bazlı chunking
            paragraphs = text.split('\n\n')
            chunks = []
            current = ""
            
            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue
                
                if len(current) + len(para) < 800:
                    current += para + "\n\n"
                else:
                    if current:
                        chunks.append(current.strip())
                    current = para + "\n\n"
            
            if current:
                chunks.append(current.strip())
            
            return chunks if chunks else [text[:1000]]
        else:
            # HTML için kayan pencere
            return self._sliding_window(text, size=600, overlap=100)
    
    def _sliding_window(self, text: str, size: int = 600, overlap: int = 100) -> List[str]:
        """Kayan pencere parçalama yöntemi."""
        if len(text) <= size:
            return [text]
        
        chunks = []
        start = 0
        while start < len(text):
            end = start + size
            chunk = text[start:end]
            
            if chunk.strip():
                chunks.append(chunk.strip())
            
            start += (size - overlap)
        
        return chunks
    
    def _calculate_priority(self, doc: Dict[str, Any]) -> float:
        """
        Döküman önceliği (akademik takvim en yüksek)
        """
        source = doc.get('source', '').lower()
        text = doc.get('text', '').lower()
        
        if 'akademik_takvim' in source or 'akademik takvim' in text:
            return 1.0
        elif any(kw in source for kw in ['yonetmelik', 'mevzuat', 'bologna']):
            return 0.9
        elif doc.get('type') == 'pdf':
            return 0.8
        elif any(kw in text for kw in ['sınav', 'final', 'vize']):
            return 0.75
        else:
            return 0.6
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Metinden önemli anahtar kelimeleri çıkarır."""
        keywords = []
        text_lower = text.lower()
        
        keyword_patterns = [
            'sınav', 'final', 'vize', 'bütünleme', 'mazeret',
            'kayıt', 'başvuru', 'tescil',
            'akademik takvim', 'takvim',
            'müfredat', 'ders programı',
            'yönetmelik', 'mevzuat'
        ]
        
        for kw in keyword_patterns:
            if kw in text_lower:
                keywords.append(kw)
        
        return keywords
    
    def _extract_dates(self, text: str) -> List[str]:
        """Metinden tarihleri çıkarır."""
        import re
        dates = re.findall(
            r'(\d{1,2})\s+(Ocak|Şubat|Mart|Nisan|Mayıs|Haziran|Temmuz|Ağustos|Eylül|Ekim|Kasım|Aralık)\s+(\d{4})',
            text
        )
        return [f"{d[0]} {d[1]} {d[2]}" for d in dates]
    
    def hybrid_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Hibrit arama: FAISS (semantic) + BM25 (keyword) birleşimi.
        
        Args:
            query: Arama sorgusu
            top_k: Döndürülecek maksimum sonuç sayısı
        
        Returns:
            Sıralanmış arama sonuçları listesi
        """
        if not self.documents:
            logger.warning("⚠️ Hiç doküman indekslenmemiş")
            return []
        
        results = []
        
        # Semantic arama (FAISS)
        if self.faiss_index and self.embedding_model:
            query_emb = self.embedding_model.encode([query], normalize_embeddings=True)
            faiss_scores, faiss_indices = self.faiss_index.search(
                query_emb.astype('float32'), 
                min(top_k * 2, len(self.documents))
            )
            
            faiss_results = {}
            for score, idx in zip(faiss_scores[0], faiss_indices[0]):
                if idx < len(self.documents):
                    faiss_results[int(idx)] = float(score)
        else:
            faiss_results = {}
        
        # Keyword arama (BM25)
        if self.bm25:
            query_tokens = query.lower().split()
            bm25_scores = self.bm25.get_scores(query_tokens)
            bm25_indices = np.argsort(bm25_scores)[::-1][:top_k * 2]
            
            bm25_results = {}
            for idx in bm25_indices:
                if idx < len(self.documents):
                    bm25_results[int(idx)] = float(bm25_scores[idx])
        else:
            bm25_results = {}
        
        # Karşılıklı Sıralama Birleştirmesi (RRF)
        fused_scores = {}
        k = 60
        
        # FAISS skorlarını ekle
        for rank, (idx, score) in enumerate(sorted(faiss_results.items(), key=lambda x: x[1], reverse=True), 1):
            if idx not in fused_scores:
                fused_scores[idx] = 0
            fused_scores[idx] += 1 / (k + rank)
        
        # BM25 skorlarını ekle
        for rank, (idx, score) in enumerate(sorted(bm25_results.items(), key=lambda x: x[1], reverse=True), 1):
            if idx not in fused_scores:
                fused_scores[idx] = 0
            fused_scores[idx] += 1 / (k + rank)
        
        # Birleşik skora göre sırala
        ranked_indices = sorted(fused_scores.keys(), key=lambda x: fused_scores[x], reverse=True)[:top_k]
        
        # Sonuçları hazırla
        for idx in ranked_indices:
            results.append({
                'content': self.documents[idx],
                'metadata': self.metadata[idx],
                'score': fused_scores[idx],
                'faiss_score': faiss_results.get(idx, 0.0),
                'bm25_score': bm25_results.get(idx, 0.0)
            })
        
        logger.info(f"🔍 Hibrit arama: sorgu='{query[:50]}...', sonuç={len(results)}")
        for i, r in enumerate(results[:3], 1):
            source = r['metadata']['source']
            source_short = source[:50] + '...' if len(source) > 50 else source
            logger.info(f"  {i}. score={r['score']:.3f}, source={source_short}")
        
        return results
    
    def get_context(self, query: str, top_k: int = 3) -> Tuple[str, List[str]]:
        """
        Sorgu için bağlam ve kaynakları getirir.
        
        Mevcut RAG arayüzü ile uyumludur.
        
        Args:
            query: Arama sorgusu
            top_k: Maksimum sonuç sayısı
        
        Returns:
            (bağlam_metni, kaynak_listesi) tuple'ı
        """
        results = self.hybrid_search(query, top_k)
        
        if not results:
            return "", []
        
        # Bağlamı oluştur
        context_parts = []
        citations = []
        
        for i, result in enumerate(results, 1):
            context_parts.append(f"[Kaynak {i}]\n{result['content']}\n")
            citations.append(result['metadata']['source'])
        
        context = "\n".join(context_parts)
        
        return context, citations
    
    def _save_index(self) -> None:
        """İndeksi diske kaydeder."""
        try:
            # FAISS indeksini kaydet
            if self.faiss_index:
                faiss_path = self.data_path / "index_improved.faiss"
                faiss.write_index(self.faiss_index, str(faiss_path))
                logger.info(f"✅ FAISS indeksi kaydedildi: {faiss_path}")
            
            # Dokümanları ve metadata'yı kaydet
            data = {
                'documents': self.documents,
                'metadata': self.metadata
            }
            data_path = self.data_path / "documents_improved.pkl"
            with open(data_path, 'wb') as f:
                pickle.dump(data, f)
            logger.info(f"✅ Dokümanlar kaydedildi: {data_path}")
            
            # BM25'i kaydet
            if self.bm25:
                bm25_path = self.data_path / "bm25_improved.pkl"
                with open(bm25_path, 'wb') as f:
                    pickle.dump(self.bm25, f)
                logger.info(f"✅ BM25 indeksi kaydedildi: {bm25_path}")
            
        except Exception as e:
            logger.error(f"❌ İndeks kaydedilemedi: {e}")
    
    def _load_index(self) -> None:
        """İndeksi diskten yükler."""
        try:
            # FAISS indeksini yükle
            faiss_path = self.data_path / "index_improved.faiss"
            if faiss_path.exists() and FAISS_AVAILABLE:
                self.faiss_index = faiss.read_index(str(faiss_path))
                logger.info(f"✅ FAISS indeksi yüklendi: {self.faiss_index.ntotal} vektör")
            
            # Dokümanları ve metadata'yı yükle
            data_path = self.data_path / "documents_improved.pkl"
            if data_path.exists():
                with open(data_path, 'rb') as f:
                    data = pickle.load(f)
                self.documents = data['documents']
                self.metadata = data['metadata']
                logger.info(f"✅ Dokümanlar yüklendi: {len(self.documents)} parça")
            
            # BM25'i yükle
            bm25_path = self.data_path / "bm25_improved.pkl"
            if bm25_path.exists():
                with open(bm25_path, 'rb') as f:
                    self.bm25 = pickle.load(f)
                logger.info(f"✅ BM25 indeksi yüklendi")
            
        except Exception as e:
            logger.warning(f"⚠️ Mevcut indeks yüklenemedi: {e}")


# Tekil örnek (Singleton)
_rag_service_improved = None

def get_improved_rag_service(data_path: Path = None) -> ImprovedRAGService:
    """Geliştirilmiş RAG servisi tekil örneğini alır veya oluşturur."""
    global _rag_service_improved
    
    if _rag_service_improved is None:
        if data_path is None:
            data_path = Path(__file__).parent / "data" / "rag"
        _rag_service_improved = ImprovedRAGService(data_path)
    
    return _rag_service_improved
