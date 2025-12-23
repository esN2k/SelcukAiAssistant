import 'dart:async';
import 'dart:convert';
import 'dart:developer';

import 'package:http/http.dart' as http;
import 'package:selcukaiassistant/config/backend_config.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
import 'package:selcukaiassistant/model/chat_api_response.dart';
import 'package:selcukaiassistant/services/sse_client.dart';

class APIs {
  static const Duration _responseTimeout = Duration(seconds: 120);

  static Map<String, String> _buildHeaders() {
    final locale = Pref.localeCode ?? L10n.fallbackLocale.languageCode;
    return {
      'Content-Type': 'application/json; charset=utf-8',
      'Accept-Language': locale,
    };
  }

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
      'rag_enabled': Pref.ragEnabled,
      'rag_strict': Pref.ragStrict,
      'rag_top_k': Pref.ragTopK,
    };
  }

  static Future<String> getAnswer(
    String question, {
    String? model,
    String? systemPrompt,
  }) async {
    final messages = <Map<String, String>>[];
    if (systemPrompt != null && systemPrompt.trim().isNotEmpty) {
      messages.add({'role': 'system', 'content': systemPrompt});
    }
    messages.add({'role': 'user', 'content': question});

    final response = await sendChat(
      messages: messages,
      model: model,
    );
    return response.answer;
  }

  static Future<ChatApiResponse> sendChat({
    required List<Map<String, String>> messages,
    String? model,
  }) async {
    final l10n = L10n.current();
    final timeoutMessage =
        l10n?.requestTimeoutMessage ?? 'Request timed out. Please try again.';
    try {
      log('Backend API: ${BackendConfig.chatEndpoint}');

      final requestBody = jsonEncode(
        _buildPayload(messages: messages, model: model),
      );

      final response = await http
          .post(
            Uri.parse(BackendConfig.chatEndpoint),
            headers: _buildHeaders(),
            body: requestBody,
          )
          .timeout(
            _responseTimeout,
            onTimeout: () {
              throw TimeoutException(timeoutMessage);
            },
          );

      if (response.statusCode == 200) {
        final responseData = jsonDecode(utf8.decode(response.bodyBytes))
            as Map<String, dynamic>;
        final answer = (responseData['answer'] as String?) ??
            (l10n?.noResponseGenerated ?? 'Sorry, no response generated.');
        final citations = (responseData['citations'] as List<dynamic>?)
                ?.map((item) => item.toString())
                .toList() ??
            <String>[];
        final usage =
            responseData['usage'] as Map<String, dynamic>? ??
                <String, dynamic>{};
        return ChatApiResponse(
          answer: answer,
          citations: citations,
          usage: usage,
        );
      } else if (response.statusCode == 400) {
        try {
          final errorData =
              jsonDecode(response.body) as Map<String, dynamic>;
          final errorMessage =
              errorData['detail'] as String? ?? l10n?.errorInvalidRequest;
          return ChatApiResponse(
            answer: errorMessage ?? 'Error: Invalid request',
          );
        } on FormatException {
          return ChatApiResponse(
            answer: l10n?.errorInvalidRequestFormat ??
                'Error: Invalid request format.',
          );
        }
      } else if (response.statusCode == 503) {
        return ChatApiResponse(
          answer: l10n?.errorServiceUnavailable ??
              'Error: AI service is unavailable.',
        );
      } else if (response.statusCode == 504) {
        return ChatApiResponse(
          answer: l10n?.errorTimeout ?? 'Error: AI response timeout.',
        );
      }

      return ChatApiResponse(
        answer: l10n?.errorBackendUnavailable ??
            'Error: Backend service unavailable.',
      );
    } on TimeoutException catch (e) {
      log('Backend timeout: $e');
      return ChatApiResponse(answer: e.message ?? timeoutMessage);
    } on http.ClientException catch (e) {
      log('Network error: $e');
      return ChatApiResponse(
        answer: l10n?.errorNoInternet ?? 'Error: No internet connection.',
      );
    } on FormatException catch (e) {
      log('Parse error: $e');
      return ChatApiResponse(
        answer: l10n?.errorInvalidServerResponse ??
            'Error: Invalid server response.',
      );
    } on Exception catch (e) {
      log('Backend error: $e');
      return ChatApiResponse(
        answer: l10n?.errorUnexpected ?? 'Error: Unexpected error.',
      );
    }
  }

  static Future<ChatStreamSession> streamChat({
    required List<Map<String, String>> messages,
    String? model,
  }) async {
    final client = SseClient();
    return client.connect(
      url: Uri.parse(BackendConfig.chatStreamEndpoint),
      headers: _buildHeaders(),
      body: jsonEncode(
        _buildPayload(messages: messages, model: model, stream: true),
      ),
    );
  }
}
