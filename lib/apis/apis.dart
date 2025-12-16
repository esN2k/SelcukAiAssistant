import 'dart:async';
import 'dart:convert';
import 'dart:developer';
import 'dart:io';

import 'package:http/http.dart' as http;
import 'package:selcukaiassistant/helper/global.dart';

class APIs {
  // Timeout configuration
  static const Duration _responseTimeout = Duration(seconds: 120);

  /// Get AI answer from the backend chat endpoint.
  /// 
  /// Throws detailed exceptions for better error handling.
  /// Returns the AI-generated answer or a user-friendly error message.
  static Future<String> getAnswer(String question) async {
    try {
      log('Backend API çağrılıyor: ${Global.chatEndpoint}');

      // Prepare the request body
      final requestBody = jsonEncode({
        'question': question,
      });

      // Send POST request to the backend with timeout
      final response = await http
          .post(
            Uri.parse(Global.chatEndpoint),
            headers: {
              'Content-Type': 'application/json; charset=utf-8',
            },
            body: requestBody,
          )
          .timeout(
            _responseTimeout,
            onTimeout: () {
              throw TimeoutException(
                'İstek zaman aşımına uğradı. '
                'Lütfen daha kısa bir soru deneyin veya '
                'daha sonra tekrar deneyin.',
              );
            },
          );

      // Check if the request was successful
      if (response.statusCode == 200) {
        final responseData = jsonDecode(utf8.decode(response.bodyBytes))
            as Map<String, dynamic>;
        final answer = (responseData['answer'] as String?) ??
            'Üzgünüm, bir yanıt oluşturulamadı.';
        final preview = answer.substring(
          0,
          answer.length > 100 ? 100 : answer.length,
        );
        log('Backend Yanıtı: $preview...');
        return answer;
      } else if (response.statusCode == 400) {
        // Bad request - likely validation error
        try {
          final errorData =
              jsonDecode(response.body) as Map<String, dynamic>;
          final errorMessage = errorData['detail'] as String? ?? 
              'Geçersiz istek';
          return 'Hata: $errorMessage';
        } on FormatException {
          return 'Hata: Geçersiz soru formatı. '
              'Lütfen sorunuzu kontrol edin ve tekrar deneyin.';
        }
      } else if (response.statusCode == 503) {
        // Service unavailable - backend or Ollama is down
        return 'Hata: AI servisi şu anda kullanılamıyor. '
            'Lütfen daha sonra tekrar deneyin. '
            'Eğer sorun devam ederse, sistem yöneticisi ile iletişime geçin.';
      } else if (response.statusCode == 504) {
        // Gateway timeout - request took too long
        return 'Hata: AI yanıt verme süresi aşıldı. '
            'Lütfen daha kısa bir soru deneyin veya daha sonra tekrar deneyin.';
      } else {
        // Other HTTP errors
        log('Backend HATASI: ${response.statusCode}');
        return 'Hata: Backend servisi geçici olarak kullanılamıyor '
            '(HTTP ${response.statusCode}). '
            'Lütfen daha sonra tekrar deneyin.';
      }
    } on TimeoutException catch (e) {
      log('Backend ZAMAN AŞIMI: $e');
      return e.message ?? 'İstek zaman aşımına uğradı. Lütfen tekrar deneyin.';
    } on SocketException catch (e) {
      // Network connectivity issues
      log('AĞ BAĞLANTI HATASI: $e');
      return 'Hata: İnternet bağlantısı bulunamadı. '
          'Lütfen internet bağlantınızı kontrol edin ve tekrar deneyin.';
    } on FormatException catch (e) {
      // JSON parsing errors
      log('YANIT PARSE HATASI: $e');
      return 'Hata: Sunucudan alınan yanıt okunamadı. '
          'Lütfen tekrar deneyin.';
    } on Exception catch (e) {
      // Handle other errors
      log('Backend HATA: $e');
      return 'Hata: Beklenmeyen bir hata oluştu. '
          'Lütfen daha sonra tekrar deneyin. '
          'Hata: ${e.toString().replaceAll('Exception: ', '')}';
    }
  }
}
