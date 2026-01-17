/// DOSYA ADI: conversation_export_service.dart
/// AMAÇ: Konuşma dışa aktarma işlemini platforma göre yönlendirmek.
/// NE YAPAR:
///   - IO ve Web implementasyonlarını koşullu olarak seçer.
/// BAĞIMLILIKLAR:
///   - conversation_export_service_io.dart
///   - conversation_export_service_web.dart
/// SON DEĞİŞİKLİK: 17.01.2026
library;
import 'package:selcukaiassistant/services/conversation_export_service_stub.dart'
    if (dart.library.io)
        'package:selcukaiassistant/services/conversation_export_service_io.dart'
    if (dart.library.html)
        'package:selcukaiassistant/services/conversation_export_service_web.dart';
import 'package:selcukaiassistant/services/conversation_export_types.dart';

/// Giriş: Dosya adı ve içerik.
/// Çıkış: ExportResult.
/// İşleyiş: Platforma uygun dışa aktarma fonksiyonunu çağırır.
Future<ExportResult> exportConversation(String filename, String content) {
  return exportConversationImpl(filename, content);
}
