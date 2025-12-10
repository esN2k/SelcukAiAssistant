# VİZE RAPORU HAZIRLAMA BRİEFİ

## Proje Bilgileri

- **Proje Adı:** Selçuk Üniversitesi İçin Yapay Zeka Destekli Akademik Asistan Mobil Uygulaması
- **Öğrenci:** [Adınız Soyadınız]
- **Danışman:** [Danışman Unvanı ve Adı]
- **Ders:** Bilgisayar Mühendisliği Uygulamaları
- **Tarih:** Aralık 2025

## Proje Özeti

- Flutter mobil uygulama (Android/iOS)
- Python FastAPI backend
- Ollama + Llama 3.1 (8B) yerel AI modeli
- Google Gemini API → Ollama migrasyonu tamamlandı
- %100 offline çalışan, veri gizliliği odaklı sistem
- 9 birim test yazıldı, tamamı başarılı
- CodeQL güvenlik taraması:  0 kritik açık

## Teknik Stack

### Frontend

- Flutter 3.4.3 (Dart)
- GetX (State management)
- speech_to_text (Sesli giriş)
- flutter_markdown_plus (Markdown rendering)

### Backend

- Python 3.8+
- FastAPI 0.115.5
- Uvicorn (ASGI server)
- Pydantic (Data validation)

### AI Engine

- Ollama platform
- Llama 3.1 (8B parameters, Q4_0 quantized)
- ~4.7 GB RAM kullanımı
- 42 token/saniye ortalama hız

## Mimari

Flutter App (Mobile)
↓
HTTP POST /chat FastAPI Backend (Python)
↓
HTTP POST /api/generate Ollama (Local AI Server)
↓
Llama 3.1 Model

## Başarılan Kilometre Taşları

1. ✅ Flutter cross-platform app geliştirme
2. ✅ Gemini → Ollama migrasyonu
3. ✅ Sesli giriş entegrasyonu
4. ✅ FastAPI backend tamamlandı
5. ✅ Birim testleri %100 başarılı
6. ✅ APK hazır ve test edildi

## Rapor Gereksinimleri

- Selçuk Üniversitesi Teknoloji Fakültesi Bilgisayar Mühendisliği proje yazım kurallarına uygun
- Bölümler:  Özet, Abstract, Giriş, Kaynak Araştırması, Materyal ve Yöntem, Bulgular, Sonuç
- Times New Roman 12 punto, 1.5 satır aralığı
- A4, sol kenar 3. 5cm, diğerleri 2.5cm
- Kaynaklar: "yazar, yıl" sistemi
- Çizelge ve şekiller numaralı
- Türkçe yazılacak (Abstract hariç)

## Kullanılacak Kaynaklar

- Brown ve ark., 2020 (GPT-3)
- Vaswani ve ark., 2017 (Transformer)
- Touvron ve ark., 2023 (LLaMA)
- Lewis ve ark., 2020 (RAG)
- Richardson, 2018 (Microservices)
- Voigt ve Von dem Bussche, 2017 (GDPR)
- Zhou ve ark., 2019 (Edge AI)