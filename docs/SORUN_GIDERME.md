# Sorun Giderme

## Backend erisilemiyor
- `backend/.env` icindeki HOST/PORT ayarlarini kontrol edin.
- Firewall veya antivirus engellerini kontrol edin.
- `GET /health` ile saglik kontrolu yapin.

## Model bulunamiyor / yuklu degil
- `GET /models` ile uygunluk durumunu kontrol edin.
- Ollama icin `ollama pull <model>` calistirin.

## Streaming akmiyor
- Nginx kullaniyorsaniz `X-Accel-Buffering: no` ve `Cache-Control: no-cache` ayarlari gerekir.
- Proxy time-out degerlerini artirin.

## Windows build - WebView2.h hatasi
- **Belirti**: `WebView2.h(20,10)` icin `disable` tanimsiz / syntax hatasi
- **Neden**: pub cache bozulmasi
- **Cozum**:
  - `flutter clean`
  - `dart pub cache repair` veya cache temizleme
  - Gerekirse `dotnet nuget locals all --clear`
  - Problem devam ederse ilgili plugin cache klasorunu silip yeniden `flutter pub get` calistirin
