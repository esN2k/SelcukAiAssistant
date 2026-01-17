# Başlangıç Rehberi

Bu rehber, projeyi ilk kez çalıştıracak öğrenciler için hazırlanmıştır. Adımların çoğu kopyala‑yapıştır şeklindedir.

## 1) Ön Koşullar
- Python 3.10+ (tercihen 3.11)
- Flutter SDK (stabil sürüm)
- Git
- Ollama (yerel LLM çalıştırmak için)

## 2) Projeyi İndirme
```bash
git clone <repo-adresi>
cd SelcukAiAssistant/repo
```

## 3) Backend Kurulumu
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### .env Dosyası
`backend/.env` dosyasını oluşturun veya `backend/.env.example` varsa kopyalayın.
Aşağıdaki değerleri kontrol edin:
```
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=selcuk-assistant-v1
RAG_ENABLED=true
RAG_VECTOR_DB_PATH=./data/rag
```

Not: Eğer `selcuk-assistant-v1` modeli yoksa `OLLAMA_MODEL` değerini elinizdeki Ollama modeline göre değiştirin.
Örnek: `turkcell_llm_7b_selcuk_4k`

### Backend Çalıştırma
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 4) Ollama Modeli
Ollama kurulumu sonrası örnek model çekmek için:
```bash
ollama pull turkcell_llm_7b
```
Ardından `.env` içindeki `OLLAMA_MODEL` değerini güncelleyin.

## 5) Flutter Kurulumu
```bash
flutter pub get
flutter run
```

## 6) Hızlı Kontrol
- Backend: `http://localhost:8000/health`
- Flutter uygulaması açılıyorsa temel kurulum tamamdır.

## 7) Ek Notlar
- RAG veri indeksleme için `backend/rag_ingest.py` kullanılır.
- Detaylı hata çözümleri için `docs/HATA_COZUMLEME.md` dosyasına bakın.
