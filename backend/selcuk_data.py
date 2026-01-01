"""Selçuk Üniversitesi temel bilgileri - Manuel doğrulanmış veriler."""

SELCUK_UNI_FACTS = {
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
        "ard��çlı": {
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
        ],
        "akredite": "MÜDEK akreditasyonu",
        "web": "https://bilgisayar.selcuk.edu.tr",
    },
    
    "iletisim": {
        "telefon": "+90 332 223 1000",
        "web": "https://www.selcuk.edu.tr",
        "email": "info@selcuk.edu.tr",
        "adres": "Selçuklu, 42250 Konya",
    }
}


# Sık sorulan sorular ve cevaplar
QA_PAIRS = [
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
        "question": "Bilgisayar Mühendisliği bölümü hangi kampusta?",
        "answer": "Bilgisayar Mühendisliği bölümü, Mühendislik Fakültesi bünyesinde Alaeddin Keykubat Kampüsü'nde bulunmaktadır.",
        "category": "bilgisayar",
    },
    {
        "question": "Bilgisayar Mühendisliği hangi araştırma alanları var?",
        "answer": """Bilgisayar Mühendisliği bölümünde şu araştırma alanları bulunmaktadır:
- Yapay Zeka ve Makine Öğrenmesi
- Bilgisayar Görüsü
- Doğal Dil İşleme
- Veri Bilimi ve Büyük Veri
- Siber Güvenlik
- Yazılım Mühendisliği
- Bulut Bilişim ve Dağıtık Sistemler""",
        "category": "bilgisayar",
    },
    {
        "question": "Bilgisayar Mühendisliği lisansüstü programları var mı?",
        "answer": "Evet, Bilgisayar Mühendisliği bölümünde Yüksek Lisans ve Doktora programları bulunmaktadır.",
        "category": "bilgisayar",
    },
    {
        "question": "Selçuk Üniversitesi web sitesi nedir?",
        "answer": "Selçuk Üniversitesi ana web sitesi: https://www.selcuk.edu.tr\nBilgisayar Mühendisliği: https://bilgisayar.selcuk.edu.tr",
        "category": "genel",
    },
    {
        "question": "Selçuk Üniversitesi Mühendislik Fakültesi hangi bölümler var?",
        "answer": """Mühendislik Fakültesi'nde şu bölümler bulunmaktadır:
- Bilgisayar Mühendisliği
- Elektrik-Elektronik Mühendisliği
- Makine Mühendisliği
- İnşaat Mühendisliği
- Endüstri Mühendisliği
- Harita Mühendisliği
- Jeoloji Mühendisliği""",
        "category": "muhendislik",
    },
    {
        "question": "Selçuk Üniversitesi kaç öğrencisi var?",
        "answer": "Selçuk Üniversitesi'nde yaklaşık 100.000'den fazla öğrenci bulunmaktadır.",
        "category": "genel",
    },
]
