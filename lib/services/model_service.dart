/// DOSYA ADI: model_service.dart
/// AMAÇ: Model listesini backend'den almak.
/// NE YAPAR:
///   - Model listesini `/models` uç noktasından çeker.
///   - Hata durumlarında Türkçe mesaj üretir.
/// BAĞIMLILIKLAR:
///   - backend_config.dart: API adresleri
///   - error_handler.dart: hata metni dönüştürme
/// SON DEĞİŞİKLİK: 17.01.2026
library;
import 'dart:convert';
import 'dart:developer';

import 'package:http/http.dart' as http;
import 'package:selcukaiassistant/config/backend_config.dart';
import 'package:selcukaiassistant/core/errors/app_exception.dart';
import 'package:selcukaiassistant/core/errors/error_handler.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
import 'package:selcukaiassistant/model/model_info.dart';

class ModelService {
  /// Giriş: yok.
  /// Çıkış: ModelInfo listesi.
  /// İşleyiş: Başarılı değilse AppException fırlatır.
  static Future<List<ModelInfo>> fetchModels() async {
    try {
      final locale = Pref.localeCode ?? L10n.fallbackLocale.languageCode;
      final response = await http.get(
        Uri.parse(BackendConfig.modelsEndpoint),
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
          'Accept-Language': locale,
        },
      );

      if (response.statusCode != 200) {
        final message = ErrorHandler.fromResponse(response);
        log('Model listesi alınamadı: $message');
        throw AppException(message, code: 'model_listesi');
      }

      final payload = jsonDecode(utf8.decode(response.bodyBytes))
          as Map<String, dynamic>;
      final items = payload['models'] as List<dynamic>? ?? [];
      return items
          .map((item) => ModelInfo.fromJson(item as Map<String, dynamic>))
          .toList();
    } on AppException {
      rethrow;
    } on Exception catch (e) {
      final message = ErrorHandler.fromException(e);
      log('Model listesi alınamadı: $message');
      throw AppException(message, code: 'model_listesi');
    }
  }
}
