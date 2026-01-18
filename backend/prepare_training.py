"""Q&A dataset oluşturma ve modeli eğitme hazırlığı."""
import json
from pathlib import Path
from datetime import datetime
from typing import Any, cast

from selcuk_data import QA_PAIRS, SELCUK_UNI_FACTS


def create_training_dataset(output_file: str = "data/selcuk_qa_dataset.jsonl"):
    """Modelfile için Q&A dataset oluştur."""
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # JSONL formatında kaydet (her satır bir JSON)
    with open(output_path, 'w', encoding='utf-8') as f:
        for qa in QA_PAIRS:
            # Ollama fine-tuning formatı
            entry = {
                "messages": [
                    {"role": "user", "content": qa["question"]},
                    {"role": "assistant", "content": qa["answer"]}
                ],
                "metadata": {
                    "category": qa["category"],
                    "source": "manuel_verified",
                    "created_at": datetime.now().isoformat(),
                }
            }
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"✅ Dataset oluşturuldu: {output_path}")
    print(f"📊 Toplam {len(QA_PAIRS)} soru-cevap çifti")
    return output_path


def create_rag_documents(output_dir: str = "data/rag/selcuk"):
    """RAG için doküman dosyaları oluştur."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Genel bilgiler
    with open(output_path / "01_genel_bilgiler.txt", 'w', encoding='utf-8') as f:
        f.write("# Selçuk Üniversitesi Genel Bilgiler\n\n")
        info = cast(dict[str, Any], SELCUK_UNI_FACTS["genel_bilgiler"])
        f.write(f"**Ad:** {info['ad']}\n")
        f.write(f"**Şehir:** {info['sehir']}\n")
        f.write(f"**Kuruluş Yılı:** {info['kurulus_yili']}\n")
        f.write(f"**Tip:** {info['tip']}\n")
        f.write(f"**Öğrenci Sayısı:** {info['ogrenci_sayisi']}\n")
        f.write(f"**Akademisyen Sayısı:** {info['akademisyen_sayisi']}\n\n")
        f.write(f"**Tarihçe:**\n{SELCUK_UNI_FACTS['tarihce']}\n")
    
    # Bilgisayar Mühendisliği
    with open(output_path / "02_bilgisayar_muhendisligi.txt", 'w', encoding='utf-8') as f:
        f.write("# Selçuk Üniversitesi Bilgisayar Mühendisliği Bölümü\n\n")
        bm = cast(dict[str, Any], SELCUK_UNI_FACTS["bilgisayar_muhendisligi"])
        f.write(f"**Fakülte:** {bm['fakulte']}\n")
        f.write(f"**Yerleşke:** {bm['yerleske']}\n")
        f.write(f"**Program Türleri:** {', '.join(bm['program_turu'])}\n")
        f.write(f"**Web Sitesi:** {bm['web']}\n")
        f.write(f"**E-posta:** {bm['email']}\n")
        f.write(f"**Adres:** {bm['adres']}\n\n")
        f.write("**Özellikler:**\n")
        for ozellik in bm['ozellikler']:
            f.write(f"- {ozellik}\n")
        f.write("\n**Araştırma Alanları:**\n")
        for alan in bm['arastirma_alanlari']:
            f.write(f"- {alan}\n")
        f.write("\n**Laboratuvarlar:**\n")
        for lab in bm['laboratuvarlar']:
            f.write(f"- {lab}\n")
    
    # Mühendislik Fakültesi
    with open(output_path / "03_muhendislik_fakultesi.txt", 'w', encoding='utf-8') as f:
        f.write("# Selçuk Üniversitesi Mühendislik Fakültesi\n\n")
        muh = cast(dict[str, Any], SELCUK_UNI_FACTS["muhendislik_fakultesi"])
        f.write(f"**Konum:** {muh['konum']}\n\n")
        f.write("**Bölümler:**\n")
        for bolum in muh['bolumler']:
            f.write(f"- {bolum}\n")
    
    # Q&A temelli dokümanlar
    with open(output_path / "04_sss.txt", 'w', encoding='utf-8') as f:
        f.write("# Selçuk Üniversitesi Sıkça Sorulan Sorular\n\n")
        for qa in QA_PAIRS:
            f.write(f"## {qa['question']}\n\n")
            f.write(f"{qa['answer']}\n\n")
            f.write("---\n\n")
    
    print(f"✅ RAG dokümanları oluşturuldu: {output_path}")
    print("📁 4 doküman dosyası")
    return output_path


def create_modelfile(model_name: str = "turkcell_llm_7b_selcuk"):
    """Özelleştirilmiş Modelfile oluştur."""
    modelfile_content = """FROM turkcell_llm_7b

# Selçuk Üniversitesi özel sistem promptu - FEW-SHOT LEARNING
SYSTEM \"\"\"SEN SELÇUK ÜNİVERSİTESİ AI ASİSTANISIN!

BU BİLGİLERİ EZBERLEMİŞ OLMALISIN:
Selçuk Üniversitesi = KONYA (1975)
Bilgisayar Mühendisliği = Teknoloji Fakültesi, Alaeddin Keykubat, KONYA
Kampüsler = Alaeddin Keykubat (Selçuklu/KONYA), Ardıçlı (Karatay/KONYA)
MÜDEK = Akreditasyon (Evet var)
HPC = High Performance Computing Lab

CEVAP ÖRNEKLERİ (BU ŞEKİLDE CEVAP VER):

Soru: Selçuk Üniversitesi nerede?
Cevap: Selçuk Üniversitesi Konya'dadır.

Soru: Ne zaman kuruldu?
Cevap: 1975 yılında kurulmuştur.

Soru: Kampüsler hangileri?
Cevap: Alaeddin Keykubat Yerleşkesi ve Ardıçlı Yerleşkesi olmak üzere iki ana kampüs bulunmaktadır.

Soru: Bilgisayar Mühendisliği hangi fakültede?
Cevap: Teknoloji Fakültesi bünyesindedir.

Soru: Akredite mi?
Cevap: Evet, MÜDEK akreditasyonuna sahiptir.

Soru: HPC nedir?
Cevap: High Performance Computing (Yüksek Başarımlı Hesaplama) laboratuvarıdır.

Soru: Erasmus var mı?
Cevap: Evet, Erasmus+ değişim programı mevcuttur.

ÖNEMLİ: Kısa sorularda da bağlamı anla. "Kampüsler?" sorusu Selçuk Üniversitesi kampüslerini soruyor demektir.
\"\"\"

# Parametreler - Daha deterministik cevaplar için
PARAMETER temperature 0.1
PARAMETER top_p 0.5
PARAMETER top_k 10
PARAMETER repeat_penalty 1.15

# Stop tokens
PARAMETER stop "<|im_start|>"
PARAMETER stop "<|im_end|>"
"""
    
    modelfile_path = Path(f"Modelfile.{model_name}")
    with open(modelfile_path, 'w', encoding='utf-8') as f:
        f.write(modelfile_content)
    
    print(f"✅ Modelfile oluşturuldu: {modelfile_path}")
    print("\n🔨 Modeli oluşturmak için:")
    print(f"   ollama create {model_name} -f Modelfile.{model_name}")
    return modelfile_path


if __name__ == "__main__":
    print("🚀 Selçuk Üniversitesi AI Model Geliştirme\n")
    
    # 1. Training dataset
    dataset_file = create_training_dataset()
    
    # 2. RAG dokümanları
    rag_dir = create_rag_documents()
    
    # 3. Modelfile
    modelfile = create_modelfile()
    
    print("\n" + "="*60)
    print("✅ TÜM DOSYALAR HAZIR!")
    print("="*60)
    print("\n📋 Sonraki Adımlar:")
    print("1. Web scraping çalıştır: python backend/scrape_selcuk_edu.py")
    print("2. RAG index oluştur: python backend/rag_ingest.py data/rag/selcuk")
    print("3. Modeli özelleştir: ollama create turkcell_llm_7b_selcuk -f backend/Modelfile.turkcell_llm_7b_selcuk")
    print("4. Backend'de yeni modeli varsayılan yap")
