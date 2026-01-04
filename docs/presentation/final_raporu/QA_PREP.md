# Soru-Cevap Hazırlık Notları

## 1) Neden bulut (Gemini/OpenAI) yerine yerel LLM?
- Gizlilik ve KVKK uyumu için verinin kurum dışına çıkmaması hedeflendi.
- README.md ve docs/presentation/final_raporu/SUNUM.md’de yerel LLM (Ollama) tercihi vurgulanıyor.

## 2) Halüsinasyon nasıl azaltılıyor?
- RAG ile kaynaklı yanıt üretiliyor.
- Katı mod açıkken kaynak yoksa “Bu bilgi kaynaklarda yok.” mesajı dönüyor (prompts.py).

## 3) RAG teknik olarak nasıl çalışıyor?
- Soru → gömme (SentenceTransformer) → FAISS top_k → isteme kaynak ekleme → yanıt + atıflar (`citations`) (docs/technical/RAG.md).

## 4) Neden FAISS? ChromaDB nerede kullanılıyor?
- Uygulama kodu FAISS indeks + metadata ile çalışıyor (rag_service.py, rag_ingest.py).
- ChromaDB dokümanlarda isteğe bağlı katman olarak geçiyor; aktif uygulama FAISS.

## 5) Performans nasıl?
- docs/reports/BENCHMARK_RAPORU.md’de TTFT ve belirteç/sn ölçümleri var.
- Örnek: llama3.2:3b için ort. TTFT 5.18 sn, 5.41 belirteç/sn (12 örnek koşum).

## 6) Çoklu sağlayıcı (sağlayıcı deseni) ne işe yarıyor?
- MODEL_BACKEND ayarıyla Ollama veya HF seçilebiliyor.
- /models uç noktası uygunluk durumunu raporluyor (providers/registry.py).

## 7) Çevrimdışı çalışabilir mi?
- Ollama yerel çalıştığı için internet olmadan temel sohbet akışı sürer.
- HF modelleri önceden indirildiyse çevrimdışı kullanılabilir.

## 8) Veri nasıl güncelleniyor?
- `selcuk_knowledge_base.json` güncellenir.
- `validate_knowledge.py` ile kritik doğruluk kontrol edilir.
- `rag_ingest.py` ile FAISS indeks yenilenir.

## 9) Uygulama verisi nerede tutuluyor?
- Bilgi tabanı: JSON/JSONL dosyaları.
- RAG indeks: `data/rag/index.faiss` + `metadata.json`.
- İstemci: Hive ile sohbet geçmişi (Flutter).
- Appwrite isteğe bağlı (kimlik doğrulama/günlük).

## 10) Güvenlik önlemleri neler?
- .env ile anahtar yönetimi.
- Girdi doğrulama ve Türkçe hata mesajları.
- Bulut API bağımlılığı yok.

## 11) Test kapsamı yeterli mi?
- docs/reports/TEST_RAPORU.md: 50 pytest testi + ruff/mypy + flutter analyze/test.
- Kodlama denetimi ve duman testi betikleri mevcut.

## 12) Gelecek geliştirme planı?
- LoRA/QLoRA ince ayar (docs/reports/FINE_TUNING_REPORT.md).
- RAG kaynaklarının genişletilmesi.
- Resmi sistem entegrasyonları.
