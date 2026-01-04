# Konuşmacı Notları (SPEAKER_NOTES)

## SLAYT 1: KAPAK
- Proje adı ve kapsam: Selçuk Üniversitesi’ne özel yerel yapay zeka asistanı.
- Katkı: CONTRIBUTORS.md’de tek geliştirici esN2k görünüyor.
- Tarih: 04.01.2026.
- Gizlilik ve yerel çalışma motivasyonu bir cümlede özetlenir.

## SLAYT 2: İÇİNDEKİLER
- 10 dakikalık akış: problem → çözüm → teknoloji → test → sonuç.
- Kaynaklar slaytı sunum sınırı dışında.

## SLAYT 3: PROJE ÖZETİ
- README.md: gizliliğe odaklı yerel LLM + RAG yaklaşımı.
- Flutter istemci + FastAPI arka uç birleşimi.
- /chat ve /chat/stream ile hem tek yanıt hem akışlı yanıt.
- Ollama birincil sağlayıcı, HF opsiyonel.

## SLAYT 4: PROBLEM TANIMI
- Bilgiler dağınık, doğru bilgiye erişim güç.
- 7/24 destek yok; tekrar eden sorular idari yük oluşturuyor.
- Bulut API kullanımı gizlilik riski doğuruyor.
- Bilgi tabanı verisine göre öğrenci sayısı 100.000+.

## SLAYT 5: AMAÇ VE HEDEFLER
- Yerel LLM ile veri gizliliği (README.md).
- RAG ile kaynaklı yanıt ve katı mod (docs/technical/RAG.md).
- TR/EN dil desteği (l10n dosyaları).
- Sağlayıcı Deseni ile esneklik (backend/providers/).
- SSE akışı ile hızlı algılanan yanıt.

## SLAYT 6: LİTERATÜR / MEVCUT ÇÖZÜMLER
- RAG literatürü: Lewis et al., 2020.
- Üniversite sohbet botları ve SSS sistemleri genel yaklaşım.
- Bu projede fark: yerel LLM + doğrulanmış bilgi tabanı + atıflar (`citations`).

## SLAYT 7: METODOLOJİ
- Veri toplama: tools/collect_sources.py.
- Bilgi tabanı ve soru-cevap veri seti: backend/data.
- RAG içe aktarma: rag_ingest.py, FAISS indeks.
- Arka uç: FastAPI + sağlayıcı deseni.
- Ön uç: Flutter + GetX + Hive.
- Test/Kıyaslama: pytest/ruff/mypy, benchmark/run.py.

## SLAYT 8: SİSTEM MİMARİSİ
- Flutter → FastAPI → Ollama/HF.
- RAG: FAISS + metadata (üstveri), katı mod destekli.
- SSE: /chat/stream ile belirteç akışı.

## SLAYT 9: KULLANILAN TEKNOLOJİLER
- Arka uç bağımlılıkları: requirements.txt ve requirements-hf.txt.
- RAG gömme: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2.
- Flutter paketleri: pubspec.yaml.
- Appwrite isteğe bağlı (kimlik doğrulama/günlük).

## SLAYT 10: VERİ TABANI YAPISI
- selcuk_knowledge_base.json: konum, kampüs, fakülte, takvim, SSS.
- selcuk_qa_dataset.jsonl: eğitim/örnek veri.
- data/rag: index.faiss + metadata.json.
- Flutter tarafı Hive ile yerel sohbet geçmişi.

## SLAYT 11: ARKA UÇ DETAYLARI
- /health, /health/ollama, /health/hf durum kontrolü.
- /models: model listesi ve uygunluk.
- /chat: tek seferlik yanıt; /chat/stream: SSE.
- Appwrite loglama ortam değişkenlerine bağlı.

## SLAYT 12: YAPAY ZEKA ENTEGRASYONU
- Sistem istemi: Konya (İzmir değil), 1975, kampüsler (prompts.py).
- İstemci varsayılan parametreleri: temperature 0.2, top_p 0.9, max_tokens 256.
- RAG katı mod: kaynak yoksa sabit mesaj.

## SLAYT 13: ÖN UÇ DETAYLARI
- ChatGPT benzeri deneyim; Markdown + kopyala/düzenle/yenile.
- Sesli giriş (speech_to_text).
- Model seçici ve tanılama ekranı.
- RAG ayarları ve katı mod anahtarı.

## SLAYT 14: ANA SAYFA GÖRÜNTÜSÜ
- Yeni sohbet ekranı ve konuşma listesi.
- Tema değişimi ve aksiyon menüsü.
- Giriş alanı: mikrofon + gönder/durdur.

## SLAYT 15: SOHBET ÖRNEĞİ
- Örnek soru: “Selçuk Üniversitesi nerede?”
- Bilgi tabanı yanıtı Konya ve kampüs bilgisi içerir.
- Atıflar (`citations`) alanı gösterilir.

## SLAYT 16: FARKLI SORU TİPLERİ
- Kampüs, fakülte, takvim, iletişim, rektörlük.
- Bilgi tabanı ve SSS başlıklarıyla uyumlu örnekler.

## SLAYT 17: TEST SENARYOLARI
- validate_knowledge.py kritik bilgi doğrulaması sağlar.
- docs/reports/TEST_RAPORU.md: pytest 50 test, ruff/mypy, flutter analyze/test.
- Test tablosu, doğrulama kurallarına dayanır.

## SLAYT 18: PERFORMANS METRİKLERİ
- docs/reports/BENCHMARK_RAPORU.md kıyaslama metrikleri sunulur.
- llama3.2:3b (12 örnek) TTFT 5.18 sn, 5.41 belirteç/sn.
- SSE akışı ile algılanan gecikme düşer.

## SLAYT 19: ZORLUKLAR
- Halüsinasyon → RAG katı mod.
- Türkçe üslup → sistem istemi ve bilgi tabanı.
- Performans → küçük model alternatifleri + SSE.

## SLAYT 20: ÇÖZÜMLER
- RAG + atıflar (`citations`).
- validate_knowledge.py ile kritik doğruluk.
- Sağlayıcı deseni ile model esnekliği.
- Türkçe hata mesajları ve girdi doğrulama.

## SLAYT 21: SONUÇLAR
- Yerel LLM + RAG prototipi tamamlandı.
- Çoklu platform arayüz çalışır durumda.
- CI kalite kapıları mevcut (README + TEST_RAPORU).

## SLAYT 22: SWOT
- Güçlü: gizlilik + kaynaklı yanıt.
- Zayıf: donanım gereksinimi.
- Fırsat: resmi entegrasyon ve LoRA.
- Tehdit: model sürüm değişimleri.

## SLAYT 23: GELECEK ÇALIŞMALAR
- docs/reports/FINE_TUNING_REPORT.md: LoRA/QLoRA ince ayar planı.
- Appwrite entegrasyonunun genişletilmesi.

## SLAYT 24: CANLI GÖSTERİM
- DEMO_SCRIPT.md’deki adımları izleyin.
- Önce /health, sonra /models, ardından /chat (sohbet) ve RAG.
- Olası sorunlar için ekran görüntüsü yedeği.

## SLAYT 25: TEŞEKKÜRLER
- Katkıda bulunanlar ve Selçuk Üniversitesi’ne teşekkür.
- Soru-cevap kısmına davet.

## SLAYT 26+: KAYNAKLAR
- Repo dokümantasyonu ve temel teknoloji dokümanları.
- RAG makalesi ve Selçuk Üniversitesi resmi sitesi.
