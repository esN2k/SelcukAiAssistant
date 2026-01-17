/// DOSYA ADI: conversation_export_service_web.dart
/// AMAÇ: Web platformunda konuşma dışa aktarmak.
/// NE YAPAR:
///   - Tarayıcı üzerinden JSON indirir.
/// BAĞIMLILIKLAR:
///   - dart:html
///   - app_exception.dart
/// SON DEĞİŞİKLİK: 17.01.2026
// Web ortamı için koşullu olarak yüklenir.
// Tarayıcı indirme işlemleri için dart:html gerekir.
// ignore_for_file: avoid_web_libraries_in_flutter, deprecated_member_use

import 'dart:convert';
import 'dart:html' as html;

import 'package:selcukaiassistant/core/errors/app_exception.dart';
import 'package:selcukaiassistant/core/errors/error_messages.dart';
import 'package:selcukaiassistant/services/conversation_export_types.dart';

/// Giriş: Dosya adı ve içerik.
/// Çıkış: ExportResult (indirildi bilgisi).
/// İşleyiş: JSON içeriğini tarayıcı indirimi olarak sunar.
Future<ExportResult> exportConversationImpl(
  String filename,
  String content,
) async {
  try {
    final bytes = utf8.encode(content);
    final blob = html.Blob([bytes], 'application/json');
    final url = html.Url.createObjectUrlFromBlob(blob);
    html.AnchorElement(href: url)
      ..setAttribute('download', filename)
      ..click();
    html.Url.revokeObjectUrl(url);
    return ExportResult(downloaded: true);
  } on Exception catch (e) {
    throw AppException(
      ErrorMessages.disaAktarmaBasarisiz,
      detail: e.toString(),
    );
  }
}
