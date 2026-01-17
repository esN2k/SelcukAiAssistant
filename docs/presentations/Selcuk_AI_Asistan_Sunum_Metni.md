# SELÇUK AI ASİSTAN - SUNUM METNİ
Doğukan BALAMAN (203311066) • Ali YILDIRIM (203311008) | Ocak 2025

---

## SAYFA 1-2: GİRİŞ

Merhaba, ben Doğukan ve ben de Ali. Bugün sizlere Selçuk AI Asistan projemizi sunacağız.

[Slide 1: Title göster]

Selçuk Üniversitesi, çok sayıda fakülte ve birime sahip büyük bir kurum. Bu büyüklük, bilgiye erişim süreçlerini zorlaştırıyor. Projemizin temel motivasyonu, bu dağınık bilgiyi tek bir akıllı asistan üzerinden erişilebilir hale getirmek.

[Slide 2: Agenda göster]

Sunumumuz altı bölümden oluşuyor: motivasyon, problem, çözüm yaklaşımı, teknik yapı, bulgular ve gelecek çalışmalar.

---

## SAYFA 3-4: PROBLEM VE ÇÖZÜM

[Slide 3: Üniversite büyüklüğü]

İlk problemimiz bilgi dağınıklığı. Fakülteler, enstitüler ve koordinatörlükler farklı alan adlarında içerik yayınlıyor. Bu da öğrencilerin güncel bilgiye ulaşmasını zorlaştırıyor.

[Slide 4: Problem 1]

İkinci problem, 7/24 destek ihtiyacı. Öğrenciler gece veya hafta sonu dahi yanıt alabilmek istiyor.

[Slide 5: Problem 2]

Çözümümüz, RAG tabanlı bir yapay zeka asistanı. Bu sistem, bilgi tabanından kaynak getirerek cevap üretiyor ve yanlış bilgi riskini azaltıyor.

[Slide 6: Çözüm]

---

## SAYFA 5-9: TEKNİK DETAYLAR

[Slide 7: Sistem Mimarisi]

Mimari 3 katmanlı: Flutter mobil uygulama, FastAPI backend ve FAISS tabanlı RAG + yerel LLM katmanı.

[Slide 8: Backend]

Backend Python/FastAPI üzerinde. RAG servisi FAISS indeksleme kullanıyor. Bilgi tabanımız 645 dokümana ulaştı. Yeniden kazıma sonuçları: 135 hatalı URL’den 92’si başarıyla çekildi, başarı oranı %68.15.

[Slide 9: Frontend]

Flutter ile tek kod tabanında iOS ve Android hedeflendi. GetX ile state yönetimi, SSE ile canlı yanıt akışı yapıldı.

[Slide 10: RAG Pipeline]

RAG akışı 7 adımda:
1. Kullanıcı sorusu alınır
2. Soru gömleme vektörüne çevrilir
3. FAISS ile benzer dokümanlar aranır
4. Top-4 doküman seçilir
5. Bağlam oluşturulur
6. LLM’ye gönderilir
7. Yanıt üretilir

Bu akış, kaynaklı cevap üretimini sağlar.

---

## SAYFA 10-12: SONUÇLAR

[Slide 14: Test Sonuçları]

Backend tarafında toplam 8 test dosyası bulunuyor. Testler hazırlanmış olup, çalışma ortamındaki bağımlılık kısıtları nedeniyle otomatik koşum bu aşamada yapılmadı.

[Slide 15: Performans]

Benchmark raporuna göre `ollama:llama3.2:3b` modeli için 12 örnek koşumda ortalama TTFT 5.18 sn ve ortalama toplam süre 8.643 sn olarak ölçülmüştür. Bu değerler proje dökümanında yer almaktadır.

[Slide 16-18: Ekran Görüntüleri]

Mobil uygulama ekranları: Splash, Chat ve Settings. Ayrıca yeni Translate ekranı uygulamaya eklenmiştir.

---

## SAYFA 13-14: GELECEK ÇALIŞMALAR

[Slide 21: Gelecek]

Kısa vadede hedefler:
1. TranslateGemma entegrasyonunun HF_TOKEN ve lisans onayı ile aktif hale gelmesi
2. Redis cache sistemi ile yanıt sürelerinin düşürülmesi
3. PostgreSQL analytics ile kullanım verilerinin raporlanması

Orta vadede:
- OBS entegrasyonu
- Yönetim paneli
- Ek veri kaynakları ve otomatik veri güncelleme

---

## SAYFA 15: SORU-CEVAP REHBERİ

**S: Neden Ollama tercih edildi?**
C: Yerel çalışabilme, veri gizliliği ve maliyet avantajları nedeniyle.

**S: Scraping neden %68?**
C: 36 subdomain DNS hatası veriyor ve bazı sayfalar HTTP 404/500 dönüyor. Bu hatalar kurum altyapısına bağlıdır.

**S: TranslateGemma neden çalışmıyor?**
C: HF_TOKEN ve lisans onayı gerektiriyor, altyapı hazır ancak manuel adım bekleniyor.

**S: Test sayısı neden az?**
C: Proje hızlı prototipleme aşamasında; kritik bileşenler için 8 test dosyası hazırlanmış durumda, genişletme planı var.

---

**SUNUM BİTİŞ**

[Slide 22: Teşekkürler]

Dinlediğiniz için teşekkürler. Sorularınızı bekliyoruz.
