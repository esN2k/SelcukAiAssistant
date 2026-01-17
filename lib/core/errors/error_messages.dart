/// DOSYA ADI: error_messages.dart
/// AMAÇ: Uygulama genelindeki Türkçe hata mesajlarını merkezileştirmek.
/// NE YAPAR:
///   - Hata mesajlarını tek noktada toplar.
///   - UI ve servis katmanında tutarlı metin sağlar.
/// BAĞIMLILIKLAR:
///   - yok
/// SON DEĞİŞİKLİK: 17.01.2026
class ErrorMessages {
  /// Genel kullanım için hazır hata mesajları.
  static const String beklenmeyen =
      'Beklenmeyen bir hata oluştu. Lütfen daha sonra tekrar deneyin.';
  static const String gecersizVeri =
      'Gönderilen veri formatı hatalı. Lütfen bilgileri kontrol edin.';
  static const String sunucuHatasi =
      'Sunucu hatası oluştu. Lütfen daha sonra tekrar deneyin.';
  static const String kaynakBulunamadi = 'İstediğiniz kaynak bulunamadı.';
  static const String yetkisiz =
      'Bu işlem için yetkiniz yok. Lütfen giriş yapın.';
  static const String erisimEngellendi =
      'Bu işlem için erişiminiz yok. Yetkinizi kontrol edin.';
  static const String internetYok =
      'İnternet bağlantısı yok. Lütfen bağlantınızı kontrol edin.';
  static const String zamanAsimi =
      'Bağlantı zaman aşımına uğradı. Lütfen tekrar deneyin.';

  /// Çeviri ekranına özel mesajlar.
  static const String ceviriBos =
      'Çeviri sonucu alınamadı. Lütfen tekrar deneyin.';
  static const String ceviriBasarisiz =
      'Çeviri başarısız oldu. Lütfen tekrar deneyin.';
  static const String metinBos = 'Çevirilecek metin boş olamaz.';

  /// Akış ve bağlantı hataları.
  static const String akisBasarisiz =
      'Akış isteği başarısız oldu. Lütfen daha sonra tekrar deneyin.';
  static const String akisSunucuHatasi =
      'Akış sırasında sunucu hatası oluştu. Lütfen daha sonra tekrar deneyin.';

  /// Depolama ve dosya işlemleri.
  static const String depolamaBaslatilmadi =
      'Depolama servisi başlatılmadı. Lütfen uygulamayı yeniden başlatın.';
  static const String disaAktarmaBasarisiz =
      'Dışa aktarma işlemi başarısız oldu. Lütfen tekrar deneyin.';
  static const String disaAktarmaDesteklenmiyor =
      'Bu platformda dışa aktarma desteklenmiyor.';

  /// Appwrite hata mesajları.
  static const String appwriteBaslatilmadi =
      'Appwrite servisi başlatılamadı. Lütfen yapılandırmayı kontrol edin.';
  static const String appwriteKayitBasarisiz =
      'Kayıt oluşturulamadı. Lütfen bilgilerinizi kontrol edin.';
  static const String appwriteOturumAcilamadi =
      'Oturum açılamadı. E-posta veya şifrenizi kontrol edin.';
  static const String appwriteOturumKapatilamadi =
      'Oturum kapatılamadı. Lütfen tekrar deneyin.';
}
