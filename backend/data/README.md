# Selçuk Üniversitesi Bilgi Tabanı

## 📚 Genel Bakış

Bu dizin, Selçuk Üniversitesi Yapay Zeka Asistanı için doğrulanmış bilgi kaynaklarını içerir.

## 📁 Dosya Yapısı

```
data/
├── selcuk_knowledge_base.json  # Ana bilgi tabanı (JSON format)
├── selcuk_qa_dataset.jsonl     # Soru-cevap eğitim veri seti
└── rag/                        # RAG (Geri Getirim Destekli Üretim) dokümanları
    ├── index.faiss             # FAISS vektör indeksi
    ├── metadata.json           # Doküman üstverisi
    └── selcuk/                 # Kaynak dokümanlar
        ├── 01_genel_bilgiler.txt
        ├── 02_bilgisayar_muhendisligi.txt
        ├── 03_muhendislik_fakultesi.txt
        ├── 04_sss.txt
        └── 05_bilgisayar_web.txt
```

## 🎯 selcuk_knowledge_base.json

En güncel ve doğrulanmış Selçuk Üniversitesi bilgilerini içeren ana kaynak.

### İçerik:
- ✅ Üniversite genel bilgileri (konum: **KONYA**, kuruluş: **1975**)
- ✅ Kampüs bilgileri (Alaeddin Keykubat, Ardıçlı)
- ✅ Fakülteler ve bölümler
- ✅ Bilgisayar Mühendisliği detaylı bilgiler
- ✅ Akademik takvim
- ✅ İletişim bilgileri
- ✅ Sık sorulan sorular (SSS)
- ✅ Ulaşım bilgileri
- ✅ Sosyal olanaklar

### Kullanım:

```python
import json

# Bilgi tabanını yükle
with open('data/selcuk_knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)

# Konum bilgisine eriş
print(kb['universite_bilgileri']['şehir'])  # Çıktı: Konya

# SSS'lere eriş
for qa in kb['sık_sorulan_sorular']:
    print(f"S: {qa['soru']}")
    print(f"C: {qa['cevap']}\n")
```

## 📝 selcuk_qa_dataset.jsonl

Model ince ayar için hazırlanmış soru-cevap çiftleri.

### Format:
```jsonl
{"messages": [{"role": "user", "content": "Soru"}, {"role": "assistant", "content": "Cevap"}], "metadata": {...}}
```

### Kullanım:
```python
import json

with open('data/selcuk_qa_dataset.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        qa = json.loads(line)
        print(qa['messages'])
```

## 🔍 RAG Dokümanları

Yapay zeka asistanın kaynak gösterimli yanıtlar üretmesi için kullanılan doküman seti.

### Güncelleme:

```bash
# 1. RAG dokümanlarını yeniden oluştur
cd backend
python prepare_training.py

# 2. FAISS indeksini yeniden oluştur
python rag_ingest.py --input data/rag/selcuk --output data/rag

# 3. Arka ucu yeniden başlat
uvicorn main:app --reload
```

## ✅ Doğruluk Kontrolü

Kritik bilgilerin doğruluğunu kontrol etmek için:

```bash
cd backend
python validate_knowledge.py
```

Bu betik şunları kontrol eder:
- ✅ Konum bilgisi (KONYA olmalı, İzmir DEĞİL!)
- ✅ Kuruluş yılı (1975)
- ✅ Bilgisayar Mühendisliği fakültesi (Teknoloji Fakültesi)
- ✅ MÜDEK akreditasyonu

**Beklenen Çıktı:**
```
✅ TÜM TESTLER BAŞARILI!
```

## 🚨 Kritik Bilgiler

**ASLA YANLIŞ VERİLMEMESİ GEREKEN BİLGİLER:**

| Bilgi | Doğru Değer | Yanlış Örnekler |
|-------|-------------|-----------------|
| Konum | **KONYA** | İzmir, Ankara, vb. |
| Kuruluş Yılı | **1975** | 1976, 1974, vb. |
| Bilg. Müh. Fakültesi | **Teknoloji Fakültesi** | Mühendislik Fakültesi |
| MÜDEK | **Var** | Yok |

## 🔄 Güncelleme Süreci

1. **Bilgi Toplama**: Resmi kaynaklardan (selcuk.edu.tr) güncel bilgi topla
2. **Doğrulama**: Bilgileri çapraz kontrol et
3. **JSON Güncelleme**: `selcuk_knowledge_base.json` dosyasını güncelle
4. **Doğrulama**: `python validate_knowledge.py` çalıştır
5. **RAG Güncelleme**: RAG dokümanlarını ve indeksini yeniden oluştur
6. **Test**: Yapay zeka asistana kritik soruları sor, yanıtları kontrol et

## 📊 İstatistikler

- **Toplam SSS**: 17+ soru-cevap
- **Fakülte Sayısı**: 23
- **Kampüs Sayısı**: 2 (Alaeddin Keykubat, Ardıçlı)
- **RAG Doküman Sayısı**: 5 dosya

## 🔗 Kaynaklar

- [Selçuk Üniversitesi Resmi Web Sitesi](https://www.selcuk.edu.tr)
- [Teknoloji Fakültesi](https://www.selcuk.edu.tr/teknoloji)
- [Bilgisayar Mühendisliği](https://www.selcuk.edu.tr/Birim/Bolum/teknoloji-bilgisayar_muhendisligi/15620)

## 🛠️ Bakım

Bu bilgi tabanı düzenli olarak güncellenmeli:
- Her akademik yıl başında (Akademik takvim)
- Yeni fakülte/bölüm eklendiğinde
- İletişim bilgileri değiştiğinde
- Rektör veya dekan değişikliklerinde

---

**Son Güncelleme**: 2026-01-04
**Sorumlu**: Yapay Zeka Asistan Geliştirme Ekibi
