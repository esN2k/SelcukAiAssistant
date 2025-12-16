# 🤖 GitHub Copilot Agent Kullanım Kılavuzu

## Hızlı Başlangıç

### Adım 1: Prompt'u Aç

```
COPILOT_AGENT_PROMPT.md dosyasını GitHub Copilot Chat'e yapıştır
```

### Adım 2: Context Ekle

GitHub Copilot Agent'a şunu söyle:

```
Bu SelcukAiAssistant projesini oku ve COPILOT_AGENT_PROMPT.md'deki görevleri yap.

Öncelik sırası:
1. Reasoning artifact temizleme - final fix
2. Frontend typing indicator
3. Dark mode toggle
4. Error handling iyileştirme
5. README screenshots ekleme
```

### Adım 3: İlk Görev

```
"backend/ollama_service.py dosyasındaki _clean_reasoning_artifacts() metodunu 
incele ve daha robust hale getir. DeepSeek-R1 reasoning'i %100 temizlemeli."
```

---

## Örnek Komutlar

### Kod Analizi

```
"Tüm backend Python dosyalarını analiz et. Code smells, security issues ve 
performance bottleneck'leri listele."
```

### UI İyileştirme

```
"lib/screen/ klasöründeki tüm Flutter widget'ları incele. 
Material Design 3 best practices'e göre iyileştir ve dark mode ekle."
```

### Test Ekleme

```
"backend/ollama_service.py için pytest unit testleri yaz. 
Coverage %80+ olmalı."
```

### Dokümantasyon

```
"backend/main.py'deki tüm endpoint'ler için OpenAPI/Swagger 
documentation ekle."
```

---

## Önemli Notlar

✅ **Her değişikliği açıkla** - Neden bu değişikliği yaptın?
✅ **Test ekle** - Her yeni özellik için test
✅ **Backward compatibility** - Mevcut kodu bozma
✅ **Documentation** - Her public API için docstring

❌ **Over-engineering yapma** - KISS prensibi
❌ **Breaking changes** - Uyarı olmadan değiştirme
❌ **Hardcoded values** - Config'e taşı

---

## Sonuç Beklentileri

Agent tamamladığında:

- [ ] 0 linting errors
- [ ] %80+ test coverage
- [ ] Tüm kritik sorunlar çözülmüş
- [ ] README güncellenmiş
- [ ] CHANGELOG oluşturulmuş
- [ ] Production-ready!

🚀 **Başarılar!**

