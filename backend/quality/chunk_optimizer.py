"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  DOSYA: chunk_optimizer.py                                                     ║
║  AMAÇ: Chunk kalite optimizasyonu                                             ║
║  KULLANIM: Dokümanları ideal boyut ve metadata ile parçala                    ║
╚════════════════════════════════════════════════════════════════════════════════╝

AÇIKLAMA:
─────────
Bu modül, dokümanları RAG için optimize edilmiş chunklara böler.
Her chunk şunları içerir:
- Ana içerik (200-1000 karakter arası)
- Başlık (context için)
- Zengin metadata (kaynak, tarih, tip, kategori, güven skoru)
- Overlap (bilgi kaybı önleme)

OPTİMİZASYON KRİTERLERİ:
1. Minimum 200, maksimum 1000 karakter
2. 50 karakter overlap
3. Paragraf sınırlarına saygı
4. Başlık ve context korunması
5. Metadata zenginleştirme
"""

from __future__ import annotations

import hashlib
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class DokumanTipi(Enum):
    """Doküman tipleri"""
    PDF = "pdf"
    DOCX = "docx"
    HTML = "html"
    TEXT = "text"
    MARKDOWN = "markdown"
    UNKNOWN = "unknown"


class DokumanKategorisi(Enum):
    """Doküman kategorileri"""
    AKADEMIK = "akademik"           # Akademik takvim, müfredat
    IDARI = "idari"                 # Yönetmelik, prosedür
    DUYURU = "duyuru"               # Haberler, duyurular
    KAYIT = "kayit"                 # Kayıt, harç işlemleri
    OGRENCI = "ogrenci"             # Öğrenci işleri
    FAKULTE = "fakulte"             # Fakülte bilgileri
    BOLUM = "bolum"                 # Bölüm bilgileri
    GENEL = "genel"                 # Genel bilgiler


@dataclass
class OptimizeEdilmisChunk:
    """
    Optimize edilmiş chunk veri yapısı.
    
    Attributes:
        content: Ana içerik
        title: Başlık (context için)
        metadata: Zengin metadata
    """
    content: str
    title: str = ""
    chunk_id: str = ""
    chunk_index: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.chunk_id:
            self.chunk_id = hashlib.md5(self.content.encode()).hexdigest()[:12]
        
        # Metadata varsayılanları
        if "confidence" not in self.metadata:
            self.metadata["confidence"] = 0.0
        if "source" not in self.metadata:
            self.metadata["source"] = "unknown"
    
    @property
    def kalite_skoru(self) -> float:
        """Chunk kalite skoru"""
        return self.metadata.get("confidence", 0.0)
    
    @property
    def karakter_sayisi(self) -> int:
        """İçerik karakter sayısı"""
        return len(self.content)
    
    @property
    def kelime_sayisi(self) -> int:
        """İçerik kelime sayısı"""
        return len(self.content.split())
    
    def to_dict(self) -> Dict[str, Any]:
        """Sözlüğe dönüştür"""
        return {
            "content": self.content,
            "title": self.title,
            "chunk_id": self.chunk_id,
            "chunk_index": self.chunk_index,
            "metadata": self.metadata,
        }


@dataclass
class ChunkOptimizerAyarlar:
    """
    Chunk optimizer ayarları.
    
    Attributes:
        min_boyut: Minimum chunk boyutu (karakter)
        max_boyut: Maksimum chunk boyutu (karakter)
        ideal_boyut: İdeal chunk boyutu (karakter)
        overlap: Chunklar arası overlap (karakter)
        baslik_dahil: Başlığı her chunk'a dahil et
        paragraf_saygi: Paragraf sınırlarına saygı göster
    """
    min_boyut: int = 200
    max_boyut: int = 1000
    ideal_boyut: int = 600
    overlap: int = 50
    baslik_dahil: bool = True
    paragraf_saygi: bool = True
    min_cumle_sayisi: int = 2


class ChunkOptimizer:
    """
    Chunk optimizasyon sınıfı.
    
    Bu sınıf, dokümanları RAG için optimize edilmiş chunklara böler.
    
    Kullanım:
        optimizer = ChunkOptimizer()
        chunks = optimizer.optimize(icerik, metadata)
    """
    
    # Kategori anahtar kelimeleri
    KATEGORI_ANAHTAR_KELIMELER = {
        DokumanKategorisi.AKADEMIK: [
            "akademik takvim", "müfredat", "ders programı", "kredi",
            "akts", "ects", "yarıyıl", "dönem", "eğitim-öğretim",
        ],
        DokumanKategorisi.IDARI: [
            "yönetmelik", "yönerge", "mevzuat", "kanun", "madde",
            "prosedür", "usul", "esas", "tüzük",
        ],
        DokumanKategorisi.DUYURU: [
            "duyuru", "haber", "ilan", "açıklama", "bilgilendirme",
            "etkinlik", "toplantı", "konferans",
        ],
        DokumanKategorisi.KAYIT: [
            "kayıt", "tescil", "harç", "ücret", "ödeme",
            "başvuru", "form", "dilekçe",
        ],
        DokumanKategorisi.OGRENCI: [
            "öğrenci", "staj", "burs", "yurt", "yemekhane",
            "sağlık", "spor", "kulüp",
        ],
        DokumanKategorisi.FAKULTE: [
            "fakülte", "dekan", "dekanlik", "sekreter",
            "akademik kadro", "öğretim üyesi",
        ],
        DokumanKategorisi.BOLUM: [
            "bölüm", "anabilim dalı", "program", "lisans",
            "yüksek lisans", "doktora",
        ],
    }
    
    # Başlık kalıpları
    BASLIK_KALIPLARI = [
        r'^#{1,6}\s+(.+)$',          # Markdown başlıkları
        r'^([A-ZÇĞİÖŞÜ][A-ZÇĞİÖŞÜa-zçğıöşü\s]+):?\s*$',  # Büyük harfle başlayan
        r'^(\d+[.)]\s*.+)$',         # Numaralı başlıklar
        r'^([A-ZÇĞİÖŞÜ\s]{5,50})$',  # Tamamı büyük harf
    ]
    
    # Tarih kalıpları
    TARIH_KALIPLARI = [
        r'(\d{1,2})[./\-](\d{1,2})[./\-](\d{4})',
        r'(\d{4})[./\-](\d{1,2})[./\-](\d{1,2})',
        r'(\d{1,2})\s+(ocak|şubat|mart|nisan|mayıs|haziran|temmuz|ağustos|eylül|ekim|kasım|aralık)\s+(\d{4})',
        r'(\d{4})-(\d{4})\s*(akademik|eğitim|öğretim)?\s*yılı',
    ]
    
    def __init__(self, ayarlar: Optional[ChunkOptimizerAyarlar] = None):
        """
        Optimizer'ı başlat.
        
        Args:
            ayarlar: Chunk optimizer ayarları
        """
        self.ayarlar = ayarlar or ChunkOptimizerAyarlar()
        self._baslik_regex = [re.compile(p, re.MULTILINE) for p in self.BASLIK_KALIPLARI]
        self._tarih_regex = [re.compile(p, re.IGNORECASE) for p in self.TARIH_KALIPLARI]
        
        logger.info(
            "📦 Chunk optimizer başlatıldı (min: %d, max: %d, overlap: %d)",
            self.ayarlar.min_boyut,
            self.ayarlar.max_boyut,
            self.ayarlar.overlap,
        )
    
    def optimize(
        self,
        icerik: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> List[OptimizeEdilmisChunk]:
        """
        Dokümanı optimize edilmiş chunklara böl.
        
        Args:
            icerik: Doküman içeriği
            metadata: Doküman metadata'sı
        
        Returns:
            Optimize edilmiş chunk listesi
        """
        metadata = metadata or {}
        
        if not icerik or not icerik.strip():
            return []
        
        temiz_icerik = self._on_islem(icerik)
        
        # Doküman tipini belirle
        dok_tipi = self._dokuman_tipini_belirle(metadata)
        
        # Kategoriyi belirle
        kategori = self._kategori_belirle(temiz_icerik)
        
        # Başlığı çıkar
        baslik = self._baslik_cikar(temiz_icerik, metadata)
        
        # Tarihi çıkar
        tarih = self._tarih_cikar(temiz_icerik, metadata)
        
        # Parçalama stratejisini seç
        if dok_tipi in [DokumanTipi.PDF, DokumanTipi.DOCX]:
            chunklar = self._paragraf_bazli_parcala(temiz_icerik)
        else:
            chunklar = self._akilli_parcala(temiz_icerik)
        
        # Chunklara metadata ekle
        sonuc = []
        for i, chunk_icerik in enumerate(chunklar):
            # Kalite skoru hesapla
            kalite_skoru = self._chunk_kalitesi_hesapla(chunk_icerik, baslik)
            
            # Metadata oluştur
            chunk_metadata = {
                **metadata,
                "source": metadata.get("source", "unknown"),
                "date": tarih.isoformat() if tarih else None,
                "type": dok_tipi.value,
                "category": kategori.value,
                "confidence": kalite_skoru,
                "chunk_index": i,
                "total_chunks": len(chunklar),
                "char_count": len(chunk_icerik),
                "word_count": len(chunk_icerik.split()),
            }
            
            # Başlığı içeriğe dahil et (opsiyonel)
            icerik_final = chunk_icerik
            if self.ayarlar.baslik_dahil and baslik and i == 0:
                icerik_final = f"{baslik}\n\n{chunk_icerik}"
            
            chunk = OptimizeEdilmisChunk(
                content=icerik_final,
                title=baslik,
                chunk_index=i,
                metadata=chunk_metadata,
            )
            
            sonuc.append(chunk)
        
        logger.debug(
            "📦 %d chunk oluşturuldu (kaynak: %s, kategori: %s)",
            len(sonuc),
            metadata.get("source", "unknown")[:50],
            kategori.value,
        )
        
        return sonuc
    
    def toplu_optimize(
        self,
        dokumanlar: List[Dict[str, Any]],
    ) -> List[OptimizeEdilmisChunk]:
        """
        Birden fazla dokümanı toplu optimize et.
        
        Args:
            dokumanlar: Doküman listesi
        
        Returns:
            Tüm optimize edilmiş chunklar
        """
        tum_chunklar = []
        
        for dok in dokumanlar:
            icerik = dok.get("icerik") or dok.get("content") or dok.get("text", "")
            metadata = dok.get("metadata", {})
            
            chunklar = self.optimize(icerik, metadata)
            tum_chunklar.extend(chunklar)
        
        logger.info(
            "📦 Toplu optimizasyon: %d doküman → %d chunk",
            len(dokumanlar),
            len(tum_chunklar),
        )
        
        return tum_chunklar
    
    def _on_islem(self, icerik: str) -> str:
        """İçeriği ön işlemden geçir."""
        # Fazla boşlukları temizle
        temiz = re.sub(r'\n{3,}', '\n\n', icerik)
        temiz = re.sub(r'[ \t]{2,}', ' ', temiz)
        temiz = temiz.strip()
        
        return temiz
    
    def _dokuman_tipini_belirle(self, metadata: Dict[str, Any]) -> DokumanTipi:
        """Metadata'dan doküman tipini belirle."""
        kaynak = str(metadata.get("source", "")).lower()
        tip = str(metadata.get("type", "")).lower()
        
        if "pdf" in tip or kaynak.endswith(".pdf"):
            return DokumanTipi.PDF
        elif "docx" in tip or "doc" in tip or kaynak.endswith((".docx", ".doc")):
            return DokumanTipi.DOCX
        elif "html" in tip or kaynak.endswith((".html", ".htm")):
            return DokumanTipi.HTML
        elif "markdown" in tip or "md" in tip or kaynak.endswith(".md"):
            return DokumanTipi.MARKDOWN
        elif "text" in tip or kaynak.endswith(".txt"):
            return DokumanTipi.TEXT
        else:
            return DokumanTipi.UNKNOWN
    
    def _kategori_belirle(self, icerik: str) -> DokumanKategorisi:
        """İçerikten kategori belirle."""
        icerik_kucuk = icerik.lower()
        
        en_yuksek_skor = 0
        en_iyi_kategori = DokumanKategorisi.GENEL
        
        for kategori, anahtar_kelimeler in self.KATEGORI_ANAHTAR_KELIMELER.items():
            skor = sum(1 for k in anahtar_kelimeler if k in icerik_kucuk)
            if skor > en_yuksek_skor:
                en_yuksek_skor = skor
                en_iyi_kategori = kategori
        
        return en_iyi_kategori
    
    def _baslik_cikar(
        self,
        icerik: str,
        metadata: Dict[str, Any],
    ) -> str:
        """İçerikten veya metadata'dan başlık çıkar."""
        # Önce metadata'ya bak
        if metadata.get("title"):
            return str(metadata["title"]).strip()
        
        # İçerikten başlık ara
        satirlar = icerik.split('\n')
        for satir in satirlar[:5]:  # İlk 5 satırda ara
            satir = satir.strip()
            if not satir:
                continue
            
            for regex in self._baslik_regex:
                eslesme = regex.match(satir)
                if eslesme:
                    return eslesme.group(1).strip() if eslesme.groups() else satir
            
            # Kısa ve büyük harfle başlayan satır
            if len(satir) < 100 and satir[0].isupper():
                return satir
        
        # Kaynak dosya adından başlık oluştur
        kaynak = metadata.get("source", "")
        if kaynak:
            from pathlib import Path
            dosya_adi = Path(kaynak).stem
            return dosya_adi.replace("_", " ").replace("-", " ").title()
        
        return ""
    
    def _tarih_cikar(
        self,
        icerik: str,
        metadata: Dict[str, Any],
    ) -> Optional[datetime]:
        """İçerikten veya metadata'dan tarih çıkar."""
        # Metadata'dan tarih
        tarih_alanlari = ["date", "tarih", "updated", "created", "guncelleme"]
        for alan in tarih_alanlari:
            if metadata.get(alan):
                try:
                    deger = metadata[alan]
                    if isinstance(deger, datetime):
                        return deger
                    return datetime.fromisoformat(str(deger).replace('Z', '+00:00'))
                except (ValueError, TypeError):
                    pass
        
        # İçerikten tarih
        ay_isimleri = {
            "ocak": 1, "şubat": 2, "mart": 3, "nisan": 4,
            "mayıs": 5, "haziran": 6, "temmuz": 7, "ağustos": 8,
            "eylül": 9, "ekim": 10, "kasım": 11, "aralık": 12,
        }
        
        icerik_kucuk = icerik.lower()
        
        for regex in self._tarih_regex:
            eslesme = regex.search(icerik_kucuk)
            if eslesme:
                try:
                    gruplar = eslesme.groups()
                    
                    # Akademik yıl (2024-2025)
                    if len(gruplar) >= 2:
                        g0, g1 = gruplar[0], gruplar[1]
                        if g0.isdigit() and g1.isdigit():
                            y0, y1 = int(g0), int(g1)
                            if 2000 <= y0 <= 2100 and y0 < y1:
                                return datetime(y1, 9, 1)
                    
                    # Ay isimli format
                    for i, g in enumerate(gruplar):
                        if g and g in ay_isimleri:
                            gun = int(gruplar[i-1]) if i > 0 and gruplar[i-1].isdigit() else 1
                            ay = ay_isimleri[g]
                            yil_idx = i + 1
                            yil = int(gruplar[yil_idx]) if yil_idx < len(gruplar) and gruplar[yil_idx].isdigit() else datetime.now().year
                            return datetime(yil, ay, min(gun, 28))
                    
                    # Sayısal format
                    sayilar = [int(g) for g in gruplar if g and g.isdigit()]
                    if len(sayilar) >= 3:
                        if sayilar[0] > 31:  # YYYY-MM-DD
                            return datetime(sayilar[0], min(sayilar[1], 12), min(sayilar[2], 28))
                        else:  # DD/MM/YYYY
                            return datetime(sayilar[2], min(sayilar[1], 12), min(sayilar[0], 28))
                except (ValueError, IndexError):
                    continue
        
        return None
    
    def _paragraf_bazli_parcala(self, icerik: str) -> List[str]:
        """Paragraf bazlı parçalama (PDF/DOCX için)."""
        paragraflar = [p.strip() for p in icerik.split('\n\n') if p.strip()]
        
        chunklar = []
        mevcut = ""
        
        for para in paragraflar:
            if len(mevcut) + len(para) + 2 <= self.ayarlar.max_boyut:
                mevcut = f"{mevcut}\n\n{para}".strip() if mevcut else para
            else:
                if mevcut and len(mevcut) >= self.ayarlar.min_boyut:
                    chunklar.append(mevcut)
                    # Overlap ekle
                    if self.ayarlar.overlap > 0 and len(mevcut) > self.ayarlar.overlap:
                        overlap_text = mevcut[-self.ayarlar.overlap:]
                        mevcut = f"{overlap_text} {para}"
                    else:
                        mevcut = para
                elif mevcut:
                    # Çok kısa, sonraki paragrafa ekle
                    mevcut = f"{mevcut}\n\n{para}".strip()
                else:
                    mevcut = para
                
                # Çok uzun paragraf varsa böl
                if len(mevcut) > self.ayarlar.max_boyut:
                    alt_chunklar = self._cumle_bazli_bol(mevcut)
                    chunklar.extend(alt_chunklar[:-1])
                    mevcut = alt_chunklar[-1] if alt_chunklar else ""
        
        if mevcut and len(mevcut) >= self.ayarlar.min_boyut:
            chunklar.append(mevcut)
        elif mevcut and chunklar:
            # Son kısa parçayı öncekine ekle
            chunklar[-1] = f"{chunklar[-1]}\n\n{mevcut}"
        
        return chunklar
    
    def _akilli_parcala(self, icerik: str) -> List[str]:
        """Akıllı parçalama (HTML/text için)."""
        # Önce paragraf bazlı dene
        paragraflar = [p.strip() for p in icerik.split('\n\n') if p.strip()]
        
        if all(len(p) < self.ayarlar.max_boyut for p in paragraflar):
            return self._paragraf_bazli_parcala(icerik)
        
        # Cümle bazlı parçala
        return self._cumle_bazli_bol(icerik)
    
    def _cumle_bazli_bol(self, icerik: str) -> List[str]:
        """Cümle bazlı parçalama."""
        # Cümle sonu işaretlerinden böl
        cumle_sonu = re.compile(r'([.!?])\s+')
        cumleler = cumle_sonu.split(icerik)
        
        # Cümleleri yeniden birleştir
        birlesik_cumleler = []
        for i in range(0, len(cumleler) - 1, 2):
            cumle = cumleler[i]
            if i + 1 < len(cumleler):
                cumle += cumleler[i + 1]
            birlesik_cumleler.append(cumle.strip())
        
        if len(cumleler) % 2 == 1:
            birlesik_cumleler.append(cumleler[-1].strip())
        
        # Cümleleri chunklara birleştir
        chunklar = []
        mevcut = ""
        cumle_sayisi = 0
        
        for cumle in birlesik_cumleler:
            if not cumle:
                continue
            
            if len(mevcut) + len(cumle) + 1 <= self.ayarlar.max_boyut:
                mevcut = f"{mevcut} {cumle}".strip() if mevcut else cumle
                cumle_sayisi += 1
            else:
                if (len(mevcut) >= self.ayarlar.min_boyut and 
                    cumle_sayisi >= self.ayarlar.min_cumle_sayisi):
                    chunklar.append(mevcut)
                    
                    # Overlap
                    if self.ayarlar.overlap > 0:
                        son_cumle = mevcut.split('.')[-2] + '.' if '.' in mevcut else ""
                        mevcut = f"{son_cumle} {cumle}".strip()
                    else:
                        mevcut = cumle
                    cumle_sayisi = 1
                else:
                    mevcut = f"{mevcut} {cumle}".strip()
                    cumle_sayisi += 1
        
        if mevcut and (len(mevcut) >= self.ayarlar.min_boyut or not chunklar):
            chunklar.append(mevcut)
        elif mevcut and chunklar:
            chunklar[-1] = f"{chunklar[-1]} {mevcut}"
        
        return chunklar
    
    def _chunk_kalitesi_hesapla(self, icerik: str, baslik: str) -> float:
        """Chunk kalite skoru hesapla."""
        skor = 0.0
        
        # Uzunluk skoru (ideal: 400-800 karakter)
        uzunluk = len(icerik)
        if 400 <= uzunluk <= 800:
            skor += 0.3
        elif 200 <= uzunluk < 400 or 800 < uzunluk <= 1000:
            skor += 0.2
        elif uzunluk >= 100:
            skor += 0.1
        
        # Yapı skoru (cümle sayısı)
        cumle_sayisi = len(re.findall(r'[.!?]', icerik))
        if cumle_sayisi >= 5:
            skor += 0.2
        elif cumle_sayisi >= 3:
            skor += 0.15
        elif cumle_sayisi >= 1:
            skor += 0.1
        
        # Anlamlılık (akademik terimler)
        akademik_terimler = [
            "üniversite", "fakülte", "bölüm", "ders", "sınav",
            "öğrenci", "akademik", "not", "kredi", "müfredat",
        ]
        bulunan = sum(1 for t in akademik_terimler if t in icerik.lower())
        if bulunan >= 5:
            skor += 0.3
        elif bulunan >= 3:
            skor += 0.2
        elif bulunan >= 1:
            skor += 0.1
        
        # Başlık uyumu
        if baslik and any(k in icerik.lower() for k in baslik.lower().split()):
            skor += 0.1
        
        # Tarih varlığı
        if re.search(r'\d{4}', icerik):
            skor += 0.1
        
        return min(skor, 1.0)


def chunk_kalitesini_hesapla(chunk: Dict[str, Any]) -> float:
    """
    Tek bir chunk'ın kalitesini hesapla.
    
    Args:
        chunk: Chunk sözlüğü (content, metadata içermeli)
    
    Returns:
        Kalite skoru (0.0 - 1.0)
    """
    icerik = chunk.get("content", "")
    baslik = chunk.get("title", "")
    
    optimizer = ChunkOptimizer()
    return optimizer._chunk_kalitesi_hesapla(icerik, baslik)
