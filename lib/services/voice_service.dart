/// DOSYA ADI: voice_service.dart
/// AMAÇ: Sesli giriş için backend konuşma tanıma servisiyle iletişim kurmak.
/// NE YAPAR:
///   - Ses dosyasını backend'e gönderir.
///   - Tanınan metni döndürür.
/// BAĞIMLILIKLAR:
///   - http
///   - Pref (kullanıcı dili)
/// SON DEĞİŞİKLİK: 17.01.2026
library;
import 'dart:convert';
import 'dart:developer';

import 'package:http/http.dart' as http;
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';

class VoiceService {
  static const String _baseUrl = 'http://your-server-url.com/api';

  /// [audioPath]
  static Future<String> speechToText(String audioPath) async {
    final l10n = L10n.current();
    try {
      log('Konuşma tanıma başlatılıyor, dosya yolu: $audioPath');

      final request = http.MultipartRequest(
        'POST',
        Uri.parse('$_baseUrl/speech-to-text'),
      );

      request.files.add(
        await http.MultipartFile.fromPath('audio', audioPath),
      );

      final language = Pref.localeCode == 'en' ? 'en-US' : 'tr-TR';
      request.fields['language'] = language;

      final response = await request.send();
      final responseData = await response.stream.bytesToString();

      if (response.statusCode == 200) {
        final jsonData = json.decode(responseData) as Map<String, dynamic>;
        final recognizedText = (jsonData['text'] as String?) ?? '';
        log('Konuşma tanıma başarılı: $recognizedText');
        return recognizedText;
      } else {
        log('Konuşma tanıma başarısız, durum: ${response.statusCode}');
        return l10n?.speechRecognitionFailed ??
            'Konuşma tanıma başarısız oldu. Lütfen tekrar deneyin.';
      }
    } on Exception catch (e) {
      log('Konuşma tanıma hatası: $e');
      return l10n?.speechRecognitionError ??
          'Konuşma tanıma hatası. Lütfen ağ bağlantınızı kontrol edin.';
    }
  }

  static Future<bool> checkServerConnection() async {
    try {
      final response = await http
          .get(
            Uri.parse('$_baseUrl/health'),
            headers: {'Content-Type': 'application/json'},
          )
          .timeout(const Duration(seconds: 5));

      return response.statusCode == 200;
    } on Exception catch (e) {
      log('Sunucu bağlantı kontrolü başarısız: $e');
      return false;
    }
  }
}
