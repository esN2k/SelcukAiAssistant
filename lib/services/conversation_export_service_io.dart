/// DOSYA ADI: conversation_export_service_io.dart
/// AMAÇ: IO platformunda konuşma dışa aktarmak.
/// NE YAPAR:
///   - JSON içeriğini uygulama belgelerine yazar.
/// BAĞIMLILIKLAR:
///   - path_provider
///   - app_exception.dart
/// SON DEĞİŞİKLİK: 17.01.2026
library;
import 'dart:io';

import 'package:path_provider/path_provider.dart';
import 'package:selcukaiassistant/core/errors/app_exception.dart';
import 'package:selcukaiassistant/core/errors/error_messages.dart';
import 'package:selcukaiassistant/services/conversation_export_types.dart';

/// Giriş: Dosya adı ve içerik.
/// Çıkış: ExportResult (dosya yolu).
/// İşleyiş: İçeriği uygulama dizinine yazar.
Future<ExportResult> exportConversationImpl(
  String filename,
  String content,
) async {
  try {
    final directory = await getApplicationDocumentsDirectory();
    final file = File('${directory.path}/$filename');
    await file.writeAsString(content);
    return ExportResult(path: file.path);
  } on FileSystemException catch (e) {
    throw AppException(
      ErrorMessages.disaAktarmaBasarisiz,
      detail: e.message,
    );
  } on Exception catch (e) {
    throw AppException(
      ErrorMessages.disaAktarmaBasarisiz,
      detail: e.toString(),
    );
  }
}
