/// DOSYA ADI: conversation_export_types.dart
/// AMAÇ: Dışa aktarma sonucunu temsil etmek.
/// NE YAPAR:
///   - Dosya yolu veya indirme bilgisini taşır.
/// BAĞIMLILIKLAR:
///   - yok
/// SON DEĞİŞİKLİK: 17.01.2026
class ExportResult {
  /// Giriş: Dosya yolu ve indirme durumu.
  /// Çıkış: ExportResult nesnesi.
  /// İşleyiş: Sonuç bilgilerini saklar.
  ExportResult({this.path, this.downloaded = false});

  final String? path;
  final bool downloaded;
}
