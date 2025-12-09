import 'dart:convert';
import 'dart:developer';

import 'package:http/http.dart' as http;

class VoiceService {
  static const String _baseUrl = 'http://your-server-url.com/api';

  /// [audioPath]

  static Future<String> speechToText(String audioPath) async {
    try {
      log('Konuşma tanıma başlatılıyor, ses dosyası yolu: $audioPath');

      final request = http.MultipartRequest(
        'POST',
        Uri.parse('$_baseUrl/speech-to-text'),
      );

      request.files.add(
        await http.MultipartFile.fromPath('audio', audioPath),
      );

            request.fields['language'] = 'tr-TR';

      final response = await request.send();
      final responseData = await response.stream.bytesToString();

      if (response.statusCode == 200) {
        final jsonData = json.decode(responseData);
        final recognizedText = (jsonData['text'] as String?) ?? '';
        log('Ses tanıma başarılı: $recognizedText');
        return recognizedText;
      } else {
        log('Ses tanıma başarısız, durum kodu: ${response.statusCode}');
        return 'Ses tanıma başarısız oldu. Lütfen tekrar deneyin.';
      }
    } catch (e) {
            log('Ses tanıma hatası: $e');
      return 'Ses tanıma hatası. Lütfen ağ bağlantınızı kontrol edin.';
    }
  }

  static Future<bool> checkServerConnection() async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/health'),
        headers: {'Content-Type': 'application/json'},
      ).timeout(const Duration(seconds: 5));

      return response.statusCode == 200;
    } catch (e) {
      log('Sunucu bağlantısı kontrolü başarısız oldu: $e');
      return false;
    }
  }
}
