# Kod Standartları

Bu proje öğrenci seviyesinde anlaşılır ve düzenli kod üretmeyi hedefler.

## Genel Kurallar
- Tüm yorumlar ve hata mesajları Türkçe olmalıdır.
- Değişken/fonksiyon isimleri İngilizce olabilir; açıklamalar Türkçe olmalıdır.
- Her dosyanın başında dosya açıklama bloğu bulunmalıdır.
- Her fonksiyonun üstünde Türkçe docstring veya açıklama olmalıdır.

## Dart (Flutter)
- UI metinleri Türkçe olmalı (l10n kullanılabilir).
- Hata yönetimi için `core/errors` altyapısı kullanılmalıdır.
- HTTP hataları `ErrorHandler` üzerinden kullanıcıya iletilmelidir.

**Örnek:**
```dart
/// DOSYA ADI: example.dart
/// AMAÇ: Örnek kullanım
/// NE YAPAR:
///   - Basit bir fonksiyon örneği
/// BAĞIMLILIKLAR:
///   - yok
/// SON DEĞİŞİKLİK: 17.01.2026

/// Giriş: kullanıcı adı.
/// Çıkış: selamlama metni.
/// İşleyiş: Parametreyi birleştirir.
String selamla(String ad) {
  return 'Merhaba $ad';
}
```

## Python (Backend)
- Her dosyada üstte çok satırlı açıklama bulunmalıdır.
- Her fonksiyon/docstring Türkçe olmalıdır.
- Hatalar `error_messages.py` üzerinden yönetilmelidir.

**Örnek:**
```python
"""
DOSYA ADI: example.py
AMAÇ: Örnek fonksiyon göstermek
NE YAPAR:
  - Basit bir mesaj döndürür
SON DEĞİŞİKLİK: 17.01.2026
"""

def merhaba(ad: str) -> str:
    """Giriş: ad.

    Çıkış: selam metni.
    İşleyiş: Parametreyi birleştirir.
    """
    return f"Merhaba {ad}"
```

## Hata Yönetimi
- Backend tarafında `exceptions.py` ve `error_handlers.py` kullanılmalıdır.
- Flutter tarafında `AppException` ve `ErrorHandler` kullanılmalıdır.
- "Unknown error" gibi belirsiz mesajlar kullanılmamalıdır.
