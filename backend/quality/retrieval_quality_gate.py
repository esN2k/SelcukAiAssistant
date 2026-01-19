"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  DOSYA: retrieval_quality_gate.py                                              ║
║  AMAÇ: Retrieval sonrası kalite kapısı                                        ║
║  KULLANIM: LLM'e sadece yüksek kaliteli context gönder                        ║
╚════════════════════════════════════════════════════════════════════════════════╝

AÇIKLAMA:
─────────
Bu modül, retrieval sonrasında dönen context'leri filtreler.
Düşük kaliteli veya ilgisiz context'ler LLM'e gönderilmez.

FİLTRELEME KRİTERLERİ:
1. Skor kontrolü (min 0.5)
2. Relevance kontrolü (cross-encoder ile, min 0.7)
3. Güncellik kontrolü (2 yıldan eski değil)
4. Uzunluk kontrolü (min 200 karakter)
5. Duplicate kontrolü
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# Cross-encoder kontrolü
CROSS_ENCODER_AVAILABLE = False
try:
    from sentence_transformers import CrossEncoder
    CROSS_ENCODER_AVAILABLE = True
except ImportError:
    logger.warning("⚠️ Cross-encoder mevcut değil, basit relevance kontrolü kullanılacak")


@dataclass
class KaliteliContext:
    """
    Kalite filtresinden geçmiş context.
    
    Attributes:
        content: Context içeriği
        score: Retrieval skoru
        relevance_score: Relevance skoru (cross-encoder)
        metadata: Context metadata'sı
        kalite_notu: Kalite değerlendirme notu
    """
    content: str
    score: float
    relevance_score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    kalite_notu: str = ""
    
    @property
    def toplam_skor(self) -> float:
        """Toplam kalite skoru"""
        return (self.score + self.relevance_score) / 2
    
    def to_dict(self) -> Dict[str, Any]:
        """Sözlüğe dönüştür"""
        return {
            "content": self.content,
            "score": self.score,
            "relevance_score": self.relevance_score,
            "toplam_skor": self.toplam_skor,
            "metadata": self.metadata,
            "kalite_notu": self.kalite_notu,
        }


@dataclass
class KaliteKapisiAyarlar:
    """
    Kalite kapısı ayarları.
    
    Attributes:
        min_skor: Minimum retrieval skoru
        min_relevance: Minimum relevance skoru
        min_uzunluk: Minimum içerik uzunluğu
        max_yas_yil: Maksimum içerik yaşı (yıl)
        duplicate_esik: Duplicate benzerlik eşiği
        max_context: Maksimum döndürülecek context sayısı
    """
    min_skor: float = 0.5
    min_relevance: float = 0.7
    min_uzunluk: int = 200
    max_yas_yil: int = 2
    duplicate_esik: float = 0.9
    max_context: int = 5
    cross_encoder_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class RetrievalKaliteKapisi:
    """
    Retrieval kalite kapısı.
    
    Bu sınıf, retrieval sonuçlarını çok katmanlı kalite kontrolünden geçirir.
    Sadece yüksek kaliteli ve ilgili context'ler LLM'e gönderilir.
    
    Kullanım:
        kapi = RetrievalKaliteKapisi()
        kaliteli_contextler = kapi.filtrele(sorgu, contextler)
    """
    
    # Ay isimleri (tarih çıkarma için)
    AY_ISIMLERI = {
        "ocak": 1, "şubat": 2, "mart": 3, "nisan": 4,
        "mayıs": 5, "haziran": 6, "temmuz": 7, "ağustos": 8,
        "eylül": 9, "ekim": 10, "kasım": 11, "aralık": 12,
    }
    
    def __init__(self, ayarlar: Optional[KaliteKapisiAyarlar] = None):
        """
        Kalite kapısını başlat.
        
        Args:
            ayarlar: Kalite kapısı ayarları
        """
        self.ayarlar = ayarlar or KaliteKapisiAyarlar()
        self._cross_encoder: Optional[Any] = None
        
        # Cross-encoder yükle
        if CROSS_ENCODER_AVAILABLE:
            try:
                self._cross_encoder = CrossEncoder(
                    self.ayarlar.cross_encoder_model,
                    max_length=512,
                )
                logger.info("✅ Cross-encoder yüklendi: %s", self.ayarlar.cross_encoder_model)
            except Exception as e:
                logger.warning("⚠️ Cross-encoder yüklenemedi: %s", e)
        
        logger.info(
            "🚧 Retrieval kalite kapısı başlatıldı (min_skor: %.2f, min_relevance: %.2f)",
            self.ayarlar.min_skor,
            self.ayarlar.min_relevance,
        )
    
    def filtrele(
        self,
        sorgu: str,
        contextler: List[Dict[str, Any]],
    ) -> List[KaliteliContext]:
        """
        Context'leri kalite filtresinden geçir.
        
        Args:
            sorgu: Kullanıcı sorgusu
            contextler: Retrieval sonucu context listesi
        
        Returns:
            Kaliteli context listesi
        """
        if not contextler:
            logger.debug("Boş context listesi")
            return []
        
        filtrelenmis = []
        gorulen_icerikleri: List[str] = []
        
        for ctx in contextler:
            # Context bilgilerini çıkar
            icerik = ctx.get("content") or ctx.get("text", "")
            skor = float(ctx.get("score", 0))
            metadata = ctx.get("metadata", {})
            
            # 1. Skor kontrolü
            if skor < self.ayarlar.min_skor:
                logger.debug("❌ Düşük skor: %.3f < %.3f", skor, self.ayarlar.min_skor)
                continue
            
            # 2. Uzunluk kontrolü
            if len(icerik) < self.ayarlar.min_uzunluk:
                logger.debug("❌ Kısa içerik: %d < %d", len(icerik), self.ayarlar.min_uzunluk)
                continue
            
            # 3. Relevance kontrolü
            relevance_skor = self._relevance_hesapla(sorgu, icerik)
            if relevance_skor < self.ayarlar.min_relevance:
                logger.debug("❌ Düşük relevance: %.3f < %.3f", relevance_skor, self.ayarlar.min_relevance)
                continue
            
            # 4. Güncellik kontrolü
            tarih = self._tarih_cikar(icerik, metadata)
            if tarih:
                yas = (datetime.now() - tarih).days / 365
                if yas > self.ayarlar.max_yas_yil:
                    logger.debug("❌ Eski içerik: %.1f yıl", yas)
                    continue
            
            # 5. Duplicate kontrolü
            if self._duplicate_mi(icerik, gorulen_icerikleri):
                logger.debug("❌ Duplicate içerik")
                continue
            
            gorulen_icerikleri.append(icerik)
            
            # Kalite notu oluştur
            kalite_notu = self._kalite_notu_olustur(skor, relevance_skor, tarih)
            
            kaliteli_ctx = KaliteliContext(
                content=icerik,
                score=skor,
                relevance_score=relevance_skor,
                metadata=metadata,
                kalite_notu=kalite_notu,
            )
            
            filtrelenmis.append(kaliteli_ctx)
        
        # Toplam skora göre sırala
        filtrelenmis.sort(key=lambda x: x.toplam_skor, reverse=True)
        
        # Maksimum context sayısına kırp
        sonuc = filtrelenmis[:self.ayarlar.max_context]
        
        logger.info(
            "🚧 Kalite kapısı: %d/%d context geçti (%.1f%%)",
            len(sonuc),
            len(contextler),
            len(sonuc) / len(contextler) * 100 if contextler else 0,
        )
        
        return sonuc
    
    def context_skorla(
        self,
        sorgu: str,
        context: Dict[str, Any],
    ) -> Tuple[float, str]:
        """
        Tek bir context'i skorla.
        
        Args:
            sorgu: Kullanıcı sorgusu
            context: Context sözlüğü
        
        Returns:
            (toplam_skor, kalite_notu) tuple
        """
        icerik = context.get("content") or context.get("text", "")
        retrieval_skor = float(context.get("score", 0))
        metadata = context.get("metadata", {})
        
        # Relevance skoru
        relevance_skor = self._relevance_hesapla(sorgu, icerik)
        
        # Uzunluk skoru (0.0-1.0)
        uzunluk_skor = min(len(icerik) / 1000, 1.0)
        
        # Tarih skoru
        tarih = self._tarih_cikar(icerik, metadata)
        if tarih:
            yas = (datetime.now() - tarih).days / 365
            tarih_skor = max(0, 1 - yas / 5)  # 5 yılda 0'a düşer
        else:
            tarih_skor = 0.5  # Tarih yoksa orta skor
        
        # Toplam skor (ağırlıklı ortalama)
        toplam_skor = (
            retrieval_skor * 0.3 +
            relevance_skor * 0.4 +
            uzunluk_skor * 0.15 +
            tarih_skor * 0.15
        )
        
        kalite_notu = self._kalite_notu_olustur(retrieval_skor, relevance_skor, tarih)
        
        return toplam_skor, kalite_notu
    
    def _relevance_hesapla(self, sorgu: str, icerik: str) -> float:
        """
        Sorgu-içerik relevance skoru hesapla.
        
        Cross-encoder varsa kullanır, yoksa basit kelime eşleşmesi yapar.
        """
        if self._cross_encoder:
            try:
                skor = self._cross_encoder.predict([[sorgu, icerik]])[0]
                # Normalize et (cross-encoder -10 ile +10 arası verebilir)
                return max(0, min(1, (skor + 10) / 20))
            except Exception as e:
                logger.warning("Cross-encoder hatası: %s", e)
        
        # Basit kelime eşleşmesi (fallback)
        return self._basit_relevance_hesapla(sorgu, icerik)
    
    def _basit_relevance_hesapla(self, sorgu: str, icerik: str) -> float:
        """Basit kelime eşleşmesi tabanlı relevance."""
        sorgu_kelimeler = set(self._tokenize(sorgu.lower()))
        icerik_kelimeler = set(self._tokenize(icerik.lower()))
        
        if not sorgu_kelimeler:
            return 0.0
        
        # Jaccard benzerliği
        kesisim = len(sorgu_kelimeler & icerik_kelimeler)
        birlesim = len(sorgu_kelimeler | icerik_kelimeler)
        
        jaccard = kesisim / birlesim if birlesim > 0 else 0
        
        # Sorgu kelimelerinin içerikte bulunma oranı
        kapsam = kesisim / len(sorgu_kelimeler)
        
        # Ağırlıklı ortalama
        return jaccard * 0.4 + kapsam * 0.6
    
    def _tokenize(self, metin: str) -> List[str]:
        """Metni kelimelere ayır (stop word'leri çıkar)."""
        # Türkçe stop words
        stop_words = {
            "ve", "veya", "ile", "için", "bu", "bir", "de", "da", "mi", "mı",
            "ne", "nasıl", "nerede", "neden", "kim", "hangi", "kaç", "var",
            "olan", "olarak", "gibi", "daha", "çok", "en", "ise", "olup",
        }
        
        kelimeler = re.findall(r'\b\w+\b', metin)
        return [k for k in kelimeler if k not in stop_words and len(k) > 2]
    
    def _tarih_cikar(
        self,
        icerik: str,
        metadata: Dict[str, Any],
    ) -> Optional[datetime]:
        """İçerikten veya metadata'dan tarih çıkar."""
        # Metadata'dan
        for alan in ["date", "tarih", "updated", "created"]:
            if metadata.get(alan):
                try:
                    deger = metadata[alan]
                    if isinstance(deger, datetime):
                        return deger
                    return datetime.fromisoformat(str(deger).replace('Z', '+00:00'))
                except (ValueError, TypeError):
                    pass
        
        # İçerikten
        tarih_regex = [
            r'(\d{4})-(\d{1,2})-(\d{1,2})',
            r'(\d{1,2})[./](\d{1,2})[./](\d{4})',
            r'(\d{4})-(\d{4})\s*(?:akademik|eğitim)',
        ]
        
        icerik_kucuk = icerik.lower()
        
        for pattern in tarih_regex:
            eslesme = re.search(pattern, icerik_kucuk)
            if eslesme:
                try:
                    gruplar = eslesme.groups()
                    sayilar = [int(g) for g in gruplar if g.isdigit()]
                    
                    if len(sayilar) >= 2 and sayilar[0] > 2000 and sayilar[1] > sayilar[0]:
                        # Akademik yıl
                        return datetime(sayilar[1], 9, 1)
                    elif len(sayilar) >= 3:
                        if sayilar[0] > 31:  # YYYY-MM-DD
                            return datetime(sayilar[0], min(sayilar[1], 12), min(sayilar[2], 28))
                        else:  # DD/MM/YYYY
                            return datetime(sayilar[2], min(sayilar[1], 12), min(sayilar[0], 28))
                except (ValueError, IndexError):
                    continue
        
        return None
    
    def _duplicate_mi(self, icerik: str, gorulenler: List[str]) -> bool:
        """İçerik duplicate mi kontrol et."""
        icerik_normalize = re.sub(r'\s+', ' ', icerik.lower().strip())
        
        for gorulen in gorulenler:
            gorulen_normalize = re.sub(r'\s+', ' ', gorulen.lower().strip())
            
            # Basit benzerlik kontrolü
            benzerlik = self._metin_benzerligi(icerik_normalize, gorulen_normalize)
            if benzerlik > self.ayarlar.duplicate_esik:
                return True
        
        return False
    
    def _metin_benzerligi(self, metin1: str, metin2: str) -> float:
        """İki metin arasındaki benzerliği hesapla (Jaccard)."""
        kelimeler1 = set(metin1.split())
        kelimeler2 = set(metin2.split())
        
        kesisim = len(kelimeler1 & kelimeler2)
        birlesim = len(kelimeler1 | kelimeler2)
        
        return kesisim / birlesim if birlesim > 0 else 0
    
    def _kalite_notu_olustur(
        self,
        skor: float,
        relevance: float,
        tarih: Optional[datetime],
    ) -> str:
        """Kalite değerlendirme notu oluştur."""
        notlar = []
        
        if skor >= 0.8:
            notlar.append("Yüksek retrieval skoru")
        elif skor >= 0.6:
            notlar.append("Orta retrieval skoru")
        else:
            notlar.append("Düşük retrieval skoru")
        
        if relevance >= 0.8:
            notlar.append("Çok ilgili")
        elif relevance >= 0.6:
            notlar.append("İlgili")
        else:
            notlar.append("Kısmen ilgili")
        
        if tarih:
            yas = (datetime.now() - tarih).days / 365
            if yas < 1:
                notlar.append("Güncel")
            elif yas < 2:
                notlar.append("Kabul edilebilir tarih")
            else:
                notlar.append(f"{yas:.0f} yıl eski")
        else:
            notlar.append("Tarih bilinmiyor")
        
        return " | ".join(notlar)


def dusuk_kaliteli_contextleri_filtrele(
    sorgu: str,
    contextler: List[Dict[str, Any]],
    ayarlar: Optional[KaliteKapisiAyarlar] = None,
) -> List[Dict[str, Any]]:
    """
    Düşük kaliteli context'leri filtrele.
    
    LLM'e SADECE yüksek kaliteli context ver!
    
    Args:
        sorgu: Kullanıcı sorgusu
        contextler: Retrieval sonucu context listesi
        ayarlar: Kalite kapısı ayarları
    
    Returns:
        Filtrelenmiş context listesi (sözlük formatında)
    """
    kapi = RetrievalKaliteKapisi(ayarlar)
    kaliteli = kapi.filtrele(sorgu, contextler)
    
    return [ctx.to_dict() for ctx in kaliteli]
