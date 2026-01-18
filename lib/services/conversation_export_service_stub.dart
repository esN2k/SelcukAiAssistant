/// DOSYA ADI: conversation_export_service_stub.dart
/// AMAÇ: Desteklenmeyen platformlar için yer tutucu dışa aktarma.
/// NE YAPAR:
///   - Platform desteklenmiyorsa hata üretir.
/// BAĞIMLILIKLAR:
///   - app_exception.dart
/// SON DEĞİŞİKLİK: 17.01.2026
library;
import 'package:selcukaiassistant/core/errors/app_exception.dart';
import 'package:selcukaiassistant/core/errors/error_messages.dart';
import 'package:selcukaiassistant/services/conversation_export_types.dart';

/// Giriş: Dosya adı ve içerik.
/// Çıkış: ExportResult.
/// İşleyiş: Desteklenmeyen platformda hata üretir.
Future<ExportResult> exportConversationImpl(
  String filename,
  String content,
) async {
  throw AppException(ErrorMessages.disaAktarmaDesteklenmiyor);
}
