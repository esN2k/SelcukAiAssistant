/// DOSYA ADI: app_exception.dart
/// AMAÇ: Uygulamaya özel hata sınıfını tanımlamak.
/// NE YAPAR:
///   - Kullanıcıya gösterilecek mesajı taşır.
///   - Servis katmanında istisna yönetimini kolaylaştırır.
/// BAĞIMLILIKLAR:
///   - yok
/// SON DEĞİŞİKLİK: 17.01.2026
class AppException implements Exception {
  /// Kullanıcıya gösterilecek hata mesajı.
  final String message;

  /// Opsiyonel detay metni.
  final String? detail;

  /// Hata kodu veya sınıflandırma etiketi.
  final String? code;

  /// Giriş: Mesaj ve opsiyonel detay.
  /// Çıkış: AppException nesnesi.
  /// İşleyiş: Hata bilgisini tek yerde toplar.
  AppException(this.message, {this.detail, this.code});

  @override
  String toString() {
    if (detail == null || detail!.isEmpty) {
      return message;
    }
    return '$message $detail';
  }
}
