/// DOSYA ADI: apis.dart
/// AMAÇ: Backend API iletişimini yönetmek.
/// NE YAPAR:
///   - Chat isteklerini gönderir.
///   - Stream oturumlarını başlatır.
/// BAĞIMLILIKLAR:
///   - http
///   - error_handler.dart
/// SON DEĞİŞİKLİK: 17.01.2026
library;
import 'dart:async';
import 'dart:convert';
import 'dart:developer';

import 'package:http/http.dart' as http;
import 'package:selcukaiassistant/config/backend_config.dart';
import 'package:selcukaiassistant/core/errors/error_handler.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
import 'package:selcukaiassistant/model/chat_api_response.dart';
import 'package:selcukaiassistant/services/sse_client.dart';

class APIs {
  static const Duration _responseTimeout = Duration(seconds: 180);

  /// Giriş: yok.
  /// Çıkış: HTTP üstbilgileri.
  /// İşleyiş: Dil bilgisini ve içerik tipini ekler.
  static Map<String, String> _buildHeaders() {
    final locale = Pref.localeCode ?? L10n.fallbackLocale.languageCode;
    return {
      'Content-Type': 'application/json; charset=utf-8',
      'Accept-Language': locale,
    };
  }

  /// Giriş: Mesaj listesi ve model bilgileri.
  /// Çıkış: İstek payload'u.
  /// İşleyiş: Backend için ortak payload oluşturur.
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
      'max_tokens': 512,
      'stream': stream,
      'rag_enabled': Pref.ragEnabled,
      'rag_strict': Pref.ragStrict,
      'rag_top_k': Pref.ragTopK,
    };
  }

  /// Giriş: Soru metni ve opsiyonel model/sistem promptu.
  /// Çıkış: Yanıt metni.
  /// İşleyiş: Tek adımlı sohbet isteği gönderir.
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

  /// Giriş: Mesaj listesi ve opsiyonel model bilgisi.
  /// Çıkış: ChatApiResponse.
  /// İşleyiş: Backend'e istek gönderir ve hata mesajlarını dönüştürür.
  static Future<ChatApiResponse> sendChat({
    required List<Map<String, String>> messages,
    String? model,
  }) async {
    final l10n = L10n.current();
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
          .timeout(_responseTimeout);

      if (response.statusCode == 200) {
        final responseData = jsonDecode(utf8.decode(response.bodyBytes))
            as Map<String, dynamic>;
        final answer = (responseData['answer'] as String?) ??
            (l10n?.noResponseGenerated ?? 'Üzgünüm, bir yanıt üretilemedi.');
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
      }

      return ChatApiResponse(
        answer: ErrorHandler.fromResponse(response),
      );
    } on Exception catch (e) {
      log('Backend hatası: $e');
      final message = ErrorHandler.fromException(e);
      return ChatApiResponse(answer: message);
    }
  }

  /// Giriş: Mesaj listesi ve opsiyonel model bilgisi.
  /// Çıkış: ChatStreamSession.
  /// İşleyiş: SSE akışını başlatır.
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
