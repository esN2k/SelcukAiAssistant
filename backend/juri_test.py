"""
JURI SUNUM KALITE TESTI - 31 Soru
"""
import sys
import requests
import json
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

API_URL = "http://localhost:8000"

# Test sorulari ve beklenen anahtar kelimeler
TEST_CASES = [
    # Akademik Takvim (5 soru)
    {"q": "2024-2025 akademik takvimi ne zaman basliyor?", "keywords": ["eylul", "2024", "09"], "category": "Akademik Takvim"},
    {"q": "Final sinavlari ne zaman?", "keywords": ["aralik", "ocak", "2025"], "category": "Akademik Takvim"},
    {"q": "Vize sinavlari hangi donemde?", "keywords": ["ekim", "kasim", "hafta"], "category": "Akademik Takvim"},
    {"q": "Bahar donemi kayitlari ne zaman?", "keywords": ["ocak", "subat", "2025"], "category": "Akademik Takvim"},
    {"q": "Ortak zorunlu dersler final tarihi ne?", "keywords": ["06", "ocak", "2025"], "category": "Akademik Takvim"},
    
    # Harc (3 soru)
    {"q": "Harc ucreti ne kadar?", "keywords": ["ogretim", "harc"], "category": "Harc"},
    {"q": "1. ogretim harc oder mi?", "keywords": ["hayir", "yok", "odeme"], "category": "Harc"},
    {"q": "Muhendislik fakultesi 2. ogretim harc ne kadar?", "keywords": ["tl", "lira", "ucret"], "category": "Harc"},
    
    # Mufredat (5 soru)
    {"q": "Bilgisayar Muhendisligi kac donem?", "keywords": ["8", "donem", "yariyil"], "category": "Mufredat"},
    {"q": "Yapay Zeka dersi kacinci donem?", "keywords": ["6", "donem"], "category": "Mufredat"},
    {"q": "Onur Inan hangi dersleri veriyor?", "keywords": ["staj", "bulut"], "category": "Mufredat"},
    {"q": "Toplam kac AKTS gerekli?", "keywords": ["240", "akts"], "category": "Mufredat"},
    {"q": "Secmeli dersler hangi donemde basliyor?", "keywords": ["5", "donem"], "category": "Mufredat"},
    
    # Not Sistemi (5 soru)
    {"q": "DD notu ile gecebilir miyim?", "keywords": ["agno", "2.00", "ortalama"], "category": "Not Sistemi"},
    {"q": "AGNO nasil hesaplanir?", "keywords": ["kredi", "not", "toplam"], "category": "Not Sistemi"},
    {"q": "CC notu kac puan?", "keywords": ["70", "74", "puan"], "category": "Not Sistemi"},
    {"q": "Mezun olmak icin minimum AGNO?", "keywords": ["2.00", "agno"], "category": "Not Sistemi"},
    {"q": "Devamsizlik siniri nedir?", "keywords": ["30", "devam"], "category": "Not Sistemi"},
    
    # Staj (5 soru)
    {"q": "Staj kac gun?", "keywords": ["40", "gun", "20"], "category": "Staj"},
    {"q": "STAJ-1 ne zaman yapilir?", "keywords": ["yazilim", "yaz"], "category": "Staj"},
    {"q": "Staj koordinatoru kim?", "keywords": ["onur", "inan"], "category": "Staj"},
    {"q": "SGK zorunlu mu?", "keywords": ["evet", "zorunlu", "sgk"], "category": "Staj"},
    {"q": "40 gun tek staj yapabilir miyim?", "keywords": ["hayir", "20", "iki"], "category": "Staj"},
    
    # Genel Bilgi (5 soru)
    {"q": "Ders kayit nasil yapilir?", "keywords": ["obs", "kayit", "sistem"], "category": "Genel"},
    {"q": "Danismanim kim?", "keywords": ["danisman", "bolum"], "category": "Genel"},
    {"q": "Fakulte nerede?", "keywords": ["konya", "kampus", "selcuk"], "category": "Genel"},
    {"q": "Teknoloji Fakultesi telefon numarasi?", "keywords": ["0332", "telefon"], "category": "Genel"},
    {"q": "Bologna sistemi nedir?", "keywords": ["avrupa", "akts", "kredi"], "category": "Genel"},
    
    # Kayit/Islemler (3 soru)
    {"q": "Ders ekleme-cikarma ne zaman?", "keywords": ["eylul", "subat", "kayit"], "category": "Kayit"},
    {"q": "Mazeretli gec kayit tarihleri?", "keywords": ["ekim", "mart", "mazeret"], "category": "Kayit"},
    {"q": "Yaz okulu var mi?", "keywords": ["evet", "yaz", "temmuz"], "category": "Kayit"},
]

def test_chat(question):
    """Backend'e soru gonder ve cevap al"""
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={
                "messages": [{"role": "user", "content": question}],
                "temperature": 0.3,
                "max_tokens": 500
            },
            timeout=120
        )
        if response.status_code == 200:
            data = response.json()
            # answer veya message alanini kontrol et
            answer = data.get("answer", data.get("message", ""))
            return answer
        else:
            return f"HATA: {response.status_code} - {response.text[:100]}"
    except requests.exceptions.Timeout:
        return "HATA: Timeout (120s)"
    except Exception as e:
        return f"HATA: {e}"

def check_keywords(answer, keywords):
    """Cevap icinde anahtar kelime kontrolu"""
    answer_lower = answer.lower()
    found = []
    missing = []
    for kw in keywords:
        if kw.lower() in answer_lower:
            found.append(kw)
        else:
            missing.append(kw)
    return len(found) > 0, found, missing

def main():
    print("="*70)
    print("JURI SUNUM KALITE TESTI")
    print(f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*70)
    
    results = {"basarili": 0, "basarisiz": 0, "hata": 0}
    category_results = {}
    failed_tests = []
    
    for i, test in enumerate(TEST_CASES, 1):
        q = test["q"]
        keywords = test["keywords"]
        category = test["category"]
        
        if category not in category_results:
            category_results[category] = {"basarili": 0, "toplam": 0}
        category_results[category]["toplam"] += 1
        
        print(f"\n[{i}/{len(TEST_CASES)}] {q}")
        
        answer = test_chat(q)
        
        if answer.startswith("HATA"):
            print(f"  X HATA: {answer}")
            results["hata"] += 1
            failed_tests.append({"q": q, "reason": answer, "category": category})
        else:
            success, found, missing = check_keywords(answer, keywords)
            if success:
                print(f"  + BASARILI (bulundu: {found})")
                results["basarili"] += 1
                category_results[category]["basarili"] += 1
            else:
                print(f"  - BASARISIZ (eksik: {missing})")
                print(f"    Cevap: {answer[:150]}...")
                results["basarisiz"] += 1
                failed_tests.append({"q": q, "reason": f"Eksik: {missing}", "category": category, "answer": answer[:200]})
    
    # Ozet
    total = len(TEST_CASES)
    basari_orani = (results["basarili"] / total) * 100
    
    print("\n" + "="*70)
    print("SONUC OZETI")
    print("="*70)
    print(f"Toplam Test: {total}")
    print(f"Basarili: {results['basarili']} ({basari_orani:.1f}%)")
    print(f"Basarisiz: {results['basarisiz']}")
    print(f"Hata: {results['hata']}")
    
    print("\nKATEGORI BAZINDA:")
    for cat, res in category_results.items():
        cat_oran = (res["basarili"] / res["toplam"]) * 100 if res["toplam"] > 0 else 0
        status = "OK" if cat_oran >= 60 else "DUSUK"
        print(f"  {cat}: {res['basarili']}/{res['toplam']} ({cat_oran:.0f}%) [{status}]")
    
    if failed_tests:
        print("\nBASARISIZ TESTLER:")
        for ft in failed_tests[:10]:
            print(f"  - [{ft['category']}] {ft['q']}")
            print(f"    Sebep: {ft['reason']}")
    
    print("\n" + "="*70)
    if basari_orani >= 85:
        print("SONUC: MUKEMMEL! Juriye hazir.")
    elif basari_orani >= 70:
        print("SONUC: IYI. Kucuk iyilestirmeler gerekebilir.")
    elif basari_orani >= 50:
        print("SONUC: ORTA. Optimizasyon gerekli.")
    else:
        print("SONUC: DUSUK. Acil mudahale gerekli!")
    print("="*70)
    
    return basari_orani

if __name__ == "__main__":
    main()
