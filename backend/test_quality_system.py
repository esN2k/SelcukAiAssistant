#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  DOSYA: test_quality_system.py                                                 ║
║  AMAÇ: Kalite sistemini test eden standalone script                            ║
║  KULLANIM: python test_quality_system.py                                       ║
╚════════════════════════════════════════════════════════════════════════════════╝

AÇIKLAMA:
─────────
Bu script, RAG sisteminin kalite modüllerini bağımsız olarak test eder.
Backend başlatmadan önce sistemin çalıştığından emin olmak için kullanılır.
"""

import sys
from pathlib import Path

# Backend dizinini path'e ekle
sys.path.insert(0, str(Path(__file__).parent))

import logging

# Logging ayarla
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Ana test fonksiyonu"""
    
    print("="*60)
    print("🧪 KALİTE SİSTEMİ TESTİ")
    print("="*60)
    
    # 1. RAG sistemini yükle
    print("\n📂 RAG sistemi yükleniyor...")
    try:
        from rag_service_improved import ImprovedRAGService
        from rag_guard_improved import ImprovedRAGGuard
        
        rag_data_path = Path("data/rag")
        faiss_path = rag_data_path / "index_labse.faiss"
        metadata_path = rag_data_path / "metadata_labse.pkl"
        
        if not faiss_path.exists() or not metadata_path.exists():
            print(f"❌ RAG indeks dosyaları bulunamadı!")
            print(f"   Beklenen: {faiss_path}")
            print(f"   Beklenen: {metadata_path}")
            print("\n💡 Önce scraping ve indexing yapmanız gerekiyor.")
            return 1
        
        rag = ImprovedRAGService(rag_data_path)
        
        # Manuel yükleme
        import faiss
        import pickle
        from rank_bm25 import BM25Okapi
        
        rag.faiss_index = faiss.read_index(str(faiss_path))
        
        with open(metadata_path, 'rb') as f:
            data = pickle.load(f)
            rag.documents = data['documents']
            rag.metadata = data['metadata']
        
        tokenized_docs = [doc.lower().split() for doc in rag.documents]
        rag.bm25 = BM25Okapi(tokenized_docs)
        
        print(f"✅ {rag.faiss_index.ntotal} vektör yüklendi")
        
    except Exception as e:
        print(f"❌ RAG sistemi yüklenemedi: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # 2. Guard yükle
    print("\n🛡️ Guard yükleniyor...")
    try:
        guard = ImprovedRAGGuard()
        print("✅ Guard hazır")
    except Exception as e:
        print(f"❌ Guard yüklenemedi: {e}")
        return 1
    
    # 3. Kalite pipeline'ı test et
    print("\n🎯 Kalite pipeline test ediliyor...")
    try:
        from quality.entegrasyon import KaliteliRAGPipeline
        pipeline = KaliteliRAGPipeline()
        print("✅ Kalite pipeline hazır")
    except Exception as e:
        print(f"❌ Kalite pipeline yüklenemedi: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # 4. Test fonksiyonu
    def test_query(sorgu: str) -> str:
        try:
            contexts = rag.hybrid_search(sorgu, top_k=5)
            validated = guard.validate_and_rerank(sorgu, contexts)
            
            if not validated:
                return "Bu konuda bilgim yok."
            
            cevap = f"Bulunan bilgiler:\n"
            for i, ctx in enumerate(validated[:3], 1):
                cevap += f"{i}. {ctx['content'][:200]}...\n"
                cevap += f"   [Kaynak: {ctx.get('metadata', {}).get('source', 'Bilinmiyor')}]\n"
            
            return cevap
        except Exception as e:
            return f"Hata: {e}"
    
    # 5. Testleri çalıştır
    print("\n🧪 Kalite testleri başlatılıyor...\n")
    try:
        from quality.quality_tester import KaliteTesti
        
        tester = KaliteTesti(test_query)
        rapor = tester.testleri_calistir()
        
        # Sonuçları göster
        print("\n" + "="*60)
        print("📊 TEST SONUÇLARI")
        print("="*60)
        print(rapor.ozet())
        print("="*60)
        
        # Başarısız testleri listele
        basarisizlar = tester.basarisiz_testleri_getir(rapor)
        if basarisizlar:
            print("\n❌ BAŞARISIZ TESTLER:")
            print("-"*40)
            for sonuc in basarisizlar[:5]:  # İlk 5 tanesini göster
                print(f"  • [{sonuc.test_id}] {sonuc.sorgu[:50]}...")
                if sonuc.detaylar.get('eksik_kelimeler'):
                    print(f"    Eksik kelimeler: {sonuc.detaylar['eksik_kelimeler']}")
            print()
        
        # Kategori bazlı analiz
        print("\n📈 KATEGORİ BAZLI ANALİZ:")
        print("-"*40)
        kategori_analiz = tester.kategori_bazli_analiz(rapor)
        for kategori, istat in kategori_analiz.items():
            basari = istat['basari_orani'] * 100
            emoji = "✅" if basari >= 80 else "⚠️" if basari >= 60 else "❌"
            print(f"  {emoji} {kategori}: {istat['basarili']}/{istat['toplam']} (%{basari:.0f})")
        
        print("="*60)
        
        # Başarı kontrolü
        if rapor.basari_orani >= 0.95:
            print("\n✅ HEDEF BAŞARILDI! (%95+ başarı)")
            return 0
        elif rapor.basari_orani >= 0.80:
            print(f"\n⚠️ Hedefe yakın: %{rapor.basari_orani*100:.1f} (hedef: %95)")
            return 0
        else:
            print(f"\n❌ Hedef başarılamadı: %{rapor.basari_orani*100:.1f}")
            return 1
            
    except Exception as e:
        print(f"❌ Test hatası: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
