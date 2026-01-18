---
theme: modern
colors: blue-professional
---

# Slide 1
**YAPAY ZEKA DESTEKLİ ÜNİVERSİTE BİLGİ ASİSTANI**  
**SELÇUK AI ASİSTAN**

Doğukan BALAMAN (203311066) • Ali YILDIRIM (203311008)

Prof. Dr. Nurettin DOĞAN • Dr. Öğr. Üyesi Onur İNAN

📅 Ocak 2025 - KONYA

---

# Slide 2: AGENDA
📋 İçerik

✓ Giriş ve Motivasyon  
✓ Problem Tanımı  
✓ Çözüm Yaklaşımı  
✓ Teknik Detaylar  
✓ Bulgular  
✓ Gelecek Çalışmalar

---

# Slide 3: SELÇUK ÜNİVERSİTESİ
📊 Büyüklük

🎓 **80.000+** öğrenci  
🏫 **Çoklu kampüs**  
📚 **Farklı fakülte ve birimler**  
❌ **Sorun:** Bilgi dağınıklığı

---

# Slide 4: PROBLEM 1
❌ Bilgi Dağınıklığı

• Web sitesi  
• Duyuru sayfaları  
• Farklı fakülte siteleri  
• **Sonuç:** Bilgiye erişim zor

---

# Slide 5: PROBLEM 2
⏰ 7/24 Destek Yok

• Akşam 10:00 → ❌  
• Gece 02:00 → ❌  
• Pazar 06:00 → ❌  
• **Çözüm:** AI Asistan

---

# Slide 6: ÇÖZÜM
🎯 RAG + LLM

**RAG:** Retrieval Augmented Generation  
**LLM:** Local Language Model (Ollama)

✅ Gerçek bilgi (645 doküman)  
✅ Kaynaklı cevap  
✅ 7/24 erişim  
✅ Mobil uygulama

---

# Slide 7: SİSTEM MİMARİSİ
🏗️ 3-Tier Architecture

```
┌─────────────────┐
│   FLUTTER APP   │ ← Presentation Layer
├─────────────────┤
│   FASTAPI       │ ← Application Layer
├─────────────────┤
│ RAG + OLLAMA    │ ← Data Layer
└─────────────────┘
```

---

# Slide 8: BACKEND STACK
⚙️ Teknolojiler

🐍 **Python 3.11**  
⚡ **FastAPI**  
🔎 **FAISS**  
🧠 **Ollama (Local LLM)**  
📄 **645 doküman**

---

# Slide 9: FRONTEND STACK
📱 Mobil Uygulama

💙 **Flutter 3.x**  
🎯 **Dart**  
🔄 **GetX** (State Management)  
🎨 **Material Design**  
📱 **iOS + Android**

---

# Slide 10: RAG PİPELINE
🔄 7 Adım

1️⃣ Kullanıcı sorusu  
2️⃣ Vektöre çevirme  
3️⃣ FAISS arama  
4️⃣ Top-4 doküman  
5️⃣ Context oluşturma  
6️⃣ LLM'ye gönderme  
7️⃣ Cevap üretme

⏱️ **Süre:** Benchmark raporlarına göre değişken

---

# Slide 11: AI MODEL
🤖 Model Seçenekleri (Ollama Kataloğu)

| Model | Amaç | Not |
|-------|------|-----|
| turkcell_llm_7b_selcuk_4k | Varsayılan | Yerel LLM profili |
| llama3.2:3b | Hız odaklı | 6GB GPU uyumlu |
| deepseek-r1:8b | Kalite/akıl yürütme | Daha ağır |

---

# Slide 12: KNOWLEDGE BASE
📚 Bilgi Tabanı

📊 **645** doküman  
🌐 **92** başarılı URL  
❌ **43** hatalı URL  
📈 **%68.15** başarı oranı  

**Kaynak:** selcuk.edu.tr

---

# Slide 13: API ENDPOINTS
🔌 Backend API (Özet)

| Endpoint | Method | Durum |
|----------|--------|-------|
| /health | GET | ✅ |
| /chat | POST | ✅ |
| /chat/stream | POST | ✅ |
| /models | GET | ✅ |
| /api/translate | POST | ⏭️ (HF_TOKEN) |
| /admin/cache/stats | GET | ⏭️ (Redis) |

---

# Slide 14: TEST SONUÇLARI
✅ Testler

🧪 **8** backend test dosyası (hazır)  
🧪 Otomatik koşum: ortam kısıtları nedeniyle yapılmadı  
📋 Test kapsamı: API, Ollama servis, RAG guard

---

# Slide 15: PERFORMANS
📈 Benchmark Metrikleri (docs/reports/BENCHMARK_RAPORU.md)

- **Model:** ollama:llama3.2:3b  
- **Ort. TTFT:** 5180.24 ms  
- **Ort. belirteç/sn:** 5.41  
- **Ort. toplam süre:** 8.643 s

---

# Slide 16: EKRAN 1
📱 Splash Screen

[PLACEHOLDER: Splash screen görsel]

---

# Slide 17: EKRAN 2
💬 Chat Screen

[PLACEHOLDER: Chat screen görsel]

---

# Slide 18: EKRAN 3
⚙️ Settings / Translate Screen

[PLACEHOLDER: Settings ve Translate ekranı görsel]

---

# Slide 19: BAŞARILAR
🏆 Kazanımlar

✅ Tam fonksiyonel backend API  
✅ RAG tabanlı bilgi erişimi  
✅ 645 dokümanlık bilgi tabanı  
✅ Flutter mobil uygulama  
✅ Çeviri ekranı (hazır)

---

# Slide 20: ZORLUKLAR
⚠️ Karşılaşılan Sorunlar

**1. DNS Hataları**  
→ 36 subdomain erişilemiyor  

**2. SSL Sorunları**  
→ SSL fallback ile çözüldü

---

# Slide 21: GELECEK ÇALIŞMALAR
🚀 Roadmap

**Kısa Vade:**  
✨ TranslateGemma (55 dil)  
⚡ Redis Cache  
📊 PostgreSQL Analytics

**Orta Vade:**  
🌐 Web arayüzü  
🔐 Production deployment  
🧪 Otomatik testler

---

# Slide 22: TEŞEKKÜRLER
🙏 Questions?

**İletişim:**  
📧 [e-posta]  
💻 [GitHub]

**Danışmanlarımız:**  
Prof. Dr. Nurettin DOĞAN  
Dr. Öğr. Üyesi Onur İNAN

---
