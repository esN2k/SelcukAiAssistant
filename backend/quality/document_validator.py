"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  DOSYA: document_validator.py                                                  ║
║  AMAÇ: Doküman kalite doğrulama sistemi                                       ║
║  KULLANIM: Scrape edilen dokümanları indeksleme öncesi doğrula                ║
╚════════════════════════════════════════════════════════════════════════════════╝

AÇIKLAMA:
─────────
Bu modül, RAG sistemine eklenmeden önce dokümanların kalitesini kontrol eder.
Düşük kaliteli dokümanlar (boş, kısa, eski, duplicate) reddedilir.

KALİTE KRİTERLERİ:
1. Minimum karakter sayısı (varsayılan: 100)
2. Anlamlı içerik kontrolü (menü/footer değil)
3. Tarih güncelliği (2 yıldan eski değil)
4. Duplicate kontrolü (hash tabanlı)
5. Hata sayfası tespiti (404, 500)
"""

from __future__ import annotations

import hashlib
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)


class KaliteDurumu(Enum):
    """Doküman kalite durumu"""
    KABUL = "kabul"
    RED = "red"
    UYARI = "uyari"


class RedNedeni(Enum):
    """Doküman red nedenleri"""
    BOS_ICERIK = "bos_icerik"
    COK_KISA = "cok_kisa"
    MENU_FOOTER = "menu_footer"
    HATA_SAYFASI = "hata_sayfasi"
    DUPLICATE = "duplicate"
    ESKI_TARIH = "eski_tarih"
    ANLAMSIZ_ICERIK = "anlamsiz_icerik"
    YAPISAL_SORUN = "yapisal_sorun"


@dataclass
class DokumanKaliteSonucu:
    """
    Doküman kalite doğrulama sonucu.
    
    Attributes:
        durum: Kalite durumu (kabul/red/uyari)
        skor: Kalite skoru (0.0 - 1.0)
        neden: Red nedeni (varsa)
        detay: Detaylı açıklama
        oneriler: İyileştirme önerileri
    """
    durum: KaliteDurumu
    skor: float
    neden: Optional[RedNedeni] = None
    detay: str = ""
    oneriler: List[str] = field(default_factory=list)
    
    @property
    def kabul_edildi(self) -> bool:
        """Doküman kabul edildi mi?"""
        return self.durum == KaliteDurumu.KABUL
    
    def __str__(self) -> str:
        if self.kabul_edildi:
            return f"✅ KABUL (skor: {self.skor:.2f})"
        return f"❌ RED: {self.neden.value if self.neden else 'bilinmiyor'} (skor: {self.skor:.2f})"


@dataclass
class DokumanKaliteAyarlari:
    """
    Kalite doğrulama ayarları.
    
    Attributes:
        min_karakter: Minimum karakter sayısı
        min_kelime: Minimum kelime sayısı
        max_yas_yil: Maksimum yaş (yıl)
        min_paragraf: Minimum paragraf sayısı
        duplicate_kontrol: Duplicate kontrolü aktif mi?
    """
    min_karakter: int = 100
    ideal_min_karakter: int = 500
    min_kelime: int = 20
    max_yas_yil: int = 2
    min_paragraf: int = 1
    duplicate_kontrol: bool = True
    min_baslik_uzunluk: int = 3
    max_menu_oran: float = 0.5


class DokumanKaliteDogrulayici:
    """
    Doküman kalite doğrulayıcı.
    
    Bu sınıf, RAG sistemine eklenecek dokümanların kalitesini
    çok katmanlı kontroller ile doğrular.
    
    Kullanım:
        dogrulayici = DokumanKaliteDogrulayici()
        sonuc = dogrulayici.dogrula(icerik, metadata)
        if sonuc.kabul_edildi:
            # Dokümani indeksle
    """
    
    # Hata sayfası kalıpları
    HATA_KALIPLARI = [
        r"404\s*(not\s*found|bulunamadı|sayfa\s*yok)",
        r"500\s*(internal\s*server|sunucu\s*hatası)",
        r"sayfa\s*(bulunamadı|mevcut\s*değil)",
        r"page\s*not\s*found",
        r"error\s*(404|500|502|503)",
        r"hata\s*oluştu",
        r"erişim\s*reddedildi",
        r"access\s*denied",
    ]
    
    # Menü/footer kalıpları
    MENU_KALIPLARI = [
        r"ana\s*sayfa",
        r"iletişim",
        r"hakkımızda",
        r"gizlilik\s*politikası",
        r"çerez\s*politikası",
        r"copyright\s*©",
        r"tüm\s*hakları\s*saklıdır",
        r"sosyal\s*medya",
        r"facebook|twitter|instagram|linkedin",
        r"site\s*haritası",
        r"menü",
        r"footer",
        r"header",
    ]
    
    # Tarih kalıpları (Türkçe ve İngilizce)
    TARIH_KALIPLARI = [
        r"(\d{1,2})[./\-](\d{1,2})[./\-](\d{4})",  # 01/01/2024, 01-01-2024
        r"(\d{4})[./\-](\d{1,2})[./\-](\d{1,2})",  # 2024-01-01
        r"(\d{1,2})\s+(ocak|şubat|mart|nisan|mayıs|haziran|temmuz|ağustos|eylül|ekim|kasım|aralık)\s+(\d{4})",
        r"(\d{1,2})\s+(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})",
        r"(\d{4})-(\d{4})\s*(akademik|eğitim|öğretim)\s*yılı",  # 2024-2025 akademik yılı
    ]
    
    # Ay isimleri (tarih çıkarma için)
    AY_ISIMLERI = {
        "ocak": 1, "şubat": 2, "mart": 3, "nisan": 4,
        "mayıs": 5, "haziran": 6, "temmuz": 7, "ağustos": 8,
        "eylül": 9, "ekim": 10, "kasım": 11, "aralık": 12,
        "january": 1, "february": 2, "march": 3, "april": 4,
        "may": 5, "june": 6, "july": 7, "august": 8,
        "september": 9, "october": 10, "november": 11, "december": 12,
    }
    
    def __init__(self, ayarlar: Optional[DokumanKaliteAyarlari] = None):
        """
        Doğrulayıcıyı başlat.
        
        Args:
            ayarlar: Kalite doğrulama ayarları
        """
        self.ayarlar = ayarlar or DokumanKaliteAyarlari()
        self._hash_seti: Set[str] = set()
        self._hata_regex = [re.compile(p, re.IGNORECASE) for p in self.HATA_KALIPLARI]
        self._menu_regex = [re.compile(p, re.IGNORECASE) for p in self.MENU_KALIPLARI]
        self._tarih_regex = [re.compile(p, re.IGNORECASE) for p in self.TARIH_KALIPLARI]
        
        logger.info("📋 Doküman kalite doğrulayıcı başlatıldı")
    
    def dogrula(
        self,
        icerik: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> DokumanKaliteSonucu:
        """
        Doküman kalitesini doğrula.
        
        Args:
            icerik: Doküman içeriği
            metadata: Doküman metadata'sı (kaynak, tarih, tip vb.)
        
        Returns:
            DokumanKaliteSonucu: Kalite doğrulama sonucu
        """
        metadata = metadata or {}
        oneriler = []
        
        # 1. Boş içerik kontrolü
        if not icerik or not icerik.strip():
            return DokumanKaliteSonucu(
                durum=KaliteDurumu.RED,
                skor=0.0,
                neden=RedNedeni.BOS_ICERIK,
                detay="Doküman içeriği boş",
            )
        
        temiz_icerik = icerik.strip()
        
        # 2. Minimum karakter kontrolü
        karakter_sayisi = len(temiz_icerik)
        if karakter_sayisi < self.ayarlar.min_karakter:
            return DokumanKaliteSonucu(
                durum=KaliteDurumu.RED,
                skor=karakter_sayisi / self.ayarlar.min_karakter,
                neden=RedNedeni.COK_KISA,
                detay=f"İçerik çok kısa: {karakter_sayisi} karakter (min: {self.ayarlar.min_karakter})",
                oneriler=["Daha fazla içerik ekleyin"],
            )
        
        # 3. Hata sayfası kontrolü
        if self._hata_sayfasi_mi(temiz_icerik):
            return DokumanKaliteSonucu(
                durum=KaliteDurumu.RED,
                skor=0.0,
                neden=RedNedeni.HATA_SAYFASI,
                detay="Hata sayfası tespit edildi (404, 500 vb.)",
            )
        
        # 4. Duplicate kontrolü
        if self.ayarlar.duplicate_kontrol:
            icerik_hash = self._hash_hesapla(temiz_icerik)
            if icerik_hash in self._hash_seti:
                return DokumanKaliteSonucu(
                    durum=KaliteDurumu.RED,
                    skor=0.0,
                    neden=RedNedeni.DUPLICATE,
                    detay="Aynı içerik daha önce eklenmiş",
                )
            self._hash_seti.add(icerik_hash)
        
        # 5. Menü/footer oranı kontrolü
        menu_orani = self._menu_orani_hesapla(temiz_icerik)
        if menu_orani > self.ayarlar.max_menu_oran:
            return DokumanKaliteSonucu(
                durum=KaliteDurumu.RED,
                skor=1 - menu_orani,
                neden=RedNedeni.MENU_FOOTER,
                detay=f"İçeriğin %{menu_orani*100:.0f}'i menü/footer elementi",
                oneriler=["Sadece ana içeriği çıkarın"],
            )
        
        # 6. Tarih güncelliği kontrolü
        tarih = self._tarih_cikar(temiz_icerik, metadata)
        if tarih:
            yas = (datetime.now() - tarih).days / 365
            if yas > self.ayarlar.max_yas_yil:
                return DokumanKaliteSonucu(
                    durum=KaliteDurumu.RED,
                    skor=max(0, 1 - (yas / 10)),
                    neden=RedNedeni.ESKI_TARIH,
                    detay=f"Doküman {yas:.1f} yıl eski (max: {self.ayarlar.max_yas_yil} yıl)",
                    oneriler=["Güncel versiyon kullanın"],
                )
        
        # 7. Yapısal kalite kontrolü
        yapisal_skor = self._yapisal_kalite_hesapla(temiz_icerik)
        if yapisal_skor < 0.3:
            oneriler.append("Başlık ve paragraf yapısı ekleyin")
        
        # 8. Anlamlılık kontrolü
        anlamlilik_skoru = self._anlamlilik_skoru_hesapla(temiz_icerik)
        if anlamlilik_skoru < 0.3:
            return DokumanKaliteSonucu(
                durum=KaliteDurumu.RED,
                skor=anlamlilik_skoru,
                neden=RedNedeni.ANLAMSIZ_ICERIK,
                detay="İçerik anlamlı bilgi içermiyor",
            )
        
        # Toplam skor hesapla
        skor = self._toplam_skor_hesapla(
            karakter_sayisi=karakter_sayisi,
            menu_orani=menu_orani,
            yapisal_skor=yapisal_skor,
            anlamlilik_skoru=anlamlilik_skoru,
            tarih_var=tarih is not None,
        )
        
        # Uyarı durumu
        if skor < 0.7:
            if karakter_sayisi < self.ayarlar.ideal_min_karakter:
                oneriler.append(f"En az {self.ayarlar.ideal_min_karakter} karakter önerilir")
            
            return DokumanKaliteSonucu(
                durum=KaliteDurumu.UYARI,
                skor=skor,
                detay="Doküman kabul edildi ancak kalitesi düşük",
                oneriler=oneriler,
            )
        
        # Kabul
        return DokumanKaliteSonucu(
            durum=KaliteDurumu.KABUL,
            skor=skor,
            detay="Doküman tüm kalite kontrollerinden geçti",
        )
    
    def toplu_dogrula(
        self,
        dokumanlar: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Birden fazla dokümanı toplu doğrula.
        
        Args:
            dokumanlar: Doküman listesi (her biri 'icerik' ve 'metadata' içermeli)
        
        Returns:
            Toplu doğrulama sonuçları
        """
        sonuclar = []
        kabul_sayisi = 0
        red_sayisi = 0
        uyari_sayisi = 0
        
        for dok in dokumanlar:
            icerik = dok.get("icerik") or dok.get("content") or dok.get("text", "")
            metadata = dok.get("metadata", {})
            
            sonuc = self.dogrula(icerik, metadata)
            sonuclar.append({
                "kaynak": metadata.get("source", "bilinmiyor"),
                "sonuc": sonuc,
            })
            
            if sonuc.durum == KaliteDurumu.KABUL:
                kabul_sayisi += 1
            elif sonuc.durum == KaliteDurumu.RED:
                red_sayisi += 1
            else:
                uyari_sayisi += 1
        
        return {
            "toplam": len(dokumanlar),
            "kabul": kabul_sayisi,
            "red": red_sayisi,
            "uyari": uyari_sayisi,
            "kabul_orani": kabul_sayisi / len(dokumanlar) if dokumanlar else 0,
            "sonuclar": sonuclar,
        }
    
    def hash_setini_temizle(self) -> None:
        """Duplicate kontrol için kullanılan hash setini temizle."""
        self._hash_seti.clear()
        logger.info("🗑️ Duplicate hash seti temizlendi")
    
    def _hash_hesapla(self, icerik: str) -> str:
        """İçerik hash'i hesapla (duplicate tespiti için)."""
        # Normalize et: küçük harf, fazla boşlukları sil
        normalize = re.sub(r'\s+', ' ', icerik.lower().strip())
        return hashlib.sha256(normalize.encode('utf-8')).hexdigest()
    
    def _hata_sayfasi_mi(self, icerik: str) -> bool:
        """Hata sayfası kontrolü."""
        icerik_kucuk = icerik.lower()
        
        for regex in self._hata_regex:
            if regex.search(icerik_kucuk):
                return True
        
        return False
    
    def _menu_orani_hesapla(self, icerik: str) -> float:
        """Menü/footer içerik oranını hesapla."""
        satirlar = icerik.split('\n')
        menu_satir_sayisi = 0
        
        for satir in satirlar:
            satir_temiz = satir.strip().lower()
            if len(satir_temiz) < 50:  # Kısa satırlar menü olabilir
                for regex in self._menu_regex:
                    if regex.search(satir_temiz):
                        menu_satir_sayisi += 1
                        break
        
        return menu_satir_sayisi / len(satirlar) if satirlar else 0
    
    def _tarih_cikar(
        self,
        icerik: str,
        metadata: Dict[str, Any],
    ) -> Optional[datetime]:
        """İçerikten veya metadata'dan tarih çıkar."""
        # Önce metadata'ya bak
        tarih_alanlari = ["date", "tarih", "updated", "guncelleme", "created"]
        for alan in tarih_alanlari:
            if alan in metadata and metadata[alan]:
                try:
                    if isinstance(metadata[alan], datetime):
                        return metadata[alan]
                    return datetime.fromisoformat(str(metadata[alan]).replace('Z', '+00:00'))
                except (ValueError, TypeError):
                    pass
        
        # İçerikten tarih ara
        icerik_kucuk = icerik.lower()
        
        for regex in self._tarih_regex:
            eslesme = regex.search(icerik_kucuk)
            if eslesme:
                try:
                    gruplar = eslesme.groups()
                    
                    # Akademik yıl formatı (2024-2025)
                    if len(gruplar) >= 2 and gruplar[0].isdigit() and gruplar[1].isdigit():
                        yil1, yil2 = int(gruplar[0]), int(gruplar[1])
                        if 2000 <= yil1 <= 2100 and yil1 < yil2:
                            return datetime(yil2, 9, 1)  # Akademik yıl başı
                    
                    # Ay isimli format
                    for i, grup in enumerate(gruplar):
                        if grup in self.AY_ISIMLERI:
                            gun = int(gruplar[i-1]) if i > 0 else 1
                            ay = self.AY_ISIMLERI[grup]
                            yil = int(gruplar[i+1]) if i+1 < len(gruplar) else datetime.now().year
                            return datetime(yil, ay, gun)
                    
                    # Sayısal format (GG/AA/YYYY veya YYYY-AA-GG)
                    sayilar = [int(g) for g in gruplar if g.isdigit()]
                    if len(sayilar) >= 3:
                        if sayilar[0] > 31:  # YYYY-MM-DD
                            return datetime(sayilar[0], sayilar[1], sayilar[2])
                        else:  # DD/MM/YYYY
                            return datetime(sayilar[2], sayilar[1], sayilar[0])
                            
                except (ValueError, IndexError):
                    continue
        
        return None
    
    def _yapisal_kalite_hesapla(self, icerik: str) -> float:
        """Yapısal kalite skoru hesapla (başlık, paragraf vb.)."""
        skor = 0.0
        
        # Paragraf sayısı
        paragraflar = [p for p in icerik.split('\n\n') if p.strip()]
        if len(paragraflar) >= 2:
            skor += 0.3
        elif len(paragraflar) >= 1:
            skor += 0.1
        
        # Başlık kontrolü (büyük harfle başlayan kısa satırlar)
        satirlar = icerik.split('\n')
        baslik_sayisi = sum(
            1 for s in satirlar
            if s.strip() and len(s.strip()) < 100 and s.strip()[0].isupper()
        )
        if baslik_sayisi >= 3:
            skor += 0.3
        elif baslik_sayisi >= 1:
            skor += 0.2
        
        # Liste öğeleri
        liste_kaliplari = [r'^\s*[-•*]\s+', r'^\s*\d+[.)]\s+']
        liste_sayisi = sum(
            1 for s in satirlar
            for p in liste_kaliplari
            if re.match(p, s)
        )
        if liste_sayisi >= 5:
            skor += 0.2
        elif liste_sayisi >= 2:
            skor += 0.1
        
        # Tablo varlığı
        if '|' in icerik or '\t' in icerik:
            skor += 0.2
        
        return min(skor, 1.0)
    
    def _anlamlilik_skoru_hesapla(self, icerik: str) -> float:
        """Anlamlılık skoru hesapla."""
        skor = 0.0
        icerik_kucuk = icerik.lower()
        
        # Akademik anahtar kelimeler
        akademik_kelimeler = [
            "üniversite", "fakülte", "bölüm", "öğrenci", "akademik",
            "ders", "sınav", "not", "kredi", "müfredat", "program",
            "profesör", "doçent", "yardımcı", "araştırma", "lisans",
            "yüksek lisans", "doktora", "diploma", "mezuniyet",
            "kayıt", "harç", "burs", "yurt", "kütüphane", "laboratuvar",
        ]
        
        bulunan = sum(1 for k in akademik_kelimeler if k in icerik_kucuk)
        if bulunan >= 10:
            skor += 0.5
        elif bulunan >= 5:
            skor += 0.3
        elif bulunan >= 2:
            skor += 0.1
        
        # Cümle yapısı (. ile biten cümleler)
        cumle_sayisi = len(re.findall(r'[.!?]\s+[A-ZÇĞİÖŞÜ]', icerik))
        if cumle_sayisi >= 10:
            skor += 0.3
        elif cumle_sayisi >= 5:
            skor += 0.2
        
        # Sayısal veri (tarih, saat, oran vb.)
        sayisal = len(re.findall(r'\d+', icerik))
        if sayisal >= 10:
            skor += 0.2
        elif sayisal >= 5:
            skor += 0.1
        
        return min(skor, 1.0)
    
    def _toplam_skor_hesapla(
        self,
        karakter_sayisi: int,
        menu_orani: float,
        yapisal_skor: float,
        anlamlilik_skoru: float,
        tarih_var: bool,
    ) -> float:
        """Toplam kalite skoru hesapla."""
        # Ağırlıklar
        agirliklar = {
            "uzunluk": 0.2,
            "menu": 0.15,
            "yapisal": 0.25,
            "anlamlilik": 0.3,
            "tarih": 0.1,
        }
        
        # Uzunluk skoru (ideal: 500-2000 karakter)
        if karakter_sayisi >= 500:
            uzunluk_skor = min(karakter_sayisi / 2000, 1.0)
        else:
            uzunluk_skor = karakter_sayisi / 500
        
        # Toplam skor
        skor = (
            uzunluk_skor * agirliklar["uzunluk"] +
            (1 - menu_orani) * agirliklar["menu"] +
            yapisal_skor * agirliklar["yapisal"] +
            anlamlilik_skoru * agirliklar["anlamlilik"] +
            (1.0 if tarih_var else 0.5) * agirliklar["tarih"]
        )
        
        return min(max(skor, 0.0), 1.0)


def kalite_filtresi_uygula(
    dokumanlar: List[Dict[str, Any]],
    ayarlar: Optional[DokumanKaliteAyarlari] = None,
) -> List[Dict[str, Any]]:
    """
    Doküman listesine kalite filtresi uygula.
    
    Args:
        dokumanlar: Doküman listesi
        ayarlar: Kalite ayarları
    
    Returns:
        Sadece kaliteli dokümanlar
    """
    dogrulayici = DokumanKaliteDogrulayici(ayarlar)
    kaliteli_dokumanlar = []
    
    for dok in dokumanlar:
        icerik = dok.get("icerik") or dok.get("content") or dok.get("text", "")
        metadata = dok.get("metadata", {})
        
        sonuc = dogrulayici.dogrula(icerik, metadata)
        
        if sonuc.kabul_edildi or sonuc.durum == KaliteDurumu.UYARI:
            # Kalite skorunu metadata'ya ekle
            dok["metadata"] = metadata
            dok["metadata"]["kalite_skoru"] = sonuc.skor
            dok["metadata"]["kalite_durumu"] = sonuc.durum.value
            kaliteli_dokumanlar.append(dok)
        else:
            logger.debug(
                "Doküman reddedildi: %s - %s",
                metadata.get("source", "bilinmiyor"),
                sonuc.neden.value if sonuc.neden else "bilinmiyor",
            )
    
    logger.info(
        "📊 Kalite filtresi: %d/%d doküman kabul edildi (%.1f%%)",
        len(kaliteli_dokumanlar),
        len(dokumanlar),
        len(kaliteli_dokumanlar) / len(dokumanlar) * 100 if dokumanlar else 0,
    )
    
    return kaliteli_dokumanlar
