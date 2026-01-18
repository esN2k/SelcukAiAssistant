/// DOSYA ADI: error_handler.dart
/// AMAÇ: Hataları kullanıcıya uygun Türkçe mesajlara dönüştürmek.
/// NE YAPAR:
///   - HTTP yanıtlarını analiz eder.
///   - Exception türlerine göre mesaj üretir.
/// BAĞIMLILIKLAR:
///   - http
///   - error_messages.dart
///   - app_exception.dart
/// SON DEĞİŞİKLİK: 17.01.2026
library;
import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;

import 'package:selcukaiassistant/core/errors/app_exception.dart';
import 'package:selcukaiassistant/core/errors/error_messages.dart';

class ErrorHandler {
  /// Giriş: HTTP yanıtı.
  /// Çıkış: Türkçe hata mesajı.
  /// İşleyiş: Durum kodu ve yanıt gövdesine göre mesaj seçer.
  static String fromResponse(http.Response response) {
    final bodyText = utf8.decode(response.bodyBytes).trim();
    final parsed = _tryParseJson(bodyText);

    final messageFromBody = _extractMessage(parsed, bodyText);
    if (messageFromBody != null && messageFromBody.isNotEmpty) {
      return messageFromBody;
    }

    switch (response.statusCode) {
      case 400:
      case 422:
        return ErrorMessages.gecersizVeri;
      case 401:
        return ErrorMessages.yetkisiz;
      case 403:
        return ErrorMessages.erisimEngellendi;
      case 404:
        return ErrorMessages.kaynakBulunamadi;
      case 408:
      case 504:
        return ErrorMessages.zamanAsimi;
      case 500:
        return ErrorMessages.sunucuHatasi;
      case 503:
        return ErrorMessages.internetYok;
      default:
        return ErrorMessages.beklenmeyen;
    }
  }

  /// Giriş: Hata nesnesi.
  /// Çıkış: Türkçe hata mesajı.
  /// İşleyiş: Exception türüne göre kullanıcıya uygun metin seçer.
  static String fromException(Object error) {
    if (error is AppException) {
      return error.toString();
    }
    if (error is SocketException) {
      return ErrorMessages.internetYok;
    }
    if (error is TimeoutException) {
      return ErrorMessages.zamanAsimi;
    }
    if (error is FileSystemException) {
      return ErrorMessages.disaAktarmaBasarisiz;
    }
    if (error is StateError) {
      final message = error.message;
      if (message.trim().isNotEmpty) {
        return message.trim();
      }
    }
    if (error is FormatException) {
      return ErrorMessages.gecersizVeri;
    }
    return ErrorMessages.beklenmeyen;
  }

  /// Giriş: Metin verisi.
  /// Çıkış: JSON nesnesi veya null.
  /// İşleyiş: JSON parse hatalarında null döndürür.
  static Map<String, dynamic>? _tryParseJson(String bodyText) {
    if (bodyText.isEmpty) return null;
    try {
      final decoded = jsonDecode(bodyText);
      if (decoded is Map<String, dynamic>) {
        return decoded;
      }
    } on FormatException {
      return null;
    }
    return null;
  }

  /// Giriş: JSON veri ve ham metin.
  /// Çıkış: Çıkarılan mesaj veya null.
  /// İşleyiş: "hata", "detail" veya "message" alanlarını önceliklendirir.
  static String? _extractMessage(
    Map<String, dynamic>? payload,
    String rawText,
  ) {
    if (payload == null) {
      return rawText.isEmpty ? null : rawText;
    }
    for (final key in ['hata', 'detail', 'message']) {
      final value = payload[key];
      if (value is String && value.trim().isNotEmpty) {
        return value.trim();
      }
    }
    return rawText.isEmpty ? null : rawText;
  }
}
