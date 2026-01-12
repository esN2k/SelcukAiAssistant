"""Kritik bilgi doğruluğu için guard fonksiyonları.

Bu modül, Selçuk Üniversitesi hakkında verilen yanıtlarda
kritik bilgilerin (konum, kuruluş yılı, vb.) doğru olduğundan emin olur.
"""
from __future__ import annotations

import re
from typing import Optional


def _turkish_lower(text: str) -> str:
    """Türkçe karakterleri doğru şekilde küçük harfe çevirir.
    
    Python'ın standart lower() fonksiyonu İ -> i̇ dönüşümü yapar,
    ancak biz İ -> i dönüşümü istiyoruz.
    """
    return text.replace("İ", "i").replace("I", "ı").lower()


# Kritik bilgiler ve doğrulama kuralları
CRITICAL_FACTS = {
    "konum": {
        "doğru": ["konya"],
        "yanlış": ["izmir", "ankara", "istanbul", "bursa", "antalya", "eskişehir"],
        "triggers": [
            r"nerede",
            r"hangi (şehir|il|yer)",
            r"konum",
            r"bulunur",
            r"location",
            r"where",
            r"city",
        ]
    },
    "kuruluş_yılı": {
        "doğru": ["1975"],
        "yanlış": ["1974", "1976", "1980", "1970", "1982"],
        "triggers": [
            r"ne zaman kuruldu",
            r"kaç yılında",
            r"kuruluş yılı",
            r"founded",
            r"established",
        ]
    },
}


def _detect_question_category(question: str) -> Optional[str]:
    """Giriş: Soru metni.
    
    Çıkış: Kategori adı veya None.
    İşleyiş: Sorunun hangi kritik bilgi kategorisine ait olduğunu tespit eder.
    """
    question_lower = _turkish_lower(question)
    
    # Selçuk Üniversitesi ile ilgili mi kontrol et
    has_university_context = any(keyword in question_lower for keyword in ["selçuk", "selcuk", "üniversite", "university"])
    
    # Kategori tetikleyicilerini kontrol et
    for category, rules in CRITICAL_FACTS.items():
        for trigger_pattern in rules["triggers"]:
            if re.search(trigger_pattern, question_lower, re.IGNORECASE):
                # Eğer üniversite bağlamı varsa veya çok spesifik bir tetikleyici ise kabul et
                if has_university_context or "kuruluş" in trigger_pattern or "founded" in trigger_pattern:
                    return category
    
    return None


def _contains_wrong_fact(text: str, category: str) -> Optional[str]:
    """Giriş: Yanıt metni ve kategori.
    
    Çıkış: Bulunan yanlış bilgi veya None.
    İşleyiş: Yanıtta yanlış bilgi var mı kontrol eder.
    """
    if category not in CRITICAL_FACTS:
        return None
    
    text_lower = _turkish_lower(text)
    rules = CRITICAL_FACTS[category]
    
    # Yanlış bilgileri kontrol et
    for wrong_fact in rules["yanlış"]:
        # Kelime sınırlarıyla ara (örn: "konyadaki" değil, "konya" ara)
        pattern = r'\b' + re.escape(wrong_fact) + r'\b'
        if re.search(pattern, text_lower, re.IGNORECASE):
            return wrong_fact
    
    return None


def _contains_correct_fact(text: str, category: str) -> bool:
    """Giriş: Yanıt metni ve kategori.
    
    Çıkış: bool.
    İşleyiş: Yanıtta doğru bilgi var mı kontrol eder.
    """
    if category not in CRITICAL_FACTS:
        return True  # Bilinmeyen kategori için geç
    
    text_lower = _turkish_lower(text)
    rules = CRITICAL_FACTS[category]
    
    # Doğru bilgilerden en az biri var mı
    for correct_fact in rules["doğru"]:
        pattern = r'\b' + re.escape(correct_fact) + r'\b'
        if re.search(pattern, text_lower, re.IGNORECASE):
            return True
    
    return False


def guard_response_accuracy(
    question: str,
    answer: str,
    language: str = "tr",
) -> tuple[str, bool]:
    """Giriş: Soru, yanıt ve dil.
    
    Çıkış: (düzeltilmiş_yanıt, değişti_mi).
    İşleyiş: Kritik bilgileri kontrol eder ve gerekirse düzeltir.
    """
    # Sorunun kategorisini tespit et
    category = _detect_question_category(question)
    
    if category is None:
        # Kritik soru değil, yanıtı olduğu gibi döndür
        return answer, False
    
    # Yanlış bilgi var mı kontrol et
    wrong_fact = _contains_wrong_fact(answer, category)
    
    if wrong_fact:
        # Yanlış bilgi tespit edildi - tamamen düzeltilmiş yanıt döndür
        if category == "konum":
            if language.lower().startswith("en"):
                corrected = (
                    "Selçuk University is located in **Konya**, Turkey.\n\n"
                    "Specifically, it has two main campuses:\n"
                    "- **Alaeddin Keykubat Campus** in Selçuklu district (Engineering, Technology, Science faculties)\n"
                    "- **Ardıçlı Campus** in Karatay district (Medicine, Health Sciences)\n\n"
                    "The university was founded in 1975 and is one of Turkey's prominent state universities."
                )
            else:
                corrected = (
                    "Selçuk Üniversitesi **Konya**'dadır.\n\n"
                    "İki ana kampüsü bulunmaktadır:\n"
                    "- **Alaeddin Keykubat Yerleşkesi** (Selçuklu/Konya): Mühendislik, Teknoloji, Fen fakülteleri\n"
                    "- **Ardıçlı Yerleşkesi** (Karatay/Konya): Tıp, Sağlık Bilimleri\n\n"
                    "Üniversite 1975 yılında kurulmuş olup, Türkiye'nin önde gelen devlet üniversitelerinden biridir."
                )
        elif category == "kuruluş_yılı":
            if language.lower().startswith("en"):
                corrected = (
                    "Selçuk University was founded in **1975** in Konya, Turkey.\n\n"
                    "It started with the Konya State Academy of Architecture and Engineering "
                    "and gained its current structure in 1982."
                )
            else:
                corrected = (
                    "Selçuk Üniversitesi **1975** yılında Konya'da kurulmuştur.\n\n"
                    "Konya Devlet Mimarlık ve Mühendislik Akademisi temelinde kurulan üniversite, "
                    "1982 yılında mevcut yapısına kavuşmuştur."
                )
        else:
            # Diğer kategoriler için orijinal yanıtı kullan ama uyarı ekle
            corrected = answer
        
        return corrected, True
    
    # Doğru bilgi var mı kontrol et
    has_correct = _contains_correct_fact(answer, category)
    
    if not has_correct and category == "konum":
        # Konya bilgisi eksik - eklenmeli
        if language.lower().startswith("en"):
            corrected = (
                f"Selçuk University is in **Konya**, Turkey.\n\n{answer}"
            )
        else:
            corrected = (
                f"Selçuk Üniversitesi **Konya**'dadır.\n\n{answer}"
            )
        return corrected, True
    
    # Yanıt doğru, değişiklik gerekmez
    return answer, False


def validate_critical_answer(question: str, answer: str) -> tuple[bool, Optional[str]]:
    """Giriş: Soru ve yanıt metni.
    
    Çıkış: (geçerli_mi, hata_mesajı).
    İşleyiş: Kritik soruların yanıtlarını doğrular, test için kullanılır.
    """
    category = _detect_question_category(question)
    
    if category is None:
        return True, None  # Kritik soru değil
    
    # Yanlış bilgi kontrolü
    wrong_fact = _contains_wrong_fact(answer, category)
    if wrong_fact:
        return False, f"Yanıtta yanlış bilgi bulundu: '{wrong_fact}'"
    
    # Doğru bilgi kontrolü
    has_correct = _contains_correct_fact(answer, category)
    if not has_correct:
        return False, f"Yanıtta '{category}' kategorisi için doğru bilgi bulunamadı"
    
    return True, None
