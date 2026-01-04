"""Model test scripti - Çeşitli sorularla modeli test et."""
import subprocess
import json

TEST_QUESTIONS = [
    # Konum ve Genel Bilgiler
    "Selçuk Üniversitesi nerede?",
    "Selçuk Üniversitesi hangi şehirde?",
    "Selçuk Üniversitesi ne zaman kuruldu?",
    "Selçuk Üniversitesi kaç yılında kuruldu?",
    "Kampüsler hangileri?",
    "Alaeddin Keykubat Yerleşkesi nerede?",
    
    # Bilgisayar Mühendisliği
    "Bilgisayar Mühendisliği hangi fakültede?",
    "Bilgisayar Mühendisliği bölümü nerede?",
    "Bilgisayar Mühendisliği akredite mi?",
    "Bilgisayar Mühendisliği hangi yerleşkede?",
    "Bilgisayar Mühendisliği email adresi nedir?",
    "HPC nedir?",
    "Erasmus programı var mı?",
    
    # Teknoloji Fakültesi
    "Teknoloji Fakültesi nerede?",
    "Teknoloji Fakültesi hangi bölümler var?",
    "Teknoloji Fakültesi dekanlık telefonu?",
    
    # Araştırma ve Eğitim
    "Çift anadal programı var mı?",
    "Lisansüstü programlar var mı?",
    "Kariyer ofisi var mı?",
    "Konya Teknokent ile işbirliği var mı?",
]

def test_model(question: str, model: str = "turkcell_llm_7b_selcuk") -> dict:
    """Modele soru sor ve cevabı al."""
    try:
        result = subprocess.run(
            ["ollama", "run", model, question],
            capture_output=True,
            text=True,
            timeout=30,
            encoding='utf-8'
        )
        return {
            "question": question,
            "answer": result.stdout.strip(),
            "success": result.returncode == 0
        }
    except Exception as e:
        return {
            "question": question,
            "answer": f"HATA: {e}",
            "success": False
        }

def main():
    print("🧪 Model Test Başlıyor...\n")
    print("="*80)
    
    results = []
    for i, question in enumerate(TEST_QUESTIONS, 1):
        print(f"\n[{i}/{len(TEST_QUESTIONS)}] ❓ {question}")
        result = test_model(question)
        results.append(result)
        
        if result['success']:
            print(f"✅ {result['answer']}")
        else:
            print(f"❌ {result['answer']}")
        
        print("-" * 80)
    
    # Özet
    print("\n" + "="*80)
    print("📊 TEST ÖZET")
    print("="*80)
    successful = sum(1 for r in results if r['success'])
    print(f"Başarılı: {successful}/{len(TEST_QUESTIONS)}")
    
    # JSON'a kaydet
    with open('test_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("\n💾 Sonuçlar kaydedildi: test_results.json")

if __name__ == "__main__":
    main()
