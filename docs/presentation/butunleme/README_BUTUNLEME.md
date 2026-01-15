# Bütünleme Sunumu Notları (Öğrenci Anlatımı)

Bu metin, final sunumundan kaldıktan sonra (6c5a7ff1... sonrası) son 2-3 günde Copilot desteğiyle yaptığımız düzeltmeleri **öğrenci gözüyle** özetler. Amaç: jüriye tekrar çıktığımızda aynı hataları yapmamak ve güvenilir, kaynaklı cevap üretmek.

## Neden kaldık?
Finalde tek bir kritik soru soruldu: **"Selçuk Üniversitesi nerede?"**
Model **İzmir** dedi. Bu, sistemin güvenilirliğini kırdı ve sunum başarısız oldu.

## Hedefimiz
- Kritik bilgileri **%100 doğru** vermek.
- Kaynak yoksa **"bilmiyorum"** diyebilmek.
- RAG cevaplarının **kaynakla uyumlu** olmasını sağlamak.
- Demo sırasında net ve kısa yanıtlar üretmek.

## 2-3 Günlük Düzeltme Süreci (Copilot ile)
1. **Kritik doğruluk koruması kurduk**: Konya, 1975, kampüsler gibi bilgiler kanonik cevap haline getirildi.
2. **RAG doğru değilse cevap yok** kuralı getirildi: Kaynak dışı cümleler filtreleniyor.
3. **Veri tabanını güncelledik**: adres, telefon, rektör, öğrenci sayısı ve bölüm linkleri eklendi.
4. **Testleri genişlettik**: kritik sorular ve RAG guard testleri eklendi.
5. **RAG indeks yenilemeyi otomatikleştirdik**: manuel unutma riski kalktı.

## Teknik Olarak Neleri Değiştirdik?
- **Kritik soru koruması**: yanlış şehir/yıl engelleniyor; doğru cevap zorunlu.
- **RAG guard**: soru–kaynak uyumu kontrolü + cümle bazlı kaynak filtreleme.
- **"Kaynak yoksa cevap verme"**: otomatik fallback mesajı.
- **Prompt güncellemesi**: doğrulanmış resmi bilgiler sabitlendi.
- **RAG veri güncellemesi**: JSON ve TXT kaynaklar yenilendi.
- **Testler**: `test_critical_guard.py`, `test_rag_guard.py`.

## Demo Akışı (Bütünleme İçin)
- **Kritik soru**: "Selçuk Üniversitesi nerede?" → **Konya + kampüsler**
- **Bilinmeyen soru**: "Mars'ta yaşam var mı?" → **"Bu bilgi kaynaklarda yok. Bu konuda kesin bilgiye sahip değilim."**
- **Bölüm soruları**: Bilgisayar Müh. fakülte, program kodu, Bologna linki

## RAG İndeks Yenileme
Doküman güncellenince aşağıdaki komutla indeks yenilenir:
```bash
python backend/rag_ingest.py --input backend/data/rag/selcuk --output backend/data/rag --reset
```

## Otomasyon (CI)
- **GitHub Actions** her gün **02:00 TR** çalışır.
- RAG indeksini yeniler ve `main` dalına commit eder.
- Commit mesajında `[skip ci]` var, gereksiz CI tetiklenmez.

## Kalan Riskler
- RAG dokümanları güncellenmezse bilgi eski kalır.
- Branch protection açık ise Actions için push izni gerekir.
- Model kalitesi düşükse kritik dışı sorularda RAG şarttır.

## Kısa Sonuç
Finalde tek bir yanlış cevapla kaldık. Bütünleme için sistem artık:
- **kritik bilgileri doğru veriyor**,
- **bilmediği konuda "bilmiyorum" diyebiliyor**,
- **RAG kaynaklarına göre cevap üretiyor**.

Bu yüzden bütünleme sunumuna hazırız.
