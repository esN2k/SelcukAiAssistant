"""Selçuk Üniversitesi temel bilgileri - Manuel doğrulanmış veriler."""
from typing import Any

SELCUK_UNI_FACTS: dict[str, Any] = {
    "genel_bilgiler": {
        "ad": "Selçuk Üniversitesi",
        "sehir": "Konya",
        "kurulus_yili": 1975,
        "rektör": "Prof. Dr. Metin Aksoy",  # Güncel rektör bilgisi
        "tip": "Devlet Üniversitesi",
        "kampus": ["Alaeddin Keykubat Kampüsü", "Ardıçlı Kampüsü"],
        "ogrenci_sayisi": "100,000+",  # Yaklaşık
        "akademisyen_sayisi": "4,000+",  # Yaklaşık
    },
    
    "tarihce": """Selçuk Üniversitesi, 1975 yılında Konya'da kurulmuştur. 
    Konya Devlet Mimarlık ve Mühendislik Akademisi'nin temelini oluşturduğu üniversite, 
    1982 yılında mevcut yapısına kavuşmuştur. Adını Selçuklu Devleti'nden almaktadır.""",
    
    "kampusler": {
        "alaeddin_keykubat": {
            "konum": "Selçuklu/Konya",
            "alan": "Geniş kampus alanı",
            "fakulteler": ["Mühendislik", "Fen", "Edebiyat", "İletişim"],
        },
        "ardıçlı": {
            "konum": "Karatay/Konya", 
            "fakulteler": ["Tıp", "Sağlık Bilimleri", "Diş Hekimliği"],
        }
    },
    
    "muhendislik_fakultesi": {
        "bolumler": [
            "Bilgisayar Mühendisliği",
            "Elektrik-Elektronik Mühendisliği",
            "Makine Mühendisliği",
            "İnşaat Mühendisliği",
            "Endüstri Mühendisliği",
            "Harita Mühendisliği",
            "Jeoloji Mühendisliği",
        ],
        "konum": "Alaeddin Keykubat Kampüsü",
    },
    
    "bilgisayar_muhendisligi": {
        "fakulte": "Teknoloji Fakültesi",
        "yerleske": "Alaeddin Keykubat Yerleşkesi",
        "bolum_baskani": "Bilgisayar Mühendisliği Bölüm Başkanı",  # Güncellenebilir
        "program_turu": ["Lisans", "Yüksek Lisans", "Doktora"],
        "kontenjan": "120 (yaklaşık)",
        "arastirma_alanlari": [
            "Yapay Zeka",
            "Makine Öğrenmesi",
            "Bilgisayar Görüsü",
            "Doğal Dil İşleme",
            "Veri Bilimi",
            "Siber Güvenlik",
            "Yazılım Mühendisliği",
            "Bulut Bilişim",
            "High Performance Computing (HPC)",
        ],
        "laboratuvarlar": [
            "Bilgisayar Laboratuvarı",
            "Yazılım Geliştirme Laboratuvarı",
            "Ağ ve Güvenlik Laboratuvarı",
            "HPC Laboratuvarı",
        ],
        "ozellikler": [
            "MÜDEK Akreditasyonu",
            "Bologna Süreci Uyumlu",
            "Çift Anadal Programı",
            "Erasmus+ Değişim Programı",
            "Girişimcilik Saati",
            "Kariyer Planlama ve Takibi Ofisi",
            "ArGe İşbirlikleri",
            "Konya Teknokent İşbirliği",
        ],
        "web": "https://www.selcuk.edu.tr/Birim/Bolum/teknoloji-bilgisayar_muhendisligi/15620",
        "email": "tfdekanlik@selcuk.edu.tr",
        "adres": "Selçuk Üniversitesi Alaeddin Keykubat Yerleşkesi Teknoloji Fakültesi PK:42075 Selçuklu / KONYA",
    },
    
    "iletisim": {
        "telefon": "+90 332 223 1000",
        "web": "https://www.selcuk.edu.tr",
        "email": "info@selcuk.edu.tr",
        "adres": "Selçuklu, 42250 Konya",
    }
}


# Sık sorulan sorular ve cevaplar
QA_PAIRS: list[dict[str, str]] = [
    # Konum soruları
    {
        "question": "Selçuk Üniversitesi nerede?",
        "answer": "Selçuk Üniversitesi, Konya ilinde bulunmaktadır. Alaeddin Keykubat ve Ardıçlı olmak üzere iki ana kampüsü vardır.",
        "category": "genel",
    },
    {
        "question": "Selçuk Üniversitesi hangi şehirde?",
        "answer": "Selçuk Üniversitesi Konya'dadır.",
        "category": "genel",
    },
    {
        "question": "Selçuk Üniversitesi hangi ilde?",
        "answer": "Konya ilinde.",
        "category": "genel",
    },
    # Kuruluş soruları
    {
        "question": "Selçuk Üniversitesi ne zaman kuruldu?",
        "answer": "Selçuk Üniversitesi 1975 yılında Konya'da kurulmuştur.",
        "category": "genel",
    },
    {
        "question": "Selçuk Üniversitesi kaç yılında kuruldu?",
        "answer": "1975 yılında kurulmuştur.",
        "category": "genel",
    },
    {
        "question": "Kuruluş yılı nedir?",
        "answer": "1975",
        "category": "genel",
    },
    # Kampüs soruları
    {
        "question": "Kampüsler hangileri?",
        "answer": "Selçuk Üniversitesi'nde iki ana kampüs bulunmaktadır: Alaeddin Keykubat Yerleşkesi ve Ardıçlı Yerleşkesi.",
        "category": "genel",
    },
    {
        "question": "Alaeddin Keykubat Yerleşkesi nerede?",
        "answer": "Alaeddin Keykubat Yerleşkesi Selçuklu/Konya'da bulunmaktadır. Mühendislik, Fen, Edebiyat ve Teknoloji fakülteleri bu kampüstedir.",
        "category": "genel",
    },
    {
        "question": "Ardıçlı Yerleşkesi nerede?",
        "answer": "Ardıçlı Yerleşkesi Karatay/Konya'da bulunmaktadır. Tıp, Sağlık Bilimleri ve Diş Hekimliği fakülteleri bu kampüstedir.",
        "category": "genel",
    },
    # Bilgisayar Mühendisliği - Temel Bilgiler
    {
        "question": "Bilgisayar Mühendisliği bölümü hangi kampusta?",
        "answer": "Bilgisayar Mühendisliği bölümü, Teknoloji Fakültesi bünyesinde Alaeddin Keykubat Yerleşkesi'nde bulunmaktadır. Adres: Selçuk Üniversitesi Alaeddin Keykubat Yerleşkesi Teknoloji Fakültesi PK:42075 Selçuklu / KONYA",
        "category": "bilgisayar",
    },
    {
        "question": "Bilgisayar Mühendisliği hangi fakültede?",
        "answer": "Bilgisayar Mühendisliği, Teknoloji Fakültesi bünyesindedir.",
        "category": "bilgisayar",
    },
    {
        "question": "Bilgisayar Mühendisliği nerede?",
        "answer": "Teknoloji Fakültesi, Alaeddin Keykubat Yerleşkesi, Konya.",
        "category": "bilgisayar",
    },
    # Bilgisayar Mühendisliği - İletişim
    {
        "question": "Bilgisayar Mühendisliği email adresi nedir?",
        "answer": "Teknoloji Fakültesi Dekanlık e-posta: tfdekanlik@selcuk.edu.tr",
        "category": "bilgisayar",
    },
    {
        "question": "Bilgisayar Mühendisliği telefon numarası?",
        "answer": "Dekanlık: 0(332) 223 33 68, Öğrenci İşleri: 0(332) 223 33 73",
        "category": "bilgisayar",
    },
    {
        "question": "Bilgisayar Mühendisliği web sitesi?",
        "answer": "https://www.selcuk.edu.tr/Birim/Bolum/teknoloji-bilgisayar_muhendisligi/15620",
        "category": "bilgisayar",
    },
    # Bilgisayar Mühendisliği - Akademik
    {
        "question": "Bilgisayar Mühendisliği hangi araştırma alanları var?",
        "answer": """Bilgisayar Mühendisliği bölümünde şu araştırma alanları bulunmaktadır:
- Yapay Zeka ve Makine Öğrenmesi
- Bilgisayar Görüsü
- Doğal Dil İşleme
- Veri Bilimi ve Büyük Veri
- Siber Güvenlik
- Yazılım Mühendisliği
- Bulut Bilişim ve Dağıtık Sistemler
- High Performance Computing (HPC)""",
        "category": "bilgisayar",
    },
    {
        "question": "Bilgisayar Mühendisliği lisansüstü programları var mı?",
        "answer": "Evet, Bilgisayar Mühendisliği bölümünde Yüksek Lisans ve Doktora programları bulunmaktadır.",
        "category": "bilgisayar",
    },
    {
        "question": "HPC nedir?",
        "answer": "HPC (High Performance Computing - Yüksek Başarımlı Hesaplama) laboratuvarı, Bilgisayar Mühendisliği bölümünde bulunan özel bir araştırma altyapısıdır.",
        "category": "bilgisayar",
    },
    # Bilgisayar Mühendisliği - Akreditasyon ve Olanaklar
    {
        "question": "Bilgisayar Mühendisliği akredite mi?",
        "answer": "Evet, Bilgisayar Mühendisliği bölümü MÜDEK (Mühendislik Eğitim Programları Değerlendirme ve Akreditasyon Derneği) akreditasyonuna sahiptir.",
        "category": "bilgisayar",
    },
    {
        "question": "MÜDEK nedir?",
        "answer": "MÜDEK (Mühendislik Eğitim Programları Değerlendirme ve Akreditasyon Derneği), mühendislik programlarının kalite güvencesini sağlayan akreditasyon kuruluşudur. Bilgisayar Mühendisliği bölümü MÜDEK akreditasyonuna sahiptir.",
        "category": "bilgisayar",
    },
    {
        "question": "Erasmus programı var mı?",
        "answer": "Evet, Bilgisayar Mühendisliği bölümünde Erasmus+ değişim programı mevcuttur.",
        "category": "bilgisayar",
    },
    {
        "question": "Çift anadal programı var mı?",
        "answer": "Evet, Bilgisayar Mühendisliği bölümünde çift anadal programı bulunmaktadır.",
        "category": "bilgisayar",
    },
    {
        "question": "Kariyer ofisi var mı?",
        "answer": "Evet, Kariyer Planlama ve Takibi Ofisi mevcuttur.",
        "category": "bilgisayar",
    },
    {
        "question": "Bilgisayar Mühendisliği hangi olanaklar sunuyor?",
        "answer": """Bilgisayar Mühendisliği bölümü şu olanakları sunar:
- MÜDEK Akreditasyonu
- Bologna Süreci Uyumlu Eğitim
- Çift Anadal Programı
- Erasmus+ Değişim Programı
- Girişimcilik Saati
- Kariyer Planlama ve Takibi Ofisi
- ArGe İşbirlikleri
- Konya Teknokent İşbirliği
- High Performance Computing (HPC) Laboratuvarı""",
        "category": "bilgisayar",
    },
    # Teknoloji Fakültesi
    {
        "question": "Teknoloji Fakültesi nerede?",
        "answer": "Teknoloji Fakültesi, Alaeddin Keykubat Yerleşkesi'nde, Konya'dadır.",
        "category": "teknoloji",
    },
    {
        "question": "Teknoloji Fakültesi dekanlık telefonu?",
        "answer": "Dekanlık: 0(332) 223 33 68",
        "category": "teknoloji",
    },
    # Genel İstatistikler
    {
        "question": "Selçuk Üniversitesi kaç öğrencisi var?",
        "answer": "Selçuk Üniversitesi'nde yaklaşık 100.000'den fazla öğrenci bulunmaktadır.",
        "category": "genel",
    },
    {
        "question": "Kaç akademisyen var?",
        "answer": "Yaklaşık 4.000'den fazla akademisyen bulunmaktadır.",
        "category": "genel",
    },
    # İşbirliği ve Sanayi
    {
        "question": "Konya Teknokent ile işbirliği var mı?",
        "answer": "Evet, Bilgisayar Mühendisliği bölümü Konya Teknokent ile işbirliği içindedir.",
        "category": "bilgisayar",
    },
    {
        "question": "ArGe işbirlikleri var mı?",
        "answer": "Evet, Bilgisayar Mühendisliği bölümünde çeşitli ArGe işbirlikleri ve projeler bulunmaktadır.",
        "category": "bilgisayar",
    },
    {
        "question": "Girişimcilik desteği var mı?",
        "answer": "Evet, Girişimcilik Saati programı mevcuttur.",
        "category": "bilgisayar",
    },
]
