# LoRA İnce Ayar Planı (Selçuk AI Asistanı)

Bu plan, öncelikle RAG ile doğruluk artırıldıktan sonra LoRA/QLoRA ile yerel modelin Selçuk Üniversitesi verisine uyarlanmasını hedefler.

## 1) Hedef
- Üniversiteye özel mevzuat, duyuru, süreç ve formlara dayalı doğru ve kısa yanıt üretimi
- Türkçe akıcılığı korunurken akademik ve resmi üslup standardı sağlanması

## 2) Temel Model Seçimi
- **Birincil aday:** `turkcell-llm-7b` (Türkçe odaklı, benchmarkta en dengeli sonuç)
- **İkincil aday:** `selcuk_ai_assistant` (üniversiteye özel sistem istemi ile uyumlu)

## 3) Veri Kaynağı Stratejisi
- Resmi web içerikleri: `data/processed_web/docs`
- Kurum içi belgeler (yönerge, form, takvim, yönetmelik) için ayrı klasör: `data/local_docs/`
- RAG kaynakları ile tutarlı olacak şekilde kaynak URL ve belge adı metadatası korunmalıdır

## 4) Veri Hazırlama ve Temizlik
- Yinelenen paragraflar ve şablon tekrarları ayıklanmalıdır
- Tablolar ve madde listeleri düz metne dönüştürülmelidir
- Soru-cevap çiftleri için otomatik üretim + manuel doğrulama önerilir
- Hassas veri temizliği: isim, telefon, TCKN gibi alanlar maskelenmelidir

## 5) Eğitim Formatı
- Format: JSONL (instruction + input + output) veya chat formatı (role: system/user/assistant)
- Örnek şema:
```json
{"instruction": "Soruya kısa cevap ver", "input": "...", "output": "..."}
```

## 6) QLoRA Parametre Önerisi (RTX 3060 6GB)
- 4-bit quantization (NF4)
- LoRA rank: 8 veya 16
- LoRA alpha: 16 veya 32
- LoRA dropout: 0.05
- Seq length: 1024-2048 (veri uzunluğuna göre)
- Mikro batch: 1-2, gradient accumulation ile efektif batch 8-16
- Gradient checkpointing: açık

## 7) Eğitim Aşamaları
1. **Pilot**: 1-2K örnekle kısa eğitim, hatalı cevap analizi
2. **Genişletme**: 5-10K örnekle kapsam artışı
3. **Stabilizasyon**: kritik süreç soruları için kontrollü test seti

## 8) Değerlendirme
- Otomatik: `docs/BENCHMARK_RAPORU.md` yöntemine benzer hız/tutarlılık testleri
- Manuel: 20-30 kritik soru ile akademik doğruluk kontrolü
- RAG ile karşılaştırma: LoRA yalnız, RAG+LoRA kombinasyonu

## 9) Çıktı ve Sürümleme
- LoRA ağırlıkları ayrı saklanmalı (`models/lora/selcuk-ai-vX`)
- GGUF export ile Ollama modeli olarak paketlenmeli
- Sürüm etiketi: `selcuk_ai_assistant:vX`

## 10) Risk ve Güvenlik
- Hallucination riski için kritik sorularda RAG zorunlu tutulmalıdır
- Yanıt denetimi: kaynak gösterimi ve kullanıcıya yönlendirme cümleleri
- Eğitim verisinde kişisel veri bulunmamalıdır
