# QA Hazırlık Notları

## 1) Neden bulut (Gemini/OpenAI) yerine yerel LLM?
- Gizlilik ve KVKK uyumu için verinin kurum dışına çıkmaması hedeflendi.
- README.md ve docs/presentation/final_raporu/SUNUM.md’de yerel LLM (Ollama) tercihi vurgulanıyor.

## 2) Hallucination nasıl azaltılıyor?
- RAG ile kaynaklı yanıt üretiliyor.
- Strict mod açıkken kaynak yoksa “Bu bilgi kaynaklarda yok.” mesajı dönüyor (prompts.py).

## 3) RAG teknik olarak nasıl çalışıyor?
- Soru → embedding (SentenceTransformer) → FAISS top_k → prompta kaynak ekleme → yanıt + citations (docs/technical/RAG.md).

## 4) Neden FAISS? ChromaDB nerede kullanılıyor?
- Uygulama kodu FAISS index + metadata ile çalışıyor (rag_service.py, rag_ingest.py).
- ChromaDB dokümanlarda opsiyonel katman olarak geçiyor; aktif implementasyon FAISS.

## 5) Performans nasıl?
- docs/reports/BENCHMARK_RAPORU.md’de TTFT ve tok/s ölçümleri var.
- Örnek: llama3.2:3b için Avg TTFT 5.18 sn, 5.41 tok/s (12 örnek koşum).

## 6) Çoklu sağlayıcı (provider pattern) ne işe yarıyor?
- MODEL_BACKEND ayarıyla Ollama veya HF seçilebiliyor.
- /models endpoint’i uygunluk durumunu raporluyor (providers/registry.py).

## 7) Offline çalışabilir mi?
- Ollama yerel çalıştığı için internet olmadan temel sohbet akışı sürer.
- HF modelleri önceden indirildiyse offline kullanılabilir.

## 8) Veri nasıl güncelleniyor?
- `selcuk_knowledge_base.json` güncellenir.
- `validate_knowledge.py` ile kritik doğruluk kontrol edilir.
- `rag_ingest.py` ile FAISS index yenilenir.

## 9) Uygulama verisi nerede tutuluyor?
- Bilgi tabanı: JSON/JSONL dosyaları.
- RAG index: `data/rag/index.faiss` + `metadata.json`.
- İstemci: Hive ile sohbet geçmişi (Flutter).
- Appwrite opsiyonel (auth/log).

## 10) Güvenlik önlemleri neler?
- .env ile anahtar yönetimi.
- Input doğrulama ve Türkçe hata mesajları.
- Bulut API bağımlılığı yok.

## 11) Test kapsamı yeterli mi?
- docs/reports/TEST_RAPORU.md: 50 pytest testi + ruff/mypy + flutter analyze/test.
- Encoding guard ve smoke test scriptleri mevcut.

## 12) Gelecek geliştirme planı?
- LoRA/QLoRA ince ayar (docs/reports/FINE_TUNING_REPORT.md).
- RAG kaynaklarının genişletilmesi.
- Resmi sistem entegrasyonları.
