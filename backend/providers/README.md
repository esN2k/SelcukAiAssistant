# Providers Klasörü

## 📁 İçerik

Bu klasör, farklı LLM sağlayıcılarını (Ollama, HuggingFace) aynı arayüzle kullanmayı sağlayan **Provider Pattern** implementasyonunu içerir.

## 🎯 Provider Pattern Nedir?

Provider Pattern, farklı LLM servislerini (Ollama, HuggingFace, OpenAI vb.) aynı arayüzle çağırmayı sağlar. Bu sayede:
- Backend kodu sağlayıcıdan bağımsız çalışır
- Yeni sağlayıcı eklemek kolay
- Test edilebilirlik artar
- Yapılandırma ile sağlayıcı değiştirilebilir

---

## 📄 Dosyalar

### `base.py` (Temel Arayüz)
**Amaç:** Tüm provider'ların uygulaması gereken temel arayüzü tanımlar  
**İçerik:**
- `ModelProvider` (Protocol): Ana arayüz
- `ChatResult`: Senkron yanıt sonucu
- `StreamChunk`: Akış yanıt parçası
- `Usage`: Token kullanım bilgisi
- `ModelInfo`: Model metadata
- `CancellationToken`: Akış iptali için

**Kullanım:**
```python
from providers.base import ModelProvider, ChatResult

class MyProvider(ModelProvider):
    name = "my-provider"
    
    async def generate(self, messages, model_id, ...) -> ChatResult:
        # Implementasyon
        pass
```

---

### `ollama_provider.py` ⭐ (Ana Sağlayıcı)
**Amaç:** Yerel Ollama LLM servisine bağlanır  
**Ana Sınıf:** `OllamaProvider`  
**Desteklenen Modeller:** Llama 3.1, Qwen, Gemma, vb.

**Özellikler:**
- ✅ Senkron yanıt (`generate`)
- ✅ Akış yanıtı (`stream`)
- ✅ Model listesi (`list_models`)
- ✅ Sağlık kontrolü (`health_check`)
- ✅ Reasoning filter (düşünce izlerini temizler)
- ✅ Retry mekanizması

**Kullanım:**
```python
from providers.ollama_provider import OllamaProvider

provider = OllamaProvider()

# Senkron yanıt
result = await provider.generate(
    messages=[{"role": "user", "content": "Merhaba"}],
    model_id="llama3.1",
    temperature=0.2,
    top_p=0.9,
    max_tokens=500,
    request_id="req-001"
)
print(result.text)

# Akış yanıtı
async for chunk in provider.stream(...):
    print(chunk.token, end="")
```

**Yapılandırma (.env):**
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1
OLLAMA_TIMEOUT=120
OLLAMA_MAX_RETRIES=3
OLLAMA_RETRY_DELAY=1.0
```

---

### `huggingface_provider.py`
**Amaç:** HuggingFace transformers modellerini kullanır  
**Ana Sınıf:** `HuggingFaceProvider`  
**Desteklenen Modeller:** Turkcell-LLM-7B, Qwen2.5, vb.

**Özellikler:**
- ✅ GPU/CPU desteği
- ✅ 4-bit quantization (QLoRA)
- ✅ Batch inference
- ⚠️ Streaming kısıtlı (transformers limitasyonu)

**Kullanım:**
```python
from providers.huggingface_provider import HuggingFaceProvider

provider = HuggingFaceProvider()
result = await provider.generate(...)
```

---

### `translate_provider.py`
**Amaç:** TranslateGemma-4B ile çeviri  
**Ana Sınıf:** `TranslateProvider`  
**Model:** google/translategemma-4b-it

**Özellikler:**
- 77 dil desteği
- Görsel + metin çevirisi
- Bfloat16 precision (GPU)

⚠️ **Not:** Yeni `services/translator.py` (Helsinki-NLP) daha iyi Türkçe↔İngilizce performansı sağlar.

---

### `registry.py` (Model Kataloğu)
**Amaç:** Tüm modelleri kataloglar ve yönlendirir  
**Ana Sınıf:** `ModelRegistry`

**Özellikler:**
- Model listesi yönetimi
- Model çözümleme (alias → gerçek model)
- Uygunluk kontrolü (availability check)

**Kullanım:**
```python
from providers.registry import ModelRegistry

registry = ModelRegistry(providers)

# Model listesi
models = await registry.list_models()

# Model çözümleme
resolved = registry.resolve("llama3.1")
print(resolved.provider)  # "ollama"
print(resolved.model_id)  # "llama3.1"
```

---

## 🏗️ Mimari Diyagram

```
┌─────────────────────────────────────────────┐
│  FastAPI Backend (main.py)                  │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│  ModelRegistry                              │
│  • Model listesi                            │
│  • Model çözümleme                          │
└──────────────┬──────────────────────────────┘
               │
       ┌───────┴───────┐
       ▼               ▼
┌─────────────┐ ┌─────────────┐
│ OllamaProvider│ │HFProvider  │
│ (Yerel LLM) │ │(GPU/CPU)    │
└─────────────┘ └─────────────┘
       │               │
       ▼               ▼
┌─────────────┐ ┌─────────────┐
│Ollama API   │ │Transformers │
│localhost:   │ │Library      │
│11434        │ │             │
└─────────────┘ └─────────────┘
```

---

## 🔗 Veri Akışı

```
1. İstemci → POST /chat
2. main.py → ModelRegistry.resolve("llama3.1")
3. ModelRegistry → OllamaProvider seçer
4. OllamaProvider → Ollama API çağrısı
5. Ollama → Model inference
6. OllamaProvider → ChatResult döndürür
7. main.py → İstemciye yanıt
```

---

## 📊 Provider Karşılaştırması

| Özellik | OllamaProvider | HuggingFaceProvider |
|---------|----------------|---------------------|
| **Konum** | Yerel (localhost) | Yerel (GPU/CPU) |
| **Hız** | ⚡ Çok Hızlı | 🐢 Yavaş (ilk yükleme) |
| **Bellek** | 8-16 GB VRAM | 8-24 GB VRAM |
| **Streaming** | ✅ Mükemmel | ⚠️ Kısıtlı |
| **Model Değiştirme** | ✅ Kolay | ⚠️ Yeniden yükleme gerekir |
| **Quantization** | ✅ Otomatik | ✅ Manuel (4-bit) |
| **Kullanım** | Üretim | Geliştirme/Test |

---

## 🧪 Test Coverage

| Test Dosyası | Coverage | Durum |
|--------------|----------|-------|
| `tests/test_ollama_provider.py` | 90% | ✅ İyi |
| `tests/test_huggingface_provider.py` | 75% | ⚠️ Geliştirilebilir |
| `tests/test_registry.py` | 85% | ✅ İyi |

---

## 🚀 Yeni Provider Ekleme

Yeni bir LLM sağlayıcısı eklemek için:

1. **base.py'den ModelProvider'ı uygula:**
```python
from providers.base import ModelProvider, ChatResult

class OpenAIProvider(ModelProvider):
    name = "openai"
    
    async def generate(self, messages, model_id, ...) -> ChatResult:
        # OpenAI API çağrısı
        pass
    
    async def stream(self, ...):
        # Streaming implementasyonu
        pass
    
    def list_models(self):
        return [...]
```

2. **main.py'de kaydet:**
```python
openai_provider = OpenAIProvider()
providers["openai"] = openai_provider
```

3. **Test yaz:**
```python
# tests/test_openai_provider.py
def test_openai_generate():
    provider = OpenAIProvider()
    result = await provider.generate(...)
    assert result.text
```

---

## 📚 Kaynaklar

- [Ollama Documentation](https://github.com/ollama/ollama)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers)
- [Provider Pattern](https://refactoring.guru/design-patterns/provider)
