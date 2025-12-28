# Sorun Giderme

## Backend erişilemiyor
- `backend/.env` içindeki HOST/PORT ayarlarını kontrol edin.
- Firewall veya antivirüs engellerini kontrol edin.
- `GET /health` ile sağlık kontrolü yapın.

## Model bulunamıyor / yüklü değil
- `GET /models` ile uygunluk durumunu kontrol edin.
- Ollama için `ollama pull <model>` çalıştırın.
- HuggingFace için `backend/requirements-hf.txt` kurulu olmalı.

## Windows: `torch_python.dll` / WinError 126
**Belirti:** HuggingFace modeli çağrılırken `WinError 126` ve `torch_python.dll` hatası.  
**Anlamı:** Torch çalışma zamanı (runtime) bağımlılıkları veya DLL (Dinamik Bağlantı Kütüphanesi) eksik.

**Çözüm adımları:**
1. **Microsoft Visual C++ 2015–2022 Redistributable** kurulu olmalı.
2. CPU kullanacaksanız PyTorch CPU sürümünü kurun:
   ```powershell
   pip install torch --index-url https://download.pytorch.org/whl/cpu
   ```
3. GPU kullanıyorsanız CUDA sürümünüz ile PyTorch sürümü uyumlu olmalı.
4. Geçici çözüm: terminalde `torch\lib` dizinini PATH’e ekleyin:
   ```powershell
   $env:Path += ";$env:VIRTUAL_ENV\\Lib\\site-packages\\torch\\lib"
   ```

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
