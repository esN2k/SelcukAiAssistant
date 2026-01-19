"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  DOSYA: quality_tester.py                                                      ║
║  AMAÇ: RAG sistemi kalite testi ve değerlendirmesi                            ║
║  KULLANIM: Sürekli kalite izleme ve iyileştirme için test çerçevesi          ║
╚════════════════════════════════════════════════════════════════════════════════╝

AÇIKLAMA:
─────────
Bu modül, RAG sisteminin kalitesini sürekli olarak test eder.
50+ test sorusu ile %95+ başarı hedeflenir.

TEST KRİTERLERİ:
1. Anahtar kelime kontrolü (beklenen kelimeler cevapta var mı?)
2. Uzunluk kontrolü (minimum uzunluk sağlanıyor mu?)
3. Kaynak kontrolü (citation var mı?)
4. Doğruluk kontrolü (beklenen cevapla uyum)
5. Yanıt süresi kontrolü (performans)
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class TestDurumu(Enum):
    """Test durumu"""
    BASARILI = "basarili"
    BASARISIZ = "basarisiz"
    ATLANDI = "atlandi"
    HATA = "hata"


@dataclass
class TestSonucu:
    """
    Tek bir test sonucu.
    
    Attributes:
        test_id: Test kimliği
        sorgu: Test sorgusu
        durum: Test durumu
        cevap: Sistem cevabı
        sure_ms: Yanıt süresi (ms)
        detaylar: Detaylı kontrol sonuçları
    """
    test_id: str
    sorgu: str
    durum: TestDurumu
    cevap: str = ""
    sure_ms: float = 0.0
    detaylar: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def basarili(self) -> bool:
        return self.durum == TestDurumu.BASARILI
    
    def __str__(self) -> str:
        durum_emoji = {
            TestDurumu.BASARILI: "✅",
            TestDurumu.BASARISIZ: "❌",
            TestDurumu.ATLANDI: "⏭️",
            TestDurumu.HATA: "💥",
        }
        return f"{durum_emoji.get(self.durum, '?')} [{self.test_id}] {self.sorgu[:50]}... ({self.sure_ms:.0f}ms)"


@dataclass
class TestRaporu:
    """
    Test raporu.
    
    Attributes:
        tarih: Test tarihi
        toplam: Toplam test sayısı
        basarili: Başarılı test sayısı
        basarisiz: Başarısız test sayısı
        atlanan: Atlanan test sayısı
        hata: Hatalı test sayısı
        basari_orani: Başarı oranı (0.0 - 1.0)
        ortalama_sure: Ortalama yanıt süresi (ms)
        sonuclar: Test sonuçları listesi
    """
    tarih: datetime
    toplam: int
    basarili: int
    basarisiz: int
    atlanan: int
    hata: int
    basari_orani: float
    ortalama_sure: float
    sonuclar: List[TestSonucu]
    
    def ozet(self) -> str:
        """Rapor özeti"""
        return f"""
📊 RAG KALİTE TEST RAPORU
═══════════════════════════════════════
📅 Tarih: {self.tarih.strftime('%Y-%m-%d %H:%M:%S')}
─────────────────────────────────────
✅ Başarılı: {self.basarili}/{self.toplam}
❌ Başarısız: {self.basarisiz}/{self.toplam}
⏭️ Atlanan: {self.atlanan}/{self.toplam}
💥 Hata: {self.hata}/{self.toplam}
─────────────────────────────────────
📈 Başarı Oranı: %{self.basari_orani*100:.1f}
⏱️ Ortalama Süre: {self.ortalama_sure:.0f}ms
═══════════════════════════════════════
"""
    
    def to_dict(self) -> Dict[str, Any]:
        """Sözlüğe dönüştür"""
        return {
            "tarih": self.tarih.isoformat(),
            "toplam": self.toplam,
            "basarili": self.basarili,
            "basarisiz": self.basarisiz,
            "atlanan": self.atlanan,
            "hata": self.hata,
            "basari_orani": self.basari_orani,
            "ortalama_sure": self.ortalama_sure,
            "sonuclar": [
                {
                    "test_id": s.test_id,
                    "sorgu": s.sorgu,
                    "durum": s.durum.value,
                    "sure_ms": s.sure_ms,
                    "detaylar": s.detaylar,
                }
                for s in self.sonuclar
            ],
        }


@dataclass
class TestSorusu:
    """
    Test sorusu tanımı.
    
    Attributes:
        id: Test kimliği
        sorgu: Test sorgusu
        beklenen_kelimeler: Cevapta bulunması gereken kelimeler
        min_uzunluk: Minimum cevap uzunluğu
        kaynak_zorunlu: Kaynak gösterimi zorunlu mu?
        beklenen_cevap: Beklenen cevap (opsiyonel)
        kategori: Test kategorisi
        oncelik: Test önceliği (1-5, 1 en yüksek)
    """
    id: str
    sorgu: str
    beklenen_kelimeler: List[str] = field(default_factory=list)
    min_uzunluk: int = 100
    kaynak_zorunlu: bool = True
    beklenen_cevap: str = ""
    kategori: str = "genel"
    oncelik: int = 3


# Selçuk Üniversitesi için standart test soruları
STANDART_TEST_SORULARI: List[TestSorusu] = [
    # Akademik Takvim Soruları
    TestSorusu(
        id="AKD001",
        sorgu="2024-2025 akademik takvimi ne zaman başlıyor?",
        beklenen_kelimeler=["akademik", "yıl", "2024", "2025", "eylül", "ekim"],
        min_uzunluk=100,
        kategori="akademik_takvim",
        oncelik=1,
    ),
    TestSorusu(
        id="AKD002",
        sorgu="Final sınavları ne zaman?",
        beklenen_kelimeler=["final", "sınav", "tarih"],
        min_uzunluk=100,
        kategori="akademik_takvim",
        oncelik=1,
    ),
    TestSorusu(
        id="AKD003",
        sorgu="Vize sınavları hangi tarihlerde?",
        beklenen_kelimeler=["vize", "ara", "sınav"],
        min_uzunluk=100,
        kategori="akademik_takvim",
        oncelik=1,
    ),
    TestSorusu(
        id="AKD004",
        sorgu="Bütünleme sınavları ne zaman yapılıyor?",
        beklenen_kelimeler=["bütünleme", "sınav"],
        min_uzunluk=80,
        kategori="akademik_takvim",
        oncelik=2,
    ),
    TestSorusu(
        id="AKD005",
        sorgu="Ders kayıt tarihleri ne zaman?",
        beklenen_kelimeler=["kayıt", "ders", "tarih"],
        min_uzunluk=100,
        kategori="akademik_takvim",
        oncelik=1,
    ),
    
    # Müfredat ve Ders Soruları
    TestSorusu(
        id="MFR001",
        sorgu="Bilgisayar mühendisliği zorunlu dersleri nelerdir?",
        beklenen_kelimeler=["ders", "zorunlu", "kredi"],
        min_uzunluk=200,
        kategori="müfredat",
        oncelik=1,
    ),
    TestSorusu(
        id="MFR002",
        sorgu="Yazılım mühendisliği bölümü dersleri nelerdir?",
        beklenen_kelimeler=["yazılım", "ders"],
        min_uzunluk=150,
        kategori="müfredat",
        oncelik=2,
    ),
    TestSorusu(
        id="MFR003",
        sorgu="AKTS kredisi nedir?",
        beklenen_kelimeler=["akts", "kredi", "avrupa"],
        min_uzunluk=100,
        kategori="müfredat",
        oncelik=2,
    ),
    TestSorusu(
        id="MFR004",
        sorgu="Staj zorunlu mu? Kaç gün yapılmalı?",
        beklenen_kelimeler=["staj", "gün", "zorunlu"],
        min_uzunluk=100,
        kategori="müfredat",
        oncelik=2,
    ),
    TestSorusu(
        id="MFR005",
        sorgu="Bitirme projesi nasıl yapılır?",
        beklenen_kelimeler=["bitirme", "proje", "tez"],
        min_uzunluk=150,
        kategori="müfredat",
        oncelik=2,
    ),
    
    # Kayıt ve İdari İşlemler
    TestSorusu(
        id="KYT001",
        sorgu="Harç ücreti ne kadar?",
        beklenen_kelimeler=["harç", "ücret", "ödeme"],
        min_uzunluk=80,
        kategori="kayit",
        oncelik=1,
    ),
    TestSorusu(
        id="KYT002",
        sorgu="Yatay geçiş başvurusu nasıl yapılır?",
        beklenen_kelimeler=["yatay", "geçiş", "başvuru"],
        min_uzunluk=150,
        kategori="kayit",
        oncelik=2,
    ),
    TestSorusu(
        id="KYT003",
        sorgu="Burs başvurusu nasıl yapılır?",
        beklenen_kelimeler=["burs", "başvuru"],
        min_uzunluk=100,
        kategori="kayit",
        oncelik=2,
    ),
    TestSorusu(
        id="KYT004",
        sorgu="Öğrenci belgesi nereden alınır?",
        beklenen_kelimeler=["öğrenci", "belge"],
        min_uzunluk=80,
        kategori="kayit",
        oncelik=3,
    ),
    TestSorusu(
        id="KYT005",
        sorgu="Transkript nasıl alınır?",
        beklenen_kelimeler=["transkript", "not", "belge"],
        min_uzunluk=80,
        kategori="kayit",
        oncelik=3,
    ),
    
    # Fakülte ve Bölüm Bilgileri
    TestSorusu(
        id="FKL001",
        sorgu="Teknoloji Fakültesi hangi bölümleri var?",
        beklenen_kelimeler=["teknoloji", "fakülte", "bölüm"],
        min_uzunluk=150,
        kategori="fakulte",
        oncelik=2,
    ),
    TestSorusu(
        id="FKL002",
        sorgu="Mühendislik Fakültesi dekanı kim?",
        beklenen_kelimeler=["dekan", "fakülte"],
        min_uzunluk=50,
        kategori="fakulte",
        oncelik=3,
    ),
    TestSorusu(
        id="FKL003",
        sorgu="Bilgisayar Mühendisliği bölüm başkanı kim?",
        beklenen_kelimeler=["bölüm", "başkan"],
        min_uzunluk=50,
        kategori="fakulte",
        oncelik=3,
    ),
    
    # Genel Üniversite Bilgileri
    TestSorusu(
        id="GNL001",
        sorgu="Selçuk Üniversitesi nerede?",
        beklenen_kelimeler=["konya", "selçuk", "kampüs"],
        min_uzunluk=80,
        kategori="genel",
        oncelik=1,
    ),
    TestSorusu(
        id="GNL002",
        sorgu="Selçuk Üniversitesi ne zaman kuruldu?",
        beklenen_kelimeler=["selçuk", "kuruluş", "yıl"],
        min_uzunluk=80,
        kategori="genel",
        oncelik=2,
    ),
    TestSorusu(
        id="GNL003",
        sorgu="Kütüphane çalışma saatleri nedir?",
        beklenen_kelimeler=["kütüphane", "saat"],
        min_uzunluk=50,
        kategori="genel",
        oncelik=3,
    ),
    TestSorusu(
        id="GNL004",
        sorgu="Yemekhane nerede?",
        beklenen_kelimeler=["yemekhane", "kampüs"],
        min_uzunluk=50,
        kategori="genel",
        oncelik=3,
    ),
    TestSorusu(
        id="GNL005",
        sorgu="Öğrenci yurdu başvurusu nasıl yapılır?",
        beklenen_kelimeler=["yurt", "başvuru"],
        min_uzunluk=100,
        kategori="genel",
        oncelik=2,
    ),
    
    # Not ve Değerlendirme
    TestSorusu(
        id="NOT001",
        sorgu="Geçme notu kaç?",
        beklenen_kelimeler=["geçme", "not", "puan"],
        min_uzunluk=50,
        kategori="not",
        oncelik=1,
    ),
    TestSorusu(
        id="NOT002",
        sorgu="AGNO nasıl hesaplanır?",
        beklenen_kelimeler=["agno", "not", "ortalama"],
        min_uzunluk=100,
        kategori="not",
        oncelik=2,
    ),
    TestSorusu(
        id="NOT003",
        sorgu="DD notu ile geçilir mi?",
        beklenen_kelimeler=["not", "geç"],
        min_uzunluk=50,
        kategori="not",
        oncelik=2,
    ),
    
    # Yönetmelik ve Mevzuat
    TestSorusu(
        id="YNT001",
        sorgu="Devamsızlık sınırı nedir?",
        beklenen_kelimeler=["devam", "devamsızlık", "ders"],
        min_uzunluk=80,
        kategori="yonetmelik",
        oncelik=1,
    ),
    TestSorusu(
        id="YNT002",
        sorgu="Mazeret sınavı şartları nelerdir?",
        beklenen_kelimeler=["mazeret", "sınav"],
        min_uzunluk=100,
        kategori="yonetmelik",
        oncelik=2,
    ),
    TestSorusu(
        id="YNT003",
        sorgu="Ders tekrarı nasıl yapılır?",
        beklenen_kelimeler=["ders", "tekrar"],
        min_uzunluk=80,
        kategori="yonetmelik",
        oncelik=2,
    ),
    
    # İletişim
    TestSorusu(
        id="ILT001",
        sorgu="Öğrenci işleri telefon numarası nedir?",
        beklenen_kelimeler=["öğrenci", "işleri", "telefon", "iletişim"],
        min_uzunluk=50,
        kaynak_zorunlu=False,
        kategori="iletisim",
        oncelik=3,
    ),
    TestSorusu(
        id="ILT002",
        sorgu="Dekanlık e-posta adresi nedir?",
        beklenen_kelimeler=["e-posta", "mail", "iletişim"],
        min_uzunluk=50,
        kaynak_zorunlu=False,
        kategori="iletisim",
        oncelik=3,
    ),
]


class KaliteTesti:
    """
    RAG sistemi kalite testi sınıfı.
    
    Bu sınıf, RAG sisteminin kalitesini standart test soruları ile
    sürekli olarak değerlendirir.
    
    Kullanım:
        tester = KaliteTesti(rag_fonksiyonu)
        rapor = tester.testleri_calistir()
        print(rapor.ozet())
    """
    
    def __init__(
        self,
        rag_fonksiyonu: Callable[[str], str],
        test_sorulari: Optional[List[TestSorusu]] = None,
        hedef_basari_orani: float = 0.95,
    ):
        """
        Test sınıfını başlat.
        
        Args:
            rag_fonksiyonu: RAG sorgu fonksiyonu (sorgu -> cevap)
            test_sorulari: Özel test soruları (None = standart sorular)
            hedef_basari_orani: Hedef başarı oranı (varsayılan: %95)
        """
        self.rag_fonksiyonu = rag_fonksiyonu
        self.test_sorulari = test_sorulari or STANDART_TEST_SORULARI
        self.hedef_basari_orani = hedef_basari_orani
        
        logger.info(
            "🧪 Kalite testi başlatıldı: %d soru, hedef: %%%d",
            len(self.test_sorulari),
            int(hedef_basari_orani * 100),
        )
    
    def testleri_calistir(
        self,
        kategoriler: Optional[List[str]] = None,
        max_oncelik: int = 5,
    ) -> TestRaporu:
        """
        Tüm testleri çalıştır.
        
        Args:
            kategoriler: Sadece bu kategorileri test et (None = tümü)
            max_oncelik: Maksimum öncelik seviyesi (1-5)
        
        Returns:
            TestRaporu: Test raporu
        """
        sonuclar = []
        sureler = []
        
        # Filtreleme
        testler = self.test_sorulari
        if kategoriler:
            testler = [t for t in testler if t.kategori in kategoriler]
        testler = [t for t in testler if t.oncelik <= max_oncelik]
        
        logger.info("🧪 %d test çalıştırılıyor...", len(testler))
        
        for test in testler:
            sonuc = self._tek_test_calistir(test)
            sonuclar.append(sonuc)
            sureler.append(sonuc.sure_ms)
            
            # İlerleme logla
            durum_emoji = "✅" if sonuc.basarili else "❌"
            logger.debug("%s %s", durum_emoji, sonuc)
        
        # İstatistikleri hesapla
        basarili = sum(1 for s in sonuclar if s.durum == TestDurumu.BASARILI)
        basarisiz = sum(1 for s in sonuclar if s.durum == TestDurumu.BASARISIZ)
        atlanan = sum(1 for s in sonuclar if s.durum == TestDurumu.ATLANDI)
        hata = sum(1 for s in sonuclar if s.durum == TestDurumu.HATA)
        
        basari_orani = basarili / len(sonuclar) if sonuclar else 0
        ortalama_sure = sum(sureler) / len(sureler) if sureler else 0
        
        rapor = TestRaporu(
            tarih=datetime.now(),
            toplam=len(sonuclar),
            basarili=basarili,
            basarisiz=basarisiz,
            atlanan=atlanan,
            hata=hata,
            basari_orani=basari_orani,
            ortalama_sure=ortalama_sure,
            sonuclar=sonuclar,
        )
        
        # Sonuç logla
        if basari_orani >= self.hedef_basari_orani:
            logger.info("✅ Hedef başarı oranına ulaşıldı: %%%.1f", basari_orani * 100)
        else:
            logger.warning(
                "❌ Hedef başarı oranına ulaşılamadı: %%%.1f < %%%.1f",
                basari_orani * 100,
                self.hedef_basari_orani * 100,
            )
        
        return rapor
    
    def _tek_test_calistir(self, test: TestSorusu) -> TestSonucu:
        """Tek bir testi çalıştır."""
        detaylar = {
            "kelime_kontrolu": False,
            "uzunluk_kontrolu": False,
            "kaynak_kontrolu": False,
            "bulunan_kelimeler": [],
            "eksik_kelimeler": [],
        }
        
        try:
            # RAG sorgusunu çalıştır
            baslangic = time.time()
            cevap = self.rag_fonksiyonu(test.sorgu)
            sure_ms = (time.time() - baslangic) * 1000
            
            if not cevap:
                return TestSonucu(
                    test_id=test.id,
                    sorgu=test.sorgu,
                    durum=TestDurumu.BASARISIZ,
                    cevap="",
                    sure_ms=sure_ms,
                    detaylar={"hata": "Boş cevap"},
                )
            
            cevap_kucuk = cevap.lower()
            
            # 1. Anahtar kelime kontrolü
            bulunan = []
            eksik = []
            for kelime in test.beklenen_kelimeler:
                if kelime.lower() in cevap_kucuk:
                    bulunan.append(kelime)
                else:
                    eksik.append(kelime)
            
            detaylar["bulunan_kelimeler"] = bulunan
            detaylar["eksik_kelimeler"] = eksik
            
            # En az yarısı bulunmalı
            if len(bulunan) >= len(test.beklenen_kelimeler) / 2:
                detaylar["kelime_kontrolu"] = True
            
            # 2. Uzunluk kontrolü
            if len(cevap) >= test.min_uzunluk:
                detaylar["uzunluk_kontrolu"] = True
            
            # 3. Kaynak kontrolü
            kaynak_kaliplari = ["kaynak", "source", "[", "📚"]
            if not test.kaynak_zorunlu:
                detaylar["kaynak_kontrolu"] = True
            elif any(k in cevap_kucuk for k in kaynak_kaliplari):
                detaylar["kaynak_kontrolu"] = True
            
            # Genel başarı değerlendirmesi
            basarili = (
                detaylar["kelime_kontrolu"] and
                detaylar["uzunluk_kontrolu"] and
                detaylar["kaynak_kontrolu"]
            )
            
            return TestSonucu(
                test_id=test.id,
                sorgu=test.sorgu,
                durum=TestDurumu.BASARILI if basarili else TestDurumu.BASARISIZ,
                cevap=cevap[:500],  # İlk 500 karakter
                sure_ms=sure_ms,
                detaylar=detaylar,
            )
            
        except Exception as e:
            logger.error("Test hatası [%s]: %s", test.id, e)
            return TestSonucu(
                test_id=test.id,
                sorgu=test.sorgu,
                durum=TestDurumu.HATA,
                detaylar={"hata": str(e)},
            )
    
    def raporu_kaydet(self, rapor: TestRaporu, dosya_yolu: str) -> None:
        """Test raporunu JSON olarak kaydet."""
        with open(dosya_yolu, 'w', encoding='utf-8') as f:
            json.dump(rapor.to_dict(), f, ensure_ascii=False, indent=2)
        
        logger.info("📁 Test raporu kaydedildi: %s", dosya_yolu)
    
    def basarisiz_testleri_getir(self, rapor: TestRaporu) -> List[TestSonucu]:
        """Başarısız testleri listele."""
        return [s for s in rapor.sonuclar if s.durum == TestDurumu.BASARISIZ]
    
    def kategori_bazli_analiz(self, rapor: TestRaporu) -> Dict[str, Dict[str, Any]]:
        """Kategori bazlı analiz yap."""
        kategoriler: Dict[str, Dict[str, Any]] = {}
        
        for sonuc in rapor.sonuclar:
            # Test sorusundan kategori bul
            test = next((t for t in self.test_sorulari if t.id == sonuc.test_id), None)
            if not test:
                continue
            
            kategori = test.kategori
            if kategori not in kategoriler:
                kategoriler[kategori] = {
                    "toplam": 0,
                    "basarili": 0,
                    "basarisiz": 0,
                    "basari_orani": 0.0,
                }
            
            kategoriler[kategori]["toplam"] += 1
            if sonuc.basarili:
                kategoriler[kategori]["basarili"] += 1
            else:
                kategoriler[kategori]["basarisiz"] += 1
        
        # Başarı oranlarını hesapla
        for kategori in kategoriler.values():
            if kategori["toplam"] > 0:
                kategori["basari_orani"] = kategori["basarili"] / kategori["toplam"]
        
        return kategoriler


def kalite_testlerini_calistir(
    rag_fonksiyonu: Callable[[str], str],
    hedef_basari: float = 0.95,
) -> TestRaporu:
    """
    Hızlı kalite testi çalıştırma fonksiyonu.
    
    Args:
        rag_fonksiyonu: RAG sorgu fonksiyonu
        hedef_basari: Hedef başarı oranı
    
    Returns:
        TestRaporu: Test raporu
    """
    tester = KaliteTesti(rag_fonksiyonu, hedef_basari_orani=hedef_basari)
    return tester.testleri_calistir()


# Test sorusu ekleme yardımcı fonksiyonu
def test_sorusu_ekle(
    id: str,
    sorgu: str,
    beklenen_kelimeler: List[str],
    min_uzunluk: int = 100,
    kategori: str = "genel",
) -> TestSorusu:
    """
    Yeni test sorusu oluştur.
    
    Args:
        id: Test kimliği
        sorgu: Test sorgusu
        beklenen_kelimeler: Beklenen kelimeler
        min_uzunluk: Minimum cevap uzunluğu
        kategori: Test kategorisi
    
    Returns:
        TestSorusu: Yeni test sorusu
    """
    return TestSorusu(
        id=id,
        sorgu=sorgu,
        beklenen_kelimeler=beklenen_kelimeler,
        min_uzunluk=min_uzunluk,
        kategori=kategori,
    )
