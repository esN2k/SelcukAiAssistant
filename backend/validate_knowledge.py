"""Kritik bilgilerin doğruluğunu test eden script.

Bu script, Selçuk Üniversitesi hakkında kritik soruların
doğru yanıtlandığını kontrol eder.
"""
import json
import sys
from pathlib import Path


# Kritik bilgi validasyonları
CRITICAL_FACTS = {
    "konum": {
        "doğru": ["konya", "selçuklu", "karatay"],
        "yanlış": ["izmir", "ankara", "istanbul", "bursa"],
        "test_soruları": [
            "Selçuk Üniversitesi nerede?",
            "Selçuk Üniversitesi hangi şehirde?",
            "Selçuk Üniversitesi hangi ilde?",
        ]
    },
    "kuruluş_yılı": {
        "doğru": ["1975"],
        "yanlış": ["1976", "1974", "1980", "1970"],
        "test_soruları": [
            "Selçuk Üniversitesi ne zaman kuruldu?",
            "Selçuk Üniversitesi kaç yılında kuruldu?",
            "Kuruluş yılı nedir?",
        ]
    },
    "bilgisayar_muhendisligi": {
        "doğru": ["teknoloji fakültesi", "alaeddin keykubat"],
        "yanlış": ["mühendislik fakültesi", "ardıçlı"],
        "test_soruları": [
            "Bilgisayar Mühendisliği hangi fakültede?",
            "Bilgisayar Mühendisliği hangi kampusta?",
        ]
    },
    "akreditasyon": {
        "doğru": ["müdek", "evet", "var"],
        "yanlış": ["hayır", "yok"],
        "test_soruları": [
            "Bilgisayar Mühendisliği akredite mi?",
            "MÜDEK akreditasyonu var mı?",
        ]
    }
}


def validate_knowledge_base():
    """Knowledge base dosyasındaki kritik bilgileri kontrol eder."""
    kb_path = Path(__file__).parent / "data" / "selcuk_knowledge_base.json"
    
    if not kb_path.exists():
        print(f"❌ HATA: {kb_path} bulunamadı!")
        return False
    
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    errors = []
    
    # Konum kontrolü
    sehir = kb.get("universite_bilgileri", {}).get("şehir", "").lower()
    if sehir != "konya":
        errors.append(f"❌ Şehir yanlış: '{sehir}' olmalı 'konya'")
    else:
        print(f"✅ Şehir doğru: {sehir.upper()}")
    
    # Kuruluş yılı kontrolü
    yil = kb.get("universite_bilgileri", {}).get("kuruluş_yılı")
    if yil != 1975:
        errors.append(f"❌ Kuruluş yılı yanlış: {yil} olmalı 1975")
    else:
        print(f"✅ Kuruluş yılı doğru: {yil}")
    
    # Bilgisayar Mühendisliği fakültesi kontrolü
    bm_fakulte = kb.get("bilgisayar_muhendisligi", {}).get("fakulte", "").lower()
    if "teknoloji" not in bm_fakulte:
        errors.append(f"❌ Bilgisayar Müh. fakültesi yanlış: '{bm_fakulte}' olmalı 'Teknoloji Fakültesi'")
    else:
        print(f"✅ Bilgisayar Müh. fakültesi doğru: {kb['bilgisayar_muhendisligi']['fakulte']}")
    
    # MÜDEK kontrolü
    mudek = kb.get("bilgisayar_muhendisligi", {}).get("akreditasyon", {}).get("mudek", False)
    if not mudek:
        errors.append("❌ MÜDEK akreditasyonu eksik veya yanlış")
    else:
        print("✅ MÜDEK akreditasyonu doğru: Var")
    
    if errors:
        print("\n❌ HATALAR:")
        for error in errors:
            print(f"  {error}")
        return False
    
    print("\n✅ Tüm kritik bilgiler doğru!")
    return True


def validate_response(question: str, answer: str, category: str) -> bool:
    """Bir yanıtın doğru olup olmadığını kontrol eder."""
    answer_lower = answer.lower()
    
    if category not in CRITICAL_FACTS:
        return True  # Bilinen kategori değilse geç
    
    rules = CRITICAL_FACTS[category]
    
    # Yanlış kelimeler var mı kontrol et
    for yanlis in rules["yanlış"]:
        if yanlis in answer_lower:
            print("❌ YANLIŞ BİLGİ tespit edildi!")
            print(f"   Soru: {question}")
            print(f"   Yanıt: {answer}")
            print(f"   Sorun: '{yanlis}' kelimesi bulunmamalı!")
            return False
    
    # Doğru kelimelerden en az biri var mı kontrol et
    has_correct = any(dogru in answer_lower for dogru in rules["doğru"])
    if not has_correct:
        print("⚠️  UYARI: Yanıtta beklenen kelimeler bulunamadı!")
        print(f"   Soru: {question}")
        print(f"   Yanıt: {answer}")
        print(f"   Beklenen kelimelerden biri: {', '.join(rules['doğru'])}")
        return False
    
    return True


def test_critical_responses():
    """Kritik soruların yanıtlarını test eder."""
    print("\n" + "="*60)
    print("KRİTİK SORULAR TESTİ")
    print("="*60)
    
    # Bu gerçek API testi yapacak şekilde genişletilebilir
    # Şimdilik knowledge base'i kontrol ediyoruz
    
    kb_path = Path(__file__).parent / "data" / "selcuk_knowledge_base.json"
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    # SSS'leri kontrol et
    sss = kb.get("sık_sorulan_sorular", [])
    
    passed = 0
    failed = 0
    
    for qa in sss:
        soru = qa.get("soru", "")
        cevap = qa.get("cevap", "")
        
        # Kategoriye göre validasyon
        if "nerede" in soru.lower() or "hangi şehir" in soru.lower() or "hangi il" in soru.lower():
            if validate_response(soru, cevap, "konum"):
                passed += 1
                print(f"✅ {soru}")
            else:
                failed += 1
        elif "kuruldu" in soru.lower() or "kuruluş" in soru.lower():
            if validate_response(soru, cevap, "kuruluş_yılı"):
                passed += 1
                print(f"✅ {soru}")
            else:
                failed += 1
        elif "bilgisayar" in soru.lower() and "fakülte" in soru.lower():
            if validate_response(soru, cevap, "bilgisayar_muhendisligi"):
                passed += 1
                print(f"✅ {soru}")
            else:
                failed += 1
        elif "akredite" in soru.lower() or "müdek" in soru.lower():
            if validate_response(soru, cevap, "akreditasyon"):
                passed += 1
                print(f"✅ {soru}")
            else:
                failed += 1
    
    print(f"\n📊 Sonuç: {passed} başarılı, {failed} başarısız")
    return failed == 0


def main():
    """Ana test fonksiyonu."""
    print("="*60)
    print("SELÇUK ÜNİVERSİTESİ AI ASİSTANI - DOĞRULUK TESTİ")
    print("="*60)
    
    # Knowledge base validasyonu
    print("\n1️⃣  Knowledge Base Kontrolü")
    print("-" * 60)
    kb_valid = validate_knowledge_base()
    
    # Kritik soru-cevap testleri
    print("\n2️⃣  Soru-Cevap Kontrolü")
    print("-" * 60)
    qa_valid = test_critical_responses()
    
    # Sonuç
    print("\n" + "="*60)
    if kb_valid and qa_valid:
        print("✅ TÜM TESTLER BAŞARILI!")
        print("="*60)
        return 0
    else:
        print("❌ TESTLER BAŞARISIZ!")
        print("="*60)
        print("\nLütfen yukarıdaki hataları düzeltin!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
