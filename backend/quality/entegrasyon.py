"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  DOSYA: entegrasyon.py                                                         ║
║  AMAÇ: Kalite modüllerini mevcut RAG sistemine entegre etme                   ║
║  KULLANIM: RAG pipeline'ına kalite kontrollerini eklemek için                 ║
╚════════════════════════════════════════════════════════════════════════════════╝

AÇIKLAMA:
─────────
Bu modül, tüm kalite kontrol modüllerini birleştirerek mevcut RAG sistemine
entegre edilebilir tek bir arayüz sağlar.

ENTEGRASYON ADIMLARI:
1. Doküman yükleme sırasında kalite kontrolü
2. Chunk oluşturma sırasında optimizasyon
3. Retrieval sonrasında kalite kapısı
4. LLM cevabı sonrasında doğrulama
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

from quality.document_validator import (
    DokumanKaliteDogrulayici,
    DokumanKaliteAyarlari,
    kalite_filtresi_uygula,
)
from quality.chunk_optimizer import (
    ChunkOptimizer,
    ChunkOptimizerAyarlar,
    OptimizeEdilmisChunk,
)
from quality.retrieval_quality_gate import (
    RetrievalKaliteKapisi,
    KaliteKapisiAyarlar,
    dusuk_kaliteli_contextleri_filtrele,
)
from quality.response_validator import (
    CevapDogrulayici,
    DogrulayiciAyarlar,
    DogrulamaSonucu,
)
from quality.prompts_kalite import (
    sistem_promptu_olustur,
    kullanici_sorusu_sablonu,
    context_zenginlestir,
    hata_mesaji_olustur,
)

logger = logging.getLogger(__name__)


@dataclass
class KaliteAyarlari:
    """
    Tüm kalite modülleri için birleşik ayarlar.
    
    Attributes:
        dokuman_ayarlari: Doküman kalite ayarları
        chunk_ayarlari: Chunk optimizer ayarları
        retrieval_ayarlari: Retrieval kalite kapısı ayarları
        dogrulayici_ayarlari: Cevap doğrulayıcı ayarları
        dil: Varsayılan dil
        strict_mod: Strict mod aktif mi?
    """
    dokuman_ayarlari: DokumanKaliteAyarlari = field(default_factory=DokumanKaliteAyarlari)
    chunk_ayarlari: ChunkOptimizerAyarlar = field(default_factory=ChunkOptimizerAyarlar)
    retrieval_ayarlari: KaliteKapisiAyarlar = field(default_factory=KaliteKapisiAyarlar)
    dogrulayici_ayarlari: DogrulayiciAyarlar = field(default_factory=DogrulayiciAyarlar)
    dil: str = "tr"
    strict_mod: bool = True


@dataclass
class KaliteliRAGSonucu:
    """
    Kalite kontrollü RAG sonucu.
    
    Attributes:
        cevap: LLM cevabı
        contextler: Kullanılan context'ler
        kaynaklar: Kaynak listesi
        kalite_skoru: Toplam kalite skoru
        dogrulama_sonucu: Cevap doğrulama sonucu
        istatistikler: İşlem istatistikleri
    """
    cevap: str
    contextler: List[Dict[str, Any]] = field(default_factory=list)
    kaynaklar: List[str] = field(default_factory=list)
    kalite_skoru: float = 0.0
    dogrulama_sonucu: Optional[DogrulamaSonucu] = None
    istatistikler: Dict[str, Any] = field(default_factory=dict)


class KaliteliRAGPipeline:
    """
    Kalite kontrollü RAG pipeline.
    
    Bu sınıf, tüm kalite modüllerini birleştirerek end-to-end
    kalite kontrollü RAG işlemi sağlar.
    
    Kullanım:
        pipeline = KaliteliRAGPipeline()
        sonuc = pipeline.sorgula("Sınav tarihleri nedir?", contextler)
    """
    
    def __init__(self, ayarlar: Optional[KaliteAyarlari] = None):
        """
        Pipeline'ı başlat.
        
        Args:
            ayarlar: Kalite ayarları
        """
        self.ayarlar = ayarlar or KaliteAyarlari()
        
        # Alt modülleri başlat
        self._dokuman_dogrulayici = DokumanKaliteDogrulayici(self.ayarlar.dokuman_ayarlari)
        self._chunk_optimizer = ChunkOptimizer(self.ayarlar.chunk_ayarlari)
        self._retrieval_kapisi = RetrievalKaliteKapisi(self.ayarlar.retrieval_ayarlari)
        self._cevap_dogrulayici = CevapDogrulayici(self.ayarlar.dogrulayici_ayarlari)
        
        logger.info("✅ KaliteliRAGPipeline başlatıldı")
    
    def dokumanlari_isle(
        self,
        dokumanlar: List[Dict[str, Any]],
    ) -> Tuple[List[OptimizeEdilmisChunk], Dict[str, Any]]:
        """
        Dokümanları kalite kontrolü ile işle.
        
        Args:
            dokumanlar: Ham doküman listesi
        
        Returns:
            (optimize_edilmis_chunklar, istatistikler)
        """
        istatistikler = {
            "toplam_dokuman": len(dokumanlar),
            "kabul_edilen": 0,
            "reddedilen": 0,
            "toplam_chunk": 0,
        }
        
        # 1. Kalite filtresi uygula
        kaliteli_dokumanlar = kalite_filtresi_uygula(
            dokumanlar,
            self.ayarlar.dokuman_ayarlari,
        )
        
        istatistikler["kabul_edilen"] = len(kaliteli_dokumanlar)
        istatistikler["reddedilen"] = len(dokumanlar) - len(kaliteli_dokumanlar)
        
        # 2. Chunk optimization
        tum_chunklar = self._chunk_optimizer.toplu_optimize(kaliteli_dokumanlar)
        istatistikler["toplam_chunk"] = len(tum_chunklar)
        
        logger.info(
            "📦 Doküman işleme tamamlandı: %d/%d doküman → %d chunk",
            len(kaliteli_dokumanlar),
            len(dokumanlar),
            len(tum_chunklar),
        )
        
        return tum_chunklar, istatistikler
    
    def contextleri_filtrele(
        self,
        sorgu: str,
        contextler: List[Dict[str, Any]],
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Context'leri kalite kapısından geçir.
        
        Args:
            sorgu: Kullanıcı sorgusu
            contextler: Ham context listesi
        
        Returns:
            (filtrelenmis_contextler, istatistikler)
        """
        istatistikler = {
            "toplam_context": len(contextler),
            "gecen_context": 0,
            "ortalama_skor": 0.0,
        }
        
        # Kalite kapısından geçir
        kaliteli = self._retrieval_kapisi.filtrele(sorgu, contextler)
        
        istatistikler["gecen_context"] = len(kaliteli)
        if kaliteli:
            istatistikler["ortalama_skor"] = sum(c.toplam_skor for c in kaliteli) / len(kaliteli)
        
        # Sözlük formatına dönüştür
        filtrelenmis = [c.to_dict() for c in kaliteli]
        
        return filtrelenmis, istatistikler
    
    def sistem_promptu_olustur(
        self,
        context: str = "",
        kaynaklar: Optional[List[str]] = None,
    ) -> str:
        """
        Gelişmiş sistem promptu oluştur.
        
        Args:
            context: RAG context'i
            kaynaklar: Kaynak listesi
        
        Returns:
            Sistem promptu
        """
        return sistem_promptu_olustur(
            dil=self.ayarlar.dil,
            context=context,
            kaynaklar=kaynaklar,
            strict_mod=self.ayarlar.strict_mod,
        )
    
    def kullanici_promptu_olustur(
        self,
        sorgu: str,
        contextler: List[Dict[str, Any]],
    ) -> str:
        """
        Kullanıcı promptu oluştur.
        
        Args:
            sorgu: Kullanıcı sorgusu
            contextler: Filtrelenmiş context'ler
        
        Returns:
            Kullanıcı promptu
        """
        # Context'leri zenginleştir
        zengin_context = context_zenginlestir(contextler, self.ayarlar.dil)
        
        return kullanici_sorusu_sablonu(
            soru=sorgu,
            context=zengin_context,
            dil=self.ayarlar.dil,
        )
    
    def cevabi_dogrula(
        self,
        cevap: str,
        contextler: List[Dict[str, Any]],
        sorgu: str = "",
    ) -> DogrulamaSonucu:
        """
        LLM cevabını doğrula.
        
        Args:
            cevap: LLM cevabı
            contextler: Kullanılan context'ler
            sorgu: Orijinal sorgu
        
        Returns:
            DogrulamaSonucu
        """
        return self._cevap_dogrulayici.dogrula(cevap, contextler, sorgu)
    
    def sorgula(
        self,
        sorgu: str,
        contextler: List[Dict[str, Any]],
        llm_fonksiyonu: Callable[[str, str], str],
    ) -> KaliteliRAGSonucu:
        """
        Kalite kontrollü tam RAG sorgusu.
        
        Args:
            sorgu: Kullanıcı sorgusu
            contextler: Ham context listesi
            llm_fonksiyonu: LLM çağrı fonksiyonu (sistem_prompt, kullanici_prompt) -> cevap
        
        Returns:
            KaliteliRAGSonucu
        """
        istatistikler = {}
        
        # 1. Context'leri filtrele
        filtrelenmis, ctx_istat = self.contextleri_filtrele(sorgu, contextler)
        istatistikler["retrieval"] = ctx_istat
        
        # Context yoksa hata mesajı döndür
        if not filtrelenmis:
            return KaliteliRAGSonucu(
                cevap=hata_mesaji_olustur("kaynak_yok", self.ayarlar.dil),
                contextler=[],
                kaynaklar=[],
                kalite_skoru=0.0,
                istatistikler=istatistikler,
            )
        
        # 2. Kaynakları çıkar
        kaynaklar = []
        for ctx in filtrelenmis:
            kaynak = ctx.get("metadata", {}).get("source", "")
            if kaynak:
                from pathlib import Path
                kaynaklar.append(Path(kaynak).stem)
        kaynaklar = list(dict.fromkeys(kaynaklar))  # Benzersiz
        
        # 3. Promptları oluştur
        zengin_context = context_zenginlestir(filtrelenmis, self.ayarlar.dil)
        sistem_prompt = self.sistem_promptu_olustur(zengin_context, kaynaklar)
        kullanici_prompt = kullanici_sorusu_sablonu(sorgu, zengin_context, self.ayarlar.dil)
        
        # 4. LLM'i çağır
        try:
            cevap = llm_fonksiyonu(sistem_prompt, kullanici_prompt)
        except Exception as e:
            logger.error("LLM hatası: %s", e)
            return KaliteliRAGSonucu(
                cevap=hata_mesaji_olustur("bilgi_yok", self.ayarlar.dil),
                contextler=filtrelenmis,
                kaynaklar=kaynaklar,
                kalite_skoru=0.0,
                istatistikler=istatistikler,
            )
        
        # 5. Cevabı doğrula
        dogrulama = self.cevabi_dogrula(cevap, filtrelenmis, sorgu)
        istatistikler["dogrulama"] = {
            "gecerli": dogrulama.gecerli,
            "skor": dogrulama.skor,
            "uyari_sayisi": len(dogrulama.uyarilar),
            "halusinsyon_sayisi": len(dogrulama.haluninasyonlar),
        }
        
        # Geçersiz cevap ise düzeltilmiş versiyonu kullan
        final_cevap = dogrulama.cevap
        
        return KaliteliRAGSonucu(
            cevap=final_cevap,
            contextler=filtrelenmis,
            kaynaklar=kaynaklar,
            kalite_skoru=dogrulama.skor,
            dogrulama_sonucu=dogrulama,
            istatistikler=istatistikler,
        )


# ═══════════════════════════════════════════════════════════════════════════════
# YARDIMCI FONKSİYONLAR
# ═══════════════════════════════════════════════════════════════════════════════

def kaliteli_rag_sorgula(
    sorgu: str,
    contextler: List[Dict[str, Any]],
    llm_fonksiyonu: Callable[[str, str], str],
    ayarlar: Optional[KaliteAyarlari] = None,
) -> KaliteliRAGSonucu:
    """
    Hızlı kaliteli RAG sorgusu.
    
    Args:
        sorgu: Kullanıcı sorgusu
        contextler: Context listesi
        llm_fonksiyonu: LLM fonksiyonu
        ayarlar: Kalite ayarları
    
    Returns:
        KaliteliRAGSonucu
    """
    pipeline = KaliteliRAGPipeline(ayarlar)
    return pipeline.sorgula(sorgu, contextler, llm_fonksiyonu)


def context_hazirla(
    contextler: List[Dict[str, Any]],
    sorgu: str,
    dil: str = "tr",
) -> Tuple[str, List[str]]:
    """
    Context'leri LLM için hazırla.
    
    Args:
        contextler: Ham context listesi
        sorgu: Kullanıcı sorgusu
        dil: Dil kodu
    
    Returns:
        (zenginlestirilmis_context, kaynak_listesi)
    """
    # Filtreleme
    ayarlar = KaliteKapisiAyarlar()
    kapi = RetrievalKaliteKapisi(ayarlar)
    kaliteli = kapi.filtrele(sorgu, contextler)
    
    # Sözlüğe dönüştür
    ctx_dict = [c.to_dict() for c in kaliteli]
    
    # Zenginleştir
    zengin = context_zenginlestir(ctx_dict, dil)
    
    # Kaynakları çıkar
    kaynaklar = []
    for c in kaliteli:
        kaynak = c.metadata.get("source", "")
        if kaynak:
            from pathlib import Path
            kaynaklar.append(Path(kaynak).stem)
    
    return zengin, list(dict.fromkeys(kaynaklar))


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "KaliteAyarlari",
    "KaliteliRAGSonucu",
    "KaliteliRAGPipeline",
    "kaliteli_rag_sorgula",
    "context_hazirla",
]
