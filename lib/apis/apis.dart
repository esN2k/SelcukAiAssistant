import 'dart:async';
import 'dart:convert';
import 'dart:developer';
import 'dart:io';

import 'package:http/http.dart' as http;
import 'package:selcukaiassistant/helper/global.dart';
import 'package:selcukaiassistant/services/sse_client.dart';

class APIs {
  static const Duration _responseTimeout = Duration(seconds: 120);

  static Map<String, dynamic> _buildPayload({
    required List<Map<String, String>> messages,
    String? model,
    bool stream = false,
  }) {
    return {
      'model': model,
      'messages': messages,
      'temperature': 0.2,
      'top_p': 0.9,
      'max_tokens': 256,
      'stream': stream,
    };
  }

  static Future<String> getAnswer(String question, {String? model}) async {
    return sendChat(
      messages: [
        {'role': 'user', 'content': question},
      ],
      model: model,
    );
  }

  static Future<String> sendChat({
    required List<Map<String, String>> messages,
    String? model,
  }) async {
    try {
      log('Backend API: ${Global.chatEndpoint}');

      final requestBody = jsonEncode(
        _buildPayload(messages: messages, model: model),
      );

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
                'Request timed out. Please try again.',
              );
            },
          );

      if (response.statusCode == 200) {
        final responseData = jsonDecode(utf8.decode(response.bodyBytes))
            as Map<String, dynamic>;
        final answer = (responseData['answer'] as String?) ??
            'Sorry, no response generated.';
        return answer;
      } else if (response.statusCode == 400) {
        try {
          final errorData =
              jsonDecode(response.body) as Map<String, dynamic>;
          final errorMessage =
              errorData['detail'] as String? ?? 'Invalid request';
          return 'Error: $errorMessage';
        } on FormatException {
          return 'Error: Invalid request format.';
        }
      } else if (response.statusCode == 503) {
        return 'Error: AI service is unavailable.';
      } else if (response.statusCode == 504) {
        return 'Error: AI response timeout.';
      }

      return 'Error: Backend service unavailable.';
    } on TimeoutException catch (e) {
      log('Backend timeout: $e');
      return e.message ?? 'Request timed out.';
    } on SocketException catch (e) {
      log('Network error: $e');
      return 'Error: No internet connection.';
    } on FormatException catch (e) {
      log('Parse error: $e');
      return 'Error: Invalid server response.';
    } on Exception catch (e) {
      log('Backend error: $e');
      return 'Error: Unexpected error.';
    }
  }

  static Future<ChatStreamSession> streamChat({
    required List<Map<String, String>> messages,
    String? model,
  }) async {
    final client = SseClient();
    return client.connect(
      url: Uri.parse(Global.chatStreamEndpoint),
      headers: {'Content-Type': 'application/json; charset=utf-8'},
      body: jsonEncode(
        _buildPayload(messages: messages, model: model, stream: true),
      ),
    );
  }
}
