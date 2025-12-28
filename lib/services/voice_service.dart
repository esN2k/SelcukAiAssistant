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
      log('Starting speech recognition, audio path: $audioPath');

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
        log('Speech recognition success: $recognizedText');
        return recognizedText;
      } else {
        log('Speech recognition failed, status: ${response.statusCode}');
        return l10n?.speechRecognitionFailed ??
            'Konuşma tanıma başarısız oldu. Lütfen tekrar deneyin.';
      }
    } on Exception catch (e) {
      log('Speech recognition error: $e');
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
      log('Server connection check failed: $e');
      return false;
    }
  }
}
