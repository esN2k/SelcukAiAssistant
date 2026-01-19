"""
═══════════════════════════════════════════════════════════════════════════════
KRİTİK BİLGİ KORUMA SİSTEMİ
═══════════════════════════════════════════════════════════════════════════════

Modül: critical_facts.py
Açıklama: Selçuk Üniversitesi için kritik bilgi doğrulama ve koruma sistemi

Özellikler:
    - Önceden tanımlı kritik cevaplar (konum, kuruluş yılı, rektör vb.)
    - Yanlış bilgi tespiti ve düzeltme (1974 → 1975, İzmir → Konya)
    - Soru sınıflandırma (foundation, location, rector vb.)
    - Selamlama algılama (merhaba, selam vb.)
    - Metin normalizasyonu (Türkçe karakter dönüşümü)

Kritik Bilgiler:
    - Konum: Konya (İzmir, Ankara değil!)
    - Kuruluş: 1975 (1974, 1976 değil!)
    - Rektör: Prof. Dr. Hüseyin Yılmaz
    - Fakülte sayısı: 23
    - Öğrenci sayısı: ~70.000
    - Bilgisayar Müh. Fakültesi: Teknoloji Fakültesi

Koruma Mekanizması:
    1. Soru sınıflandırma (classify_question)
    2. Kritik cevap getirme (get_critical_answer)
    3. Guard uygulama (apply_guard)
    4. Yanlış cümle filtreleme (_filter_sentences)

Yazar: SelçukAI Ekibi
═══════════════════════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import json
import logging
import re
import unicodedata
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


_TURKISH_MAP = str.maketrans(
    {
        "ç": "c",
        "ğ": "g",
        "ı": "i",
        "İ": "i",
        "ö": "o",
        "ş": "s",
        "ü": "u",
    }
)

_KB_PATH = Path(__file__).resolve().parent / "data" / "selcuk_knowledge_base.json"


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().translate(_TURKISH_MAP)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _find_kb_key(data: dict[str, Any], key: str) -> Any:
    target = _normalize(key)
    for candidate, value in data.items():
        if _normalize(candidate) == target:
            return value
    return None


def _load_kb() -> Optional[dict[str, Any]]:
    if not _KB_PATH.exists():
        return None
    try:
        with _KB_PATH.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception as exc:
        logger.warning("KB okunamadi: %s", exc)
        return None
    return data if isinstance(data, dict) else None


LOCATION_KEYWORDS = [
    "nerede",
    "neresinde",
    "konum",
    "lokasyon",
    "hangi sehir",
    "hangi il",
    "hangi ilde",
    "hangi sehirde",
    "where",
    "location",
    "located",
    "which city",
    "which province",
    "izmir",
    "ankara",
    "istanbul",
    "bursa",
    "antalya",
    "eskisehir",
]

ADDRESS_KEYWORDS = [
    "adres",
    "adresi",
    "address",
    "kampus adres",
    "kampus adresi",
    "yerleske adres",
    "yerleske adresi",
]

CONTACT_KEYWORDS = [
    "iletisim",
    "contact",
    "contact info",
    "iletisim bilgileri",
]

PHONE_KEYWORDS = [
    "telefon",
    "telefonu",
    "telefon numarasi",
    "phone",
    "contact number",
]

WEBSITE_KEYWORDS = [
    "web sitesi",
    "web",
    "internet sitesi",
    "website",
    "site",
    "official site",
    "resmi web",
    "resmi site",
]

RECTOR_KEYWORDS = [
    "rektor",
    "rektorlugu",
    "rektoru",
    "rector",
]

FACULTY_COUNT_KEYWORDS = [
    "fakulte sayisi",
    "kac fakulte",
    "fakulte kac",
    "faculty count",
    "how many faculties",
]

STUDENT_COUNT_KEYWORDS = [
    "ogrenci sayisi",
    "kac ogrenci",
    "ogrenci sayisi kac",
    "student count",
    "how many students",
]

ACADEMIC_UNITS_KEYWORDS = [
    "enstitu sayisi",
    "kac enstitu",
    "yuksekokul sayisi",
    "meslek yuksekokulu",
    "myo",
    "arastirma merkezi",
    "devlet konservatuvari",
    "akademik yapi",
    "akademik birim",
    "akademik birimler",
    "akademik birimleri",
    "birimler",
    "birimleri",
    "birim sayisi",
]

FOUNDATION_KEYWORDS = [
    "ne zaman kuruldu",
    "kac yilinda kuruldu",
    "kurulus yili",
    "kurulus tarihi",
    "kuruldu",
    "founded",
    "established",
    "when was",
    "year founded",
]

CE_KEYWORDS = [
    "bilgisayar muhendisligi",
    "computer engineering",
]

CE_WEB_KEYWORDS = [
    "web",
    "web sitesi",
    "website",
    "site",
]

CE_BOLONYA_KEYWORDS = [
    "bologna",
    "bolonya",
    "dersler",
]

CE_YOKATLAS_KEYWORDS = [
    "yok atlas",
    "yokatlas",
]

CE_FACEBOOK_KEYWORDS = [
    "facebook",
    "fb",
]

CE_PROGRAM_CODE_KEYWORDS = [
    "program kodu",
    "program code",
    "yok atlas kodu",
    "kodu",
]

CE_LANGUAGE_KEYWORDS = [
    "egitim dili",
    "language of instruction",
]

CE_SCORE_TYPE_KEYWORDS = [
    "puan turu",
    "score type",
    "say",
]

CE_FACULTY_KEYWORDS = [
    "hangi fakulte",
    "fakulte",
    "fakultede",
    "faculty",
]

CE_CAMPUS_KEYWORDS = [
    "hangi kampus",
    "kampus",
    "kampusunde",
    "yerleske",
    "nerede",
    "where",
    "location",
]

ACCREDITATION_KEYWORDS = [
    "mudek",
    "akredite",
    "akreditasyon",
    "accredited",
    "accreditation",
]

WRONG_CITY_KEYWORDS = [
    "izmir",
    "ankara",
    "istanbul",
    "bursa",
    "antalya",
    "eskisehir",
]

WRONG_YEAR_KEYWORDS = [
    "1974",
    "1976",
    "1980",
    "1970",
    "1982",
]

FALLBACK_TR = (
    "Bu konuda kesin bilgiye sahip değilim. "
    "Lütfen Selçuk Üniversitesi ile ilgili sorunu netleştir."
)
FALLBACK_EN = (
    "I do not have a verified answer for this. "
    "Please clarify your question about Selçuk University."
)


CRITICAL_ANSWERS_TR = {
    "location": (
        "Selçuk Üniversitesi **Konya**'dadır.\n\n"
        "İki ana kampüsü bulunmaktadır:\n"
        "- **Alaeddin Keykubat Yerleşkesi** (Selçuklu/Konya)\n"
        "- **Ardıçlı Yerleşkesi** (Karatay/Konya)"
    ),
    "foundation": "Selçuk Üniversitesi 1975 yılında Konya'da kurulmuştur.",
    "address": (
        "Resmi adres: Alaeddin Keykubat Yerleşkesi, Akademi Mah. "
        "Yeni İstanbul Cad. No:369, 42130 Selçuklu/Konya"
    ),
    "phone": "Telefon: +90 332 241 0041",
    "website": "Resmi web sitesi: https://www.selcuk.edu.tr/",
    "contact": (
        "İletişim: +90 332 241 0041\n"
        "Web: https://www.selcuk.edu.tr/\n"
        "Adres: Alaeddin Keykubat Yerleşkesi, Akademi Mah. "
        "Yeni İstanbul Cad. No:369, 42130 Selçuklu/Konya"
    ),
    "rector": (
        "Selçuk Üniversitesi Rektörü Prof. Dr. Hüseyin Yılmaz'dır "
        "(26 Temmuz 2024'ten beri görevde)."
    ),
    "faculty_count": "Selçuk Üniversitesi'nde 23 fakülte bulunmaktadır.",
    "student_count": "Selçuk Üniversitesi'nde yaklaşık 70.000 öğrenci bulunmaktadır.",
    "academic_units": (
        "Akademik yapı: 23 fakülte, 7 enstitü, 5 yüksekokul, "
        "1 devlet konservatuvarı, 23 meslek yüksekokulu ve "
        "53 araştırma merkezi."
    ),
    "ce_faculty": "Bilgisayar Mühendisliği bölümü Teknoloji Fakültesi bünyesindedir.",
    "ce_campus": (
        "Bilgisayar Mühendisliği, Alaeddin Keykubat Yerleşkesi'nde "
        "(Selçuklu/Konya) yer alır."
    ),
    "ce_accreditation": "Evet, Bilgisayar Mühendisliği programı MÜDEK akreditasyonuna sahiptir.",
    "ce_web": (
        "Bölüm web sitesi: "
        "https://www.selcuk.edu.tr/Birim/Bolum/teknoloji-bilgisayar_muhendisligi/15620"
    ),
    "ce_bologna": (
        "Bologna sistemi: "
        "https://bologna.selcuk.edu.tr/tr/dersler/"
        "teknoloji-bilgisayar_muhendisligi-bilgisayar_muhendisligi-lisans"
    ),
    "ce_yokatlas": "YÖK Atlas: https://yokatlas.yok.gov.tr/lisans.php?y=108911205",
    "ce_facebook": "Facebook: https://www.facebook.com/selcukteknolojibilgisayar/",
    "ce_program_code": "Bilgisayar Mühendisliği program kodu: 108911205.",
    "ce_language": "Bilgisayar Mühendisliği eğitim dili: Türkçe.",
    "ce_score_type": "Bilgisayar Mühendisliği puan türü: SAY (Sayısal).",
}

CRITICAL_ANSWERS_EN = {
    "location": (
        "Selçuk University is in **Konya**.\n\n"
        "Main campuses:\n"
        "- **Alaeddin Keykubat Campus** (Selçuklu/Konya)\n"
        "- **Ardıçlı Campus** (Karatay/Konya)"
    ),
    "foundation": "Selçuk University was founded in 1975 in Konya.",
    "address": (
        "Official address: Alaeddin Keykubat Campus, Akademi Mah. "
        "Yeni İstanbul St. No:369, 42130 Selçuklu/Konya"
    ),
    "phone": "Phone: +90 332 241 0041",
    "website": "Official website: https://www.selcuk.edu.tr/",
    "contact": (
        "Contact: +90 332 241 0041\n"
        "Web: https://www.selcuk.edu.tr/\n"
        "Address: Alaeddin Keykubat Campus, Akademi Mah. "
        "Yeni İstanbul St. No:369, 42130 Selçuklu/Konya"
    ),
    "rector": (
        "The Rector is Prof. Dr. Hüseyin Yılmaz "
        "(in office since 26 July 2024)."
    ),
    "faculty_count": "Selçuk University has 23 faculties.",
    "student_count": "Selçuk University has approximately 70,000 students.",
    "academic_units": (
        "Academic structure: 23 faculties, 7 institutes, 5 schools, "
        "1 state conservatory, 23 vocational schools, and 53 research centers."
    ),
    "ce_faculty": "The Computer Engineering department is in the Faculty of Technology.",
    "ce_campus": (
        "Computer Engineering is located at the Alaeddin Keykubat Campus "
        "(Selçuklu/Konya)."
    ),
    "ce_accreditation": "Yes, the Computer Engineering program is accredited by MÜDEK.",
    "ce_web": (
        "Department website: "
        "https://www.selcuk.edu.tr/Birim/Bolum/teknoloji-bilgisayar_muhendisligi/15620"
    ),
    "ce_bologna": (
        "Bologna system: "
        "https://bologna.selcuk.edu.tr/tr/dersler/"
        "teknoloji-bilgisayar_muhendisligi-bilgisayar_muhendisligi-lisans"
    ),
    "ce_yokatlas": "YÖK Atlas: https://yokatlas.yok.gov.tr/lisans.php?y=108911205",
    "ce_facebook": "Facebook: https://www.facebook.com/selcukteknolojibilgisayar/",
    "ce_program_code": "Computer Engineering program code: 108911205.",
    "ce_language": "Computer Engineering language of instruction: Turkish.",
    "ce_score_type": "Computer Engineering score type: SAY (Quantitative).",
}


def _apply_kb_overrides() -> None:
    data = _load_kb()
    if not data:
        return

    def to_str(value: Any) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, str):
            return value.strip()
        return str(value)

    uni = _find_kb_key(data, "universite_bilgileri")
    if isinstance(uni, dict):
        city = to_str(_find_kb_key(uni, "sehir") or _find_kb_key(uni, "il"))
        year = to_str(_find_kb_key(uni, "kurulus_yili"))
        address = to_str(_find_kb_key(uni, "adres"))
        phone = to_str(_find_kb_key(uni, "telefon"))
        website = to_str(_find_kb_key(uni, "web_sitesi"))
        rector = to_str(_find_kb_key(uni, "rektor"))
        faculty_count = to_str(_find_kb_key(uni, "fakulte_sayisi"))
        student_count = to_str(_find_kb_key(uni, "ogrenci_sayisi"))
        institute_count = to_str(_find_kb_key(uni, "enstitu_sayisi"))
        school_count = to_str(_find_kb_key(uni, "yuksekokul_sayisi"))
        conserv_count = to_str(_find_kb_key(uni, "devlet_konservatuvari_sayisi"))
        voc_count = to_str(_find_kb_key(uni, "meslek_yuksekokulu_sayisi"))
        research_count = to_str(_find_kb_key(uni, "arastirma_merkezi_sayisi"))

        campus_lines: list[str] = []
        campus_detail = _find_kb_key(data, "kampusler_detay")
        if isinstance(campus_detail, dict):
            for campus in campus_detail.values():
                if not isinstance(campus, dict):
                    continue
                name = to_str(_find_kb_key(campus, "ad"))
                location = to_str(_find_kb_key(campus, "konum"))
                if name and location:
                    campus_lines.append(f"- **{name}** ({location})")
                elif name:
                    campus_lines.append(f"- **{name}**")
        elif isinstance(_find_kb_key(uni, "kampusler"), list):
            for campus in _find_kb_key(uni, "kampusler"):
                name = to_str(campus)
                if name:
                    campus_lines.append(f"- **{name}**")

        if city:
            location_text = f"Selçuk Üniversitesi **{city}**'dadır."
            if campus_lines:
                location_text += "\n\nKampüsler:\n" + "\n".join(campus_lines)
            CRITICAL_ANSWERS_TR["location"] = location_text
        if year and city:
            CRITICAL_ANSWERS_TR["foundation"] = (
                f"Selçuk Üniversitesi {year} yılında {city}'da kurulmuştur."
            )
        elif year:
            CRITICAL_ANSWERS_TR["foundation"] = (
                f"Selçuk Üniversitesi {year} yılında kurulmuştur."
            )
        if address:
            CRITICAL_ANSWERS_TR["address"] = f"Resmi adres: {address}"
        if phone:
            CRITICAL_ANSWERS_TR["phone"] = f"Telefon: {phone}"
        if website:
            CRITICAL_ANSWERS_TR["website"] = f"Resmi web sitesi: {website}"
        if phone or website or address:
            parts = []
            if phone:
                parts.append(f"İletişim: {phone}")
            if website:
                parts.append(f"Web: {website}")
            if address:
                parts.append(f"Adres: {address}")
            if parts:
                CRITICAL_ANSWERS_TR["contact"] = "\n".join(parts)
        if rector:
            CRITICAL_ANSWERS_TR["rector"] = (
                f"Selçuk Üniversitesi Rektörü {rector}."
            )
        if faculty_count:
            CRITICAL_ANSWERS_TR["faculty_count"] = (
                f"Selçuk Üniversitesi'nde {faculty_count} fakülte bulunmaktadır."
            )
        if student_count:
            CRITICAL_ANSWERS_TR["student_count"] = (
                f"Selçuk Üniversitesi'nde yaklaşık {student_count} öğrenci bulunmaktadır."
            )
        if (
            faculty_count
            and institute_count
            and school_count
            and conserv_count
            and voc_count
            and research_count
        ):
            CRITICAL_ANSWERS_TR["academic_units"] = (
                "Akademik yapı: "
                f"{faculty_count} fakülte, {institute_count} enstitü, "
                f"{school_count} yüksekokul, {conserv_count} devlet konservatuvarı, "
                f"{voc_count} meslek yüksekokulu ve {research_count} araştırma merkezi."
            )

    ce = _find_kb_key(data, "bilgisayar_muhendisligi")
    if isinstance(ce, dict):
        faculty = to_str(_find_kb_key(ce, "fakulte"))
        campus = to_str(_find_kb_key(ce, "kampus") or _find_kb_key(ce, "yerleske"))
        location = to_str(_find_kb_key(ce, "konum"))
        program_code = to_str(_find_kb_key(ce, "program_kodu"))
        language = to_str(_find_kb_key(ce, "egitim_dili"))
        score_type = to_str(_find_kb_key(ce, "puan_turu"))
        web = to_str(_find_kb_key(ce, "web"))
        bologna = to_str(_find_kb_key(ce, "bologna_url"))
        yokatlas = to_str(_find_kb_key(ce, "yokatlas_url"))
        facebook = to_str(_find_kb_key(ce, "facebook_url"))

        accreditation = _find_kb_key(ce, "akreditasyon")
        mudek = None
        if isinstance(accreditation, dict):
            mudek = _find_kb_key(accreditation, "mudek")

        if faculty:
            CRITICAL_ANSWERS_TR["ce_faculty"] = (
                f"Bilgisayar Mühendisliği bölümü {faculty} bünyesindedir."
            )
        if campus or location:
            campus_text = "Bilgisayar Mühendisliği"
            if campus:
                campus_text += f", {campus}"
            if location:
                campus_text += f" ({location})"
            CRITICAL_ANSWERS_TR["ce_campus"] = campus_text + " yer alır."
        if isinstance(mudek, bool):
            if mudek:
                CRITICAL_ANSWERS_TR["ce_accreditation"] = (
                    "Evet, Bilgisayar Mühendisliği programı MÜDEK akreditasyonuna sahiptir."
                )
            else:
                CRITICAL_ANSWERS_TR["ce_accreditation"] = (
                    "Bilgisayar Mühendisliği programı MÜDEK akreditasyonuna sahip değildir."
                )
        if web:
            CRITICAL_ANSWERS_TR["ce_web"] = f"Bölüm web sitesi: {web}"
        if bologna:
            CRITICAL_ANSWERS_TR["ce_bologna"] = f"Bologna sistemi: {bologna}"
        if yokatlas:
            CRITICAL_ANSWERS_TR["ce_yokatlas"] = f"YÖK Atlas: {yokatlas}"
        if facebook:
            CRITICAL_ANSWERS_TR["ce_facebook"] = f"Facebook: {facebook}"
        if program_code:
            CRITICAL_ANSWERS_TR["ce_program_code"] = (
                f"Bilgisayar Mühendisliği program kodu: {program_code}."
            )
        if language:
            CRITICAL_ANSWERS_TR["ce_language"] = (
                f"Bilgisayar Mühendisliği eğitim dili: {language}."
            )
        if score_type:
            CRITICAL_ANSWERS_TR["ce_score_type"] = (
                f"Bilgisayar Mühendisliği puan türü: {score_type}."
            )


_apply_kb_overrides()


def _has_any(text: str, keywords: list[str]) -> bool:
    tokens = set(text.split())
    for keyword in keywords:
        if " " in keyword:
            if keyword in text:
                return True
        else:
            if keyword in tokens:
                return True
    return False


def classify_question(question: str) -> Optional[str]:
    normalized = _normalize(question)
    if not normalized:
        return None

    has_selcuk = "selcuk" in normalized
    has_university = "universite" in normalized or "university" in normalized

    # In conversation context, "Üniversite" alone often refers to Selçuk University
    # Allow foundation and location questions even without explicit "Selçuk" mention
    if _has_any(normalized, FOUNDATION_KEYWORDS) and has_university:
        return "foundation"
    if _has_any(normalized, LOCATION_KEYWORDS) and has_university:
        return "location"

    if has_selcuk and has_university:
        if _has_any(normalized, ADDRESS_KEYWORDS):
            return "address"
        if _has_any(normalized, CONTACT_KEYWORDS) and "fakulte" not in normalized:
            return "contact"
        if _has_any(normalized, PHONE_KEYWORDS) and "fakulte" not in normalized:
            return "phone"
        if _has_any(normalized, WEBSITE_KEYWORDS) and "fakulte" not in normalized:
            return "website"
        if _has_any(normalized, RECTOR_KEYWORDS):
            return "rector"
        if _has_any(normalized, FACULTY_COUNT_KEYWORDS):
            return "faculty_count"
        if _has_any(normalized, STUDENT_COUNT_KEYWORDS):
            return "student_count"
        if _has_any(normalized, ACADEMIC_UNITS_KEYWORDS):
            return "academic_units"

    if _has_any(normalized, CE_KEYWORDS):
        if _has_any(normalized, CE_BOLONYA_KEYWORDS):
            return "ce_bologna"
        if _has_any(normalized, CE_YOKATLAS_KEYWORDS):
            return "ce_yokatlas"
        if _has_any(normalized, CE_FACEBOOK_KEYWORDS):
            return "ce_facebook"
        if _has_any(normalized, CE_PROGRAM_CODE_KEYWORDS):
            return "ce_program_code"
        if _has_any(normalized, CE_LANGUAGE_KEYWORDS):
            return "ce_language"
        if _has_any(normalized, CE_SCORE_TYPE_KEYWORDS):
            return "ce_score_type"
        if _has_any(normalized, ACCREDITATION_KEYWORDS):
            return "ce_accreditation"
        # Yanlış fakülte ifadelerini kontrol et (örn. "Mühendislik Fakültesi")
        if _has_any(normalized, CE_FACULTY_KEYWORDS) or "muhendislik fakultesi" in normalized or "engineering faculty" in normalized:
            return "ce_faculty"
        if _has_any(normalized, CE_CAMPUS_KEYWORDS):
            return "ce_campus"
        if _has_any(normalized, CE_WEB_KEYWORDS):
            return "ce_web"

    return None


def is_greeting(question: str) -> bool:
    """Sorunun RAG gerektirmeyen basit bir selamlama olup olmadığını kontrol eder."""
    normalized = _normalize(question)
    if not normalized:
        return False
    
    greeting_keywords = [
        "merhaba", "selam", "hello", "hi", "hey", "gunaydin", "iyi gunler",
        "nasilsin", "nasil gidiyor", "how are you", "whats up"
    ]
    
    words = normalized.split()
    if len(words) <= 3 and any(kw in normalized for kw in greeting_keywords):
        return True
    
    return False


def is_selcuk_related(question: str) -> bool:
    normalized = _normalize(question)
    if not normalized:
        return False
    if "selcuk" in normalized and (
        "universite" in normalized or "university" in normalized
    ):
        return True
    return classify_question(question) is not None


def _contains_forbidden(text: str) -> bool:
    normalized = _normalize(text)
    if not normalized:
        return False
    if any(city in normalized for city in WRONG_CITY_KEYWORDS):
        return True
    if any(year in normalized for year in WRONG_YEAR_KEYWORDS):
        return True
    return False


def _filter_sentences(text: str) -> str:
    lines = text.splitlines()
    filtered_lines: list[str] = []
    for line in lines:
        if not line.strip():
            filtered_lines.append(line)
            continue

        bullet_match = re.match(r"^(\s*[-*]\s+)(.*)$", line)
        prefix = ""
        body = line
        if bullet_match:
            prefix = bullet_match.group(1)
            body = bullet_match.group(2)

        sentences = re.split(r"(?<=[.!?])\s+", body.strip())
        kept = [s for s in sentences if s and not _contains_forbidden(s)]
        if kept:
            filtered_lines.append(prefix + " ".join(kept))

    return "\n".join(filtered_lines).strip()


def get_critical_answer(question: str, language: str) -> Optional[str]:
    key = classify_question(question)
    if not key:
        return None
    if language.lower().startswith("en"):
        return CRITICAL_ANSWERS_EN.get(key)
    return CRITICAL_ANSWERS_TR.get(key)


def apply_guard(question: str, answer: str, language: str) -> tuple[str, bool]:
    critical = get_critical_answer(question, language)
    if critical:
        return critical, True

    if not is_selcuk_related(question):
        return answer, False

    filtered = _filter_sentences(answer)
    if filtered and filtered != answer:
        return filtered, True
    if not filtered:
        fallback = FALLBACK_EN if language.lower().startswith("en") else FALLBACK_TR
        return fallback, True
    return filtered, False
