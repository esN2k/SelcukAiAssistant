import 'dart:convert';
import 'dart:developer';

import 'package:http/http.dart' as http;
import 'package:selcukaiassistant/helper/global.dart';

class APIs {
  static Future<String> getAnswer(String question) async {
    try {
      log('Backend API çağrılıyor: $backendUrl/chat');

      // Prepare the request body
      final requestBody = jsonEncode({
        'question': question,
      });

      // Send POST request to the backend
      final response = await http.post(
        Uri.parse('$backendUrl/chat'),
        headers: {
          'Content-Type': 'application/json',
        },
        body: requestBody,
      );

      // Check if the request was successful
      if (response.statusCode == 200) {
        final responseData = jsonDecode(response.body) as Map<String, dynamic>;
        final answer = (responseData['answer'] as String?) ??
            'Üzgünüm, bir yanıt oluşturulamadı.';
        final preview = answer.substring(
          0,
          answer.length > 100 ? 100 : answer.length,
        );
        log('Backend Yanıtı: $preview...');
        return answer;
      } else {
        // Handle HTTP errors
        log('Backend HATASI: ${response.statusCode}');
        return 'Hata: Backend servisi geçici olarak kullanılamıyor '
            '(HTTP ${response.statusCode}). '
            'Lütfen backend servisinin çalıştığından emin olun.';
      }
    } on Exception catch (e) {
      // Handle network and other errors
      log('Backend BAĞLANTI HATASI: $e');
      return 'Hata: Backend servisine bağlanılamadı. '
          'Lütfen backend servisinin çalıştığından emin olun. '
          'Hata Detayı: $e';
    }
  }
}
