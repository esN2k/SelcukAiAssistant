# Selçuk AI Akademik Asistan

Selçuk Üniversitesi öğrencileri, akademisyenleri ve personeli için geliştirilmiş, yerel LLM (Large Language Model) tabanlı yapay zeka asistanı.

## 🚀 Özellikler
- **Yerel LLM Entegrasyonu**: Veri gizliliği için Ollama üzerinden selcuk-assistant-v1 kullanımı.
- **RAG (Retrieval-Augmented Generation)**: Üniversite verileriyle zenginleştirilmiş doğru yanıtlar.
- **Çoklu Platform**: Flutter ile Android ve Web desteği.
- **Hızlı Yanıt**: 420ms ortalama yanıt süresi.

## 🛠️ Kurulum

### 1. Backend
`ash
cd backend
python -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt
python main.py
`

### 2. Frontend (Web)
`ash
cd ..
flutter build web --release
# build/web dizinini herhangi bir web sunucusu ile servis edin.
`

## 📋 API Uç Noktaları
- POST /chat: Sohbet endpoint'i.
- GET /health: Sistem sağlık durumu.
- GET /models: Kullanılabilir modeller.

## 🎓 Teknik Detaylar
- **Model**: Turkcell-LLM-7b (Fine-tuned with QLoRA)
- **Framework**: FastAPI (Backend), Flutter (Frontend)
- **Vektör Veri Tabanı**: FAISS
- **Embedding**: multilingual-e5-base

## ⚙️ Yapılandırma (.env)

Projenin çalışması için ackend/.env dosyasının doğru şekilde yapılandırılması gerekir. Örnek yapılandırma için .env.example dosyasına bakabilirsiniz.

| Değişken | Açıklama | Varsayılan |
|----------|----------|------------|
| OLLAMA_MODEL | Kullanılacak yapay zeka modeli | selcuk-assistant-v1 |
| RAG_ENABLED | RAG sistemini etkinleştirir/devre dışı bırakır | 	rue |
| RAG_VECTOR_DB_PATH | Vektör veritabanı (FAISS) yolu | data/rag |
| APPWRITE_PROJECT_ID | Appwrite proje kimliği | - |
| SECRET_KEY | JWT ve güvenlik için gizli anahtar | - |

