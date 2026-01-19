"""
Mevcut RAG indeksine yeni dokumanlari ekler (hizli guncelleme)
"""
import sys
import pickle
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

def main():
    logger.info("="*60)
    logger.info("HIZLI RAG GUNCELLEME - Yeni MD dosyalari ekleniyor")
    logger.info("="*60)
    
    # Yeni MD dosyalarini yukle
    scraped_dir = backend_path / "data" / "scraped"
    md_files = list(scraped_dir.glob("*.md"))
    
    logger.info(f"Bulunan MD dosyalari: {len(md_files)}")
    
    new_documents = []
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            if len(text.strip()) > 100:
                new_documents.append({
                    'text': text,
                    'source': str(md_file),
                    'type': 'markdown',
                    'metadata': {
                        'chars': len(text),
                        'filename': md_file.name,
                        'domain': 'selcuk_ozel_veri',
                        'priority': 'high'
                    }
                })
                logger.info(f"  - {md_file.name} ({len(text)} karakter)")
        except Exception as e:
            logger.warning(f"Hata: {md_file.name}: {e}")
    
    if not new_documents:
        logger.error("Yeni dokuman bulunamadi!")
        return
    
    logger.info(f"\nToplam {len(new_documents)} yeni dokuman yuklendi")
    
    # RAG servisini yukle ve yeni dokumanlari ekle
    try:
        from rag_service_improved import ImprovedRAGService
        import faiss
        
        rag_data_path = backend_path / "data" / "rag"
        
        logger.info("\nRAG servisi yukleniyor...")
        rag_service = ImprovedRAGService(rag_data_path)
        
        current_vectors = rag_service.faiss_index.ntotal
        logger.info(f"Mevcut vektor sayisi: {current_vectors}")
        
        # Yeni dokumanlari indeksle
        logger.info(f"\n{len(new_documents)} yeni dokuman indeksleniyor...")
        rag_service.index_documents(new_documents)
        
        new_total = rag_service.faiss_index.ntotal
        logger.info(f"Yeni toplam vektor sayisi: {new_total}")
        logger.info(f"Eklenen vektor: {new_total - current_vectors}")
        
        # Kaydet
        faiss_path = rag_data_path / "index_labse.faiss"
        metadata_path = rag_data_path / "metadata_labse.pkl"
        
        faiss.write_index(rag_service.faiss_index, str(faiss_path))
        
        with open(metadata_path, 'wb') as f:
            pickle.dump({
                'documents': rag_service.documents,
                'metadata': rag_service.metadata
            }, f)
        
        logger.info(f"\nIndeks kaydedildi:")
        logger.info(f"  FAISS: {faiss_path}")
        logger.info(f"  Metadata: {metadata_path}")
        logger.info(f"  Toplam vektor: {new_total}")
        
        # Test
        logger.info("\n" + "="*60)
        logger.info("HIZLI TEST")
        logger.info("="*60)
        
        test_queries = [
            "akademik takvim 2024-2025",
            "final sinavlari ne zaman",
            "harc ucreti",
            "DD notu",
            "staj kac gun"
        ]
        
        for query in test_queries:
            results = rag_service.hybrid_search(query, top_k=3)
            if results:
                top_source = Path(results[0]['metadata'].get('source', 'unknown')).name
                score = results[0].get('score', 0)
                logger.info(f"  '{query}' -> {top_source} (skor: {score:.3f})")
            else:
                logger.info(f"  '{query}' -> Sonuc yok")
        
        logger.info("\n" + "="*60)
        logger.info("GUNCELLEME TAMAMLANDI!")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"Hata: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
