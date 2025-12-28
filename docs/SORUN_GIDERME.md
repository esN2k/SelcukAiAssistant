# Sorun Giderme

## Backend erişilemiyor
- `backend/.env` içindeki HOST/PORT ayarlarını kontrol edin.
- Firewall veya antivirüs engellerini kontrol edin.
- `GET /health` ile sağlık kontrolü yapın.

## Model bulunamıyor / yüklü değil
- `GET /models` ile uygunluk durumunu kontrol edin.
- Ollama için `ollama pull <model>` çalıştırın.
- HuggingFace için `backend/requirements-hf.txt` kurulu olmalı.

## Streaming akmıyor
- Nginx kullanıyorsanız `X-Accel-Buffering: no` ve `Cache-Control: no-cache` ayarları gerekir.
- Proxy time-out değerlerini artırın.

## RAG kaynak göstermiyor
- `RAG_ENABLED=true` ve `RAG_VECTOR_DB_PATH` ayarlarını kontrol edin.
- İndeksin üretildiğinden emin olun: `python rag_ingest.py`.

## Windows build - WebView2.h hatası
- **Belirti:** `WebView2.h(20,10)` için `disable` tanımsız / syntax hatası
- **Neden:** pub cache bozulması
- **Çözüm:**
  - `flutter clean`
  - `dart pub cache repair` veya cache temizleme
  - Gerekirse `dotnet nuget locals all --clear`
  - Problem devam ederse ilgili plugin cache klasörünü silip yeniden `flutter pub get` çalıştırın
