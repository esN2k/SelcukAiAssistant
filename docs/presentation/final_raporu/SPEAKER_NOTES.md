# Konuşmacı Notları (SPEAKER_NOTES)

## SLAYT 1: KAPAK
- Proje adı ve kapsam: Selçuk Üniversitesi’ne özel yerel AI asistan.
- Katkı: CONTRIBUTOR.md’de tek geliştirici esN2k görünüyor.
- Tarih: 04.01.2026.
- Gizlilik ve yerel çalışma motivasyonu bir cümlede özetlenir.

## SLAYT 2: İÇİNDEKİLER
- 10 dakikalık akış: problem → çözüm → teknoloji → test → sonuç.
- Kaynaklar slaytı sunum sınırı dışında.

## SLAYT 3: PROJE ÖZETİ
- README.md: gizliliğe odaklı yerel LLM + RAG yaklaşımı.
- Flutter istemci + FastAPI backend birleşimi.
- /chat ve /chat/stream ile hem tek yanıt hem akışlı yanıt.
- Ollama birincil sağlayıcı, HF opsiyonel.

## SLAYT 4: PROBLEM TANIMI
- Bilgiler dağınık, doğru bilgiye erişim güç.
- 7/24 destek yok; tekrar eden sorular idari yük oluşturuyor.
- Bulut API kullanımı gizlilik riski doğuruyor.
- KB verisine göre öğrenci sayısı 100.000+.

## SLAYT 5: AMAÇ VE HEDEFLER
- Yerel LLM ile veri gizliliği (README.md).
- RAG ile kaynaklı yanıt ve strict mod (docs/technical/RAG.md).
- TR/EN dil desteği (l10n dosyaları).
- Provider Pattern ile esneklik (backend/providers/).
- SSE streaming ile hızlı algılanan yanıt.

## SLAYT 6: LİTERATÜR / MEVCUT ÇÖZÜMLER
- RAG literatürü: Lewis et al., 2020.
- Üniversite chatbotları ve SSS sistemleri genel yaklaşım.
- Bu projede fark: yerel LLM + doğrulanmış KB + citations.

## SLAYT 7: METODOLOJİ
- Veri toplama: tools/collect_sources.py.
- KB ve QA dataset: backend/data.
- RAG ingest: rag_ingest.py, FAISS index.
- Backend: FastAPI + provider pattern.
- Frontend: Flutter + GetX + Hive.
- Test: pytest/ruff/mypy, benchmark/run.py.

## SLAYT 8: SİSTEM MİMARİSİ
- Flutter → FastAPI → Ollama/HF.
- RAG: FAISS + metadata, strict mod destekli.
- SSE: /chat/stream ile token akışı.

## SLAYT 9: KULLANILAN TEKNOLOJİLER
- Backend bağımlılıkları: requirements.txt ve requirements-hf.txt.
- RAG embedding: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2.
- Flutter paketleri: pubspec.yaml.
- Appwrite opsiyonel (auth/log).

## SLAYT 10: VERİ TABANI YAPISI
- selcuk_knowledge_base.json: konum, kampüs, fakülte, takvim, SSS.
- selcuk_qa_dataset.jsonl: eğitim/örnek veri.
- data/rag: index.faiss + metadata.json.
- Flutter tarafı Hive ile lokal sohbet geçmişi.

## SLAYT 11: BACKEND DETAYLARI
- /health, /health/ollama, /health/hf durum kontrolü.
- /models: model listesi ve uygunluk.
- /chat: tek seferlik yanıt; /chat/stream: SSE.
- Appwrite loglama ortam değişkenlerine bağlı.

## SLAYT 12: AI ENTEGRASYONU
- System prompt: Konya (İzmir değil), 1975, kampüsler (prompts.py).
- İstemci varsayılan parametreleri: temperature 0.2, top_p 0.9, max_tokens 256.
- RAG strict mod: kaynak yoksa sabit mesaj.

## SLAYT 13: FRONTEND DETAYLARI
- ChatGPT benzeri deneyim; markdown + kopyala/düzenle/yenile.
- Sesli giriş (speech_to_text).
- Model seçici ve diagnostics ekranı.
- RAG ayarları ve strict mod toggle.

## SLAYT 14: ANA SAYFA GÖRÜNTÜSÜ
- Yeni sohbet ekranı ve konuşma listesi.
- Tema değişimi ve aksiyon menüsü.
- Giriş alanı: mikrofon + gönder/durdur.

## SLAYT 15: SOHBET ÖRNEĞİ
- Örnek soru: “Selçuk Üniversitesi nerede?”
- KB yanıtı Konya ve kampüs bilgisi içerir.
- Citations alanı gösterilir.

## SLAYT 16: FARKLI SORU TİPLERİ
- Kampüs, fakülte, takvim, iletişim, rektörlük.
- KB ve SSS başlıklarıyla uyumlu örnekler.

## SLAYT 17: TEST SENARYOLARI
- validate_knowledge.py kritik bilgi doğrulaması sağlar.
- docs/reports/TEST_RAPORU.md: pytest 50 test, ruff/mypy, flutter analyze/test.
- Test tablosu, doğrulama kurallarına dayanır.

## SLAYT 18: PERFORMANS METRİKLERİ
- docs/reports/BENCHMARK_RAPORU.md metrikleri sunulur.
- llama3.2:3b (12 örnek) TTFT 5.18 sn, 5.41 tok/s.
- SSE streaming ile algılanan gecikme düşer.

## SLAYT 19: ZORLUKLAR
- Hallucination → RAG strict mod.
- Türkçe üslup → sistem promptu ve KB.
- Performans → küçük model alternatifleri + SSE.

## SLAYT 20: ÇÖZÜMLER
- RAG + citations.
- validate_knowledge.py ile kritik doğruluk.
- Provider pattern ile model esnekliği.
- Türkçe hata mesajları ve input doğrulama.

## SLAYT 21: SONUÇLAR
- Yerel LLM + RAG prototipi tamamlandı.
- Cross-platform arayüz çalışır durumda.
- CI kalite kapıları mevcut (README + TEST_RAPORU).

## SLAYT 22: SWOT
- Güçlü: gizlilik + kaynaklı yanıt.
- Zayıf: donanım gereksinimi.
- Fırsat: resmi entegrasyon ve LoRA.
- Tehdit: model sürüm değişimleri.

## SLAYT 23: GELECEK ÇALIŞMALAR
- docs/reports/FINE_TUNING_REPORT.md: LoRA/QLoRA ince ayar planı.
- Appwrite entegrasyonunun genişletilmesi.

## SLAYT 24: DEMO
- DEMO_SCRIPT.md’deki adımları izleyin.
- Önce /health, sonra /models, ardından chat ve RAG.
- Olası sorunlar için ekran görüntüsü yedeği.

## SLAYT 25: TEŞEKKÜRLER
- Katkıda bulunanlar ve Selçuk Üniversitesi’ne teşekkür.
- Soru-cevap kısmına davet.

## SLAYT 26+: KAYNAKLAR
- Repo dokümantasyonu ve temel teknoloji dokümanları.
- RAG makalesi ve Selçuk Üniversitesi resmi sitesi.
