"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  DOSYA: response_validator.py                                                  ║
║  AMAÇ: LLM cevap doğrulama ve kalite kontrolü                                 ║
║  KULLANIM: Halüsinasyon tespiti, kaynak kontrolü, cevap zenginleştirme        ║
╚════════════════════════════════════════════════════════════════════════════════╝

AÇIKLAMA:
─────────
Bu modül, LLM'in ürettiği cevapları doğrular ve kalitesini kontrol eder.
Hatalı veya eksik cevaplar düzeltilir veya reddedilir.

DOĞRULAMA KRİTERLERİ:
1. Halüsinasyon kontrolü (context'te olmayan bilgi)
2. Kaynak/citation kontrolü (her iddia kaynaklı olmalı)
3. Uzunluk/detay kontrolü (çok kısa cevaplar reddedilir)
4. Doğruluk kontrolü (context ile tutarlılık)
5. Format kontrolü (liste, tarih vb.)
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class DogrulamaSonucu:
    """
    Cevap doğrulama sonucu.
    
    Attributes:
        gecerli: Cevap geçerli mi?
        skor: Doğruluk skoru (0.0 - 1.0)
        cevap: İşlenmiş cevap (düzeltilmiş veya orijinal)
        uyarilar: Tespit edilen uyarılar
        haluninasyonlar: Tespit edilen halüsinasyonlar
        eklenen_kaynaklar: Otomatik eklenen kaynaklar
    """
    gecerli: bool
    skor: float
    cevap: str
    uyarilar: List[str] = field(default_factory=list)
    haluninasyonlar: List[str] = field(default_factory=list)
    eklenen_kaynaklar: List[str] = field(default_factory=list)
    
    def __str__(self) -> str:
        durum = "✅ GEÇERLİ" if self.gecerli else "❌ GEÇERSİZ"
        return f"{durum} (skor: {self.skor:.2f}, uyarı: {len(self.uyarilar)}, halüsinasyon: {len(self.haluninasyonlar)})"


@dataclass
class DogrulayiciAyarlar:
    """
    Cevap doğrulayıcı ayarları.
    
    Attributes:
        min_cevap_uzunluk: Minimum cevap uzunluğu
        min_dogruluk_skor: Minimum doğruluk skoru
        kaynak_zorunlu: Kaynak gösterimi zorunlu mu?
        oto_kaynak_ekle: Otomatik kaynak eklensin mi?
        halusinsyon_esik: Halüsinasyon tespit eşiği
    """
    min_cevap_uzunluk: int = 50
    min_dogruluk_skor: float = 0.8
    kaynak_zorunlu: bool = True
    oto_kaynak_ekle: bool = True
    halusinsyon_esik: float = 0.3
    max_halusinsyon_oran: float = 0.2


class CevapDogrulayici:
    """
    LLM cevap doğrulayıcı.
    
    Bu sınıf, LLM'in ürettiği cevapları context ile karşılaştırarak
    doğrular ve gerekirse düzeltir.
    
    Kullanım:
        dogrulayici = CevapDogrulayici()
        sonuc = dogrulayici.dogrula(cevap, context, sorgu)
        if sonuc.gecerli:
            return sonuc.cevap
    """
    
    # Halüsinasyon işaretleri (bu ifadeler context'te yoksa dikkat)
    HALUSINSYON_ISARETLERI = [
        r'(\d{4})\s*yılında',                    # Tarih iddiası
        r'(\d+)\s*(kişi|öğrenci|akademisyen)',   # Sayısal iddia
        r'(profesör|doçent|dr\.)\s+([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)',  # İsim iddiası
        r'(telefon|fax|e-posta):\s*([^\n]+)',    # İletişim bilgisi
        r'(adres|konum):\s*([^\n]+)',            # Adres iddiası
    ]
    
    # Kaynak kalıpları
    KAYNAK_KALIPLARI = [
        r'\[Kaynak[:\s]*([^\]]+)\]',
        r'\(Kaynak[:\s]*([^\)]+)\)',
        r'Kaynak:\s*(.+?)(?:\n|$)',
        r'\[(\d+)\]',  # Numaralı referans
    ]
    
    # Belirsizlik ifadeleri (bu ifadeler halüsinasyon riskini azaltır)
    BELIRSIZLIK_IFADELERI = [
        "muhtemelen", "olabilir", "tahminen", "yaklaşık",
        "belki", "sanırım", "görünüyor", "anlaşılan",
        "kesin değil", "bilgim yok", "bulamadım",
    ]
    
    def __init__(self, ayarlar: Optional[DogrulayiciAyarlar] = None):
        """
        Doğrulayıcıyı başlat.
        
        Args:
            ayarlar: Doğrulayıcı ayarları
        """
        self.ayarlar = ayarlar or DogrulayiciAyarlar()
        self._halusinsyon_regex = [re.compile(p, re.IGNORECASE) for p in self.HALUSINSYON_ISARETLERI]
        self._kaynak_regex = [re.compile(p, re.IGNORECASE) for p in self.KAYNAK_KALIPLARI]
        
        logger.info("🔍 Cevap doğrulayıcı başlatıldı")
    
    def dogrula(
        self,
        cevap: str,
        contextler: List[Dict[str, Any]],
        sorgu: str = "",
    ) -> DogrulamaSonucu:
        """
        LLM cevabını doğrula.
        
        Args:
            cevap: LLM'in ürettiği cevap
            contextler: Kullanılan context listesi
            sorgu: Orijinal kullanıcı sorgusu
        
        Returns:
            DogrulamaSonucu: Doğrulama sonucu
        """
        uyarilar = []
        haluninasyonlar = []
        eklenen_kaynaklar = []
        
        # Context metinlerini birleştir
        context_metni = "\n".join([
            ctx.get("content") or ctx.get("text", "")
            for ctx in contextler
        ])
        
        # 1. Uzunluk kontrolü
        if len(cevap.strip()) < self.ayarlar.min_cevap_uzunluk:
            uyarilar.append(f"Cevap çok kısa: {len(cevap)} karakter")
            # Çok kısa cevapları reddet
            if len(cevap.strip()) < 20:
                return DogrulamaSonucu(
                    gecerli=False,
                    skor=0.0,
                    cevap="Bu konuda yeterli bilgim yok, lütfen başka bir soru sorun.",
                    uyarilar=["Cevap yetersiz uzunlukta"],
                )
        
        # 2. Halüsinasyon kontrolü
        haluninasyonlar = self._halusinsyon_kontrol(cevap, context_metni)
        halusinsyon_orani = len(haluninasyonlar) / max(len(cevap.split('.')), 1)
        
        if halusinsyon_orani > self.ayarlar.max_halusinsyon_oran:
            uyarilar.append(f"Yüksek halüsinasyon oranı: {halusinsyon_orani:.2%}")
            
            # Çok fazla halüsinasyon varsa reddet
            if halusinsyon_orani > 0.5:
                return DogrulamaSonucu(
                    gecerli=False,
                    skor=0.2,
                    cevap="Üzgünüm, bu konuda kesin bilgi veremiyorum.",
                    uyarilar=uyarilar,
                    haluninasyonlar=haluninasyonlar,
                )
        
        # 3. Kaynak kontrolü
        mevcut_kaynaklar = self._kaynak_bul(cevap)
        
        if not mevcut_kaynaklar and self.ayarlar.kaynak_zorunlu:
            uyarilar.append("Kaynak gösterimi eksik")
            
            # Otomatik kaynak ekle
            if self.ayarlar.oto_kaynak_ekle and contextler:
                cevap, eklenen_kaynaklar = self._kaynak_ekle(cevap, contextler)
        
        # 4. Doğruluk skoru hesapla
        dogruluk_skoru = self._dogruluk_skoru_hesapla(cevap, context_metni)
        
        if dogruluk_skoru < self.ayarlar.min_dogruluk_skor:
            uyarilar.append(f"Düşük doğruluk skoru: {dogruluk_skoru:.2f}")
            
            # Çok düşük doğruluk varsa reddet
            if dogruluk_skoru < 0.5:
                return DogrulamaSonucu(
                    gecerli=False,
                    skor=dogruluk_skoru,
                    cevap="Bu konuda yeterli bilgim yok, lütfen başka bir soru sorun.",
                    uyarilar=uyarilar,
                    haluninasyonlar=haluninasyonlar,
                )
        
        # 5. Format düzeltmeleri
        cevap = self._format_duzelt(cevap)
        
        # Toplam skor hesapla
        toplam_skor = self._toplam_skor_hesapla(
            dogruluk_skoru=dogruluk_skoru,
            halusinsyon_orani=halusinsyon_orani,
            kaynak_var=bool(mevcut_kaynaklar or eklenen_kaynaklar),
            uzunluk=len(cevap),
        )
        
        gecerli = toplam_skor >= 0.6 and halusinsyon_orani <= self.ayarlar.max_halusinsyon_oran
        
        return DogrulamaSonucu(
            gecerli=gecerli,
            skor=toplam_skor,
            cevap=cevap,
            uyarilar=uyarilar,
            haluninasyonlar=haluninasyonlar,
            eklenen_kaynaklar=eklenen_kaynaklar,
        )
    
    def _halusinsyon_kontrol(self, cevap: str, context: str) -> List[str]:
        """Halüsinasyon tespiti yap."""
        haluninasyonlar = []
        context_kucuk = context.lower()
        
        for regex in self._halusinsyon_regex:
            eslesme = regex.search(cevap)
            if eslesme:
                iddia = eslesme.group(0)
                
                # Context'te bu bilgi var mı kontrol et
                iddia_kucuk = iddia.lower()
                
                # Tam eşleşme ara
                if iddia_kucuk not in context_kucuk:
                    # Benzerlik kontrolü
                    benzerlik = self._en_yuksek_benzerlik(iddia, context)
                    
                    if benzerlik < self.ayarlar.halusinsyon_esik:
                        haluninasyonlar.append(iddia)
        
        # Sayısal iddiaları kontrol et
        sayilar_cevapta = re.findall(r'\b(\d{2,})\b', cevap)
        sayilar_contextte = re.findall(r'\b(\d{2,})\b', context)
        
        for sayi in sayilar_cevapta:
            if sayi not in sayilar_contextte:
                # Bu sayı context'te yok, halüsinasyon olabilir
                haluninasyonlar.append(f"Sayı: {sayi}")
        
        return haluninasyonlar
    
    def _en_yuksek_benzerlik(self, metin: str, context: str) -> float:
        """Metin ile context arasındaki en yüksek benzerliği bul."""
        metin = metin.lower()
        context = context.lower()
        
        # Kayan pencere ile benzerlik ara
        metin_uzunluk = len(metin)
        en_yuksek = 0.0
        
        for i in range(0, len(context) - metin_uzunluk, metin_uzunluk // 2):
            pencere = context[i:i + metin_uzunluk * 2]
            benzerlik = SequenceMatcher(None, metin, pencere).ratio()
            en_yuksek = max(en_yuksek, benzerlik)
        
        return en_yuksek
    
    def _kaynak_bul(self, cevap: str) -> List[str]:
        """Cevapta mevcut kaynakları bul."""
        kaynaklar = []
        
        for regex in self._kaynak_regex:
            eslesmeler = regex.findall(cevap)
            kaynaklar.extend(eslesmeler)
        
        return kaynaklar
    
    def _kaynak_ekle(
        self,
        cevap: str,
        contextler: List[Dict[str, Any]],
    ) -> Tuple[str, List[str]]:
        """Cevaba otomatik kaynak ekle."""
        eklenen = []
        
        # Context kaynaklarını çıkar
        kaynaklar = []
        for ctx in contextler:
            metadata = ctx.get("metadata", {})
            kaynak = metadata.get("source", "")
            if kaynak:
                # Dosya adını al
                from pathlib import Path
                kaynak_adi = Path(kaynak).stem
                kaynaklar.append(kaynak_adi)
        
        if not kaynaklar:
            return cevap, eklenen
        
        # Benzersiz kaynaklar
        benzersiz_kaynaklar = list(dict.fromkeys(kaynaklar))[:3]
        
        # Cevabın sonuna kaynak ekle
        kaynak_metni = "\n\n---\n📚 **Kaynaklar:**\n"
        for i, kaynak in enumerate(benzersiz_kaynaklar, 1):
            kaynak_metni += f"- [{i}] {kaynak}\n"
            eklenen.append(kaynak)
        
        cevap = cevap.rstrip() + kaynak_metni
        
        return cevap, eklenen
    
    def _dogruluk_skoru_hesapla(self, cevap: str, context: str) -> float:
        """Cevap-context doğruluk skoru hesapla."""
        cevap_kelimeler = set(self._onemli_kelimeler(cevap))
        context_kelimeler = set(self._onemli_kelimeler(context))
        
        if not cevap_kelimeler:
            return 0.5
        
        # Cevaptaki kelimelerin context'te bulunma oranı
        bulunan = len(cevap_kelimeler & context_kelimeler)
        oran = bulunan / len(cevap_kelimeler)
        
        # Belirsizlik ifadeleri varsa toleranslı ol
        belirsiz = any(ifade in cevap.lower() for ifade in self.BELIRSIZLIK_IFADELERI)
        if belirsiz:
            oran = min(oran + 0.2, 1.0)
        
        return oran
    
    def _onemli_kelimeler(self, metin: str) -> List[str]:
        """Metinden önemli kelimeleri çıkar."""
        # Stop words
        stop_words = {
            "ve", "veya", "ile", "için", "bu", "bir", "de", "da", "mi", "mı",
            "ne", "nasıl", "nerede", "neden", "kim", "hangi", "kaç", "var",
            "olan", "olarak", "gibi", "daha", "çok", "en", "ise", "olup",
            "the", "a", "an", "is", "are", "was", "were", "be", "been",
        }
        
        kelimeler = re.findall(r'\b\w{3,}\b', metin.lower())
        return [k for k in kelimeler if k not in stop_words]
    
    def _format_duzelt(self, cevap: str) -> str:
        """Cevap formatını düzelt."""
        # Fazla boşlukları temizle
        cevap = re.sub(r'\n{3,}', '\n\n', cevap)
        cevap = re.sub(r' {2,}', ' ', cevap)
        
        # Başta/sonda boşluk
        cevap = cevap.strip()
        
        return cevap
    
    def _toplam_skor_hesapla(
        self,
        dogruluk_skoru: float,
        halusinsyon_orani: float,
        kaynak_var: bool,
        uzunluk: int,
    ) -> float:
        """Toplam kalite skoru hesapla."""
        # Uzunluk skoru (ideal: 100-500 karakter)
        if 100 <= uzunluk <= 500:
            uzunluk_skor = 1.0
        elif uzunluk < 100:
            uzunluk_skor = uzunluk / 100
        else:
            uzunluk_skor = max(0.5, 1 - (uzunluk - 500) / 1000)
        
        # Halüsinasyon skoru (düşük oran = yüksek skor)
        halusinsyon_skor = max(0, 1 - halusinsyon_orani * 2)
        
        # Kaynak skoru
        kaynak_skor = 1.0 if kaynak_var else 0.7
        
        # Ağırlıklı ortalama
        toplam = (
            dogruluk_skoru * 0.4 +
            halusinsyon_skor * 0.3 +
            kaynak_skor * 0.2 +
            uzunluk_skor * 0.1
        )
        
        return min(max(toplam, 0.0), 1.0)


def halusinasyon_kontrol(
    cevap: str,
    contextler: List[Dict[str, Any]],
) -> Tuple[bool, List[str]]:
    """
    Cevaptaki halüsinasyonları tespit et.
    
    Args:
        cevap: LLM cevabı
        contextler: Kullanılan context'ler
    
    Returns:
        (halusinasyon_var_mi, halusinasyon_listesi)
    """
    dogrulayici = CevapDogrulayici()
    context_metni = "\n".join([
        ctx.get("content") or ctx.get("text", "")
        for ctx in contextler
    ])
    
    haluninasyonlar = dogrulayici._halusinsyon_kontrol(cevap, context_metni)
    
    return len(haluninasyonlar) > 0, haluninasyonlar


def kaynak_ekle(
    cevap: str,
    contextler: List[Dict[str, Any]],
) -> str:
    """
    Cevaba otomatik kaynak ekle.
    
    Args:
        cevap: LLM cevabı
        contextler: Kullanılan context'ler
    
    Returns:
        Kaynak eklenmiş cevap
    """
    dogrulayici = CevapDogrulayici()
    yeni_cevap, _ = dogrulayici._kaynak_ekle(cevap, contextler)
    return yeni_cevap
